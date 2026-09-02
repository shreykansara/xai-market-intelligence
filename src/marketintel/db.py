"""Supabase (Postgres + pgvector) access layer for the data that GROWS:
announcements, facts + their embeddings, ingestion run status, and exclusions.

Why this exists at all: the nearest-neighbour operations in seed_inference.py
and comparative_matching.py were brute-force numpy dot products over an
in-memory array of EVERY embedding. That is fine at 1,000 fabricated articles
and untenable at the projected ~186,500 LPU facts - it forces server.py to load
~145 MB of vectors on every cold start (and Render's free tier cold-starts
often). Pushing the search into pgvector means the server holds no corpus in
memory and the database returns only the k rows actually needed.

Static training artifacts (subclusters.json, startups.json,
interaction_matrix.npy) deliberately do NOT live here. They are regenerated
wholesale by offline scripts and never mutated at runtime, so they ship as
files with the deployment.

Connection string comes from DATABASE_URL (see .env.example). psycopg is
imported lazily so that importing this module - which config-level code does -
never hard-fails on a machine that has no driver installed and no database
configured; callers get a clear error only when they actually try to connect.
"""
import json
import os
from contextlib import contextmanager

import numpy as np

DATABASE_URL_ENV_VAR = "DATABASE_URL"
EMBEDDING_DIMS = 384


class DatabaseUnavailable(RuntimeError):
    """No DATABASE_URL configured, or the driver/connection failed. Callers
    that can still work from files should catch this and degrade, exactly as
    load_real_facts() degrades on a missing file."""


def database_url() -> str | None:
    return os.environ.get(DATABASE_URL_ENV_VAR, "").strip() or None


def is_configured() -> bool:
    return database_url() is not None


@contextmanager
def connect():
    """Yields a psycopg connection. Lazy import so this module stays importable
    without the driver installed."""
    url = database_url()
    if not url:
        raise DatabaseUnavailable(
            f"{DATABASE_URL_ENV_VAR} is not set - add your Supabase connection string to .env"
        )
    try:
        import psycopg
    except ImportError as exc:  # pragma: no cover - environment-dependent
        raise DatabaseUnavailable(
            "psycopg is not installed - `pip install 'psycopg[binary]'`"
        ) from exc
    try:
        conn = psycopg.connect(url)
    except Exception as exc:  # noqa: BLE001 - driver raises many types
        raise DatabaseUnavailable(f"could not connect to the database: {exc}") from exc
    try:
        yield conn
    except Exception as exc:  # noqa: BLE001 - see below
        # This is what actually caught the real production bug: a bare
        # `try/finally` here means an error from USING the connection (e.g.
        # `cur.execute()` failing because a table doesn't exist - schema.sql
        # never applied to this Supabase project) propagated straight past
        # every review-queue endpoint's error handling and out as an
        # unhandled Starlette 500 with no body at all, instead of the clear
        # "Database unavailable: ..." message /api/analyze's equivalent
        # degraded-mode path already gives. Converting every failure that
        # happens while a connection is in use - not just failing to obtain
        # one - into the same DatabaseUnavailable the global exception
        # handler already turns into a clean 503 closes that gap.
        try:
            conn.rollback()
        except Exception:  # noqa: BLE001 - best-effort; the real error is re-raised below regardless
            pass
        raise DatabaseUnavailable(f"database operation failed: {exc}") from exc
    finally:
        conn.close()


def _vector_literal(embedding) -> str:
    """pgvector accepts a bracketed list literal. Cast at the call site to
    halfvec so the comparison matches the column type and uses the HNSW index."""
    values = np.asarray(embedding, dtype=np.float32).ravel()
    if values.shape[0] != EMBEDDING_DIMS:
        raise ValueError(f"expected {EMBEDDING_DIMS}-dim embedding, got {values.shape[0]}")
    return "[" + ",".join(f"{v:.6f}" for v in values) + "]"


# ---------------------------------------------------------------------------
# Nearest-neighbour search - the pgvector replacement for brute-force numpy
# ---------------------------------------------------------------------------
def nearest_facts(embedding, k: int = 10, scope: str | None = None,
                  source: str | None = None, published_before=None) -> list[dict]:
    """The k most similar stored facts by COSINE distance, computed in the
    database. `<=>` is pgvector's cosine-distance operator, so similarity is
    1 - distance; ORDER BY on it is what lets the HNSW index serve the query
    instead of a sequential scan.

    Replaces the `embeddings @ query` full-array dot product that
    seed_inference.nearest_neighbors() did in Python. Optional filters cover
    what the callers actually need:
      - `scope`/`source`: per-class lookups (seed_inference groups by scope).
      - `published_before`: comparative_matching only ever considers STRICTLY
        EARLIER facts as a prior value, so that constraint belongs in the query
        rather than being filtered out afterwards in Python.
    """
    where, params = ["embedding IS NOT NULL"], {}
    if scope is not None:
        where.append("scope = %(scope)s")
        params["scope"] = scope
    if source is not None:
        where.append("source = %(source)s")
        params["source"] = source
    if published_before is not None:
        where.append("published < %(before)s")
        params["before"] = published_before
    params["q"] = _vector_literal(embedding)
    params["k"] = k

    sql = f"""
        SELECT id, fact_text, entities, published, scope, source,
               pestle_scores, porters_scores, polarity, mention_count,
               1 - (embedding <=> %(q)s::halfvec) AS similarity
        FROM facts
        WHERE {' AND '.join(where)}
        ORDER BY embedding <=> %(q)s::halfvec
        LIMIT %(k)s
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        columns = [c.name for c in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]


def best_match_per_scope(embedding, scopes: list[str]) -> dict[str, float]:
    """Each scope class's single closest match, which is exactly what
    seed_inference.infer_scope_best_match() needs: per-class best, so majority
    classes can't win on population size alone. One indexed query per class is
    still far cheaper than materializing every embedding in Python.

    Note this is only needed for sources WITHOUT structured geography - the RSS
    feeds and LPU now take their scope from the source directly.
    """
    return {
        scope: (rows[0]["similarity"] if (rows := nearest_facts(embedding, k=1, scope=scope)) else -1.0)
        for scope in scopes
    }


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------
def upsert_announcement(cur, announcement: dict) -> None:
    cur.execute(
        """
        INSERT INTO announcements (id, source, content_key, source_file, source_row_id,
                                   title, body, uploaded_by, link, links, published, raw_date)
        VALUES (%(id)s, %(source)s, %(content_key)s, %(source_file)s, %(source_row_id)s,
                %(title)s, %(body)s, %(uploaded_by)s, %(link)s, %(links)s, %(published)s, %(raw_date)s)
        ON CONFLICT (id) DO NOTHING
        """,
        {**{k: announcement.get(k) for k in
            ("id", "source", "content_key", "source_file", "source_row_id",
             "title", "body", "uploaded_by", "link", "published", "raw_date")},
         "links": json.dumps(announcement.get("links") or [])},
    )


def insert_facts(cur, facts: list[dict], embeddings) -> int:
    """Bulk-inserts facts with their vectors. ON CONFLICT DO NOTHING makes a
    re-run after an interrupted job idempotent rather than duplicating rows -
    the same property the JSON checkpoint gave us."""
    inserted = 0
    for fact, embedding in zip(facts, embeddings):
        cur.execute(
            """
            INSERT INTO facts (id, announcement_id, fact_text, entities, published, scope, source,
                               pestle_scores, porters_scores, polarity, mention_count,
                               decomposition_ok, classification_ok, scope_source, comparative, embedding)
            VALUES (%(id)s, %(announcement_id)s, %(fact_text)s, %(entities)s, %(published)s,
                    %(scope)s, %(source)s, %(pestle_scores)s, %(porters_scores)s, %(polarity)s,
                    %(mention_count)s, %(decomposition_ok)s, %(classification_ok)s,
                    %(scope_source)s, %(comparative)s, %(embedding)s::halfvec)
            ON CONFLICT (id) DO NOTHING
            """,
            {
                "id": fact["id"],
                "announcement_id": fact.get("parent_announcement_id") or fact.get("parent_article_id"),
                "fact_text": fact["fact_text"],
                "entities": json.dumps(fact.get("entities") or []),
                "published": fact.get("published"),
                "scope": fact.get("scope", ""),
                "source": fact.get("source", ""),
                "pestle_scores": json.dumps(fact.get("pestle_scores") or {}),
                "porters_scores": json.dumps(fact.get("porters_scores") or {}),
                "polarity": fact.get("polarity", ""),
                "mention_count": int(fact.get("mention_count", 1) or 1),
                "decomposition_ok": bool(fact.get("decomposition_ok", True)),
                "classification_ok": bool(fact.get("classification_ok", True)),
                "scope_source": fact.get("scope_source"),
                "comparative": json.dumps(fact["comparative"]) if fact.get("comparative") else None,
                "embedding": _vector_literal(embedding),
            },
        )
        inserted += cur.rowcount
    return inserted


def record_ingestion_run(stats: dict, ok: bool, source: str | None = None,
                         error: str | None = None, last_published=None) -> None:
    """One row per scheduled run. This is BOTH the health signal server.py
    reads AND - deliberately - a database WRITE on every run: see README's
    operational-risk section on Supabase free-tier inactivity pausing."""
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO ingestion_runs (finished_at, ok, source, error, stats, last_published)
            VALUES (now(), %s, %s, %s, %s, %s)
            """,
            (ok, source, error, json.dumps(stats or {}), last_published),
        )
        conn.commit()


def latest_ingestion_run() -> dict | None:
    """Newest run row, for server.py's health reporting. Returns None when the
    table is empty (nothing has ever run) rather than raising."""
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT started_at, finished_at, ok, source, error, stats, last_published
            FROM ingestion_runs ORDER BY started_at DESC LIMIT 1
            """
        )
        row = cur.fetchone()
        if row is None:
            return None
        return dict(zip([c.name for c in cur.description], row))


# ---------------------------------------------------------------------------
# Review queue - the human-in-the-loop gate between raw ingestion and the
# scored corpus. Nothing in `facts`/`announcements` was written without
# passing through here and being approved at both stages (see db/schema.sql's
# review_batches/review_items comment for the full lifecycle).
# ---------------------------------------------------------------------------
def create_review_batch(batch_id: str, source: str, label: str) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO review_batches (id, source, label, status) VALUES (%s, %s, %s, 'processing_chunks')",
            (batch_id, source, label),
        )
        conn.commit()


def update_batch_status(batch_id: str, status: str, error: str | None = None, item_count: int | None = None) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE review_batches
            SET status = %s, error = %s, updated_at = now(),
                item_count = COALESCE(%s, item_count)
            WHERE id = %s
            """,
            (status, error, item_count, batch_id),
        )
        conn.commit()


def insert_review_items(cur, items: list[dict]) -> None:
    """Stage-1 insert: chunked facts awaiting the first approval. No embedding,
    no summary yet - those are added by update_review_item_embedding() once the
    batch clears chunk review."""
    for item in items:
        cur.execute(
            """
            INSERT INTO review_items (id, batch_id, source_title, source_body, source_published,
                                      source_link, source_scope, fact_text, entities,
                                      pestle_scores, porters_scores, polarity,
                                      decomposition_ok, classification_ok, status)
            VALUES (%(id)s, %(batch_id)s, %(source_title)s, %(source_body)s, %(source_published)s,
                    %(source_link)s, %(source_scope)s, %(fact_text)s, %(entities)s,
                    %(pestle_scores)s, %(porters_scores)s, %(polarity)s,
                    %(decomposition_ok)s, %(classification_ok)s, 'pending_chunk_review')
            """,
            {
                "id": item["id"], "batch_id": item["batch_id"],
                "source_title": item.get("source_title", ""), "source_body": item.get("source_body", ""),
                "source_published": item.get("source_published"), "source_link": item.get("source_link"),
                "source_scope": item.get("source_scope"),
                "fact_text": item["fact_text"], "entities": json.dumps(item.get("entities") or []),
                "pestle_scores": json.dumps(item.get("pestle_scores") or {}),
                "porters_scores": json.dumps(item.get("porters_scores") or {}),
                "polarity": item.get("polarity"),
                "decomposition_ok": bool(item.get("decomposition_ok", True)),
                "classification_ok": bool(item.get("classification_ok", True)),
            },
        )


def list_review_batches(status: str | None = None) -> list[dict]:
    with connect() as conn, conn.cursor() as cur:
        if status:
            cur.execute(
                "SELECT * FROM review_batches WHERE status = %s ORDER BY created_at DESC", (status,)
            )
        else:
            cur.execute("SELECT * FROM review_batches ORDER BY created_at DESC LIMIT 100")
        cols = [c.name for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def get_review_batch(batch_id: str) -> dict | None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM review_batches WHERE id = %s", (batch_id,))
        row = cur.fetchone()
        return dict(zip([c.name for c in cur.description], row)) if row else None


def list_review_items(batch_id: str, status: str | None = None) -> list[dict]:
    with connect() as conn, conn.cursor() as cur:
        if status:
            cur.execute(
                "SELECT id, batch_id, source_title, source_body, source_published, source_link, "
                "source_scope, fact_text, entities, pestle_scores, porters_scores, polarity, "
                "summary, decomposition_ok, classification_ok, status, rejection_reason, created_at "
                "FROM review_items WHERE batch_id = %s AND status = %s ORDER BY created_at",
                (batch_id, status),
            )
        else:
            cur.execute(
                "SELECT id, batch_id, source_title, source_body, source_published, source_link, "
                "source_scope, fact_text, entities, pestle_scores, porters_scores, polarity, "
                "summary, decomposition_ok, classification_ok, status, rejection_reason, created_at "
                "FROM review_items WHERE batch_id = %s ORDER BY created_at",
                (batch_id,),
            )
        cols = [c.name for c in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


def mark_items_chunk_approved(item_ids: list[str]) -> int:
    """First approval: moves items from pending_chunk_review to
    chunk_approved. Only items still actually pending are touched, so
    re-clicking approve on an already-processed batch is a harmless no-op
    rather than silently re-approving something already rejected."""
    if not item_ids:
        return 0
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE review_items SET status = 'chunk_approved' "
            "WHERE id = ANY(%s) AND status = 'pending_chunk_review'",
            (item_ids,),
        )
        n = cur.rowcount
        conn.commit()
        return n


def reject_review_items(item_ids: list[str], reason: str) -> int:
    """Rejects items still in a pending state - deliberately excludes already-
    'approved' items (those are in the scored corpus; un-approving them isn't
    what this endpoint is for) so a stray call can't silently retract a
    committed fact."""
    if not item_ids:
        return 0
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE review_items SET status = 'rejected', rejection_reason = %s "
            "WHERE id = ANY(%s) AND status IN ('pending_chunk_review', 'chunk_approved', 'pending_embedding_review')",
            (reason, item_ids),
        )
        n = cur.rowcount
        conn.commit()
        return n


def update_review_item_embedding(item_id: str, summary: str, embedding) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE review_items SET summary = %s, embedding = %s::halfvec, status = 'pending_embedding_review' "
            "WHERE id = %s",
            (summary, _vector_literal(embedding), item_id),
        )
        conn.commit()


def promote_review_items_to_corpus(item_ids: list[str]) -> int:
    """Final approval: copies approved review_items into the real facts /
    announcements tables the app scores against, and marks them 'approved' in
    the review queue (kept as an audit trail, not deleted)."""
    if not item_ids:
        return 0
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, batch_id, source_title, source_body, source_published, source_link, "
            "source_scope, fact_text, entities, pestle_scores, porters_scores, polarity, "
            "decomposition_ok, classification_ok "
            "FROM review_items WHERE id = ANY(%s) AND status = 'pending_embedding_review'",
            (item_ids,),
        )
        cols = [c.name for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

        promoted = 0
        for row in rows:
            announcement_id = f"review_{row['batch_id']}"
            upsert_announcement(cur, {
                "id": announcement_id, "source": row["source_scope"] or "review",
                "content_key": None, "source_file": None, "source_row_id": None,
                "title": row["source_title"], "body": row["source_body"],
                "uploaded_by": None, "link": row["source_link"], "links": [],
                "published": row["source_published"], "raw_date": None,
            })
            cur.execute(
                "SELECT embedding FROM review_items WHERE id = %s", (row["id"],)
            )
            embedding_row = cur.fetchone()
            cur.execute(
                """
                INSERT INTO facts (id, announcement_id, fact_text, entities, published, scope, source,
                                   pestle_scores, porters_scores, polarity, mention_count,
                                   decomposition_ok, classification_ok, embedding)
                VALUES (%(id)s, %(announcement_id)s, %(fact_text)s, %(entities)s, %(published)s,
                        %(scope)s, %(source)s, %(pestle_scores)s, %(porters_scores)s, %(polarity)s, 1,
                        %(decomposition_ok)s, %(classification_ok)s, %(embedding)s)
                ON CONFLICT (id) DO NOTHING
                """,
                {
                    "id": f"fact_{row['id']}", "announcement_id": announcement_id,
                    "fact_text": row["fact_text"], "entities": json.dumps(row["entities"]),
                    "published": row["source_published"], "scope": row["source_scope"] or "unknown",
                    "source": row["source_scope"] or "review",
                    "pestle_scores": json.dumps(row["pestle_scores"] or {}),
                    "porters_scores": json.dumps(row["porters_scores"] or {}),
                    "polarity": row["polarity"] or "negative",
                    "decomposition_ok": row["decomposition_ok"], "classification_ok": row["classification_ok"],
                    "embedding": embedding_row[0],
                },
            )
            promoted += cur.rowcount

        cur.execute("UPDATE review_items SET status = 'approved' WHERE id = ANY(%s)", (item_ids,))
        conn.commit()
        return promoted


def corpus_counts() -> dict:
    """Row counts + on-disk size, so capacity against the free tier's 500 MB
    can be checked from the live database rather than estimated."""
    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM facts")
        facts = cur.fetchone()[0]
        cur.execute("SELECT count(*) FROM announcements")
        announcements = cur.fetchone()[0]
        cur.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
        size = cur.fetchone()[0]
        return {"facts": facts, "announcements": announcements, "database_size": size}

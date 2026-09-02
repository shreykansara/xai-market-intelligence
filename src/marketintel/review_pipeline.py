"""Human-in-the-loop ingestion: the ONLY way real news reaches the scored
corpus right now. Nothing is written to `facts`/`announcements` without
passing through this queue and being explicitly approved twice.

Two sources feed the same queue:
  - GDELT (live DOC 2.0 API, `start_gdelt_batch`) - real-time world news.
  - LPU announcements you scrape and upload yourself as JSON
    (`start_lpu_upload_batch`) - same {date, title, body, links, id} shape
    as data/lpudata/, but arriving through the UI instead of a scheduled crawl.

Pipeline, identical for both sources:

  1. CHUNK - each raw item (GDELT article / LPU announcement) is broken into
     atomic facts via fact_pipeline.py's bundled decomposition+classification
     (one Groq call - same mechanism validated for the LPU corpus build,
     reused unchanged here), then grounding.py's pre-filter and per-fact
     check run exactly as they do everywhere else in the system. Results land
     in review_items with status='pending_chunk_review'. NOTHING is
     embedded yet.

  2. APPROVE CHUNKS -> EMBED - only once you approve (per-item or per-batch),
     each surviving item gets embedded (embeddings.py, the same local
     MiniLM model everything else uses) and a short one-line summary
     (a second, lightweight Groq call, batched per source-batch to keep
     usage down). Status moves to 'pending_embedding_review'.

  3. APPROVE EMBEDDINGS -> COMMIT - only once you approve again, the item is
     copied into the real `facts`/`announcements` tables via
     db.promote_review_items_to_corpus() - the tables /api/analyze and the
     nearest-neighbour queries actually read from. Only at this point does
     anything become part of the corpus.

A batch or item can be rejected at either stage instead; rejected items are
kept (status='rejected'), never silently deleted, so what was rejected and
why stays inspectable.
"""
import json
import uuid
from datetime import datetime, timedelta, timezone

from . import db
from .config import GROQ_MAX_ATTEMPTS, OLLAMA_RETRY_BACKOFF_SECONDS
from .embeddings import embed_text
from .fact_pipeline import extract_and_classify_with_status
from .grounding import is_grounded, is_likely_non_content
from .groq_client import GroqError, GroqRateLimited, call_groq

SUMMARY_PROMPT = """Write ONE short, plain-English summary sentence (max 20 words) for EACH of \
the following statements - a quick gloss a human reviewer can read at a glance, not a restatement \
of every detail.

Return ONLY a JSON array of strings, one per statement, in the same order. No other text.

Statements:
{statements}

JSON array of strings:"""


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _chunk_one_source_item(batch_id: str, source_scope: str, title: str, body: str,
                           published, link: str | None) -> tuple[list[dict], dict]:
    """Runs pre-filter -> bundled decomposition+classification -> per-fact
    grounding on ONE raw item (article or announcement). Returns
    (review_item_rows, stats_delta) - mirrors lpu_ingestion._process_announcement,
    reused conceptually rather than literally since this writes review_items
    shaped dicts, not local-file fact records."""
    stats = {"noncontent_skipped": 0, "decomposition_failed": 0, "rejected_by_grounding": 0, "facts": 0}
    is_junk, _reason = is_likely_non_content(title)
    if is_junk:
        stats["noncontent_skipped"] = 1
        return [], stats

    text = f"{title}\n\n{body}" if body else title
    extracted, ok = extract_and_classify_with_status(text)
    if not ok:
        stats["decomposition_failed"] = 1

    full_source = f"{title}\n\n{body}"
    rows = []
    for fact in extracted:
        grounded, _ungrounded = is_grounded(fact["text"], full_source)
        if not grounded:
            stats["rejected_by_grounding"] += 1
            continue
        rows.append({
            "id": _new_id("ritem"),
            "batch_id": batch_id,
            "source_title": title,
            "source_body": body,
            "source_published": published,
            "source_link": link,
            "source_scope": source_scope,
            "fact_text": fact["text"],
            "entities": fact.get("entities", []),
            "pestle_scores": fact["pestle_scores"],
            "porters_scores": fact["porters_scores"],
            "polarity": fact["polarity"],
            "decomposition_ok": ok,
            "classification_ok": ok,
        })
        stats["facts"] += 1
    return rows, stats


def run_chunk_stage(batch_id: str, source: str, raw_items: list[dict]) -> dict:
    """Stage 1 for a whole batch: chunks every raw item and writes the
    resulting review_items. `raw_items` is a list of
    {title, body, published, link, scope} dicts - the caller (GDELT fetch or
    LPU upload parsing) is responsible for getting raw text into this shape;
    this function only runs the shared chunk+ground pipeline on it."""
    all_rows = []
    totals = {"raw_items": len(raw_items), "noncontent_skipped": 0,
              "decomposition_failed": 0, "rejected_by_grounding": 0, "facts": 0}
    try:
        for item in raw_items:
            rows, delta = _chunk_one_source_item(
                batch_id, item.get("scope", ""), item.get("title", ""), item.get("body", ""),
                item.get("published"), item.get("link"),
            )
            all_rows.extend(rows)
            for key in ("noncontent_skipped", "decomposition_failed", "rejected_by_grounding", "facts"):
                totals[key] += delta[key]

        with db.connect() as conn, conn.cursor() as cur:
            db.insert_review_items(cur, all_rows)
            conn.commit()
        db.update_batch_status(batch_id, "pending_chunk_review", item_count=len(all_rows))
    except db.DatabaseUnavailable as exc:
        db.update_batch_status(batch_id, "failed", error=str(exc))
        raise
    except Exception as exc:  # noqa: BLE001 - a failed batch must be visible, not a silently hung "processing" row
        db.update_batch_status(batch_id, "failed", error=f"{type(exc).__name__}: {exc}")
        raise
    return totals


def start_gdelt_batch(hours_back: int | None = None) -> tuple[str, list[dict]]:
    """Fetches recent world news from GDELT's live DOC 2.0 API (the same
    fetch_gdelt() the (currently idle) live ingestion path uses - reused, not
    reimplemented) and creates a review batch. Returns (batch_id, raw_items)
    so the caller can run the (potentially slow) chunk stage as a background
    task rather than blocking the request that triggered it.

    This is REAL-TIME news only - no historical backfill, no curated-actor
    scoping. That question stays exactly as deferred as it was."""
    from .ingestion import GDELT_LOOKBACK_HOURS, fetch_gdelt

    now = datetime.now(timezone.utc)
    since = now - timedelta(hours=hours_back or GDELT_LOOKBACK_HOURS)
    articles = fetch_gdelt(since)

    batch_id = _new_id("gdelt")
    db.create_review_batch(batch_id, "gdelt", f"GDELT live run @ {now.strftime('%Y-%m-%d %H:%M UTC')}")

    raw_items = [
        {"title": a["title"], "body": "", "published": a["published"], "link": a["link"], "scope": ""}
        for a in articles
    ]
    return batch_id, raw_items


def start_lpu_upload_batch(filename: str, raw_json: bytes) -> tuple[str, list[dict]]:
    """Parses an uploaded JSON file in the SAME shape as data/lpudata/
    ({date, title, body, links, id} records) and creates a review batch.
    Reuses lpu_ingestion's own date normalization and text-assembly logic so
    an upload is processed identically to how the (separate, file-based) bulk
    LPU corpus build already does it - not a second, divergent parser."""
    from .lpu_ingestion import _normalize_date

    try:
        records = json.loads(raw_json.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ValueError(f"Could not parse {filename!r} as JSON: {exc}") from exc
    if not isinstance(records, list):
        raise ValueError(f"{filename!r} must contain a JSON array of announcement records.")

    raw_items = []
    for record in records:
        title = (record.get("title") or "").strip()
        body = (record.get("body") or "").strip()
        if not title and not body:
            continue
        links = record.get("links") or []
        raw_items.append({
            "title": title, "body": body,
            "published": _normalize_date(record.get("date")),
            "link": links[0] if links and isinstance(links[0], str) else None,
            "scope": "LPU",
        })

    if not raw_items:
        raise ValueError(f"{filename!r} contained no usable records (need at least a title or body per item).")

    batch_id = _new_id("lpu")
    db.create_review_batch(batch_id, "lpu_upload", f"{filename} ({len(raw_items)} records)")
    return batch_id, raw_items


def _summarize_batch(fact_texts: list[str], attempts: int = GROQ_MAX_ATTEMPTS) -> list[str]:
    """One short summary per fact, batched into as few Groq calls as
    reasonable - same batching-per-call-cost reasoning as classify_facts()
    originally used. Falls back to the fact text itself (truncated) for any
    summary the model doesn't return, rather than leaving it blank - a review
    UI with a missing summary is worse than one with a slightly redundant one."""
    import re
    import time

    fallback = [t if len(t) <= 100 else t[:97] + "..." for t in fact_texts]
    if not fact_texts:
        return []
    statements = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(fact_texts))
    for attempt in range(1, attempts + 1):
        try:
            raw = call_groq(SUMMARY_PROMPT.format(statements=statements), temperature=0.2)
            match = re.search(r"\[.*\]", raw, re.DOTALL)
            if match:
                items = json.loads(match.group(0))
                if isinstance(items, list):
                    return [str(items[i]).strip() if i < len(items) else fallback[i]
                            for i in range(len(fact_texts))]
        except (GroqRateLimited, GroqError, json.JSONDecodeError):
            pass
        if attempt < attempts:
            time.sleep(OLLAMA_RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1)))
    return fallback


def run_embedding_stage(item_ids: list[str]) -> dict:
    """Stage 2 for a set of already chunk-approved items: generates a summary
    (batched per call) and an embedding (local, per item) for each, then marks
    them 'pending_embedding_review'. Does NOT touch the scored corpus - that
    only happens on the final approval (db.promote_review_items_to_corpus)."""
    if not item_ids:
        return {"embedded": 0}
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, fact_text FROM review_items WHERE id = ANY(%s) AND status = 'chunk_approved'",
            (item_ids,),
        )
        items = [{"id": r[0], "fact_text": r[1]} for r in cur.fetchall()]

    if not items:
        return {"embedded": 0}

    summaries = _summarize_batch([i["fact_text"] for i in items])
    embedded = 0
    for item, summary in zip(items, summaries):
        embedding = embed_text(item["fact_text"])
        db.update_review_item_embedding(item["id"], summary, embedding)
        embedded += 1
    return {"embedded": embedded}

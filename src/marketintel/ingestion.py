"""Real-world news ingestion pipeline: fetches world-level headlines from a small
set of free, no-key sources, decomposes each fetched article into one or more
atomic facts (a local Ollama model, see fact_extraction.py), deduplicates
near-identical FACTS via embedding similarity, and infers PESTLE/Porter's
relevance, polarity, and (for facts that clear a relevance gate) geographic
scope. No per-source scope tagging, no trained classifier.

**Migrated off the fabricated seed corpus onto the accumulated real-fact
corpus itself, per dimension** (see real_data_inference.py) - new real facts
are now scored primarily against OLDER real facts, self-referentially,
rather than the 1000 fabricated articles. This is per-dimension, not
all-or-nothing: a dimension only draws from real data once the accumulated
corpus has enough of its own (a direct coverage check, re-run fresh on every
ingestion pass - see real_data_inference.assess_dimension_coverage); thin
dimensions keep falling back to the fabricated corpus rather than silently
degrading. Geographic scope migrates per SCOPE CLASS instead, with a much
lower bar (one real exemplar is enough, given how per-class-best-match
already works). The relevance GATE THRESHOLD itself also switches to being
calibrated from the real corpus once there's enough of it (see
real_data_inference.choose_gate_threshold). None of this affects the GDELT
historical GDELT bulk backfill (since removed), which looked up the fabricated
corpus unchanged - the underlying seed_inference.py functions were already
parameterized on their reference pool, so only THIS module's call sites
needed to change.

Shares its grounding safeguards (grounding.py) and comparative-fact matching
(comparative_matching.py) - originally built for the historical GDELT bulk
backfill (since removed), retained here because this path relies on them -
these are standalone, source-agnostic modules, not tied to either pipeline,
so both codepaths call the SAME underlying safety logic rather than each
maintaining their own. The two ORCHESTRATION pipelines remain intentionally
separate (different sources, different step ordering - see this module's
docstring for why bulk volume needs the relevance gate before decomposition,
which this live per-item path does not), but neither has weaker safety
guarantees than the other. Titles are HTML-unescaped at fetch time for the
same reason the bulk fetcher did: an entity like "&#x2013;" left
undecoded contains a spurious digit run that can corrupt the grounding
check's number matching.

The unit of analysis is the fact, not the article: a tax policy piece with a
bracket increase and a separate bracket decrease becomes two fact records with
their own (likely opposing) polarity, not one blended one. The relevance gate,
scope classification, and dedup all now run on facts. The original article is
kept only as a provenance container - headline, source, link, and which facts
came out of it (data/real_articles.json) - not scored or embedded itself.

Two safeguards on the nearest-neighbor labeling, added after a live run came
back scope-distributed India=47/World=36/Punjab=25 - including tagging an NFL
brain-injury study and a Nigerian kidnapping story as "India":
  1. A relevance gate runs before scope classification. A fact whose max
     relevance across all 11 dimensions falls below the 5th percentile of the
     fabricated seed corpus's own max-relevance distribution isn't
     meaningfully close to anything this system models - it's excluded
     entirely (no scope, not stored, not used downstream) and logged to
     data/ingestion_excluded.jsonl instead of silently dropped.
  2. Facts that pass the gate get scope from a per-class-best-match rule, not
     pooled top-k plurality voting: for each of the 7 scope classes, only
     that class's single closest seed article competes. This is what
     actually fixes the bias - pooled voting let India/Punjab win purely by
     having more seed articles nearby, regardless of how well any one of
     them matched.

Sources (all free, no API key, no paid tier):
  - BBC World RSS and Al Jazeera RSS - standard publisher feeds.
  - Google News RSS, queried by topic (WORLD), not scoped to any one outlet.
  - GDELT DOC 2.0 API via the open-source `gdeltdoc` package - NOT "GDELT
    Cloud" (gdeltcloud.com), which is a separate paid product requiring a key.
Reuters is not used: its public RSS was discontinued in 2020 and programmatic
access now requires a paid license.

Only title, publish timestamp, link, and the extracted/inferred tags are
stored - no raw article body text, and no vector database. This appends to
the same flat JSON + .npy embedding structure the fabricated dataset already
uses, kept in separate files (data/real_articles.json, data/real_facts.json,
real_fact_embeddings.npy) so real data never mixes into the fabricated
startups' training data. Writes go through atomic_io so a concurrent reader
never sees a half-written file.

This is the ONE implementation of the pipeline: scripts/ingest_news.py (a
thin manual/cron-friendly CLI) and ingestion_service.py (a standalone,
self-scheduling microservice) both call run_ingestion_once() from here rather
than duplicating any of this logic.
"""
import calendar
import html
import json
from datetime import datetime, timedelta, timezone

import feedparser
import numpy as np

from .atomic_io import atomic_write_json, atomic_write_npy
from .comparative_matching import resolve_comparative_fact
from .config import (
    DATA_DIR,
    DEDUP_SIMILARITY_THRESHOLD,
    DEDUP_WINDOW_HOURS,
    INGESTION_EXCLUDED_LOG_PATH,
    INGESTION_NONCONTENT_LOG_PATH,
    INGESTION_SAMPLE_LOG_PATH,
    INGESTION_STATE_PATH,
    INGESTION_UNGROUNDED_LOG_PATH,
    INGESTION_UNMATCHED_LOG_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    REAL_ARTICLES_PATH,
    REAL_FACT_EMBEDDINGS_PATH,
    REAL_FACTS_PATH,
)
from .data_loader import load_news, load_real_facts
from .embeddings import embed_text
from .fact_extraction import extract_facts_detailed
from .grounding import is_grounded, is_likely_non_content
from .real_data_inference import (
    assess_dimension_coverage,
    assess_scope_coverage,
    choose_gate_threshold,
    infer_hybrid,
    infer_scope_hybrid,
)
from .seed_inference import group_indices_by_scope

USER_AGENT = "Mozilla/5.0 (compatible; MarketIntelBot/0.1)"
SAMPLE_LOG_SIZE = 8
GDELT_LOOKBACK_HOURS = 6  # first-run-only fallback window; later runs use the state cursor
GDELT_KEYWORD = "world"

RSS_FEEDS = {
    "bbc_world": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "google_news_world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
}


def load_state() -> dict:
    if INGESTION_STATE_PATH.exists():
        with open(INGESTION_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    atomic_write_json(INGESTION_STATE_PATH, state)


def load_existing():
    """Returns (articles, facts, fact_embeddings)."""
    articles = []
    if REAL_ARTICLES_PATH.exists():
        with open(REAL_ARTICLES_PATH, encoding="utf-8") as f:
            articles = json.load(f)

    if REAL_FACTS_PATH.exists() and REAL_FACT_EMBEDDINGS_PATH.exists():
        with open(REAL_FACTS_PATH, encoding="utf-8") as f:
            facts = json.load(f)
        fact_embeddings = list(np.load(REAL_FACT_EMBEDDINGS_PATH))
    else:
        facts, fact_embeddings = [], []

    return articles, facts, fact_embeddings


def save_existing(articles: list[dict], facts: list[dict], fact_embeddings: list[np.ndarray]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(REAL_ARTICLES_PATH, articles)
    atomic_write_json(REAL_FACTS_PATH, facts)
    atomic_write_npy(REAL_FACT_EMBEDDINGS_PATH, np.array(fact_embeddings))


def parse_published(entry) -> datetime:
    if entry.get("published_parsed"):
        return datetime.fromtimestamp(calendar.timegm(entry.published_parsed), tz=timezone.utc)
    return datetime.now(timezone.utc)


def fetch_rss(url: str, since: datetime | None) -> list[dict]:
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    raw = urllib.request.urlopen(req, timeout=20).read()
    parsed = feedparser.parse(raw)

    items = []
    for entry in parsed.entries:
        published = parse_published(entry)
        if since is not None and published <= since:
            continue
        title = html.unescape(entry.get("title", "").strip())
        if not title:
            continue
        items.append({"title": title, "link": entry.get("link", ""), "published": published})
    return items


def parse_gdelt_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def fetch_gdelt(since: datetime | None) -> list[dict]:
    """GDELT DOC 2.0 API (free, no key) via the open-source `gdeltdoc` package -
    not GDELT Cloud, which is a separate paid product.

    Scope note: GDELT is the one source here that publishes structured
    geography rather than leaving it to be inferred, which is why it is
    excluded from SOURCE_FIXED_SCOPE - a blanket "World" would be strictly
    worse than what GDELT actually knows. The now-removed bulk-backfill path
    used exactly that, tiering World/India/Punjab off the GKG country and ADM1
    columns.

    This LIVE path, however, currently keeps only title/link/published from
    each row and never captures the DOC API's own `sourcecountry` field, so
    there is no structured geography in hand at scoring time and these facts
    still fall through to the content classifier. Wiring `sourcecountry` (and
    a country -> scope mapping) through would remove the last classifier
    dependency; that is a real, self-contained follow-up, deliberately not
    done here since it is beyond a scope-tagging change.
    """
    from gdeltdoc import Filters, GdeltDoc

    now = datetime.now(timezone.utc)
    start = since or (now - timedelta(hours=GDELT_LOOKBACK_HOURS))
    filters = Filters(
        keyword=GDELT_KEYWORD,
        start_date=start.replace(tzinfo=None),
        end_date=now.replace(tzinfo=None),
        num_records=250,
    )
    df = GdeltDoc().article_search(filters)

    items = []
    for _, row in df.iterrows():
        title = html.unescape(str(row.get("title") or "").strip())
        if not title:
            continue
        published = parse_gdelt_date(row.get("seendate"))
        if since is not None and published <= since:
            continue
        items.append({"title": title, "link": str(row.get("url") or ""), "published": published})
    return items


def make_rss_fetcher(url: str):
    return lambda since: fetch_rss(url, since)


SOURCES = {
    "bbc_world": make_rss_fetcher(RSS_FEEDS["bbc_world"]),
    "aljazeera": make_rss_fetcher(RSS_FEEDS["aljazeera"]),
    "google_news_world": make_rss_fetcher(RSS_FEEDS["google_news_world"]),
    "gdelt_world": fetch_gdelt,
}

# Sources whose scope is a property of the SOURCE, not of the article text, so
# it is set directly and the content-embedding scope classifier is skipped
# entirely for them.
#
# These three are world/international wire feeds: BBC World, Al Jazeera, and
# Google News queried on its WORLD topic. Every item they return is
# world-level by construction, so asking a per-class-best-match embedding
# classifier "which of the 7 scopes is this?" could only ever introduce error -
# and demonstrably did: it previously tagged an NFL story and a Nigerian
# kidnapping story with India-level scope (see this module's docstring and
# CLAUDE.md's scope-fix entry).
#
# gdelt_world is deliberately NOT in this map. Not because GDELT is
# world-only - the opposite: GDELT publishes structured per-article geography
# (country and ADM1 codes) that is strictly better than a blanket "World", so
# collapsing it here would throw away real granularity. See the note on
# fetch_gdelt() for why the LIVE DOC-API path can't currently use those fields.
SOURCE_FIXED_SCOPE = {
    "bbc_world": "World",
    "aljazeera": "World",
    "google_news_world": "World",
}


def find_duplicate_fact(new_embedding: np.ndarray, facts: list[dict], fact_embeddings: list[np.ndarray], now: datetime):
    """Cosine similarity against every fact published within the dedup window
    (embeddings are already L2-normalized, so dot product = cosine similarity).
    The same fact reported by multiple outlets collapses into one record here,
    at fact granularity rather than article granularity."""
    cutoff = now - timedelta(hours=DEDUP_WINDOW_HOURS)
    candidate_idx = [i for i, f in enumerate(facts) if datetime.fromisoformat(f["published"]) >= cutoff]
    if not candidate_idx:
        return None, 0.0

    candidate_matrix = np.array([fact_embeddings[i] for i in candidate_idx])
    sims = candidate_matrix @ new_embedding
    best_local = int(np.argmax(sims))
    best_sim = float(sims[best_local])
    if best_sim >= DEDUP_SIMILARITY_THRESHOLD:
        return candidate_idx[best_local], best_sim
    return None, best_sim


def run_ingestion_once(verbose: bool = True) -> dict:
    """Runs one full ingestion pass across all sources - fetch, decompose into
    facts, dedup, embed, relevance gate, scope classification, atomic save - and
    returns a summary dict. The single entry point both scripts/ingest_news.py
    and ingestion_service.py call; nothing about the pipeline itself should live
    anywhere else."""

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    seed_news, seed_embeddings = load_news()
    fabricated_scope_indices = group_indices_by_scope(seed_news)

    state = load_state()
    articles, facts, fact_embeddings = load_existing()

    # Frozen snapshot of the real corpus BEFORE this run's new facts get appended -
    # "new real facts get scored against older real facts", not against each other
    # from within the same batch. See real_data_inference.py for the coverage-gated
    # per-dimension/per-scope-class blending policy this feeds into.
    real_pool_facts = list(facts)
    real_pool_embeddings = np.array(fact_embeddings) if fact_embeddings else np.empty((0, 384))
    dimension_coverage = assess_dimension_coverage(real_pool_facts)
    scope_coverage = assess_scope_coverage(real_pool_facts)
    real_scope_indices = group_indices_by_scope(real_pool_facts) if real_pool_facts else {}
    relevance_threshold, gate_source = choose_gate_threshold(real_pool_facts, seed_news)

    log(f"Relevance gate threshold ({gate_source} corpus, 5th percentile): {relevance_threshold:.4f}")
    log(f"Real-data dimension coverage ({len(real_pool_facts)} accumulated real facts): "
        + ", ".join(f"{d}={'real' if ok else 'fabricated'}" for d, ok in dimension_coverage.items()))
    log(f"Real-data scope coverage: "
        + ", ".join(f"{s}={'real' if ok else 'fabricated'}" for s, ok in scope_coverage.items()) + "\n")

    next_article_id = len(articles) + 1
    next_fact_id = len(facts) + 1
    now = datetime.now(timezone.utc)

    articles_fetched = 0
    facts_extracted = 0
    new_count, dup_count, excluded_count = 0, 0, 0
    noncontent_count, ungrounded_count = 0, 0
    comparative_matched_count, comparative_unmatched_count = 0, 0
    polarity_from_real_count, polarity_from_fabricated_count = 0, 0
    sample_log = []
    excluded_log = []

    for source_id, fetch in SOURCES.items():
        since_str = state.get(source_id, {}).get("last_published")
        since = datetime.fromisoformat(since_str) if since_str else None

        try:
            items = fetch(since)
        except Exception as exc:
            log(f"[{source_id}] fetch failed: {exc}")
            continue

        articles_fetched += len(items)
        latest_published = since
        for item in items:
            article_fact_ids: list[str] = []

            is_junk, junk_reason = is_likely_non_content(item["title"])
            if is_junk:
                noncontent_count += 1
                with open(INGESTION_NONCONTENT_LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(json.dumps({
                        "title": item["title"], "published": item["published"].isoformat(),
                        "reason": junk_reason, "logged_at": now.isoformat(),
                    }) + "\n")
                fact_records = []
            else:
                fact_records = extract_facts_detailed(item["title"])
                facts_extracted += len(fact_records)

            for fact_record in fact_records:
                fact_text, entities = fact_record["text"], fact_record["entities"]

                grounded, ungrounded_numbers = is_grounded(fact_text, item["title"])
                if not grounded:
                    ungrounded_count += 1
                    with open(INGESTION_UNGROUNDED_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "fact_text": fact_text, "entities": entities, "source_title": item["title"],
                            "ungrounded_numbers": ungrounded_numbers,
                            "published": item["published"].isoformat(), "logged_at": now.isoformat(),
                        }) + "\n")
                    continue

                embedding = embed_text(fact_text)
                dup_idx, sim = find_duplicate_fact(embedding, facts, fact_embeddings, now)

                if dup_idx is not None:
                    facts[dup_idx]["mention_count"] += 1
                    facts[dup_idx]["last_seen"] = now.isoformat()
                    article_fact_ids.append(facts[dup_idx]["id"])
                    dup_count += 1
                    continue

                relevance, polarity, inference_source = infer_hybrid(
                    embedding, real_pool_facts, real_pool_embeddings, seed_news, seed_embeddings, dimension_coverage
                )
                max_relevance = max(relevance.values())

                if max_relevance < relevance_threshold:
                    excluded_count += 1
                    excluded_log.append({
                        "fact_text": fact_text,
                        "source_title": item["title"],
                        "published": item["published"].isoformat(),
                        "max_relevance": max_relevance,
                    })
                    continue

                # Scope comes from the SOURCE where the source already
                # determines it (see SOURCE_FIXED_SCOPE), and only falls back to
                # the content classifier for sources that don't - currently just
                # gdelt_world. scope_source records which applied, so a
                # spot-check can tell a source-assigned tag from an inferred one.
                fixed_scope = SOURCE_FIXED_SCOPE.get(source_id)
                if fixed_scope is not None:
                    scope, scope_source = fixed_scope, "source"
                else:
                    scope, _, scope_source = infer_scope_hybrid(
                        embedding, real_pool_embeddings, real_scope_indices,
                        seed_embeddings, fabricated_scope_indices, scope_coverage,
                    )
                pestle_scores = {d: relevance[d] for d in PESTLE_DIMS}
                porters_scores = {d: relevance[d] for d in PORTERS_DIMS}

                # Comparative-fact matching (see comparative_matching.py) - shared with the
                # historical bulk backfill. `facts` here is the SAME growing in-memory list this
                # loop appends to below, so a bare state-value fact can match against
                # anything already ingested earlier in THIS run or a prior one.
                comparative = resolve_comparative_fact(
                    fact_text, entities, embedding, item["published"], facts, fact_embeddings
                )
                if comparative["has_own_direction"]:
                    pass  # self-contained, nothing to log
                elif comparative["matched_prior_fact_id"] is not None:
                    comparative_matched_count += 1
                else:
                    comparative_unmatched_count += 1
                    with open(INGESTION_UNMATCHED_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "fact_text": fact_text, "entities": entities,
                            "published": item["published"].isoformat(),
                            "best_similarity_seen": comparative["match_similarity"],
                            "logged_at": now.isoformat(),
                        }) + "\n")

                fact_id = f"fact_{next_fact_id:05d}"
                facts.append({
                    "id": fact_id,
                    "parent_article_id": None,  # filled in once the article id is known, below
                    "fact_text": fact_text,
                    "entities": entities,
                    "published": item["published"].isoformat(),
                    "scope": scope,
                    "pestle_scores": pestle_scores,
                    "porters_scores": porters_scores,
                    "polarity": polarity,
                    "comparative": comparative,
                    "mention_count": 1,
                    "first_seen": now.isoformat(),
                    "last_seen": now.isoformat(),
                    # Which pool each part of this fact's inference actually came from -
                    # see real_data_inference.py. Kept per-fact (not just logged in
                    # aggregate) so a spot-check can see exactly why any given fact was
                    # scored the way it was.
                    "inference_source": inference_source,
                    "scope_source": scope_source,
                })
                fact_embeddings.append(embedding)
                next_fact_id += 1
                new_count += 1
                article_fact_ids.append(fact_id)
                if inference_source["polarity_source"] == "real":
                    polarity_from_real_count += 1
                else:
                    polarity_from_fabricated_count += 1

                if len(sample_log) < SAMPLE_LOG_SIZE:
                    sample_log.append({
                        "fact_text": fact_text,
                        "source_title": item["title"],
                        "relevance": relevance,
                        "polarity": polarity,
                        "scope": scope,
                    })

            if article_fact_ids:
                article_id = f"article_{next_article_id:05d}"
                for fid in article_fact_ids:
                    fact = next(f for f in facts if f["id"] == fid)
                    if fact["parent_article_id"] is None:
                        fact["parent_article_id"] = article_id
                articles.append({
                    "id": article_id,
                    "title": item["title"],
                    "link": item["link"],
                    "published": item["published"].isoformat(),
                    "source": source_id,
                    "fact_ids": article_fact_ids,
                    "first_seen": now.isoformat(),
                })
                next_article_id += 1

            if latest_published is None or item["published"] > latest_published:
                latest_published = item["published"]

        state[source_id] = {
            "last_published": (latest_published or now).isoformat(),
            "last_run": now.isoformat(),
        }
        log(f"[{source_id}] fetched {len(items)} article(s) newer than {since}")

    save_existing(articles, facts, fact_embeddings)
    save_state(state)

    log(
        f"\n{articles_fetched} article(s) fetched, {noncontent_count} rejected as non-content before "
        f"decomposition -> {facts_extracted} fact(s) extracted, {ungrounded_count} rejected as ungrounded: "
        f"{new_count} new, {dup_count} deduplicated, {excluded_count} excluded by the relevance gate."
    )
    log(
        f"Comparative-fact matching: {comparative_matched_count} matched a prior value, "
        f"{comparative_unmatched_count} left unmatched (see {INGESTION_UNMATCHED_LOG_PATH})."
    )
    log(
        f"Polarity source for new facts: {polarity_from_real_count} from the real corpus, "
        f"{polarity_from_fabricated_count} from the fabricated corpus (per-dimension relevance "
        f"blending happens per-fact too - see each fact's \"inference_source\" field)."
    )
    log(f"Total real_facts records: {len(facts)} (from {len(articles)} provenance article records)\n")

    if excluded_log:
        with open(INGESTION_EXCLUDED_LOG_PATH, "a", encoding="utf-8") as log_file:
            for entry in excluded_log:
                log_file.write(json.dumps({"logged_at": now.isoformat(), **entry}) + "\n")
        log(f"({len(excluded_log)} excluded fact(s) appended to {INGESTION_EXCLUDED_LOG_PATH})\n")

    if sample_log:
        log("Sample for spot-checking (compare fact_text against source_title for hallucinated/dropped details):")
        with open(INGESTION_SAMPLE_LOG_PATH, "a", encoding="utf-8") as log_file:
            for entry in sample_log:
                top_dims = sorted(entry["relevance"].items(), key=lambda kv: -kv[1])[:2]
                top_str = ", ".join(f"{d}={v:.2f}" for d, v in top_dims)
                log(f"  [{entry['polarity']:>8} | {entry['scope']:>11}] {entry['fact_text']}")
                log(f"             from: {entry['source_title']}")
                log(f"             top relevance: {top_str}")
                log_file.write(json.dumps({"logged_at": now.isoformat(), **entry}) + "\n")
        log(f"\n(appended to {INGESTION_SAMPLE_LOG_PATH} for later review)")

    return {
        "articles_fetched": articles_fetched,
        "articles_rejected_noncontent": noncontent_count,
        "facts_extracted": facts_extracted,
        "facts_added": new_count,
        "facts_deduped": dup_count,
        "facts_excluded": excluded_count,
        "facts_rejected_ungrounded": ungrounded_count,
        "comparative_matches_found": comparative_matched_count,
        "comparative_matches_unmatched": comparative_unmatched_count,
        "polarity_from_real": polarity_from_real_count,
        "polarity_from_fabricated": polarity_from_fabricated_count,
        "dimension_coverage": dimension_coverage,
        "scope_coverage": scope_coverage,
        "gate_threshold_source": gate_source,
        "total_fact_records": len(facts),
    }

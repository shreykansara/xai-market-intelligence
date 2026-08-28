"""Historical World/India backfill from GDELT 2.0 bulk export files - a separate,
one-off/batch collection process from the live ingestion_service.py (which keeps
running independently, on its own 30-minute schedule, for ongoing Punjab/LPU-area
coverage via RSS + GDELT DOC 2.0 API). Writes to its own files
(BACKFILL_ARTICLES_PATH / BACKFILL_FACTS_PATH / BACKFILL_FACT_EMBEDDINGS_PATH) -
never the live ingestion_service.py's real_articles.json/real_facts.json - so the
two processes never contend over the same files and a live-pipeline bug can't
corrupt backfill progress or vice versa. Merging this historical data into
server.py's live scoring path is explicitly out of scope for this module (tracked
separately, per CLAUDE.md).

Pipeline order for this batch process is DELIBERATELY DIFFERENT from the live
ingestion.py's per-item order (which stays unchanged): fetch -> embed ->
relevance gate -> only then run fact decomposition (Ollama) on survivors ->
dedup -> seed inference (relevance/polarity/scope) -> comparative-fact matching
-> atomic write. The relevance gate runs BEFORE the expensive Ollama call here
specifically to avoid decomposing articles that were never going to pass the
gate anyway - at GDELT's bulk volume this ordering is what keeps the dominant
Ollama cost bounded to only the ~50% of records that actually clear the gate,
rather than 100% of them (see the timing pilot in CLAUDE.md's backfill section).

Because a real run at even the India-only tier is estimated at several months
of continuous unattended processing, this is checkpointed and resumable at the
granularity of one 15-minute GKG file: BACKFILL_STATE_PATH records the last
successfully processed timestamp per tier, and the accumulated
articles/facts/embeddings are only re-written to disk (atomically) every
CHECKPOINT_EVERY_N_FILES files rather than after every single one - rewriting a
multi-million-record JSON file after every 15 minutes' worth of data would
itself become a real cost over a run this long. A crash or interruption between
checkpoints loses at most that window's progress, never anything already
flushed, and a restart resumes from the last flushed timestamp rather than
re-processing from the beginning.

Comparative-fact matching's per-fact prior-match search (comparative_matching.py)
is backed by an in-memory entity -> fact-index inverted index here (see
_EntityIndex below) rather than scanning every stored fact for entity overlap on
every new fact - at this data's scale (potentially millions of stored facts by
the end of a full run), an O(n) scan per fact would compound into real time
over the run, even though it's dwarfed by the ~3s/call Ollama cost for any
single file's worth of data.
"""
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import numpy as np

from .atomic_io import atomic_write_json, atomic_write_npy
from .comparative_matching import normalize_entities, resolve_comparative_fact
from .config import (
    BACKFILL_ARTICLES_PATH,
    BACKFILL_EXCLUDED_LOG_PATH,
    BACKFILL_FACT_EMBEDDINGS_PATH,
    BACKFILL_FACTS_PATH,
    BACKFILL_STATE_PATH,
    BACKFILL_UNMATCHED_LOG_PATH,
    DATA_DIR,
    DEDUP_SIMILARITY_THRESHOLD,
    DEDUP_WINDOW_HOURS,
    PESTLE_DIMS,
    PORTERS_DIMS,
)
from .data_loader import load_news
from .embeddings import embed_text, embed_texts
from .fact_extraction import extract_facts_detailed
from .gdelt_bulk import gkg_timestamps, fetch_and_filter
from .seed_inference import (
    calibrate_relevance_threshold,
    group_indices_by_scope,
    infer_categorical,
    infer_relevance,
    infer_scope_best_match,
    nearest_neighbors,
)

CHECKPOINT_EVERY_N_FILES = 20  # ~5 hours of GKG data between disk flushes


class _EntityIndex:
    """Inverted index (normalized entity string -> fact indices mentioning it),
    kept in sync as facts are appended, so comparative-fact matching only ever
    has to consider facts sharing at least one entity with the new fact -
    never the full store. See the module docstring for why this matters at
    backfill scale."""

    def __init__(self):
        self._index: dict[str, list[int]] = defaultdict(list)

    def add(self, fact_idx: int, entities: list[str]) -> None:
        for e in normalize_entities(entities):
            self._index[e].append(fact_idx)

    def candidates_for(self, entities: list[str]) -> list[int]:
        seen = set()
        result = []
        for e in normalize_entities(entities):
            for idx in self._index.get(e, ()):
                if idx not in seen:
                    seen.add(idx)
                    result.append(idx)
        return result

    def rebuild(self, facts: list[dict]) -> None:
        self._index = defaultdict(list)
        for i, f in enumerate(facts):
            self.add(i, f.get("entities", []))


def load_state() -> dict:
    if BACKFILL_STATE_PATH.exists():
        with open(BACKFILL_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict) -> None:
    atomic_write_json(BACKFILL_STATE_PATH, state)


def load_existing():
    """Returns (articles, facts, fact_embeddings) from the backfill's OWN store -
    entirely separate from the live pipeline's real_articles.json/real_facts.json."""
    articles = []
    if BACKFILL_ARTICLES_PATH.exists():
        with open(BACKFILL_ARTICLES_PATH, encoding="utf-8") as f:
            articles = json.load(f)

    if BACKFILL_FACTS_PATH.exists() and BACKFILL_FACT_EMBEDDINGS_PATH.exists():
        with open(BACKFILL_FACTS_PATH, encoding="utf-8") as f:
            facts = json.load(f)
        fact_embeddings = list(np.load(BACKFILL_FACT_EMBEDDINGS_PATH))
    else:
        facts, fact_embeddings = [], []

    return articles, facts, fact_embeddings


def save_existing(articles: list[dict], facts: list[dict], fact_embeddings: list[np.ndarray]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    atomic_write_json(BACKFILL_ARTICLES_PATH, articles)
    atomic_write_json(BACKFILL_FACTS_PATH, facts)
    atomic_write_npy(BACKFILL_FACT_EMBEDDINGS_PATH, np.array(fact_embeddings) if fact_embeddings else np.empty((0, 384)))


def find_duplicate_fact(
    new_embedding: np.ndarray, published: datetime, facts: list[dict], fact_embeddings: list[np.ndarray]
):
    """Backfill-specific dedup: the comparison window is relative to THIS FACT'S
    OWN published timestamp, not wall-clock "now" - deliberately different from
    the live ingestion.py's find_duplicate_fact, which dedups against a window
    ending at the moment the ingestion run executes (correct for a live stream,
    meaningless for a historical replay where "now" has nothing to do with when
    anything in the backfill actually happened). Only compares against facts
    published within DEDUP_WINDOW_HOURS BEFORE this fact - a later fact can't be
    "the same report" of an earlier one from the future."""
    window_start = published - timedelta(hours=DEDUP_WINDOW_HOURS)
    candidate_idx = [
        i for i, f in enumerate(facts)
        if window_start <= datetime.fromisoformat(f["published"]) <= published
    ]
    if not candidate_idx:
        return None, 0.0

    candidate_matrix = np.array([fact_embeddings[i] for i in candidate_idx])
    sims = candidate_matrix @ new_embedding
    best_local = int(np.argmax(sims))
    best_sim = float(sims[best_local])
    if best_sim >= DEDUP_SIMILARITY_THRESHOLD:
        return candidate_idx[best_local], best_sim
    return None, best_sim


def run_backfill(
    start: datetime,
    end: datetime,
    tier: str,
    verbose: bool = True,
    checkpoint_every_n_files: int = CHECKPOINT_EVERY_N_FILES,
) -> dict:
    """Runs the reordered batch pipeline over every 15-minute GKG file in
    [start, end) for the given tier ("world" or "india"), resuming from
    BACKFILL_STATE_PATH's last checkpoint if this tier has been run before.
    Returns a summary dict; also usable as a long-running unattended process
    (safe to interrupt and re-invoke with the same start/end/tier - it picks up
    where it left off)."""

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    seed_news, seed_embeddings = load_news()
    relevance_threshold = calibrate_relevance_threshold(seed_news)
    scope_indices = group_indices_by_scope(seed_news)
    log(f"Relevance gate threshold (5th percentile of seed corpus): {relevance_threshold:.4f}")
    log(f"Tier: {tier}\n")

    state = load_state()
    tier_state = state.get(tier, {})
    resume_from = datetime.fromisoformat(tier_state["last_processed"]) + timedelta(minutes=1) \
        if tier_state.get("last_processed") else start
    if resume_from > start:
        log(f"Resuming tier {tier!r} from {resume_from.isoformat()} (checkpoint found)")

    articles, facts, fact_embeddings = load_existing()
    entity_index = _EntityIndex()
    entity_index.rebuild(facts)
    next_article_id = len(articles) + 1
    next_fact_id = len(facts) + 1

    totals = {
        "files_attempted": 0, "files_failed": 0,
        "articles_seen": 0, "articles_gated_out": 0,
        "facts_extracted": 0, "facts_added": 0, "facts_deduped": 0,
        "comparative_matches_found": 0, "comparative_matches_unmatched": 0,
    }
    files_since_checkpoint = 0

    for timestamp in gkg_timestamps(resume_from, end):
        totals["files_attempted"] += 1
        records = fetch_and_filter(timestamp, tier)
        if records is None:
            totals["files_failed"] += 1
            log(f"[{timestamp.isoformat()}] fetch failed - skipping")
            continue

        totals["articles_seen"] += len(records)
        if records:
            title_embeddings = embed_texts([r["title"] for r in records])
            for record, title_embedding in zip(records, title_embeddings):
                top_idx, weights = nearest_neighbors(title_embedding, seed_embeddings)
                relevance = infer_relevance(seed_news, top_idx, weights)
                if max(relevance.values()) < relevance_threshold:
                    totals["articles_gated_out"] += 1
                    with open(BACKFILL_EXCLUDED_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps({
                            "title": record["title"], "published": record["published"].isoformat(),
                            "max_relevance": max(relevance.values()),
                        }) + "\n")
                    continue

                fact_records = extract_facts_detailed(record["title"])
                totals["facts_extracted"] += len(fact_records)
                article_fact_ids = []

                for fact_record in fact_records:
                    fact_text, entities = fact_record["text"], fact_record["entities"]
                    fact_embedding = embed_text(fact_text)

                    dup_idx, _ = find_duplicate_fact(fact_embedding, record["published"], facts, fact_embeddings)
                    if dup_idx is not None:
                        facts[dup_idx]["mention_count"] += 1
                        facts[dup_idx]["last_seen"] = record["published"].isoformat()
                        article_fact_ids.append(facts[dup_idx]["id"])
                        totals["facts_deduped"] += 1
                        continue

                    top_idx, weights = nearest_neighbors(fact_embedding, seed_embeddings)
                    fact_relevance = infer_relevance(seed_news, top_idx, weights)
                    polarity = infer_categorical(seed_news, top_idx, weights, "polarity")
                    scope, _ = infer_scope_best_match(fact_embedding, seed_embeddings, scope_indices)

                    candidate_pool = entity_index.candidates_for(entities)
                    comparative = resolve_comparative_fact(
                        fact_text, entities, fact_embedding, record["published"],
                        facts, fact_embeddings, candidate_pool_idx=candidate_pool,
                    )
                    if comparative["has_own_direction"]:
                        pass  # self-contained, nothing to log
                    elif comparative["matched_prior_fact_id"] is not None:
                        totals["comparative_matches_found"] += 1
                    else:
                        totals["comparative_matches_unmatched"] += 1
                        with open(BACKFILL_UNMATCHED_LOG_PATH, "a", encoding="utf-8") as f:
                            f.write(json.dumps({
                                "fact_text": fact_text, "entities": entities,
                                "published": record["published"].isoformat(),
                                "best_similarity_seen": comparative["match_similarity"],
                            }) + "\n")

                    fact_id = f"backfill_fact_{next_fact_id:06d}"
                    facts.append({
                        "id": fact_id,
                        "parent_article_id": None,
                        "fact_text": fact_text,
                        "entities": entities,
                        "published": record["published"].isoformat(),
                        "scope": scope,
                        "pestle_scores": {d: fact_relevance[d] for d in PESTLE_DIMS},
                        "porters_scores": {d: fact_relevance[d] for d in PORTERS_DIMS},
                        "polarity": polarity,
                        "mention_count": 1,
                        "comparative": comparative,
                        "title_source": record["title_source"],
                    })
                    fact_embeddings.append(fact_embedding)
                    entity_index.add(len(facts) - 1, entities)
                    next_fact_id += 1
                    totals["facts_added"] += 1
                    article_fact_ids.append(fact_id)

                if article_fact_ids:
                    article_id = f"backfill_article_{next_article_id:06d}"
                    for fid in article_fact_ids:
                        fact = next(f for f in facts if f["id"] == fid)
                        if fact["parent_article_id"] is None:
                            fact["parent_article_id"] = article_id
                    articles.append({
                        "id": article_id,
                        "title": record["title"],
                        "url": record["url"],
                        "published": record["published"].isoformat(),
                        "tier": tier,
                        "fact_ids": article_fact_ids,
                    })
                    next_article_id += 1

        tier_state["last_processed"] = timestamp.isoformat()
        state[tier] = tier_state
        files_since_checkpoint += 1

        if files_since_checkpoint >= checkpoint_every_n_files:
            save_existing(articles, facts, fact_embeddings)
            save_state(state)
            files_since_checkpoint = 0
            log(f"[checkpoint] {timestamp.isoformat()} - {len(facts)} total fact(s), "
                f"{totals['files_attempted']} file(s) attempted so far")

    # Final flush regardless of checkpoint cadence, so the tail of a run is never lost.
    save_existing(articles, facts, fact_embeddings)
    save_state(state)

    log(f"\nBackfill run complete for tier {tier!r}: {totals}")
    return totals

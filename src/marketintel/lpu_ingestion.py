"""Builds the system's ONLY news corpus from the real LPU announcements in
data/lpudata/, replacing the removed fabricated seed corpus and live-ingested
feed entirely.

Pipeline, per announcement:
    load + dedupe -> normalize date -> ATOMIC BREAKDOWN (fact_extraction.py)
    -> classify each fact (lpu_classification.py) -> tag scope=LPU
    -> embed each fact -> atomic write

Two properties this guarantees, both explicitly required:

1. **Every stored record is atomic.** A compound announcement ("the exam is on
   the 2nd AND the fee deadline moves to the 5th") is broken into separate
   independently-scorable facts by the SAME fact_extraction.extract_facts_detailed()
   the live news pipeline used - reused, not reimplemented, so there is exactly
   one decomposition implementation in the codebase. The stored unit is the
   fact, never the raw announcement; announcements are kept only as provenance
   containers (which facts came out of them), the same split real_articles.json
   / real_facts.json used before.

2. **Every stored record is tagged as LPU.** scope="LPU", source="lpu" and
   is_lpu=True are set by construction, not inferred - these are university
   announcements by definition, so there is no scope classification to get
   wrong here (unlike wire news, where scope had to be inferred per item).

The raw data arrives as five separate scrape files. They are NOT snapshots of
one another: they cover disjoint date ranges (2011-2026 between them) with
zero content overlap, and their `id` fields are per-file row numbers that
collide across files while pointing at completely different announcements.
Records are therefore deduped by CONTENT (see _content_key), which yields
44,695 unique announcements - deduping on `id` instead would have discarded
roughly 36k of them.

Cost note: this makes two Ollama calls per announcement (one breakdown, one
batched classification of all that announcement's facts) on a CPU-only local
model, so the full corpus is a multi-day unattended run. It is checkpointed to
LPU_STATE_PATH every LPU_CHECKPOINT_EVERY announcements and resumes from the
last flush - an interruption costs at most that window, never the whole run.
Use `limit` to build a smaller corpus now and extend it later; a resumed run
picks up exactly where it stopped, so the corpus grows monotonically rather
than needing one uninterrupted pass.
"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .atomic_io import atomic_write_json, atomic_write_npy
from .config import (
    LPU_ANNOUNCEMENTS_PATH,
    LPU_CHECKPOINT_EVERY,
    LPU_FACT_EMBEDDINGS_PATH,
    LPU_FACTS_PATH,
    LPU_MAX_DECOMPOSITION_CHARS,
    LPU_RAW_DIR,
    LPU_SCOPE,
    LPU_STATE_PATH,
    GROQ_MODEL,
)
from .embeddings import embed_text
from .fact_extraction import extract_facts_with_status
from .groq_client import API_KEY_ENV_VAR, GroqError, GroqRateLimited, api_key_present, call_groq, rate_limit_state
from .lpu_classification import classify_facts


def _normalize_date(raw: str | None) -> str | None:
    """LPU dates arrive as MM/DD/YYYY (verified empirically: 10,402 records have
    a second component >12 vs. only 13 with a first component >12, so slash-form
    is month-first), with a handful of dash-separated and 2-digit-year strays.
    Tries month-first, falls back to day-first when the month field is out of
    range, and returns None for anything unparseable rather than guessing - a
    wrong date silently mis-orders the corpus."""
    if not raw:
        return None
    text = raw.strip()
    match = re.match(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$", text)
    if not match:
        return None
    a, b, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
    if year < 100:
        year += 2000
    for month, day in ((a, b), (b, a)):  # month-first, then day-first fallback
        try:
            return datetime(year, month, day, tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    return None


def _content_key(record: dict) -> str:
    """Dedup key. Deliberately NOT the source's own `id`: that field is per-file
    ROW NUMBERING, not a stable identifier - verified directly, every one of the
    16,218 ids shared between two of the files points at a completely different
    announcement in each (id=1 is a 2018 viva notice in one file and a 2021
    holiday notice in another). Deduping on it would have silently discarded
    ~36k real announcements. The five files turn out to be disjoint scrapes of
    different date ranges with zero content overlap, so identity has to come
    from the content itself."""
    parts = [
        re.sub(r"\s+", " ", (record.get("title") or "").strip().lower()),
        re.sub(r"\s+", " ", (record.get("body") or "").strip().lower()),
        (record.get("date") or "").strip(),
    ]
    return hashlib.sha1("||".join(parts).encode("utf-8")).hexdigest()


def load_raw_announcements(raw_dir: Path = LPU_RAW_DIR) -> list[dict]:
    """Every unique announcement across the scrape files in data/lpudata/,
    deduped by content (see _content_key) and sorted oldest-first so a resumable
    run always processes them in a stable order. Records with neither a title
    nor a body are dropped - there is nothing to decompose or embed."""
    by_content: dict = {}
    for path in sorted(raw_dir.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                records = json.load(f)
        except (json.JSONDecodeError, ValueError, OSError):
            print(f"  [lpu_ingestion] skipping unreadable file: {path.name}")
            continue
        if not isinstance(records, list):
            continue
        for record in records:
            title = (record.get("title") or "").strip()
            body = (record.get("body") or "").strip()
            if not title and not body:
                continue
            key = _content_key(record)
            by_content.setdefault(key, {
                "id": f"lpu_ann_{key[:16]}",
                "content_key": key,
                "source_file": path.name,
                "source_row_id": str(record.get("id", "")).strip(),
                "title": title,
                "body": body,
                "uploaded_by": (record.get("uploaded_by") or "").strip(),
                "links": record.get("links") or [],
                "published": _normalize_date(record.get("date")),
                "raw_date": record.get("date"),
            })

    announcements = list(by_content.values())
    # Undated records sort last rather than being dropped: the announcement is
    # still real, it just can't be placed on the timeline.
    announcements.sort(key=lambda a: (a["published"] is None, a["published"] or "", a["id"]))
    return announcements


def _announcement_text(announcement: dict, cap: int | None = LPU_MAX_DECOMPOSITION_CHARS) -> str:
    """What gets decomposed: title plus body, truncated to `cap` characters.
    The title alone is often a bare reference number and the body alone often
    lacks the subject, so a fact extracted from either in isolation loses
    context the other supplies - but the full body must NOT be sent unbounded
    (see LPU_MAX_DECOMPOSITION_CHARS: the longest bodies time Ollama out, and
    the timeout fallback stores one unsplit compound fact, defeating the whole
    point of this pipeline). Truncation lands on a word boundary so the model
    never sees a half-word."""
    title, body = announcement["title"], announcement["body"]
    text = f"{title}\n\n{body}" if (title and body) else (title or body)
    if cap is None or len(text) <= cap:
        return text
    clipped = text[:cap]
    cut = clipped.rfind(" ")
    return clipped[:cut] if cut > cap // 2 else clipped


def _load_existing() -> tuple[list[dict], list[dict], np.ndarray, set]:
    """Whatever a previous (possibly interrupted) run already flushed. Any
    unreadable/inconsistent state starts over from empty rather than appending
    onto a corpus whose embeddings no longer line up with its facts."""
    try:
        with open(LPU_STATE_PATH, encoding="utf-8") as f:
            processed = set(json.load(f).get("processed_announcement_ids", []))
        with open(LPU_ANNOUNCEMENTS_PATH, encoding="utf-8") as f:
            announcements = json.load(f)
        with open(LPU_FACTS_PATH, encoding="utf-8") as f:
            facts = json.load(f)
        embeddings = np.load(LPU_FACT_EMBEDDINGS_PATH)
        if len(facts) != len(embeddings):
            raise ValueError("facts/embeddings length mismatch")
        return announcements, facts, embeddings, processed
    except (FileNotFoundError, json.JSONDecodeError, ValueError, OSError, EOFError):
        return [], [], np.empty((0, 0)), set()


def _flush(announcements: list[dict], facts: list[dict], embeddings: list, processed: set) -> None:
    atomic_write_json(LPU_ANNOUNCEMENTS_PATH, announcements)
    atomic_write_json(LPU_FACTS_PATH, facts)
    atomic_write_npy(LPU_FACT_EMBEDDINGS_PATH, np.array(embeddings) if embeddings else np.empty((0, 384)))
    atomic_write_json(LPU_STATE_PATH, {
        "processed_announcement_ids": sorted(processed),
        "facts": len(facts),
        "announcements": len(announcements),
        "last_flush": datetime.now(timezone.utc).isoformat(),
    })


def preflight_llm() -> tuple[bool, str]:
    """Confirms the LLM transport actually works BEFORE a long run starts, by
    making one real (tiny) call rather than just checking that a key exists -
    an invalid or revoked key looks identical to a valid one until it's used.

    Without this, a broken transport doesn't stop anything: every announcement
    quietly takes the unsplit fallback path and the run produces tens of
    thousands of compound, unclassified records that all have to be redone.
    Failing fast is strictly better than that."""
    if not api_key_present():
        return False, (
            f"{API_KEY_ENV_VAR} is not set - export it first "
            "(e.g. `export GROQ_API_KEY=...`); it is read from the environment, never stored in the repo"
        )
    try:
        call_groq("Reply with the single word: ok", temperature=0.0, attempts=1)
    except GroqRateLimited as exc:
        # Already rate limited before starting is a real condition, but not a
        # reason to refuse - the pipeline's own throttling handles it.
        return True, f"Groq reachable but currently rate limited ({exc}) - the run will throttle itself"
    except GroqError as exc:
        return False, f"Groq call failed: {exc}"
    budget = rate_limit_state.snapshot()
    return True, f"Groq reachable, model {GROQ_MODEL!r} responding (budget: {budget})"


def repair_failed_records(verbose: bool = True) -> dict:
    """Re-processes every ALREADY-STORED fact whose decomposition or
    classification failed, in place, so a completed corpus can be brought to
    "every record genuinely processed by the model" without redoing the whole
    run.

    Two distinct repairs:
      - decomposition_ok=False: the stored record is a whole announcement, not
        an atomic fact. Its parent is re-decomposed and the single bad record
        is REPLACED by the resulting atomic facts (so the fact count changes,
        and embeddings are rebuilt for them).
      - classification_ok=False: the text is fine, only its scores are missing,
        so it is re-classified in place with no change to fact identity.
    """
    announcements, facts, embeddings_array, processed = _load_existing()
    if not facts:
        return {"repaired_decomposition": 0, "repaired_classification": 0, "still_failing": 0}

    embeddings = [row for row in embeddings_array]
    by_id = {a["id"]: a for a in announcements}
    stats = {"repaired_decomposition": 0, "repaired_classification": 0, "still_failing": 0}

    # --- 1. Re-decompose records that were stored unsplit -------------------
    bad_indices = [i for i, f in enumerate(facts) if not f.get("decomposition_ok", True)]
    if verbose and bad_indices:
        print(f"Re-decomposing {len(bad_indices)} non-atomic record(s)...")
    # Walk backwards so replacing one record with several doesn't shift the
    # indices of the ones still to process.
    for position in sorted(bad_indices, reverse=True):
        stale = facts[position]
        announcement = by_id.get(stale["parent_announcement_id"])
        if announcement is None:
            stats["still_failing"] += 1
            continue
        text = _announcement_text(announcement)
        extracted, ok = extract_facts_with_status(text)
        if not ok:
            stats["still_failing"] += 1
            continue
        classifications = classify_facts([f["text"] for f in extracted])
        replacements, new_embeddings = [], []
        for extracted_fact, classification in zip(extracted, classifications):
            replacements.append({
                **stale,
                "fact_text": extracted_fact["text"],
                "entities": extracted_fact.get("entities", []),
                "pestle_scores": classification["pestle_scores"],
                "porters_scores": classification["porters_scores"],
                "polarity": classification["polarity"],
                "classification_ok": classification["classification_ok"],
                "decomposition_ok": True,
            })
            new_embeddings.append(embed_text(extracted_fact["text"]))
        facts[position:position + 1] = replacements
        embeddings[position:position + 1] = new_embeddings
        stats["repaired_decomposition"] += 1

    # --- 2. Re-classify records whose text is fine but scores are missing ---
    unclassified = [i for i, f in enumerate(facts) if not f.get("classification_ok", True)]
    if verbose and unclassified:
        print(f"Re-classifying {len(unclassified)} unclassified record(s)...")
    for position in unclassified:
        result = classify_facts([facts[position]["fact_text"]])[0]
        if not result["classification_ok"]:
            stats["still_failing"] += 1
            continue
        facts[position].update({
            "pestle_scores": result["pestle_scores"],
            "porters_scores": result["porters_scores"],
            "polarity": result["polarity"],
            "classification_ok": True,
        })
        stats["repaired_classification"] += 1

    _flush(announcements, facts, embeddings, processed)
    stats["total_facts_in_store"] = len(facts)
    return stats


def run_lpu_ingestion(limit: int | None = None, resume: bool = True, verbose: bool = True) -> dict:
    """Builds (or extends) the LPU fact corpus. Returns run totals.

    `limit` caps how many NOT-YET-PROCESSED announcements this run handles, so a
    partial corpus can be built now and extended later; `resume=False` starts
    over from scratch instead of adding to what's already stored."""
    # Fail fast rather than silently producing a corpus of unsplit, unscored
    # records: without Ollama, every single announcement takes the fallback path.
    ok, detail = preflight_llm()
    if not ok:
        raise RuntimeError(
            f"Refusing to start: {detail}. Fix the LLM transport first - running without it "
            "would store every announcement unsplit and unclassified."
        )
    if verbose:
        print(f"Preflight: {detail}")

    all_announcements = load_raw_announcements()
    announcements, facts, existing_embeddings, processed = _load_existing() if resume else ([], [], np.empty((0, 0)), set())
    embeddings = [row for row in existing_embeddings] if len(existing_embeddings) else []

    pending = [a for a in all_announcements if a["id"] not in processed]
    if limit is not None:
        pending = pending[:limit]

    if verbose:
        print(f"LPU corpus: {len(all_announcements)} unique announcements on disk, "
              f"{len(processed)} already processed, {len(pending)} to do this run.")

    stats = {
        "announcements_seen": len(pending),
        "announcements_undated": 0,
        "facts_added": 0,
        "facts_classified_ok": 0,
        "facts_classification_failed": 0,
        "compound_announcements": 0,
        # Announcements whose breakdown fell back to "store it unsplit" - the
        # atomicity guarantee's own failure count, surfaced rather than hidden.
        "decomposition_fallbacks": 0,
    }
    fact_counter = len(facts)

    for index, announcement in enumerate(pending, start=1):
        text = _announcement_text(announcement)
        if announcement["published"] is None:
            stats["announcements_undated"] += 1

        # 1. ATOMIC BREAKDOWN - reuses the live pipeline's decomposition verbatim,
        # now with retries. The status flag is reported by the extractor itself
        # rather than inferred from the output's shape: the earlier heuristic
        # (does the single returned fact equal the input verbatim?) also flagged
        # genuinely-single-claim notices whose neutral rewrite happened to match
        # their input, so it over-reported failures.
        extracted, decomposition_ok = extract_facts_with_status(text)
        decomposition_failed = not decomposition_ok
        if decomposition_failed:
            stats["decomposition_fallbacks"] += 1
        if len(extracted) > 1:
            stats["compound_announcements"] += 1

        # 2. Classify all of this announcement's facts in one call.
        classifications = classify_facts([f["text"] for f in extracted])

        announcement_fact_ids = []
        for extracted_fact, classification in zip(extracted, classifications):
            fact_counter += 1
            fact_id = f"lpu_fact_{fact_counter:06d}"
            announcement_fact_ids.append(fact_id)
            facts.append({
                "id": fact_id,
                "parent_announcement_id": announcement["id"],
                "fact_text": extracted_fact["text"],
                "entities": extracted_fact.get("entities", []),
                "published": announcement["published"],
                # Tagged by construction, never inferred - these ARE LPU records.
                "scope": LPU_SCOPE,
                "source": "lpu",
                "is_lpu": True,
                "pestle_scores": classification["pestle_scores"],
                "porters_scores": classification["porters_scores"],
                "polarity": classification["polarity"],
                "classification_ok": classification["classification_ok"],
                # False = this record is NOT guaranteed atomic (see above).
                "decomposition_ok": not decomposition_failed,
                "mention_count": 1,
            })
            embeddings.append(embed_text(extracted_fact["text"]))
            stats["facts_added"] += 1
            if classification["classification_ok"]:
                stats["facts_classified_ok"] += 1
            else:
                stats["facts_classification_failed"] += 1

        announcements.append({**announcement, "fact_ids": announcement_fact_ids})
        processed.add(announcement["id"])

        if verbose and index % 5 == 0:
            print(f"  [{index}/{len(pending)}] {stats['facts_added']} facts so far "
                  f"(latest: {len(extracted)} from one announcement)")

        if index % LPU_CHECKPOINT_EVERY == 0:
            _flush(announcements, facts, embeddings, processed)
            if verbose:
                print(f"  checkpoint: {len(facts)} facts / {len(announcements)} announcements written")

    _flush(announcements, facts, embeddings, processed)
    stats["total_facts_in_store"] = len(facts)
    stats["total_announcements_in_store"] = len(announcements)
    stats["remaining_unprocessed"] = len(all_announcements) - len(processed)
    return stats

"""Builds the system's ONLY news corpus from the real LPU announcements in
data/lpudata/, replacing the removed fabricated seed corpus and live-ingested
feed entirely.

Pipeline, per announcement:
    load + dedupe -> normalize date -> pre-filter (grounding.py)
    -> BUNDLED atomic breakdown + classification (fact_pipeline.py, ONE Groq
       call) -> post-decomposition grounding check per fact (grounding.py)
    -> tag scope=LPU -> embed each grounded fact -> atomic write

Three properties this guarantees, all explicitly required:

1. **Every stored record is atomic.** A compound announcement ("the exam is on
   the 2nd AND the fee deadline moves to the 5th") is broken into separate
   independently-scorable facts by fact_pipeline.extract_and_classify_with_status()
   - the SAME decomposition logic the live news pipeline's extraction used,
   now bundled with classification into one call rather than two (see that
   module's docstring for why). The stored unit is the fact, never the raw
   announcement; announcements are kept only as provenance containers.

2. **Every stored record is tagged as LPU.** scope="LPU", source="lpu" and
   is_lpu=True are set by construction, not inferred - these are university
   announcements by definition, so there is no scope classification to get
   wrong here (unlike wire news, where scope had to be inferred per item).

3. **Every stored record has been through the SAME grounding safeguard the
   rest of the system uses.** This was a real, previously-unresolved gap:
   the LPU path had NO grounding check at all, while the live ingestion path
   (ingestion.py) always did. is_likely_non_content() (pre-filter, before any
   Groq call) and is_grounded() (post-decomposition, rejects a fact whose
   number isn't traceable to the source announcement) are both reused
   UNCHANGED from grounding.py - not reimplemented, not skipped for this path.

The raw data arrives as five separate scrape files. They are NOT snapshots of
one another: they cover disjoint date ranges (2011-2026 between them) with
zero content overlap, and their `id` fields are per-file row numbers that
collide across files while pointing at completely different announcements.
Records are therefore deduped by CONTENT (see _content_key), which yields
44,695 unique announcements - deduping on `id` instead would have discarded
roughly 36k of them.

Cost note: this makes ONE Groq call per announcement now (previously two - see
fact_pipeline.py). It is checkpointed to LPU_STATE_PATH every
LPU_CHECKPOINT_EVERY announcements and resumes from the last flush - an
interruption costs at most that window, never the whole run. Use `limit` to
build a smaller corpus now and extend it later; a resumed run picks up exactly
where it stopped, so the corpus grows monotonically rather than needing one
uninterrupted pass.
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
    LPU_NONCONTENT_LOG_PATH,
    LPU_RAW_DIR,
    LPU_SCOPE,
    LPU_STATE_PATH,
    LPU_UNGROUNDED_LOG_PATH,
    GROQ_MODEL,
)
from .embeddings import embed_text
from .fact_pipeline import extract_and_classify_with_status
from .grounding import is_grounded, is_likely_non_content
from .groq_client import API_KEY_ENV_VAR, GroqError, GroqRateLimited, api_key_present, call_groq, rate_limit_state


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


def _process_announcement(announcement: dict, now: datetime | None = None) -> tuple[list[dict], list, dict]:
    """The full per-announcement pipeline, shared by the main ingestion loop
    and repair_failed_records so there is exactly one place this sequence is
    implemented: pre-filter -> bundled decomposition+classification -> per-fact
    grounding check -> embed.

    Returns (fact_records, embeddings, stats_delta). Each fact_record carries
    fact_text/entities/pestle_scores/porters_scores/polarity/decomposition_ok/
    classification_ok - callers attach id/parent_announcement_id/scope/source/
    is_lpu/mention_count themselves, since the two callers assign ids
    differently (a sequential counter vs. preserving/suffixing a stale id)."""
    now = now or datetime.now(timezone.utc)
    text = _announcement_text(announcement)
    stats = {
        "noncontent_skipped": 0, "decomposition_failed": 0, "compound": 0,
        "rejected_by_grounding": 0, "classified_ok": 0, "classification_failed": 0,
    }

    is_junk, junk_reason = is_likely_non_content(announcement["title"])
    if is_junk:
        stats["noncontent_skipped"] = 1
        with open(LPU_NONCONTENT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "announcement_id": announcement["id"], "title": announcement["title"],
                "reason": junk_reason, "logged_at": now.isoformat(),
            }) + "\n")
        return [], [], stats

    extracted, ok = extract_and_classify_with_status(text)
    if not ok:
        stats["decomposition_failed"] = 1
    if len(extracted) > 1:
        stats["compound"] = 1

    # Ground against the FULL, uncapped announcement text - the model may have
    # been given a truncated version (LPU_MAX_DECOMPOSITION_CHARS caps the
    # input), but the true source of truth for whether a number is real is the
    # whole notice, not what was sent to the model.
    full_source = f"{announcement['title']}\n\n{announcement['body']}"

    records, record_embeddings = [], []
    for fact in extracted:
        grounded, ungrounded_numbers = is_grounded(fact["text"], full_source)
        if not grounded:
            stats["rejected_by_grounding"] += 1
            with open(LPU_UNGROUNDED_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "announcement_id": announcement["id"], "fact_text": fact["text"],
                    "entities": fact.get("entities", []), "ungrounded_numbers": ungrounded_numbers,
                    "logged_at": now.isoformat(),
                }) + "\n")
            continue
        records.append({
            "fact_text": fact["text"],
            "entities": fact.get("entities", []),
            "pestle_scores": fact["pestle_scores"],
            "porters_scores": fact["porters_scores"],
            "polarity": fact["polarity"],
            # Bundled call: decomposition and classification succeed or fail
            # TOGETHER, since one call now does both jobs.
            "decomposition_ok": ok,
            "classification_ok": ok,
        })
        record_embeddings.append(embed_text(fact["text"]))
        if ok:
            stats["classified_ok"] += 1
        else:
            stats["classification_failed"] += 1

    return records, record_embeddings, stats


def repair_failed_records(verbose: bool = True) -> dict:
    """Re-processes every ALREADY-STORED fact whose decomposition or
    classification failed, in place, so a completed corpus can be brought to
    "every record genuinely processed by the model" without redoing the whole
    run.

    With the bundled call (fact_pipeline.py), decomposition_ok and
    classification_ok fail TOGETHER (one call does both jobs), so there is
    only one repair path now, not two: any record with either flag False gets
    its parent re-processed through the SAME bundled call + grounding check
    the main run uses, and the stale record is REPLACED by the resulting
    (possibly multiple, possibly zero if none pass grounding) atomic facts.
    Records from a run predating this change may still have the flags
    disagree (the old two-call path could fail one without the other) - this
    repairs those too, since "either flag False" is the trigger.
    """
    announcements, facts, embeddings_array, processed = _load_existing()
    if not facts:
        return {"repaired": 0, "still_failing": 0, "rejected_by_grounding": 0}

    embeddings = [row for row in embeddings_array]
    by_id = {a["id"]: a for a in announcements}
    stats = {"repaired": 0, "still_failing": 0, "rejected_by_grounding": 0}

    bad_indices = [
        i for i, f in enumerate(facts)
        if not f.get("decomposition_ok", True) or not f.get("classification_ok", True)
    ]
    if verbose and bad_indices:
        print(f"Re-processing {len(bad_indices)} failed record(s)...")
    # Walk backwards so replacing one record with several (or zero) doesn't
    # shift the indices of the ones still to process.
    for position in sorted(bad_indices, reverse=True):
        stale = facts[position]
        announcement = by_id.get(stale["parent_announcement_id"])
        if announcement is None:
            stats["still_failing"] += 1
            continue

        replacements, new_embeddings, delta = _process_announcement(announcement)
        stats["rejected_by_grounding"] += delta["rejected_by_grounding"]
        if not replacements:
            # Nothing survived (total failure, or every fact was ungrounded) -
            # leave the stale record in place rather than deleting it silently.
            stats["still_failing"] += 1
            continue

        final_records = [{**stale, **r, "id": stale["id"] if i == 0 else f"{stale['id']}_{i}"}
                          for i, r in enumerate(replacements)]
        facts[position:position + 1] = final_records
        embeddings[position:position + 1] = new_embeddings
        stats["repaired"] += 1

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
        "announcements_skipped_noncontent": 0,
        "facts_added": 0,
        "facts_classified_ok": 0,
        "facts_classification_failed": 0,
        "facts_rejected_by_grounding": 0,
        "compound_announcements": 0,
        # Announcements whose bundled call fell back to "store it unsplit,
        # unclassified" - the atomicity+classification guarantee's own
        # failure count, surfaced rather than hidden.
        "decomposition_fallbacks": 0,
    }
    fact_counter = len(facts)
    now = datetime.now(timezone.utc)

    for index, announcement in enumerate(pending, start=1):
        if announcement["published"] is None:
            stats["announcements_undated"] += 1

        # Pre-filter -> bundled atomic breakdown + classification -> per-fact
        # grounding check -> embed. See _process_announcement's docstring;
        # this is the one place the sequence is implemented, shared with
        # repair_failed_records.
        records, record_embeddings, delta = _process_announcement(announcement, now)
        stats["announcements_skipped_noncontent"] += delta["noncontent_skipped"]
        stats["decomposition_fallbacks"] += delta["decomposition_failed"]
        stats["compound_announcements"] += delta["compound"]
        stats["facts_rejected_by_grounding"] += delta["rejected_by_grounding"]
        stats["facts_classified_ok"] += delta["classified_ok"]
        stats["facts_classification_failed"] += delta["classification_failed"]

        announcement_fact_ids = []
        for record, embedding in zip(records, record_embeddings):
            fact_counter += 1
            fact_id = f"lpu_fact_{fact_counter:06d}"
            announcement_fact_ids.append(fact_id)
            facts.append({
                "id": fact_id,
                "parent_announcement_id": announcement["id"],
                "published": announcement["published"],
                # Tagged by construction, never inferred - these ARE LPU records.
                "scope": LPU_SCOPE,
                "source": "lpu",
                "is_lpu": True,
                "mention_count": 1,
                **record,
            })
            embeddings.append(embedding)
            stats["facts_added"] += 1

        announcements.append({**announcement, "fact_ids": announcement_fact_ids})
        processed.add(announcement["id"])

        if verbose and index % 5 == 0:
            print(f"  [{index}/{len(pending)}] {stats['facts_added']} facts so far "
                  f"(latest: {len(records)} from one announcement)")

        if index % LPU_CHECKPOINT_EVERY == 0:
            _flush(announcements, facts, embeddings, processed)
            if verbose:
                print(f"  checkpoint: {len(facts)} facts / {len(announcements)} announcements written")

    _flush(announcements, facts, embeddings, processed)
    stats["total_facts_in_store"] = len(facts)
    stats["total_announcements_in_store"] = len(announcements)
    stats["remaining_unprocessed"] = len(all_announcements) - len(processed)
    return stats

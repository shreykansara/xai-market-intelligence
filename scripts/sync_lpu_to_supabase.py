"""Uploads the locally-processed LPU corpus into Supabase (announcements,
facts + embeddings), and records the run in ingestion_runs.

This is deliberately SEPARATE from the processing step. Processing (LLM
decomposition + classification) is the expensive part and runs where the model
is cheapest - locally, against Ollama. This script only moves already-processed
results into Postgres, so it is fast, network-bound, and safe to re-run.

Idempotent: every insert is ON CONFLICT DO NOTHING keyed on the record id, and
ids are content-derived, so re-running after an interruption tops up rather
than duplicating. That makes it safe to run repeatedly from a scheduled job
while the local corpus is still growing.

Run:
    python scripts/sync_lpu_to_supabase.py              # sync everything new
    python scripts/sync_lpu_to_supabase.py --limit 500  # bounded first pass
    python scripts/sync_lpu_to_supabase.py --status     # counts only, no writes
"""
import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    LPU_ANNOUNCEMENTS_PATH,
    LPU_FACT_EMBEDDINGS_PATH,
    LPU_FACTS_PATH,
)
from marketintel.db import (  # noqa: E402
    DatabaseUnavailable,
    connect,
    corpus_counts,
    insert_facts,
    record_ingestion_run,
    upsert_announcement,
)

BATCH = 500


def load_local_corpus():
    """The processed corpus as written by lpu_ingestion.py. Refuses to proceed
    on a facts/embeddings length mismatch: row i of the .npy must be the vector
    for facts[i], and silently uploading a misaligned pair would attach the
    wrong vector to every fact after the break."""
    if not LPU_FACTS_PATH.exists():
        raise SystemExit(f"{LPU_FACTS_PATH} does not exist - run scripts/ingest_lpu_data.py first.")
    with open(LPU_FACTS_PATH, encoding="utf-8") as f:
        facts = json.load(f)
    with open(LPU_ANNOUNCEMENTS_PATH, encoding="utf-8") as f:
        announcements = json.load(f)
    embeddings = np.load(LPU_FACT_EMBEDDINGS_PATH)
    if len(facts) != len(embeddings):
        raise SystemExit(
            f"REFUSING TO SYNC: {len(facts)} facts but {len(embeddings)} embeddings. "
            "They are positionally linked; uploading them misaligned would corrupt the corpus."
        )
    return announcements, facts, embeddings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=None, help="Max facts to upload this run (default: all).")
    parser.add_argument("--status", action="store_true", help="Report local vs. remote counts, write nothing.")
    args = parser.parse_args()

    announcements, facts, embeddings = load_local_corpus()
    print(f"Local corpus: {len(announcements):,} announcements, {len(facts):,} facts, "
          f"{embeddings.shape[0]:,} embeddings")

    try:
        remote = corpus_counts()
        print(f"Supabase    : {remote['announcements']:,} announcements, {remote['facts']:,} facts "
              f"({remote['database_size']} used)")
    except DatabaseUnavailable as exc:
        raise SystemExit(f"Database unavailable: {exc}")

    if args.status:
        return

    started = time.time()
    uploaded_facts = 0
    to_upload = facts[: args.limit] if args.limit else facts
    by_id = {a["id"]: a for a in announcements}

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                # Announcements first: facts reference them by foreign key, so a
                # fact whose parent isn't inserted yet would be rejected.
                for announcement in announcements:
                    upsert_announcement(cur, {**announcement, "source": "lpu"})
                conn.commit()

                for start in range(0, len(to_upload), BATCH):
                    chunk = to_upload[start:start + BATCH]
                    offsets = range(start, start + len(chunk))
                    uploaded_facts += insert_facts(cur, chunk, [embeddings[i] for i in offsets])
                    conn.commit()
                    print(f"  {min(start + BATCH, len(to_upload)):,}/{len(to_upload):,} facts processed "
                          f"({uploaded_facts:,} newly inserted)")
                # Referenced but absent parents would be a real integrity bug,
                # so check rather than assume.
                missing_parents = {f.get("parent_announcement_id") for f in to_upload} - set(by_id)
                if missing_parents - {None}:
                    print(f"  WARNING: {len(missing_parents - {None})} fact(s) reference an unknown announcement")
    except DatabaseUnavailable as exc:
        record_ingestion_run({"stage": "sync_lpu"}, ok=False, source="lpu-sync", error=str(exc))
        raise SystemExit(f"Sync failed: {exc}")

    elapsed = time.time() - started
    final = corpus_counts()
    record_ingestion_run(
        {"stage": "sync_lpu", "facts_uploaded": uploaded_facts,
         "local_facts": len(facts), "remote_facts": final["facts"],
         "elapsed_seconds": round(elapsed, 1)},
        ok=True, source="lpu-sync",
    )
    print(f"\nUploaded {uploaded_facts:,} new facts in {elapsed:.1f}s")
    print(f"Supabase now: {final['announcements']:,} announcements, {final['facts']:,} facts "
          f"({final['database_size']} used)")
    remaining = len(facts) - final["facts"]
    if remaining > 0:
        print(f"  {remaining:,} local facts not yet uploaded - re-run to continue.")


if __name__ == "__main__":
    main()

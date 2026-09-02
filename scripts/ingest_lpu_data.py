"""CLI entry point for building the LPU announcements corpus - the system's only
news corpus (src/marketintel/lpu_ingestion.py).

Every announcement in data/lpudata/ is broken down into ATOMIC facts (a compound
notice becomes several independently-scorable records), each fact is classified
across all 11 PESTLE/Porter's dimensions, tagged scope="LPU"/is_lpu=True, and
embedded into data/lpu_fact_embeddings.npy alongside data/lpu_facts.json.

This makes two local-Ollama calls per announcement, so a full ~16.5k-announcement
run takes hours. It is checkpointed and resumable: interrupt with Ctrl+C and
re-run the same command to continue from the last checkpoint, or use --limit to
build a smaller corpus first and extend it later.

Examples:
  # Small first pass, to see real throughput and spot-check quality:
  python scripts/ingest_lpu_data.py --limit 25

  # Continue where the last run stopped (default behaviour - safe to repeat):
  python scripts/ingest_lpu_data.py

  # Full unattended run:
  python scripts/ingest_lpu_data.py --limit 0

  # Discard whatever was built and start over:
  python scripts/ingest_lpu_data.py --fresh --limit 100
"""
import argparse
import sys
import time
from pathlib import Path

# LPU notices contain non-ASCII characters (names, symbols); Windows' default
# console codepage can't encode all of it, and this is meant to run unattended
# for hours, so a stray character must not take the whole run down.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.lpu_ingestion import repair_failed_records, run_lpu_ingestion  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max NOT-yet-processed announcements to handle this run (0 = no limit, process everything).",
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help="Ignore any existing corpus/checkpoint and rebuild from scratch.",
    )
    parser.add_argument(
        "--repair", action="store_true",
        help="Don't ingest anything new - re-process already-stored records whose decomposition or "
             "classification failed, until every stored record has genuinely been through the model.",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress per-announcement progress output.")
    args = parser.parse_args()

    if args.repair:
        started = time.time()
        stats = repair_failed_records(verbose=not args.quiet)
        print("\n=== LPU repair pass complete ===")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        print(f"  elapsed_seconds: {time.time() - started:.1f}")
        if stats.get("still_failing"):
            print(f"\n  {stats['still_failing']} record(s) still failing after retries - re-run --repair, "
                  "or check that Ollama is healthy.")
        return

    limit = None if args.limit in (None, 0) else args.limit

    started = time.time()
    stats = run_lpu_ingestion(limit=limit, resume=not args.fresh, verbose=not args.quiet)
    elapsed = time.time() - started

    print("\n=== LPU ingestion run complete ===")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print(f"  elapsed_seconds: {elapsed:.1f}")
    if stats["announcements_seen"]:
        per = elapsed / stats["announcements_seen"]
        print(f"  seconds_per_announcement: {per:.1f}")
        remaining = stats["remaining_unprocessed"]
        if remaining:
            print(f"  estimated_hours_for_remaining_{remaining}: {remaining * per / 3600:.1f}")
    if stats["facts_classification_failed"]:
        print(
            f"\n  NOTE: {stats['facts_classification_failed']} fact(s) could not be classified "
            "(Ollama unreachable or unparseable output) - they are stored with all-zero relevance "
            "and classification_ok=False, NOT silently treated as genuinely irrelevant."
        )


if __name__ == "__main__":
    main()

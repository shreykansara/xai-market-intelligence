"""CLI entry point for the historical World/India GDELT bulk backfill
(src/marketintel/gdelt_backfill.py) - a separate, one-off/batch process from the
live ingestion_service.py, which keeps running independently on its own
30-minute schedule. Safe to interrupt (Ctrl+C) and re-run with the same
arguments: progress is checkpointed to data/backfill_state.json and resumes
from the last flushed timestamp rather than starting over.

Examples:
  # One week pilot, India tier only (per the pilot-before-scale-up checkpoint):
  python scripts/run_gdelt_backfill.py --tier india --start 2026-08-01 --end 2026-08-08

  # Full 2-year India backfill (run this unattended - estimated ~4 months, see
  # CLAUDE.md's timing estimate - and expect to interrupt/resume it many times
  # rather than needing one unbroken run):
  python scripts/run_gdelt_backfill.py --tier india --start 2024-08-28 --end 2026-08-28
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# Global/historical text (GDELT headlines and titles) regularly includes
# non-English characters; Windows' default console codepage can't encode a lot
# of that, and this is meant to run unattended for a long time, so a stray
# character shouldn't take the whole run down.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.gdelt_backfill import run_backfill  # noqa: E402


def parse_date(value: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"Unrecognized date/time: {value!r} (expected YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tier", required=True, choices=["world", "india"])
    parser.add_argument("--start", required=True, type=parse_date, help="YYYY-MM-DD (UTC, inclusive)")
    parser.add_argument("--end", required=True, type=parse_date, help="YYYY-MM-DD (UTC, exclusive)")
    parser.add_argument(
        "--checkpoint-every", type=int, default=20,
        help="Flush accumulated data to disk every N GKG files (default 20, ~5 hours of data)",
    )
    args = parser.parse_args()

    run_backfill(args.start, args.end, args.tier, checkpoint_every_n_files=args.checkpoint_every)


if __name__ == "__main__":
    main()

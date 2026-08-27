"""CLI entry point for the real news ingestion pipeline. The actual pipeline
(source fetching, dedup, embedding, relevance gate, scope classification) lives
in src/marketintel/ingestion.py, shared with ingestion_service.py (a standalone,
self-scheduling microservice) so it's implemented exactly once - this script is
just a thin wrapper for manual runs or an external cron/Task Scheduler entry.

Run: python scripts/ingest_news.py

Schedule examples (if you'd rather drive this with an external scheduler than
run ingestion_service.py's built-in one):
  cron (Linux/Mac):       0 */2 * * *  cd /path/to/project && .venv/bin/python scripts/ingest_news.py
  Windows Task Scheduler: trigger "every 2 hours", action = .venv\\Scripts\\python.exe scripts\\ingest_news.py

For always-on scheduling instead, run ingestion_service.py: it fires an
ingestion pass on startup, then every 30 minutes on its own, and exposes
GET /health with the last run's status.
"""
import sys
from pathlib import Path

# Global wires (especially GDELT) regularly include non-English headlines; Windows'
# default console codepage can't encode a lot of that, and this is meant to run
# unattended on a schedule, so a stray character shouldn't take the whole run down.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.ingestion import run_ingestion_once  # noqa: E402

if __name__ == "__main__":
    run_ingestion_once(verbose=True)

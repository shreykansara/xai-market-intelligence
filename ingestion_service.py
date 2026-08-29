"""Standalone ingestion microservice: runs the shared ingestion pipeline
(src/marketintel/ingestion.py) on its own self-managed schedule, on its own
port, independent of the main analysis app (server.py) - so the two processes
never conflict and either can be restarted without touching the other.

No ingestion logic lives here - this is a scheduler loop plus a status
endpoint wrapped around marketintel.ingestion.run_ingestion_once(), the exact
same function scripts/ingest_news.py calls for one-shot/cron use. Nothing
about sources, fact decomposition, dedup, the relevance gate, scope
classification, grounding, or comparative-fact matching is duplicated or
reimplemented here - all of it lives in marketintel.ingestion (which itself
shares its grounding/comparative-matching modules with the GDELT bulk
backfill - see ingestion.py's docstring). /health reports counts at both
granularities: articles fetched (raw source items, and how many were
rejected as non-content before ever reaching Ollama) and facts (extracted,
rejected as ungrounded, excluded by the relevance gate, added, and how many
comparative-fact matches were found vs. left unmatched) - the unit
everything downstream actually scores.

On startup, fires one ingestion pass immediately, then repeats every 30
minutes for as long as the process runs - a plain asyncio loop, no external
cron or scheduler dependency. The only HTTP surface is GET /health; there is
no authentication and no way to trigger a run externally, by design - this is
a local, standalone process.

Run: uvicorn ingestion_service:app --port 8502
(distinct from server.py's port, e.g. 8000, so the two never collide)
"""
import asyncio
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fastapi import FastAPI  # noqa: E402

from marketintel.ingestion import run_ingestion_once  # noqa: E402

INGEST_INTERVAL_SECONDS = 30 * 60

status = {
    "last_run_started": None,
    "last_run_finished": None,
    "last_run_ok": None,
    "last_error": None,
    "articles_fetched": None,
    "articles_rejected_noncontent": None,
    "facts_extracted": None,
    "facts_excluded": None,
    "facts_rejected_ungrounded": None,
    "facts_added": None,
    "comparative_matches_found": None,
    "comparative_matches_unmatched": None,
}


async def _run_and_record() -> None:
    status["last_run_started"] = datetime.now(timezone.utc).isoformat()
    try:
        # run_ingestion_once does blocking network calls and embedding inference -
        # offload it to a worker thread so it can't stall the event loop (and this
        # service's /health endpoint) for the run's duration.
        result = await asyncio.to_thread(run_ingestion_once, verbose=True)
        status["last_run_ok"] = True
        status["last_error"] = None
        status["articles_fetched"] = result["articles_fetched"]
        status["articles_rejected_noncontent"] = result["articles_rejected_noncontent"]
        status["facts_extracted"] = result["facts_extracted"]
        status["facts_excluded"] = result["facts_excluded"]
        status["facts_rejected_ungrounded"] = result["facts_rejected_ungrounded"]
        status["facts_added"] = result["facts_added"]
        status["comparative_matches_found"] = result["comparative_matches_found"]
        status["comparative_matches_unmatched"] = result["comparative_matches_unmatched"]
    except Exception as exc:
        status["last_run_ok"] = False
        status["last_error"] = str(exc)
    status["last_run_finished"] = datetime.now(timezone.utc).isoformat()


async def _ingestion_loop() -> None:
    while True:
        await _run_and_record()
        await asyncio.sleep(INGEST_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_ingestion_loop())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(title="Market Intelligence Ingestion Service", lifespan=lifespan)


@app.get("/health")
def health():
    return status

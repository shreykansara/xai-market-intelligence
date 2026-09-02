"""FastAPI backend for the custom frontend (web/). Pure reuse of the existing
analysis pipeline (src/marketintel) - this file only adapts it to HTTP/JSON and
serves the static frontend; no scoring/training logic lives here.

Two analysis modes: the CVP-similarity estimate (POST /api/analyze, required,
unchanged default) and the optional sales-history-derived mode (POST
/api/sales/upload -> /api/sales/confirm -> pass the resulting upload_id into
/api/analyze) - see sales_upload.py for why these are two separate steps
(never trust a column-mapping guess silently) and CLAUDE.md for the full
design and what's explicitly out of scope.

Run (analysis engine only - port 8000):
    uvicorn server:app --port 8000 --reload

This process is fully independent of the ingestion microservice
(ingestion_service.py, port 8502): it never imports, starts, waits for, or
health-checks it. Real ingested facts are picked up by READING
data/real_facts.json fresh per request, so ingestion can be running,
stopped, or never started at all - analysis degrades to the fabricated seed
corpus and says so (live_facts_count / seed_only in every /api/analyze
response). See README's "Running the services" section.
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fastapi import FastAPI, File, Form, HTTPException, UploadFile  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel  # noqa: E402

from marketintel.analysis import score_submission  # noqa: E402
from marketintel.config import (  # noqa: E402
    INTERACTION_MATRIX_PATH,
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    PESTLE_DIMS,
    PESTLE_LABELS,
    PORTERS_DIMS,
    PORTERS_LABELS,
    SUBCLUSTERS_PATH,
)
from marketintel.data_loader import load_cvp_mean, load_interaction_matrix, load_news, load_real_facts, load_subclusters  # noqa: E402
from marketintel.embeddings import embed_text, get_model  # noqa: E402
from marketintel.live_facts import assign_fact_subclusters, build_combined_corpus, compute_subcluster_centroids  # noqa: E402
from marketintel.news_browser import facet_values, filter_items, load_all_items, summarize  # noqa: E402
from marketintel.real_data_inference import assess_dimension_coverage  # noqa: E402
from marketintel.sales_upload import (  # noqa: E402
    derive_sales_profile,
    guess_columns,
    parse_upload,
    validate_upload,
)

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="Explainable Market Intelligence")

_state: dict = {}

# Ephemeral, in-process store for pending/confirmed sales uploads, keyed by a
# generated upload_id - deliberately NOT persisted to disk or folded into any
# shared corpus (see CLAUDE.md's "explicitly out of scope"). Lost on restart,
# which is fine for what is a single interactive review-then-analyze flow, not
# a durable record.
_uploads: dict[str, dict] = {}


def data_ready() -> bool:
    return NEWS_PATH.exists() and NEWS_EMBEDDINGS_PATH.exists() and INTERACTION_MATRIX_PATH.exists() and SUBCLUSTERS_PATH.exists()


def get_state() -> dict:
    if not _state:
        get_model()  # warm the embedding model once
        news, news_embeddings = load_news()
        subclusters = load_subclusters()
        _state["news"] = news
        _state["news_embeddings"] = news_embeddings
        _state["W"] = load_interaction_matrix()
        _state["cvp_mean"] = load_cvp_mean()
        _state["subclusters"] = subclusters
        # Centroids only depend on the fabricated corpus + its (one-time) discovery
        # output, so they're stable for the process's lifetime - computed once here
        # rather than on every request. Real facts themselves are NOT cached: they
        # keep arriving from ingestion_service.py independently of this process, so
        # they're loaded fresh per request in analyze() below.
        _state["centroids"] = compute_subcluster_centroids(news, news_embeddings, subclusters)
    return _state


class AnalyzeRequest(BaseModel):
    # CVP and a confirmed sales upload are each INDEPENDENTLY sufficient to
    # run analysis - neither is unconditionally required, but at least one of
    # the two must be present (enforced in analyze() below, since that also
    # needs sales_upload_id to know whether an upload covers the gap). An
    # empty string here is treated the same as "not provided", not as
    # "someone submitted a literal empty CVP" - see analyze()'s cvp_provided
    # handling for why this matters (an empty-string CVP embeds to a real,
    # non-crashing but MEANINGLESS vector, so it must never be silently
    # scored as if it were a real submission).
    cvp: str = ""
    sales_upload_id: str | None = None


class ConfirmSalesRequest(BaseModel):
    upload_id: str
    date_col: str
    value_col: str


def _jsonable_preview(rows: list[dict]) -> list[dict]:
    """Stringifies preview values (pandas Timestamps, numpy scalars, NaN) so
    the upload-guess response is always plain-JSON-serializable regardless of
    the uploaded sheet's original dtypes."""
    return [{k: ("" if v is None or v != v else str(v)) for k, v in row.items()} for row in rows]


def trim_article(article: dict) -> dict:
    return {
        "id": article["id"],
        "title": article["title"],
        "date": article["date"],
        "scope": article["scope"],
        "polarity": article["polarity"],
        "is_live": article.get("is_live", False),
    }


def serialize_breakdown(breakdown: dict, labels: dict) -> list[dict]:
    """Dict of dim -> clusters becomes an ordered list (by |aggregate score|) of
    {dim, label, score, clusters: [...]} for the frontend to render top-to-bottom."""
    dims = []
    for dim, clusters in breakdown.items():
        aggregate = sum(c["raw_score"] for c in clusters)
        dims.append({
            "dim": dim,
            "label": labels[dim],
            "raw_score": aggregate,
            "clusters": [
                {
                    "cluster_id": c["cluster_id"],
                    "label": c["label"],
                    "raw_score": c["raw_score"],
                    "top_articles": [
                        {"article": trim_article(item["article"]), "contribution": item["contribution"]}
                        for item in c["top_articles"]
                    ],
                }
                for c in clusters
            ],
        })
    dims.sort(key=lambda d: -abs(d["raw_score"]))
    return dims


def _blank_breakdown(dims: list[str], labels: dict) -> list[dict]:
    """Same shape serialize_breakdown() would return, but with no clusters -
    used when there is no CVP to gate articles against (see analyze()'s
    cvp_provided branch) so the frontend still gets real dimension names/
    labels for its radar-chart axes without a fabricated, meaningless
    empty-string-CVP score standing in for a real one."""
    return [{"dim": d, "label": labels[d], "raw_score": 0.0, "clusters": []} for d in dims]


@app.post("/api/sales/upload")
async def upload_sales(file: UploadFile = File(...)):
    """Step 1 of the optional sales-history mode: parse the file and BEST-GUESS
    the date/value columns - never trusted silently, always returned for the
    caller to confirm or correct via /api/sales/confirm before anything is
    computed. Stores the parsed (but not yet validated/analyzed) DataFrame
    in-process, keyed by a fresh upload_id."""
    file_bytes = await file.read()
    try:
        df = parse_upload(file_bytes, file.filename or "upload.csv")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if df.empty or len(df.columns) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file has no rows or columns to work with.")

    guess = guess_columns(df)
    upload_id = str(uuid.uuid4())
    _uploads[upload_id] = {"df": df}

    return {
        "upload_id": upload_id,
        "columns": guess.columns,
        "guessed_date_col": guess.guessed_date_col,
        "guessed_value_col": guess.guessed_value_col,
        "preview_rows": _jsonable_preview(guess.preview_rows),
    }


@app.post("/api/sales/confirm")
def confirm_sales(req: ConfirmSalesRequest):
    """Step 2: the caller confirms (or corrects) the column mapping. Runs
    volume/quality validation (sales_upload.validate_upload) and, if it
    passes, computes the sales-derived profile immediately via
    sales_upload.derive_sales_profile() - which news pool it regresses
    against (the real ingested-fact corpus, or today's demo fallback to the
    fabricated seed corpus) is controlled by the single
    config.SALES_REGRESSION_NEWS_SOURCE flag, not decided here. A thin
    upload<->real-news-coverage overlap (real-source path only) is reported
    explicitly, not silently ignored - see sales_upload.compute_coverage_overlap.
    Either way, the resulting profile's `news_source` field ("real" or
    "fabricated") is passed straight through to the caller so a
    fabricated-sourced result can be labeled, never presented as
    indistinguishable from a real one."""
    upload = _uploads.get(req.upload_id)
    if upload is None:
        raise HTTPException(status_code=404, detail="Unknown upload_id - upload the file again.")

    validation = validate_upload(upload["df"], req.date_col, req.value_col)
    if not validation.valid:
        upload["derived"] = None
        return {"valid": False, "reason": validation.reason}

    state = get_state()
    real_facts, real_fact_embeddings = load_real_facts()
    dimension_coverage = assess_dimension_coverage(real_facts)
    real_assignments = (
        assign_fact_subclusters(real_facts, real_fact_embeddings, state["centroids"]) if real_facts else {}
    )

    derived, overlap = derive_sales_profile(
        validation.daily_series,
        real_facts,
        dimension_coverage,
        state["subclusters"],
        real_assignments,
        state["news"],
    )
    upload["derived"] = derived

    return {
        "valid": True,
        "upload_stats": validation.stats,
        "overlap": overlap,
        "sales_derived_available": derived is not None,
        "derived_profile": derived,
    }


def _profile_to_display(profile: dict, all_dims: list[str]) -> dict:
    """Fills in 0.0 for any dimension not present in a (possibly coverage-
    restricted) derived profile, so the frontend's existing radar-chart
    rendering can be reused unchanged - the caller must still consult
    covered_dimensions/uncovered_dimensions to grey those out rather than
    reading a 0 as "negligible sensitivity" (it means "no real data yet",
    a different thing)."""
    return {d: float(profile.get(d, 0.0)) for d in all_dims}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    cvp_text = req.cvp.strip()

    # CVP and a confirmed sales upload are each independently sufficient -
    # resolve the upload FIRST so that check can see whether one covers the
    # gap, rather than rejecting a CVP-less request that actually has a
    # perfectly good sales-derived result to run (see CLAUDE.md).
    upload = _uploads.get(req.sales_upload_id) if req.sales_upload_id else None
    derived = upload.get("derived") if upload else None

    if not cvp_text and derived is None:
        raise HTTPException(
            status_code=400,
            detail="Provide a CVP, or upload and confirm a sales history file, before running analysis.",
        )
    if not data_ready():
        # Degraded mode, deliberately explicit rather than a 500. The scored
        # corpus (news.json/news_embeddings.npy) was removed when the system
        # migrated to the LPU corpus, and analysis can't run without a scored
        # corpus + trained W. Browsing (/api/news) and the frontend still work,
        # so the service stays up and says precisely what is missing instead of
        # failing opaquely.
        missing = [p.name for p in (NEWS_PATH, NEWS_EMBEDDINGS_PATH, INTERACTION_MATRIX_PATH, SUBCLUSTERS_PATH)
                   if not p.exists()]
        raise HTTPException(
            status_code=503,
            detail=(
                "Analysis is unavailable: the scored news corpus is not wired up yet. "
                f"Missing: {', '.join(missing)}. The LPU corpus is still being ingested and is not "
                "yet connected to the scoring path. Browsing collected news (/api/news) is unaffected."
            ),
        )

    response = {
        "pestle_dims": PESTLE_DIMS,
        "porters_dims": PORTERS_DIMS,
        "sales_derived": None,
        "primary_result": "sales" if derived is not None else "cvp",
        # Whether a real CVP-similarity result was actually computed below -
        # an empty/whitespace-only CVP is never silently embedded and scored
        # (that would produce a real, non-crashing, but MEANINGLESS result,
        # since an empty string still embeds to *some* vector - see CLAUDE.md).
        # The frontend must gate the CVP breakdown/comparison display on this
        # flag rather than assuming pestle_display etc. reflect a real submission.
        "cvp_provided": bool(cvp_text),
    }

    if cvp_text:
        state = get_state()
        cvp_embedding = embed_text(cvp_text)

        # Real facts are folded in alongside the fabricated seed corpus - see
        # live_facts.py for how they're assigned a sub-cluster and how they're
        # weighted (equally) relative to seed articles in the score itself.
        # live_facts_count is 0 whenever ingestion hasn't run yet or its output is
        # missing/empty/corrupted/stale (see load_real_facts()'s docstring) - this
        # is never an error case for server.py, which must run standalone on the
        # fabricated seed corpus alone; it's surfaced below so a seed-only result
        # is visible to the caller instead of looking identical to a normal one.
        combined_news, combined_embeddings, combined_subclusters, live_facts_count = build_combined_corpus(
            state["news"], state["news_embeddings"], state["subclusters"], state["centroids"]
        )
        result = score_submission(
            combined_news, combined_embeddings, cvp_embedding, state["W"], combined_subclusters, state["cvp_mean"]
        )
        response.update({
            "pestle_display": result["pestle_display"],
            "porters_display": result["porters_display"],
            "pestle_breakdown": serialize_breakdown(result["pestle_breakdown"], PESTLE_LABELS),
            "porters_breakdown": serialize_breakdown(result["porters_breakdown"], PORTERS_LABELS),
            "live_facts_count": live_facts_count,
            "seed_only": live_facts_count == 0,
            "cvp_result_label": "Estimate based on comparable businesses",
        })
    else:
        # No CVP text - nothing to gate articles against, so the CVP-similarity
        # result and its per-article breakdown are left blank rather than
        # computed from a meaningless empty-string embedding (see cvp_provided
        # above). Dimension names/labels are still real (_blank_breakdown), so
        # the frontend's radar-chart axes work whether or not this branch ran.
        response.update({
            "pestle_display": {d: 0.0 for d in PESTLE_DIMS},
            "porters_display": {d: 0.0 for d in PORTERS_DIMS},
            "pestle_breakdown": _blank_breakdown(PESTLE_DIMS, PESTLE_LABELS),
            "porters_breakdown": _blank_breakdown(PORTERS_DIMS, PORTERS_LABELS),
            "live_facts_count": 0,
            "seed_only": True,
            "cvp_result_label": None,
        })

    # Optional second mode: only engaged if the caller confirmed a valid upload
    # AND that upload's own regression cleared the coverage-overlap bar (see
    # sales_upload.py). CVP result above (if any) is unaffected either way.
    if derived is not None:
        is_demo = derived.get("news_source") == "fabricated"
        response["sales_derived"] = {
            "pestle_display": _profile_to_display(derived["pestle_profile"], PESTLE_DIMS),
            "porters_display": _profile_to_display(derived["porters_profile"], PORTERS_DIMS),
            "covered_dimensions": derived["covered_dimensions"],
            "uncovered_dimensions": derived["uncovered_dimensions"],
            "lag_days": derived["lag_days"],
            "r_squared": derived["r_squared"],
            "news_source": derived.get("news_source", "real"),
            # Labeled up front, not left for the frontend to infer from
            # news_source alone - a demo/sample-data result must never read
            # the same as a real one (see CLAUDE.md's SALES_REGRESSION_NEWS_SOURCE
            # entry). The frontend additionally renders a mandatory, impossible-
            # to-miss banner whenever news_source == "fabricated" - this label
            # alone is not considered sufficient disclosure on its own.
            "label": (
                "Derived from your sales history — DEMO: representative sample news, not your live feed"
                if is_demo
                else "Derived from your own sales history"
            ),
        }
        # primary_result was already set to "sales" above (derived is not None) -
        # no reassignment needed here.

    return response


@app.get("/api/news")
def browse_news(
    source: str = "all",
    q: str = "",
    scope: str = "all",
    polarity: str = "all",
    dimension: str = "all",
    page: int = 1,
    page_size: int = 50,
):
    """Read-only browse over every news item held across both corpora
    (fabricated seed, live ingested) - see news_browser.py. Purely an
    inspection view: it reads what's on disk and never scores, mutates, or
    re-ranks anything, so browsing can't perturb /api/analyze.

    `summary` reports each corpus's count/date coverage AND whether it
    currently feeds analysis (`in_scoring`), so a corpus that is stored but
    not wired into the scoring path can never look equivalent to one that
    is."""
    page = max(1, page)
    page_size = min(max(1, page_size), 200)

    items = load_all_items()
    filtered = filter_items(items, source=source, q=q, scope=scope, polarity=polarity, dimension=dimension)

    start = (page - 1) * page_size
    return {
        "items": filtered[start:start + page_size],
        "total": len(filtered),
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (len(filtered) + page_size - 1) // page_size),
        "summary": summarize(items),
        "facets": facet_values(items),
    }


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

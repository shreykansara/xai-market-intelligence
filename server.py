"""FastAPI backend for the custom frontend (web/). Pure reuse of the existing
analysis pipeline (src/marketintel) - this file only adapts it to HTTP/JSON and
serves the static frontend; no scoring/training logic lives here.

Run: uvicorn server:app --reload
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fastapi import FastAPI, HTTPException  # noqa: E402
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
from marketintel.data_loader import load_cvp_mean, load_interaction_matrix, load_news, load_subclusters  # noqa: E402
from marketintel.embeddings import embed_text, get_model  # noqa: E402
from marketintel.live_facts import build_combined_corpus, compute_subcluster_centroids  # noqa: E402

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="Explainable Market Intelligence")

_state: dict = {}


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
    cvp: str


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


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    if not req.cvp or not req.cvp.strip():
        raise HTTPException(status_code=400, detail="cvp must not be empty")
    if not data_ready():
        raise HTTPException(
            status_code=503,
            detail="Fabricated data / trained model not found - run the data pipeline (see README) first.",
        )

    state = get_state()
    cvp_embedding = embed_text(req.cvp)

    # Real facts are folded in alongside the fabricated seed corpus - see
    # live_facts.py for how they're assigned a sub-cluster and how they're
    # weighted (equally) relative to seed articles in the score itself.
    combined_news, combined_embeddings, combined_subclusters = build_combined_corpus(
        state["news"], state["news_embeddings"], state["subclusters"], state["centroids"]
    )
    result = score_submission(
        combined_news, combined_embeddings, cvp_embedding, state["W"], combined_subclusters, state["cvp_mean"]
    )

    return {
        "pestle_display": result["pestle_display"],
        "porters_display": result["porters_display"],
        "pestle_dims": PESTLE_DIMS,
        "porters_dims": PORTERS_DIMS,
        "pestle_breakdown": serialize_breakdown(result["pestle_breakdown"], PESTLE_LABELS),
        "porters_breakdown": serialize_breakdown(result["porters_breakdown"], PORTERS_LABELS),
    }


@app.get("/")
def index():
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")

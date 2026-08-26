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
from marketintel.data_loader import load_interaction_matrix, load_news, load_subclusters  # noqa: E402
from marketintel.embeddings import embed_text, get_model  # noqa: E402

WEB_DIR = Path(__file__).resolve().parent / "web"

app = FastAPI(title="Explainable Market Intelligence")

_state: dict = {}


def data_ready() -> bool:
    return NEWS_PATH.exists() and NEWS_EMBEDDINGS_PATH.exists() and INTERACTION_MATRIX_PATH.exists() and SUBCLUSTERS_PATH.exists()


def get_state() -> dict:
    if not _state:
        get_model()  # warm the embedding model once
        news, news_embeddings = load_news()
        _state["news"] = news
        _state["news_embeddings"] = news_embeddings
        _state["W"] = load_interaction_matrix()
        _state["subclusters"] = load_subclusters()
    return _state


class AnalyzeRequest(BaseModel):
    cvp: str


def trim_article(article: dict) -> dict:
    return {k: article[k] for k in ("id", "title", "date", "scope", "polarity")}


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
    result = score_submission(state["news"], state["news_embeddings"], cvp_embedding, state["W"], state["subclusters"])

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

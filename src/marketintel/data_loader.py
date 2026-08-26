import json

import numpy as np

from .config import (
    INTERACTION_MATRIX_PATH,
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    REAL_NEWS_EMBEDDINGS_PATH,
    REAL_NEWS_PATH,
    STARTUP_EMBEDDINGS_PATH,
    STARTUPS_PATH,
    SUBCLUSTERS_PATH,
)


def load_news():
    with open(NEWS_PATH, encoding="utf-8") as f:
        news = json.load(f)
    embeddings = np.load(NEWS_EMBEDDINGS_PATH)
    return news, embeddings


def load_startups():
    with open(STARTUPS_PATH, encoding="utf-8") as f:
        startups = json.load(f)
    embeddings = np.load(STARTUP_EMBEDDINGS_PATH)
    return startups, embeddings


def news_by_id(news: list[dict]) -> dict[str, dict]:
    return {article["id"]: article for article in news}


def load_interaction_matrix() -> np.ndarray:
    return np.load(INTERACTION_MATRIX_PATH)


def load_subclusters() -> dict:
    with open(SUBCLUSTERS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_real_news():
    """Real ingested headlines (scripts/ingest_news.py) - separate from the fabricated
    news dataset so they never leak into the fabricated startups' training data.
    Returns ([], empty array) if ingestion hasn't been run yet."""
    if not (REAL_NEWS_PATH.exists() and REAL_NEWS_EMBEDDINGS_PATH.exists()):
        return [], np.empty((0, 0))
    with open(REAL_NEWS_PATH, encoding="utf-8") as f:
        news = json.load(f)
    embeddings = np.load(REAL_NEWS_EMBEDDINGS_PATH)
    return news, embeddings

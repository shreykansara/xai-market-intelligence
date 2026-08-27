import json

import numpy as np

from .config import (
    CVP_MEAN_PATH,
    INTERACTION_MATRIX_PATH,
    NEWS_EMBEDDINGS_PATH,
    NEWS_PATH,
    REAL_ARTICLES_PATH,
    REAL_FACT_EMBEDDINGS_PATH,
    REAL_FACTS_PATH,
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


def load_cvp_mean() -> np.ndarray:
    """Mean of the training CVP embeddings, subtracted from every CVP embedding
    (training-time and inference-time alike) before it meets W - see the
    CVP_CENTERING_ENABLED comment in config.py for why. Falls back to a zero
    vector (no-op) if the file doesn't exist yet, e.g. an older W trained
    before this fix, so this loader never hard-fails an otherwise-working setup."""
    if not CVP_MEAN_PATH.exists():
        return np.zeros(384)
    return np.load(CVP_MEAN_PATH)


def load_subclusters() -> dict:
    with open(SUBCLUSTERS_PATH, encoding="utf-8") as f:
        return json.load(f)


def load_real_facts():
    """Real ingested facts (src/marketintel/ingestion.py) - the primary scored unit
    for real ingestion, separate from the fabricated news dataset so they never leak
    into the fabricated startups' training data. Returns ([], empty array) if
    ingestion hasn't been run yet."""
    if not (REAL_FACTS_PATH.exists() and REAL_FACT_EMBEDDINGS_PATH.exists()):
        return [], np.empty((0, 0))
    with open(REAL_FACTS_PATH, encoding="utf-8") as f:
        facts = json.load(f)
    embeddings = np.load(REAL_FACT_EMBEDDINGS_PATH)
    return facts, embeddings


def load_real_articles() -> list[dict]:
    """Real ingested articles - provenance containers only (headline, source, link,
    which facts came out of them), not scored or embedded themselves. Returns []
    if ingestion hasn't been run yet."""
    if not REAL_ARTICLES_PATH.exists():
        return []
    with open(REAL_ARTICLES_PATH, encoding="utf-8") as f:
        return json.load(f)

import json

import numpy as np

from .config import NEWS_EMBEDDINGS_PATH, NEWS_PATH, STARTUP_EMBEDDINGS_PATH, STARTUPS_PATH


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

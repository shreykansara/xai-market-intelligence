import numpy as np

from .config import PESTLE_DIMS, PORTERS_DIMS, TOP_K_STARTUPS


def top_k_similar_startups(cvp_embedding: np.ndarray, startup_embeddings: np.ndarray, k: int = TOP_K_STARTUPS):
    """Cosine similarity (both sides already L2-normalized -> dot product)."""
    sims = startup_embeddings @ cvp_embedding
    top_idx = np.argsort(-sims)[:k]
    return top_idx, sims[top_idx]


def _weights_from_similarity(sims: np.ndarray) -> np.ndarray:
    weights = np.clip(sims, 0, None)
    if weights.sum() <= 0:
        weights = np.ones_like(weights)
    return weights / weights.sum()


def blend_profile(startups: list[dict], top_idx: np.ndarray, sims: np.ndarray, profile_key: str, dims: list[str]):
    """Similarity-weighted average of the top-k startups' signed sensitivity vectors."""
    weights = _weights_from_similarity(sims)
    blended = {d: 0.0 for d in dims}
    for w, idx in zip(weights, top_idx):
        vec = startups[idx][profile_key]
        for d in dims:
            blended[d] += w * vec[d]
    return blended, weights


def blend_pestle(startups, top_idx, sims):
    return blend_profile(startups, top_idx, sims, "pestle_profile", PESTLE_DIMS)


def blend_porters(startups, top_idx, sims):
    return blend_profile(startups, top_idx, sims, "porters_profile", PORTERS_DIMS)


def rank_contributing_articles(startups, news_lookup, top_idx, weights, dims, score_field):
    """Union of the top-k startups' linked articles, ranked by weighted contribution to
    whichever PESTLE/Porter's dimension each article scores highest on."""
    contributions: dict[str, dict] = {}
    for w, idx in zip(weights, top_idx):
        startup = startups[idx]
        for aid in startup["linked_article_ids"]:
            article = news_lookup.get(aid)
            if article is None:
                continue
            scores = article[score_field]
            best_dim = max(dims, key=lambda d: scores[d])
            contribution = w * scores[best_dim]
            existing = contributions.get(aid)
            if existing is None or contribution > existing["contribution"]:
                contributions[aid] = {
                    "article": article,
                    "dim": best_dim,
                    "contribution": contribution,
                    "source_startup": startup["name"],
                }
    return sorted(contributions.values(), key=lambda c: -c["contribution"])


def rank_pestle_articles(startups, news_lookup, top_idx, weights):
    return rank_contributing_articles(startups, news_lookup, top_idx, weights, PESTLE_DIMS, "pestle_scores")


def rank_porters_articles(startups, news_lookup, top_idx, weights):
    return rank_contributing_articles(startups, news_lookup, top_idx, weights, PORTERS_DIMS, "porters_scores")

import numpy as np

from .config import NEAR_ZERO_FRACTION, PESTLE_DIMS, PORTERS_DIMS


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def compute_gates(news_embeddings: np.ndarray, cvp_embedding: np.ndarray, W: np.ndarray) -> np.ndarray:
    """gate(news, cvp) = news_embedding . W . cvp_embedding, for every article at once."""
    return news_embeddings @ (W @ cvp_embedding)


def contribution_matrix(news: list[dict], gates: np.ndarray, dims: list[str], score_field: str) -> np.ndarray:
    """contribution(news, cvp, dim) = relevance(news, dim) * polarity(news) * gate(news, cvp),
    returned as an (n_articles, n_dims) matrix."""
    relevance = np.array([[article[score_field][d] for d in dims] for article in news])
    signs = np.array([polarity_sign(article) for article in news])
    return relevance * signs[:, None] * gates[:, None]


def raw_dimension_scores(contributions: np.ndarray, dims: list[str]) -> dict:
    totals = contributions.sum(axis=0)
    return {d: float(v) for d, v in zip(dims, totals)}


def normalize_for_display(raw_scores: dict) -> dict:
    """Scale a chart's own dimensions so the largest magnitude hits 100, sign preserved."""
    max_abs = max((abs(v) for v in raw_scores.values()), default=0.0)
    if max_abs < 1e-9:
        return {d: 0.0 for d in raw_scores}
    return {d: v / max_abs * 100.0 for d, v in raw_scores.items()}


def near_zero_dims(raw_pestle: dict, raw_porters: dict, fraction: float = NEAR_ZERO_FRACTION) -> set[str]:
    """Dimensions whose raw magnitude is negligible next to this submission's strongest
    dimension (across both charts) - greyed out rather than styled helping/hurting."""
    all_values = list(raw_pestle.values()) + list(raw_porters.values())
    global_max = max((abs(v) for v in all_values), default=0.0)
    if global_max < 1e-9:
        return set(raw_pestle) | set(raw_porters)
    threshold = fraction * global_max
    return {d for d, v in {**raw_pestle, **raw_porters}.items() if abs(v) < threshold}


def rank_articles_by_contribution(news: list[dict], contributions: np.ndarray, dims: list[str], top_n: int = 10):
    """For each article, attribute it to whichever dimension it contributed most to, then
    rank articles across the whole PESTLE/Porter's group by |contribution|."""
    best_dim_idx = np.argmax(np.abs(contributions), axis=1)
    best_contribution = contributions[np.arange(len(news)), best_dim_idx]
    order = np.argsort(-np.abs(best_contribution))[:top_n]
    return [
        {
            "article": news[i],
            "dim": dims[best_dim_idx[i]],
            "contribution": float(best_contribution[i]),
        }
        for i in order
    ]


def score_submission(news: list[dict], news_embeddings: np.ndarray, cvp_embedding: np.ndarray, W: np.ndarray):
    """Full pipeline for one submitted CVP: gate every article, sum signed contributions
    per PESTLE/Porter's dimension, and rank the articles behind each chart."""
    gates = compute_gates(news_embeddings, cvp_embedding, W)

    pestle_contrib = contribution_matrix(news, gates, PESTLE_DIMS, "pestle_scores")
    porters_contrib = contribution_matrix(news, gates, PORTERS_DIMS, "porters_scores")

    raw_pestle = raw_dimension_scores(pestle_contrib, PESTLE_DIMS)
    raw_porters = raw_dimension_scores(porters_contrib, PORTERS_DIMS)

    return {
        "pestle_display": normalize_for_display(raw_pestle),
        "porters_display": normalize_for_display(raw_porters),
        "near_zero": near_zero_dims(raw_pestle, raw_porters),
        "pestle_articles": rank_articles_by_contribution(news, pestle_contrib, PESTLE_DIMS),
        "porters_articles": rank_articles_by_contribution(news, porters_contrib, PORTERS_DIMS),
    }

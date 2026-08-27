from collections import defaultdict

import numpy as np

from .config import NEAR_ZERO_FRACTION, PESTLE_DIMS, PORTERS_DIMS


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def compute_gates(
    news_embeddings: np.ndarray, cvp_embedding: np.ndarray, W: np.ndarray, cvp_mean: np.ndarray | None = None
) -> np.ndarray:
    """gate(news, cvp) = news_embedding . W . (cvp_embedding - cvp_mean), for every article
    at once. cvp_mean is the training CVP embeddings' mean (see CVP_CENTERING_ENABLED in
    config.py) - subtracted here to match how W was fit, removing the "generic business
    pitch text" component every CVP shares so W is only asked to react to what's
    distinctive about this one. Defaults to no-op (zero vector) for callers that don't pass
    one, e.g. tests against an older W trained before this fix."""
    if cvp_mean is None:
        cvp_mean = np.zeros_like(cvp_embedding)
    return news_embeddings @ (W @ (cvp_embedding - cvp_mean))


def subcluster_breakdown_for_dim(
    news: list[dict], gates: np.ndarray, dim: str, score_field: str, dim_subclusters: dict, top_n_articles: int = 5
) -> list[dict]:
    """contribution(news, cvp, subcluster) = subcluster_relevance(news) * polarity(news) *
    gate(news, cvp), summed per sub-cluster. Only articles above the clustering relevance
    threshold have a sub-cluster assignment for this dimension - articles without one don't
    contribute to it at all (matches how the clusters were discovered). Returns sub-clusters
    sorted by |raw_score|, each carrying its own top contributing articles for drill-down."""
    labels = dim_subclusters["labels"]
    assignments = dim_subclusters["assignments"]

    grouped = defaultdict(list)  # cluster_id -> [(article, contribution), ...]
    for i, article in enumerate(news):
        cluster_id = assignments.get(article["id"])
        if cluster_id is None:
            continue
        relevance = article[score_field][dim]
        contribution = relevance * polarity_sign(article) * gates[i]
        grouped[str(cluster_id)].append((article, float(contribution)))

    clusters = []
    for cluster_id, items in grouped.items():
        raw_score = sum(c for _, c in items)
        top_articles = sorted(items, key=lambda item: -abs(item[1]))[:top_n_articles]
        clusters.append({
            "cluster_id": cluster_id,
            "label": labels.get(cluster_id, cluster_id),
            "raw_score": raw_score,
            "top_articles": [{"article": a, "contribution": c} for a, c in top_articles],
        })

    clusters.sort(key=lambda c: -abs(c["raw_score"]))
    return clusters


def dimension_breakdowns(news: list[dict], gates: np.ndarray, dims: list[str], score_field: str, subclusters: dict):
    return {dim: subcluster_breakdown_for_dim(news, gates, dim, score_field, subclusters[dim]) for dim in dims}


def raw_dimension_scores(breakdown: dict) -> dict:
    """Roll sub-cluster scores up (sum) to the parent dimension."""
    return {dim: sum(c["raw_score"] for c in clusters) for dim, clusters in breakdown.items()}


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


def score_submission(
    news: list[dict],
    news_embeddings: np.ndarray,
    cvp_embedding: np.ndarray,
    W: np.ndarray,
    subclusters: dict,
    cvp_mean: np.ndarray | None = None,
):
    """Full pipeline for one submitted CVP: gate every article, sum signed sub-cluster
    contributions up to each PESTLE/Porter's dimension, and keep the sub-cluster breakdown
    (with its own top contributing articles) for the drill-down UI."""
    gates = compute_gates(news_embeddings, cvp_embedding, W, cvp_mean)

    pestle_breakdown = dimension_breakdowns(news, gates, PESTLE_DIMS, "pestle_scores", subclusters)
    porters_breakdown = dimension_breakdowns(news, gates, PORTERS_DIMS, "porters_scores", subclusters)

    raw_pestle = raw_dimension_scores(pestle_breakdown)
    raw_porters = raw_dimension_scores(porters_breakdown)

    return {
        "pestle_display": normalize_for_display(raw_pestle),
        "porters_display": normalize_for_display(raw_porters),
        "near_zero": near_zero_dims(raw_pestle, raw_porters),
        "pestle_breakdown": pestle_breakdown,
        "porters_breakdown": porters_breakdown,
    }

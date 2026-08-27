"""Infers relevance, polarity, and (for articles that clear the relevance gate)
geographic scope for a new (real) headline, all by looking up the fabricated seed
corpus - the only hand-labeled data anywhere in this system. No trained
classifier, no per-source tagging.

Relevance and polarity use a pooled k-nearest-neighbor vote. Scope deliberately
does NOT: pooled voting let majority-population scope classes (India, Punjab)
win just by having more seed articles nearby, regardless of how well any of them
actually matched. Scope instead uses a per-class-best-match rule - see
`infer_scope_best_match`.
"""
import numpy as np

from .config import PESTLE_DIMS, PORTERS_DIMS, RELEVANCE_GATE_PERCENTILE, SEED_NEIGHBOR_K

ALL_DIMS = PESTLE_DIMS + PORTERS_DIMS


def nearest_neighbors(embedding: np.ndarray, seed_embeddings: np.ndarray, k: int = SEED_NEIGHBOR_K):
    """Indices and weights of the k most similar seed articles. Seed embeddings are
    already L2-normalized, so the dot product is cosine similarity. Weights are the
    clipped-positive similarities, normalized to sum to 1 (mirrors how the CVP/
    startup similarity blend works elsewhere in this codebase)."""
    sims = seed_embeddings @ embedding
    top_idx = np.argsort(-sims)[:k]
    weights = np.clip(sims[top_idx], 0, None)
    if weights.sum() <= 0:
        weights = np.ones_like(weights)
    weights = weights / weights.sum()
    return top_idx, weights


def infer_relevance(seed_news: list[dict], top_idx: np.ndarray, weights: np.ndarray) -> dict:
    """Similarity-weighted average of the neighbors' PESTLE/Porter's relevance vectors."""
    relevance = {d: 0.0 for d in ALL_DIMS}
    for idx, w in zip(top_idx, weights):
        article = seed_news[idx]
        for d in PESTLE_DIMS:
            relevance[d] += w * article["pestle_scores"][d]
        for d in PORTERS_DIMS:
            relevance[d] += w * article["porters_scores"][d]
    return {d: round(float(v), 4) for d, v in relevance.items()}


def infer_categorical(seed_news: list[dict], top_idx: np.ndarray, weights: np.ndarray, field: str) -> str:
    """Similarity-weighted vote among neighbors for a categorical field (polarity) -
    the same neighbor set and weights used for relevance."""
    votes: dict[str, float] = {}
    for idx, w in zip(top_idx, weights):
        value = seed_news[idx][field]
        votes[value] = votes.get(value, 0.0) + w
    return max(votes.items(), key=lambda kv: kv[1])[0]


def calibrate_relevance_threshold(seed_news: list[dict], percentile: float = RELEVANCE_GATE_PERCENTILE) -> float:
    """The relevance gate's cutoff, calibrated from the fabricated seed corpus itself:
    the Nth percentile of each seed article's own max relevance across all 11
    dimensions (using its hand-labeled scores directly, not re-inferred). Real
    headlines scoring below this aren't meaningfully close to anything this system
    models on any dimension."""
    max_relevances = [
        max([a["pestle_scores"][d] for d in PESTLE_DIMS] + [a["porters_scores"][d] for d in PORTERS_DIMS])
        for a in seed_news
    ]
    return float(np.percentile(max_relevances, percentile))


def group_indices_by_scope(seed_news: list[dict]) -> dict:
    groups: dict[str, list[int]] = {}
    for i, article in enumerate(seed_news):
        groups.setdefault(article["scope"], []).append(i)
    return {scope: np.array(idx) for scope, idx in groups.items()}


def infer_scope_best_match(embedding: np.ndarray, seed_embeddings: np.ndarray, scope_indices: dict):
    """Per-class-best-match: for each of the 7 scope classes, find that class's
    single most similar seed article; assign whichever class's best match is
    overall the highest similarity. A class can't win by having many
    so-so-similar neighbors nearby (that's what let population size dominate the
    old pooled k-NN vote) - only its single closest example gets to compete."""
    sims = seed_embeddings @ embedding
    best_scope, best_sim = None, -1.0
    for scope, idx in scope_indices.items():
        class_best = float(sims[idx].max())
        if class_best > best_sim:
            best_sim, best_scope = class_best, scope
    return best_scope, best_sim

"""Discover a two-level hierarchy under each of the 11 PESTLE/Porter's dimensions:
dimension -> 3-5 sub-clusters, found unsupervised from the news dataset's own
embeddings (not hand-authored). For each dimension, articles with relevance above
SUBCLUSTER_RELEVANCE_THRESHOLD are agglomeratively clustered on their embeddings;
the cluster count (3, 4, or 5) is picked per dimension by silhouette score. Each
cluster gets a short human-readable label, derived after the fact from the
titles of the articles nearest its centroid - purely for display, never fed back
into the clustering itself.

An article can land in a different sub-cluster under each dimension it's
relevant to, consistent with its existing multi-dimensional relevance scores.

Only two levels for now (dimension -> sub-cluster) - see CLAUDE.md: a third
level needs more fabricated volume than this phase has.

Must run AFTER generate_news.py.
Run: python scripts/discover_subclusters.py
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    PESTLE_DIMS,
    PORTERS_DIMS,
    SUBCLUSTER_K_RANGE,
    SUBCLUSTER_RELEVANCE_THRESHOLD,
    SUBCLUSTERS_PATH,
)
from marketintel.data_loader import load_news  # noqa: E402

ALL_DIMS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]

STOPWORDS = {
    "the", "a", "an", "is", "are", "to", "of", "for", "in", "on", "and", "with", "as",
    "across", "over", "into", "amid", "new", "its", "this", "that", "at", "by", "from",
    "up", "out", "than", "after", "ahead", "well", "against", "near",
}


def best_clustering(embeddings: np.ndarray, k_range: list[int], tolerance: float = 0.9):
    """Cluster at every candidate k, then pick the SMALLEST k whose silhouette score
    reaches `tolerance` of the best score seen across the whole range. Plain
    argmax(silhouette) is biased toward the largest k in range (cosine-distance
    silhouette on this kind of short-text embedding tends to keep improving as
    clusters shrink toward singletons, not because the extra splits are
    meaningful) - this still allows a bigger k through when it's a genuine,
    substantial improvement (as with topically dense dimensions), but doesn't
    default there for every dimension just because more splits are always
    slightly tighter."""
    n = len(embeddings)
    candidates = []  # (k, labels, score)
    for k in k_range:
        if k >= n:
            continue
        model = AgglomerativeClustering(n_clusters=k, metric="cosine", linkage="average")
        labels = model.fit_predict(embeddings)
        if len(set(labels)) < 2:
            continue
        score = silhouette_score(embeddings, labels, metric="cosine")
        candidates.append((k, labels, score))

    if not candidates:
        return 1, np.zeros(n, dtype=int), 0.0

    best_score = max(score for _, _, score in candidates)
    for k, labels, score in sorted(candidates, key=lambda c: c[0]):
        if score >= tolerance * best_score:
            return k, labels, score
    return candidates[-1]


def label_cluster(articles: list[dict], embeddings: np.ndarray, member_idx: np.ndarray) -> str:
    centroid = embeddings[member_idx].mean(axis=0)
    sims = embeddings[member_idx] @ centroid / (
        np.linalg.norm(embeddings[member_idx], axis=1) * np.linalg.norm(centroid) + 1e-9
    )
    nearest_local = member_idx[np.argsort(-sims)[:3]]
    titles = [articles[i]["title"] for i in nearest_local]

    words = []
    for title in titles:
        for word in re.findall(r"[A-Za-z']+", title.lower()):
            if len(word) > 3 and word not in STOPWORDS:
                words.append(word)
    common = [w for w, _ in Counter(words).most_common(2)]
    if common:
        return " ".join(w.capitalize() for w in common)
    return titles[0]


def discover_for_dimension(news: list[dict], embeddings: np.ndarray, score_field: str, dim: str):
    idx = np.array([i for i, a in enumerate(news) if a[score_field][dim] > SUBCLUSTER_RELEVANCE_THRESHOLD])
    if len(idx) < 3:
        return {"k": 1, "labels": {"0": dim.replace("_", " ").title()}, "assignments": {news[i]["id"]: 0 for i in idx}}

    dim_embeddings = embeddings[idx]
    k, labels, score = best_clustering(dim_embeddings, SUBCLUSTER_K_RANGE)

    cluster_labels = {}
    assignments = {}
    for c in range(k):
        member_local_idx = idx[labels == c]
        if len(member_local_idx) == 0:
            continue
        cluster_labels[str(c)] = label_cluster(news, embeddings, member_local_idx)
        for i in member_local_idx:
            assignments[news[i]["id"]] = int(c)

    print(f"  {dim:<22} n={len(idx):>4} k={k} silhouette={score:.3f}  " + ", ".join(cluster_labels.values()))
    return {"k": k, "labels": cluster_labels, "assignments": assignments}


def main():
    news, embeddings = load_news()

    result = {}
    print("Discovering sub-clusters per dimension...")
    for score_field, dim in ALL_DIMS:
        result[dim] = discover_for_dimension(news, embeddings, score_field, dim)

    with open(SUBCLUSTERS_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {SUBCLUSTERS_PATH}")


if __name__ == "__main__":
    main()

"""Assigns PESTLE/Porter's relevance to arbitrary text (e.g. a real headline) by
similarity to the existing fabricated-data clustering's sub-cluster centroids,
rather than a trained classifier - see CLAUDE.md's real news ingestion phase."""
import numpy as np

from .config import PESTLE_DIMS, PORTERS_DIMS

ALL_DIMS = PESTLE_DIMS + PORTERS_DIMS


def compute_subcluster_centroids(news: list[dict], news_embeddings: np.ndarray, subclusters: dict) -> dict:
    """dim -> {cluster_id: centroid_embedding}, averaged from the fabricated articles
    already assigned to each (dimension, sub-cluster) pair."""
    id_to_idx = {article["id"]: i for i, article in enumerate(news)}
    centroids: dict = {}
    for dim in ALL_DIMS:
        by_cluster: dict = {}
        for article_id, cluster_id in subclusters[dim]["assignments"].items():
            idx = id_to_idx.get(article_id)
            if idx is None:
                continue
            by_cluster.setdefault(str(cluster_id), []).append(news_embeddings[idx])
        centroids[dim] = {cid: np.mean(vecs, axis=0) for cid, vecs in by_cluster.items()}
    return centroids


def relevance_from_centroids(text_embedding: np.ndarray, centroids: dict):
    """For each dimension, the best (max) cosine similarity to any of its sub-cluster
    centroids, clipped to [0, 1] to match the fabricated dataset's relevance scale.
    Also returns the nearest sub-cluster id per dimension, for consistency with the
    existing sub-cluster-based scoring pipeline."""
    text_norm = text_embedding / (np.linalg.norm(text_embedding) + 1e-9)
    relevance, nearest_cluster = {}, {}
    for dim, cluster_centroids in centroids.items():
        best_sim, best_cid = 0.0, None
        for cluster_id, centroid in cluster_centroids.items():
            centroid_norm = centroid / (np.linalg.norm(centroid) + 1e-9)
            sim = float(text_norm @ centroid_norm)
            if sim > best_sim:
                best_sim, best_cid = sim, cluster_id
        relevance[dim] = round(max(0.0, best_sim), 4)
        nearest_cluster[dim] = best_cid
    return relevance, nearest_cluster


def split_relevance(relevance: dict):
    pestle = {d: relevance[d] for d in PESTLE_DIMS}
    porters = {d: relevance[d] for d in PORTERS_DIMS}
    return pestle, porters

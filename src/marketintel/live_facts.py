"""Folds real ingested facts (data/real_facts.json) into the same scoring
pipeline as the fabricated seed corpus, so server.py's /api/analyze reflects
both instead of only the fabricated dataset.

Real facts were never part of the original sub-cluster discovery
(discover_subclusters.py runs once, offline, against the fabricated corpus
only; real facts arrive continuously, long after that ran). Each real fact is
assigned to its nearest EXISTING sub-cluster by cosine similarity to that
sub-cluster's centroid, rather than re-running discovery - the same "look up
against what's already known" principle used everywhere else real data is
labeled (relevance/polarity/scope in seed_inference.py).

WEIGHTING DECISION - real facts count EQUALLY to seed articles in the gate/
contribution formula (same gate = news_embedding . W . cvp_embedding, same
contribution = relevance * polarity * gate; see analysis.py, unchanged).
Reasoning: W was trained purely on the fabricated seed corpus, so a real
fact's gate score is only as trustworthy as the seed corpus's ability to
generalize to it in the first place - down-weighting by "realness" on top of
that would be an extra, unjustified parameter with no evidence behind it
(real facts haven't been shown to be systematically noisier than seed
articles at the gate/contribution stage - the known weak point is scope
classification, which is unaffected by this weighting choice). Recency-
weighting was considered and rejected for the same reason: there's no
observed real outcome yet to calibrate a decay constant against, so any
specific half-life would be arbitrary. Equal weighting is the simplest
choice that doesn't require inventing an unjustified number; revisit once
real fact volume is large enough to check empirically whether they need
down-weighting (e.g. by comparing prediction quality with and without them).
"""
import numpy as np

from .config import PESTLE_DIMS, PORTERS_DIMS, SUBCLUSTER_RELEVANCE_THRESHOLD
from .data_loader import load_real_facts

ALL_DIM_FIELDS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]


def compute_subcluster_centroids(seed_news: list[dict], seed_embeddings: np.ndarray, subclusters: dict) -> dict:
    """dim -> {cluster_id: centroid_embedding}, averaged from the fabricated seed
    articles already assigned to each (dimension, sub-cluster) pair during the
    one-time discovery run."""
    id_to_idx = {article["id"]: i for i, article in enumerate(seed_news)}
    centroids: dict = {}
    for _, dim in ALL_DIM_FIELDS:
        by_cluster: dict = {}
        for article_id, cluster_id in subclusters[dim]["assignments"].items():
            idx = id_to_idx.get(article_id)
            if idx is None:
                continue
            by_cluster.setdefault(str(cluster_id), []).append(seed_embeddings[idx])
        centroids[dim] = {cid: np.mean(vecs, axis=0) for cid, vecs in by_cluster.items()}
    return centroids


def assign_fact_subclusters(real_facts: list[dict], real_fact_embeddings: np.ndarray, centroids: dict) -> dict:
    """dim -> {fact_id: cluster_id}. A fact only gets an assignment for a dimension
    it clears SUBCLUSTER_RELEVANCE_THRESHOLD on - the same per-dimension bar
    fabricated articles had to clear to take part in discovery - so a fact that's
    only marginally relevant to a dimension doesn't get force-fit into one of
    that dimension's sub-clusters. Nearest centroid by cosine similarity, since
    these facts arrived after discovery already ran and can't be re-clustered in."""
    assignments: dict = {dim: {} for _, dim in ALL_DIM_FIELDS}
    if len(real_facts) == 0:
        return assignments

    for fact, embedding in zip(real_facts, real_fact_embeddings):
        norm_emb = embedding / (np.linalg.norm(embedding) + 1e-9)
        for score_field, dim in ALL_DIM_FIELDS:
            if fact[score_field][dim] <= SUBCLUSTER_RELEVANCE_THRESHOLD:
                continue
            dim_centroids = centroids.get(dim, {})
            best_cid, best_sim = None, -1.0
            for cluster_id, centroid in dim_centroids.items():
                centroid_norm = centroid / (np.linalg.norm(centroid) + 1e-9)
                sim = float(norm_emb @ centroid_norm)
                if sim > best_sim:
                    best_sim, best_cid = sim, cluster_id
            if best_cid is not None:
                assignments[dim][fact["id"]] = best_cid
    return assignments


def merge_subclusters(subclusters: dict, real_assignments: dict) -> dict:
    """A new dict (same shape as subclusters.json) with real facts' sub-cluster
    assignments merged in per dimension - never mutates the cached original."""
    merged = {}
    for dim, data in subclusters.items():
        merged[dim] = {
            "k": data["k"],
            "labels": data["labels"],
            "assignments": {**data["assignments"], **real_assignments.get(dim, {})},
        }
    return merged


def normalize_fact_as_article(fact: dict) -> dict:
    """Real facts and fabricated seed articles have almost the same shape already
    (id, pestle_scores, porters_scores, polarity, scope) - this fills in the two
    fields fabricated articles have and facts don't (title, date), and tags the
    result as live so the frontend can badge it, without mutating the input."""
    return {
        **fact,
        "title": fact["fact_text"],
        "date": fact["published"][:10],
        "is_live": True,
    }


def build_combined_corpus(seed_news: list[dict], seed_embeddings: np.ndarray, subclusters: dict, centroids: dict):
    """Loads whatever real facts are currently stored (fresh on every call, since
    ingestion_service.py keeps appending to them independently of this process)
    and returns (combined_news, combined_embeddings, combined_subclusters) ready
    to pass straight into analysis.score_submission - unchanged from how it's
    called with the fabricated corpus alone."""
    real_facts, real_fact_embeddings = load_real_facts()

    if len(real_facts) == 0:
        combined_news = [{**a, "is_live": False} for a in seed_news]
        return combined_news, seed_embeddings, subclusters

    real_assignments = assign_fact_subclusters(real_facts, real_fact_embeddings, centroids)
    combined_subclusters = merge_subclusters(subclusters, real_assignments)

    combined_news = [{**a, "is_live": False} for a in seed_news] + [normalize_fact_as_article(f) for f in real_facts]
    combined_embeddings = np.vstack([seed_embeddings, real_fact_embeddings])

    return combined_news, combined_embeddings, combined_subclusters

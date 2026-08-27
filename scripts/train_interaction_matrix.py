"""Fit the shared interaction matrix W from the 20 fabricated startups' ground-truth
PESTLE/Porter's profiles and their linked justifying news articles.

    gate(news, cvp) = news_embedding . W . cvp_embedding
    contribution(news, cvp, dim) = relevance(news, dim) * polarity(news) * gate(news, cvp)
    score(cvp, dim) = sum over relevant news of contribution(news, cvp, dim)

W is a single (384, 384) matrix, fit once in batch via ridge regression. The
384*384 = 147,456 parameters vastly outnumber the 50 startups * 11 dimensions
= 550 training examples, so this is solved in the ridge *dual* (550x550,
via the kernel trick) rather than the primal - the two are mathematically
equivalent for linear ridge regression, but the dual avoids ever forming a
147k x 147k system.

CVP embeddings are mean-centered before fitting, and that same mean is
persisted to CVP_MEAN_PATH for inference-time use (see fit_interaction_matrix's
docstring and the CVP_CENTERING_ENABLED comment in config.py) - fixing a
diagnosed pathology where W's dominant singular direction was ~88% aligned
with the shared "generic business pitch text" component present in every CVP,
regardless of domain, collapsing genuinely different businesses' output
patterns to 0.75-0.86 cosine similarity.

Must run AFTER generate_news.py and generate_startups.py.
Run: python scripts/train_interaction_matrix.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    CVP_MEAN_PATH,
    INTERACTION_MATRIX_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    RIDGE_ALPHA,
)
from marketintel.data_loader import load_news, load_startups, news_by_id  # noqa: E402

# (score field on the article, ground-truth profile field on the startup, dimension key)
ALL_DIMS = [("pestle_scores", "pestle_profile", d) for d in PESTLE_DIMS] + [
    ("porters_scores", "porters_profile", d) for d in PORTERS_DIMS
]


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def build_training_examples(startups, startup_embeddings, news_lookup, news_embeddings_by_id):
    """One training example per (startup, dimension): the startup's own CVP embedding,
    a combined-news vector (relevance * polarity weighted sum over its linked articles'
    embeddings, for that dimension), and the ground-truth signed target."""
    combined_vecs, cvp_vecs, targets = [], [], []

    for i, startup in enumerate(startups):
        cvp_emb = startup_embeddings[i]
        linked = [aid for aid in startup["linked_article_ids"] if aid in news_lookup]
        if not linked:
            continue
        for score_field, profile_key, dim in ALL_DIMS:
            combined = np.zeros_like(cvp_emb)
            for aid in linked:
                article = news_lookup[aid]
                relevance = article[score_field][dim]
                combined += relevance * polarity_sign(article) * news_embeddings_by_id[aid]
            combined_vecs.append(combined)
            cvp_vecs.append(cvp_emb)
            targets.append(startup[profile_key][dim])

    return np.array(combined_vecs), np.array(cvp_vecs), np.array(targets, dtype=float)


def fit_interaction_matrix(combined_vecs: np.ndarray, cvp_vecs: np.ndarray, targets: np.ndarray, alpha: float):
    """Ridge regression in the dual: score_i = combined_vecs[i] . W . cvp_vecs[i], with
    W = sum_j coef_j * outer(combined_vecs[j], cvp_vecs[j]). The Gram matrix used for the
    dual solve exploits (a1 (x) b1)-(a2 (x) b2) = (a1.a2)(b1.b2), so it never needs the
    full 147k-dim flattened features.

    cvp_vecs is mean-centered before fitting (see CVP_CENTERING_ENABLED in config.py):
    diagnosed directly that all training CVP embeddings share a large "generic business
    pitch text" component regardless of domain, and in this heavily underdetermined
    system ridge regression's minimum-norm solution spent a large share of W's capacity
    modeling that shared, uninformative axis rather than what's distinctive about each
    business. Centering removes that axis from what W is asked to explain. The SAME mean
    must be subtracted from every CVP embedding at inference time - it's returned here so
    the caller can persist it alongside W."""
    n = len(targets)
    cvp_mean = cvp_vecs.mean(axis=0)
    cvp_centered = cvp_vecs - cvp_mean

    news_gram = combined_vecs @ combined_vecs.T
    cvp_gram = cvp_centered @ cvp_centered.T
    K = news_gram * cvp_gram
    dual_coef = np.linalg.solve(K + alpha * np.eye(n), targets)

    dim = combined_vecs.shape[1]
    W = np.zeros((dim, dim))
    for j in range(n):
        W += dual_coef[j] * np.outer(combined_vecs[j], cvp_centered[j])

    predictions = K @ dual_coef
    return W, predictions, cvp_mean


def main():
    news, news_embeddings = load_news()
    news_lookup = news_by_id(news)
    news_embeddings_by_id = {a["id"]: emb for a, emb in zip(news, news_embeddings)}

    startups, startup_embeddings = load_startups()

    combined_vecs, cvp_vecs, targets = build_training_examples(
        startups, startup_embeddings, news_lookup, news_embeddings_by_id
    )
    print(f"Training on {len(targets)} (startup, dimension) examples...")

    W, predictions, cvp_mean = fit_interaction_matrix(combined_vecs, cvp_vecs, targets, RIDGE_ALPHA)

    mae = float(np.mean(np.abs(predictions - targets)))
    corr = float(np.corrcoef(predictions, targets)[0, 1])
    print(f"Training fit: MAE={mae:.2f}, correlation={corr:.3f} (ridge alpha={RIDGE_ALPHA})")

    np.save(INTERACTION_MATRIX_PATH, W)
    print(f"Wrote {INTERACTION_MATRIX_PATH} shape={W.shape}")
    np.save(CVP_MEAN_PATH, cvp_mean)
    print(f"Wrote {CVP_MEAN_PATH} shape={cvp_mean.shape}")


if __name__ == "__main__":
    main()

"""Fit the shared interaction matrix W from the 20 fabricated startups' ground-truth
PESTLE/Porter's profiles and their linked justifying news articles.

    gate(news, cvp) = news_embedding . W . cvp_embedding
    contribution(news, cvp, dim) = relevance(news, dim) * polarity(news) * gate(news, cvp)
    score(cvp, dim) = sum over relevant news of contribution(news, cvp, dim)

W is a single (384, 384) matrix, fit once in batch via ridge regression. The
384*384 = 147,456 parameters vastly outnumber the 20 startups * 11 dimensions
= 220 training examples, so this is solved in the ridge *dual* (220x220,
via the kernel trick) rather than the primal - the two are mathematically
equivalent for linear ridge regression, but the dual avoids ever forming a
147k x 147k system.

Must run AFTER generate_news.py and generate_startups.py.
Run: python scripts/train_interaction_matrix.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
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
    full 147k-dim flattened features."""
    n = len(targets)
    news_gram = combined_vecs @ combined_vecs.T
    cvp_gram = cvp_vecs @ cvp_vecs.T
    K = news_gram * cvp_gram
    dual_coef = np.linalg.solve(K + alpha * np.eye(n), targets)

    dim = combined_vecs.shape[1]
    W = np.zeros((dim, dim))
    for j in range(n):
        W += dual_coef[j] * np.outer(combined_vecs[j], cvp_vecs[j])

    predictions = K @ dual_coef
    return W, predictions


def main():
    news, news_embeddings = load_news()
    news_lookup = news_by_id(news)
    news_embeddings_by_id = {a["id"]: emb for a, emb in zip(news, news_embeddings)}

    startups, startup_embeddings = load_startups()

    combined_vecs, cvp_vecs, targets = build_training_examples(
        startups, startup_embeddings, news_lookup, news_embeddings_by_id
    )
    print(f"Training on {len(targets)} (startup, dimension) examples...")

    W, predictions = fit_interaction_matrix(combined_vecs, cvp_vecs, targets, RIDGE_ALPHA)

    mae = float(np.mean(np.abs(predictions - targets)))
    corr = float(np.corrcoef(predictions, targets)[0, 1])
    print(f"Training fit: MAE={mae:.2f}, correlation={corr:.3f} (ridge alpha={RIDGE_ALPHA})")

    np.save(INTERACTION_MATRIX_PATH, W)
    print(f"Wrote {INTERACTION_MATRIX_PATH} shape={W.shape}")


if __name__ == "__main__":
    main()

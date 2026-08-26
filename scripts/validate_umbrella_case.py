"""Validation test case for the sub-cluster drill-down pipeline (CLAUDE.md section 5):
run a fabricated umbrella-retailer CVP through the full inference pipeline and confirm,
within the "environmental" dimension's sub-clusters, that:

  - a rain/monsoon sub-cluster scores positively (more rain -> more umbrella demand),
  - a drought/dry-weather sub-cluster scores negatively (less rain -> less demand),
  - a sub-cluster for an unrelated environmental topic (deforestation/illegal logging)
    scores close to zero relative to the other two.

This is a sanity check on the clustering + regression pipeline as a whole, not just a
smoke test of the UI - if it doesn't come out roughly right, something upstream (cluster
separation, the shared matrix W, or the derived profiles feeding it) needs fixing before
building anything further on top of it.

Must run AFTER the full data/training pipeline (see README).
Run: python scripts/validate_umbrella_case.py
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.analysis import score_submission  # noqa: E402
from marketintel.data_loader import load_interaction_matrix, load_news, load_subclusters  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402

UMBRELLA_CVP = (
    "RainGuard Umbrellas designs and sells wind-resistant umbrellas, raincoats, and "
    "waterproof footwear through retail counters across Punjab. Our sales rise and fall "
    "directly with how much it rains each season, and we restock ahead of the monsoon."
)

RAIN_KEYWORDS = ["monsoon", "rain gear", "downpour"]
DRY_KEYWORDS = ["drought"]
UNRELATED_KEYWORDS = ["logging", "wildlife habitat"]


def matches_any(title: str, keywords: list[str]) -> bool:
    title = title.lower()
    return any(k in title for k in keywords)


def find_cluster(clusters: list[dict], keywords: list[str]):
    """Pick the cluster with the most member top-articles matching the given keywords -
    more robust than trusting the auto-generated label text verbatim."""
    best, best_count = None, 0
    for c in clusters:
        count = sum(1 for item in c["top_articles"] if matches_any(item["article"]["title"], keywords))
        if count > best_count:
            best, best_count = c, count
    return best


def main():
    news, news_embeddings = load_news()
    W = load_interaction_matrix()
    subclusters = load_subclusters()

    cvp_embedding = embed_text(UMBRELLA_CVP)
    result = score_submission(news, news_embeddings, cvp_embedding, W, subclusters)

    env_clusters = result["pestle_breakdown"]["environmental"]

    print("Environmental sub-clusters for the umbrella-retailer test CVP, ranked by |score|:\n")
    print(f"{'label':<28} {'raw_score':>12}")
    for c in env_clusters:
        print(f"{c['label']:<28} {c['raw_score']:>12.3f}")

    rain_cluster = find_cluster(env_clusters, RAIN_KEYWORDS)
    dry_cluster = find_cluster(env_clusters, DRY_KEYWORDS)
    unrelated_cluster = find_cluster(env_clusters, UNRELATED_KEYWORDS)

    max_abs = max((abs(c["raw_score"]) for c in env_clusters), default=1.0) or 1.0
    near_zero_threshold = 0.10 * max_abs

    print("\n=== VALIDATION ===")
    checks = []

    if rain_cluster is not None:
        passed = rain_cluster["raw_score"] > 0
        checks.append(passed)
        print(f"Rain/monsoon cluster ('{rain_cluster['label']}', score={rain_cluster['raw_score']:+.3f}): "
              f"{'PASS' if passed else 'FAIL'} (expected positive)")
    else:
        checks.append(False)
        print("Rain/monsoon cluster: NOT FOUND - FAIL")

    if dry_cluster is not None:
        passed = dry_cluster["raw_score"] < 0
        checks.append(passed)
        print(f"Drought/dry cluster ('{dry_cluster['label']}', score={dry_cluster['raw_score']:+.3f}): "
              f"{'PASS' if passed else 'FAIL'} (expected negative)")
    else:
        checks.append(False)
        print("Drought/dry cluster: NOT FOUND - FAIL")

    if unrelated_cluster is not None:
        passed = abs(unrelated_cluster["raw_score"]) <= near_zero_threshold
        checks.append(passed)
        print(f"Deforestation cluster ('{unrelated_cluster['label']}', score={unrelated_cluster['raw_score']:+.3f}): "
              f"{'PASS' if passed else 'FAIL'} (expected near zero, threshold ±{near_zero_threshold:.3f})")
    else:
        checks.append(False)
        print("Deforestation cluster: NOT FOUND - FAIL")

    print(f"\n{sum(checks)}/{len(checks)} checks passed.")
    if not all(checks):
        print(
            "Something in the clustering or regression step needs fixing before building "
            "anything further on top of it (see CLAUDE.md section 5)."
        )


if __name__ == "__main__":
    main()

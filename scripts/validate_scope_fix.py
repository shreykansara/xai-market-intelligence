"""Validates the relevance-gate + per-class-best-match fix against the exact
batch that surfaced the original bias: re-applies the new logic to the stored
data/real_news.json / real_news_embeddings.npy from the run that produced the
India=47/World=36/Punjab=25 distribution (including an NFL brain-injury study
and a Nigerian kidnapping story both tagged "India"), using their already-
computed relevance vectors and embeddings - no re-fetching, no re-embedding,
so this is a direct before/after comparison on identical input.

Run this BEFORE re-running scripts/ingest_news.py on fresh data, while
data/real_news.json still holds the pre-fix batch.

Run: python scripts/validate_scope_fix.py
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import PESTLE_DIMS, PORTERS_DIMS  # noqa: E402
from marketintel.data_loader import load_news, load_real_news  # noqa: E402
from marketintel.seed_inference import (  # noqa: E402
    calibrate_relevance_threshold,
    group_indices_by_scope,
    infer_scope_best_match,
)

WATCH_TITLES = [
    "Brain disease in dead NFL players",
    "Nigeria's president orders manhunt",
]


def max_relevance(article: dict) -> float:
    values = [article["pestle_scores"][d] for d in PESTLE_DIMS] + [article["porters_scores"][d] for d in PORTERS_DIMS]
    return max(values)


def main():
    seed_news, seed_embeddings = load_news()
    threshold = calibrate_relevance_threshold(seed_news)
    scope_indices = group_indices_by_scope(seed_news)
    print(f"Relevance gate threshold (5th percentile of seed corpus): {threshold:.4f}\n")

    records, embeddings = load_real_news()
    if not records:
        print("No data/real_news.json found - nothing to validate. Run ingest_news.py first.")
        return

    old_scope_dist = Counter(r["scope"] for r in records)

    excluded, included = [], []
    for record, embedding in zip(records, embeddings):
        mr = max_relevance(record)
        if mr < threshold:
            excluded.append((record, mr))
        else:
            new_scope, sim = infer_scope_best_match(embedding, seed_embeddings, scope_indices)
            included.append((record, mr, new_scope, record["scope"]))

    new_scope_dist = Counter(new_scope for _, _, new_scope, _ in included)

    print(f"Batch size: {len(records)}")
    print(f"Excluded by relevance gate: {len(excluded)}")
    print(f"Passed gate, re-scored for scope: {len(included)}\n")

    print("=== Watch-list check ===")
    for watch_title in WATCH_TITLES:
        match = next((r for r, mr in excluded if watch_title in r["title"]), None)
        if match:
            mr = next(mr for r, mr in excluded if r is match)
            print(f"PASS: excluded - \"{match['title']}\" (max_relevance={mr:.4f} < {threshold:.4f})")
            continue
        match = next((item for item in included if watch_title in item[0]["title"]), None)
        if match:
            record, mr, new_scope, old_scope = match
            print(
                f"FAIL: NOT excluded - \"{record['title']}\" "
                f"(max_relevance={mr:.4f}, old_scope={old_scope}, new_scope={new_scope})"
            )
        else:
            print(f"NOT FOUND in this batch: \"{watch_title}\" - cannot validate.")

    print("\n=== Scope distribution: before (pooled top-k vote) vs after (best-match, gate-filtered) ===")
    all_scopes = sorted(set(old_scope_dist) | set(new_scope_dist))
    print(f"{'scope':<12} {'before':>8} {'after':>8}")
    for scope in all_scopes:
        print(f"{scope:<12} {old_scope_dist.get(scope, 0):>8} {new_scope_dist.get(scope, 0):>8}")

    print("\n=== A few individual reclassifications (old scope -> new scope, where changed) ===")
    changed = [item for item in included if item[2] != item[3]]
    for record, mr, new_scope, old_scope in changed[:10]:
        print(f"  {old_scope:>10} -> {new_scope:<10} | {record['title']}")
    if not changed:
        print("  (none - all included articles kept the same scope)")


if __name__ == "__main__":
    main()

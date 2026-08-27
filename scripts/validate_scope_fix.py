"""Regression test for the relevance-gate + per-class-best-match scope fix,
directly re-testing the exact two headlines that originally surfaced the
pooled-voting scope bias (India=47/World=36/Punjab=25, both of these tagged
"India"), constructed here as literal strings rather than searched for in
whatever's currently in data/real_facts.json - so this keeps working as a
regression test regardless of how much the live dataset has moved on.

A note on what actually gets asserted, since it's not "both excluded":
  - The NFL brain-injury story has max relevance 0.33, well under the 0.58
    gate threshold - it's excluded, and that's asserted as a hard failure if
    it regresses.
  - The Nigerian kidnapping story has max relevance 0.80 (on "technological",
    somewhat questionably, but genuinely above the noise floor) - it is NOT
    excluded, and asserting that it should be would just be wrong: the gate's
    job is to catch headlines with no real signal on ANY dimension, not to
    catch every headline whose scope ends up wrong. This story's actual
    problem was always its SCOPE ("India", for a story with nothing to do
    with India) - a separate, still-open limitation documented in the
    README, not something the relevance gate was ever meant to fix. This
    script asserts the gate correctly leaves it in, and separately reports
    (without asserting - there's no fix for this yet) what scope it gets.

Run: python scripts/validate_scope_fix.py
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.data_loader import load_news, load_real_facts  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.seed_inference import (  # noqa: E402
    calibrate_relevance_threshold,
    group_indices_by_scope,
    infer_relevance,
    infer_scope_best_match,
    nearest_neighbors,
)

REGRESSION_CASES = [
    {
        "text": "Brain disease in dead NFL players 'higher than previously shown'",
        "label": "NFL brain-injury study",
        "expect_excluded": True,
    },
    {
        "text": "Nigeria's president orders manhunt after kidnappers upload victim video",
        "label": "Nigerian kidnapping manhunt",
        "expect_excluded": False,  # see module docstring - this one has real (if narrow) relevance
    },
]


def run_regression_cases(seed_news, seed_embeddings, threshold, scope_indices):
    print("=== Regression check: the exact two cases that surfaced the original bug ===")
    failures = []
    for case in REGRESSION_CASES:
        embedding = embed_text(case["text"])
        top_idx, weights = nearest_neighbors(embedding, seed_embeddings)
        relevance = infer_relevance(seed_news, top_idx, weights)
        max_relevance = max(relevance.values())
        excluded = max_relevance < threshold
        scope, _ = infer_scope_best_match(embedding, seed_embeddings, scope_indices)

        status = "PASS" if excluded == case["expect_excluded"] else "FAIL"
        if status == "FAIL":
            failures.append(case["label"])
        print(
            f"{status}: {case['label']} - max_relevance={max_relevance:.4f} "
            f"(threshold={threshold:.4f}) -> {'excluded' if excluded else 'NOT excluded'} "
            f"(expected {'excluded' if case['expect_excluded'] else 'NOT excluded'})"
        )
        if not excluded:
            print(f"       scope assigned: {scope} (reported, not asserted - see module docstring)")

    assert not failures, f"Regression failure on: {', '.join(failures)}"
    print("\nAll regression assertions passed.\n")


def general_audit(seed_news, seed_embeddings, threshold, scope_indices):
    facts, embeddings = load_real_facts()
    if len(facts) == 0:
        print("No data/real_facts.json found - skipping the general audit of currently stored facts.")
        return

    old_scope_dist = Counter(f["scope"] for f in facts)
    excluded, included = [], []
    for fact, embedding in zip(facts, embeddings):
        mr = max(list(fact["pestle_scores"].values()) + list(fact["porters_scores"].values()))
        if mr < threshold:
            excluded.append((fact, mr))
        else:
            new_scope, _ = infer_scope_best_match(embedding, seed_embeddings, scope_indices)
            included.append((fact, mr, new_scope, fact["scope"]))

    new_scope_dist = Counter(new_scope for _, _, new_scope, _ in included)

    print("=== General audit: whatever's currently in data/real_facts.json ===")
    print(f"Batch size: {len(facts)}, excluded: {len(excluded)}, passed gate: {len(included)}\n")

    all_scopes = sorted(set(old_scope_dist) | set(new_scope_dist))
    print(f"{'scope':<12} {'as stored':>10} {'re-scored':>10}")
    for scope in all_scopes:
        print(f"{scope:<12} {old_scope_dist.get(scope, 0):>10} {new_scope_dist.get(scope, 0):>10}")

    changed = [item for item in included if item[2] != item[3]]
    print(f"\n{len(changed)} fact(s) would be reclassified if re-scored now:")
    for fact, mr, new_scope, old_scope in changed[:10]:
        print(f"  {old_scope:>10} -> {new_scope:<10} | {fact['fact_text']}")


def main():
    seed_news, seed_embeddings = load_news()
    threshold = calibrate_relevance_threshold(seed_news)
    scope_indices = group_indices_by_scope(seed_news)
    print(f"Relevance gate threshold (5th percentile of seed corpus): {threshold:.4f}\n")

    run_regression_cases(seed_news, seed_embeddings, threshold, scope_indices)
    general_audit(seed_news, seed_embeddings, threshold, scope_indices)


if __name__ == "__main__":
    main()

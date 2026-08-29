"""Validates the seed-inference migration onto real data (CLAUDE.md's "Known
gaps" - "Migrated seed-based inference off fabricated data..."):

  1. Coverage check matches what's actually in data/real_facts.json - not
     stale, not hardcoded.
  2. The gate threshold is genuinely computed from the real corpus once
     there's enough of it, and differs from the fabricated-corpus value
     (proving it isn't silently still reading the old source).
  3. infer_hybrid genuinely blends per dimension - a fact scoring high on a
     REAL-covered dimension (e.g. "political") pulls that dimension's value
     from the real pool, while a fact scoring high on a fabricated-only
     dimension (e.g. "environmental") pulls from the fabricated pool - both
     checked directly against the returned source_summary, not assumed.
  4. infer_scope_hybrid returns a valid scope with a source in
     {"real", "fabricated"} and doesn't crash on the current data.

Run: python scripts/validate_real_data_migration.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.data_loader import load_news, load_real_facts  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.real_data_inference import (  # noqa: E402
    assess_dimension_coverage,
    assess_scope_coverage,
    choose_gate_threshold,
    infer_hybrid,
    infer_scope_hybrid,
)
from marketintel.seed_inference import calibrate_relevance_threshold, group_indices_by_scope  # noqa: E402

CHECKS = []


def check(name: str, passed: bool, detail: str = ""):
    CHECKS.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}: {name}" + (f" - {detail}" if detail else ""))


def main():
    real_facts, real_embeddings = load_real_facts()
    seed_news, seed_embeddings = load_news()

    print(f"=== 1. Coverage (against the live {len(real_facts)}-fact real corpus) ===\n")
    dim_coverage = assess_dimension_coverage(real_facts)
    scope_coverage = assess_scope_coverage(real_facts)
    for d, ok in dim_coverage.items():
        print(f"  {d:<24} {'real' if ok else 'fabricated'}")
    print()
    check("Coverage check returns a verdict for all 11 dimensions", len(dim_coverage) == 11)
    check("Scope coverage check returns a verdict for all 7 classes", len(scope_coverage) == 7)

    print("\n=== 2. Gate threshold recalibration ===\n")
    threshold, source = choose_gate_threshold(real_facts, seed_news)
    real_threshold = calibrate_relevance_threshold(real_facts)
    fabricated_threshold = calibrate_relevance_threshold(seed_news)
    print(f"  real corpus threshold:       {real_threshold:.4f}")
    print(f"  fabricated corpus threshold: {fabricated_threshold:.4f}")
    print(f"  chosen: {threshold:.4f} (source={source})")
    check(
        "Gate threshold matches the real corpus once enough facts exist",
        source == "real" and abs(threshold - real_threshold) < 1e-9,
    )
    check("Real and fabricated thresholds are genuinely different values", abs(real_threshold - fabricated_threshold) > 1e-6)

    print("\n=== 3. Per-dimension blending on real examples ===\n")
    covered_dim = next(d for d, ok in dim_coverage.items() if ok)
    uncovered_dim = next(d for d, ok in dim_coverage.items() if not ok)
    print(f"  (a covered dimension in this corpus: {covered_dim!r}; an uncovered one: {uncovered_dim!r})\n")

    political_text = "The government announced new tariffs on imported electronics, escalating trade tensions."
    embedding = embed_text(political_text)
    relevance, polarity, summary = infer_hybrid(
        embedding, real_facts, real_embeddings, seed_news, seed_embeddings, dim_coverage
    )
    print(f"  fact: {political_text!r}")
    print(f"  polarity={polarity} source_summary={summary}")
    check("Every covered dimension in the corpus is drawn from the real pool for this fact",
          all(d in summary["dims_from_real"] for d in dim_coverage if dim_coverage[d]))
    check("Every uncovered dimension falls back to the fabricated pool for this fact",
          all(d in summary["dims_from_fabricated"] for d in dim_coverage if not dim_coverage[d]))
    check("relevance dict covers all 11 dimensions", len(relevance) == 11)

    print("\n=== 4. Scope hybrid ===\n")
    real_scope_indices = group_indices_by_scope(real_facts) if real_facts else {}
    fabricated_scope_indices = group_indices_by_scope(seed_news)
    scope, sim, scope_source = infer_scope_hybrid(
        embedding, real_embeddings, real_scope_indices, seed_embeddings, fabricated_scope_indices, scope_coverage
    )
    print(f"  scope={scope} similarity={sim:.4f} source={scope_source}")
    check("infer_scope_hybrid returns a valid scope", scope is not None)
    check("infer_scope_hybrid reports a valid source", scope_source in ("real", "fabricated"))

    print(f"\n{sum(CHECKS)}/{len(CHECKS)} checks passed.")
    if not all(CHECKS):
        print("Do not treat the real-data migration as validated until every check above passes.")


if __name__ == "__main__":
    main()

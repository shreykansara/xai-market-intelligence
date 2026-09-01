"""Validates the sales-upload analysis mode (CLAUDE.md's "Sales history
upload" section) end to end:

  1. Column guessing on a realistic messy CSV (extra columns, a differently-
     named date column) - confirms the heuristic picks the right ones.
  2. Validation gate - confirms a too-short upload is correctly rejected
     with a plain-language reason, and a clean 120-day upload passes.
  3. Coverage overlap against the ACTUAL current real-fact corpus - this is
     expected to report "insufficient" today, since the accumulated real
     corpus only spans a couple of days so far (see CLAUDE.md) - confirming
     the graceful fallback path works, not treating this as a failure.
  4. Coverage overlap and full regression against a SYNTHETIC real-fact
     corpus constructed to genuinely overlap a 120-day upload, proving the
     regression mechanism itself recovers a plausible, correlated profile
     when given data that actually clears the bar - not just that it fails
     gracefully when it doesn't.

Run: python scripts/validate_sales_upload.py
"""
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import PESTLE_DIMS, PORTERS_DIMS, SUBCLUSTERS_PATH  # noqa: E402
from marketintel.data_loader import load_real_facts  # noqa: E402
from marketintel.live_facts import assign_fact_subclusters, compute_subcluster_centroids  # noqa: E402
from marketintel.data_loader import load_news  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.real_data_inference import assess_dimension_coverage  # noqa: E402
from marketintel.sales_upload import compute_coverage_overlap, derive_sales_profile, guess_columns, validate_upload  # noqa: E402

import json  # noqa: E402

CHECKS = []


def check(name: str, passed: bool, detail: str = ""):
    CHECKS.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}: {name}" + (f" - {detail}" if detail else ""))


def main():
    print("=== 1. Column guessing on a realistic messy sheet ===\n")
    df = pd.DataFrame({
        "Region": ["Punjab"] * 5,
        "Transaction Date": pd.date_range("2025-01-01", periods=5).strftime("%Y-%m-%d"),
        "Notes": ["", "promo", "", "", "restock"],
        "Monthly Revenue (INR)": [12000, 13500, 11800, 14200, 15000],
    })
    guess = guess_columns(df)
    print(f"  columns={guess.columns}")
    print(f"  guessed_date_col={guess.guessed_date_col!r} guessed_value_col={guess.guessed_value_col!r}")
    check("Date column correctly guessed", guess.guessed_date_col == "Transaction Date")
    check("Value column correctly guessed", guess.guessed_value_col == "Monthly Revenue (INR)")

    print("\n=== 2. Validation gate ===\n")
    short_df = pd.DataFrame({"date": pd.date_range("2025-01-01", periods=10), "revenue": np.random.rand(10) * 1000})
    short_result = validate_upload(short_df, "date", "revenue")
    print(f"  10-day upload: valid={short_result.valid} reason={short_result.reason!r}")
    check("Too-short upload is rejected, not silently run", not short_result.valid)

    rng = np.random.default_rng(0)
    long_dates = pd.date_range("2025-01-01", periods=120)
    long_df = pd.DataFrame({"date": long_dates, "revenue": 10000 + rng.normal(0, 200, 120).cumsum()})
    long_result = validate_upload(long_df, "date", "revenue")
    print(f"  120-day upload: valid={long_result.valid} stats={long_result.stats}")
    check("Clean 120-day upload passes validation", long_result.valid)

    print("\n=== 3. Coverage overlap against the ACTUAL current real-fact corpus ===\n")
    real_facts, _ = load_real_facts()
    overlap = compute_coverage_overlap(long_result.daily_series, real_facts)
    print(f"  {overlap}")
    check(
        "Overlap check runs without crashing on live data",
        "overlap_days" in overlap,
    )
    print(
        f"  (expected today: overlap_days is small and sufficient=False, since the real corpus "
        f"currently spans only a couple of days - this is the correct, honest outcome, not a bug)"
    )

    print("\n=== 4. Full regression against a SYNTHETIC overlapping real-fact corpus ===\n")
    seed_news, seed_embeddings = load_news()
    with open(SUBCLUSTERS_PATH, encoding="utf-8") as f:
        subclusters = json.load(f)
    centroids = compute_subcluster_centroids(seed_news, seed_embeddings, subclusters)

    # Build a synthetic real-fact corpus: 120 days overlapping the upload, with a
    # deliberately strong, known "political" signal so the regression has something
    # real to recover (mirrors how simulate_profit_history.py injects a known shock
    # to validate recovery, rather than testing on pure noise).
    base_date = datetime(2025, 1, 1, tzinfo=timezone.utc)
    synthetic_facts, synthetic_texts = [], []
    for i in range(150):
        day = base_date + timedelta(days=i % 120)
        is_political = i % 3 == 0
        # Political facts split roughly evenly between polarities (i % 2), so the
        # coverage check's "at least 3 of EACH polarity" bar is genuinely clearable -
        # not structurally impossible the way an all-one-polarity synthetic set would be.
        if is_political:
            political_negative = (i % 2 == 0)
            text = "Government raises import tariffs, squeezing costs" if political_negative else \
                   "Government cuts import tariffs, easing costs for businesses"
            polarity = "negative" if political_negative else "positive"
        else:
            text = "Local sports team wins regional tournament this weekend"
            polarity = "positive"
        synthetic_texts.append(text)
        synthetic_facts.append({
            "id": f"synthetic_{i}",
            "published": day.isoformat(),
            "polarity": polarity,
            "pestle_scores": {d: (0.9 if d == "political" and is_political else 0.05) for d in PESTLE_DIMS},
            "porters_scores": {d: 0.05 for d in PORTERS_DIMS},
        })
    synthetic_embeddings = np.array([embed_text(t) for t in synthetic_texts])

    dimension_coverage = assess_dimension_coverage(synthetic_facts)
    print(f"  synthetic corpus dimension coverage: {dimension_coverage}")
    check("Synthetic corpus gives 'political' real coverage (by construction)", dimension_coverage.get("political", False))

    real_assignments = assign_fact_subclusters(synthetic_facts, synthetic_embeddings, centroids)

    # Build an upload whose revenue reacts to the political-tariff facts with a 3-day
    # lag: tariff RAISES (negative polarity) hurt revenue, tariff CUTS (positive
    # polarity) help it - so the regression has a real, sign-consistent signal to find.
    negative_political_days = {i % 120 for i in range(150) if i % 3 == 0 and i % 2 == 0}
    positive_political_days = {i % 120 for i in range(150) if i % 3 == 0 and i % 2 == 1}
    revenue = [10000.0]
    for day in range(1, 120):
        shock = 0.0
        if (day - 3) in negative_political_days:
            shock -= 300.0
        if (day - 3) in positive_political_days:
            shock += 300.0
        revenue.append(revenue[-1] + rng.normal(0, 20) + shock)
    synthetic_upload_df = pd.DataFrame({"date": pd.date_range("2025-01-01", periods=120), "revenue": revenue})
    synthetic_validation = validate_upload(synthetic_upload_df, "date", "revenue")
    check("Synthetic upload passes validation", synthetic_validation.valid)

    # Explicitly force news_source="real" here regardless of the current
    # config.SALES_REGRESSION_NEWS_SOURCE default (temporarily "fabricated"
    # for today's demo, see CLAUDE.md) - this check's whole point is proving
    # the REAL-data regression path itself still works correctly.
    result, overlap2 = derive_sales_profile(
        synthetic_validation.daily_series,
        synthetic_facts,
        dimension_coverage,
        subclusters,
        real_assignments,
        seed_news,
        news_source="real",
    )
    print(f"  overlap: {overlap2}")
    check("Synthetic case reports sufficient overlap", overlap2["sufficient"])
    if result:
        print(f"  derived pestle_profile: {result['pestle_profile']}")
        print(f"  covered_dimensions={result['covered_dimensions']} lag={result['lag_days']} r2={result['r_squared']:.3f}")
        check("Regression recovers a strong political signal (magnitude 100, by construction of the rescale)",
              abs(result["pestle_profile"].get("political", 0)) > 50)
    else:
        check("Regression produced a result for the synthetic overlapping case", False)

    print(f"\n{sum(CHECKS)}/{len(CHECKS)} checks passed.")


if __name__ == "__main__":
    main()

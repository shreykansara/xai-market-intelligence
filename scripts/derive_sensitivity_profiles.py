"""Derive each startup's PESTLE/Porter's sensitivity profile from its fabricated
profit history (data/profit_history.json), replacing hand-authored ground truth.

The lagged regression now runs at SUB-CLUSTER granularity (data/subclusters.json,
~35-55 features - roughly one per dimension x sub-cluster) instead of the 11
dimension-level features used before: for each of a handful of candidate lag
windows, regress the startup's daily profit changes against the preceding day's
per-sub-cluster relevance-times-polarity signal plus an intercept. With ~180
daily observations and this many features, plain least squares overfits badly,
so this is ridge-regularized (the intercept itself is left unpenalized). The lag
with the highest held-out-adjusted fit (R^2) is kept, and its sub-cluster
coefficients are summed back up to their parent dimension - 11 values, rescaled
so the largest magnitude hits 100, sign preserved - to become that startup's
derived sensitivity profile. This overwrites the pestle_profile/porters_profile
fields in data/startups.json, exactly as before: only the feature granularity
of the regression changed, not the shape of what gets written out or how the
shared matrix W is trained on top of it.

The actual regression math (build_feature_columns / build_daily_signal /
fit_lag_ridge / derive_profile / profile_to_dicts) now lives in
src/marketintel/sensitivity_regression.py, extracted so the SAME mechanism can
be reused for a real company's uploaded sales history against the real news
corpus (see sales_upload.py) instead of being duplicated. This script is now a
thin caller: it supplies the fabricated corpus's fixed 180-day window anchored
on TODAY and iterates over the 50 startups; nothing about the math changed.

Then validates the recovery at this finer granularity: compares each derived
(rolled-up) profile against its hidden generation template (hidden_ground_truth.py,
never seen by the regression) and reports the correlation, plus how often the
recovered lag matches the true one - the same sanity check as before, now
confirming the sub-cluster-level regression didn't degrade recovery quality.

Must run AFTER simulate_profit_history.py and discover_subclusters.py.
Run: python scripts/derive_sensitivity_profiles.py
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from marketintel.config import (  # noqa: E402
    N_PROFIT_DAYS,
    PESTLE_DIMS,
    PORTERS_DIMS,
    PROFILE_REGRESSION_ALPHA,
    PROFIT_HISTORY_PATH,
    STARTUPS_PATH,
    SUBCLUSTERS_PATH,
)
from marketintel.data_loader import load_news, load_startups  # noqa: E402
from marketintel.sensitivity_regression import (  # noqa: E402
    ALL_DIMS,
    build_daily_signal,
    build_feature_columns,
    derive_profile,
    profile_to_dicts,
)

from hidden_ground_truth import HIDDEN_TEMPLATES  # noqa: E402

TODAY = datetime(2026, 8, 24)
WINDOW_START = TODAY - timedelta(days=N_PROFIT_DAYS - 1)


def hidden_vector(hidden: dict) -> np.ndarray:
    return np.array([hidden["pestle"][d] for d in PESTLE_DIMS] + [hidden["porters"][d] for d in PORTERS_DIMS])


def main():
    news, _ = load_news()
    startups, _ = load_startups()

    with open(SUBCLUSTERS_PATH, encoding="utf-8") as f:
        subclusters = json.load(f)
    with open(PROFIT_HISTORY_PATH, encoding="utf-8") as f:
        profit_history = json.load(f)

    columns = build_feature_columns(subclusters)
    signal = build_daily_signal(news, subclusters, columns, WINDOW_START, N_PROFIT_DAYS)
    print(f"Deriving sensitivity profiles for {len(startups)} startups via sub-cluster lag regression...")
    print(f"({len(columns)} sub-cluster features, ridge alpha={PROFILE_REGRESSION_ALPHA})")
    print(f"{'startup':<24} {'lag':>4} {'true_lag':>9} {'R^2':>7} {'corr_vs_hidden':>15}")

    hidden_vecs, derived_vecs = [], []
    lag_matches = 0

    for startup in startups:
        hidden = HIDDEN_TEMPLATES[startup["name"]]
        profit = np.array([p["profit"] for p in profit_history[startup["id"]]])

        best_lag, best_r2, dim_totals = derive_profile(profit, signal, columns)
        pestle_profile, porters_profile = profile_to_dicts(dim_totals)
        startup["pestle_profile"] = pestle_profile
        startup["porters_profile"] = porters_profile

        derived = np.array([dim_totals[d] for _, d in ALL_DIMS])
        h_vec = hidden_vector(hidden)
        corr = float(np.corrcoef(derived, h_vec)[0, 1])
        hidden_vecs.append(h_vec)
        derived_vecs.append(derived)
        if best_lag == hidden["shock_lag_days"]:
            lag_matches += 1

        print(
            f"{startup['name']:<24} {best_lag:>4} {hidden['shock_lag_days']:>9} "
            f"{best_r2:>7.3f} {corr:>15.3f}"
        )

    with open(STARTUPS_PATH, "w", encoding="utf-8") as f:
        json.dump(startups, f, indent=2)
    print(f"\nWrote derived profiles into {STARTUPS_PATH}")

    # --- Validation: derived profile vs. hidden generation template ---
    pooled_hidden = np.concatenate(hidden_vecs)
    pooled_derived = np.concatenate(derived_vecs)
    pooled_corr = float(np.corrcoef(pooled_derived, pooled_hidden)[0, 1])
    per_startup_corrs = [float(np.corrcoef(d, h)[0, 1]) for d, h in zip(derived_vecs, hidden_vecs)]

    print("\n=== VALIDATION: derived profile vs. hidden generation template (sub-cluster granularity) ===")
    print(f"Pooled correlation across all {len(startups)} startups x 11 dimensions: {pooled_corr:.3f}")
    print(f"Mean per-startup correlation: {np.mean(per_startup_corrs):.3f}")
    print(f"Recovered lag matched the true hidden lag for {lag_matches}/{len(startups)} startups.")
    if pooled_corr < 0.4:
        print(
            "WARNING: weak recovery - check the sub-cluster feature construction or "
            "PROFILE_REGRESSION_ALPHA before training the shared matrix W on these profiles."
        )


if __name__ == "__main__":
    main()

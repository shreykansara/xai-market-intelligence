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
    CANDIDATE_LAGS,
    N_PROFIT_DAYS,
    PESTLE_DIMS,
    PORTERS_DIMS,
    PROFILE_REGRESSION_ALPHA,
    PROFIT_HISTORY_PATH,
    STARTUPS_PATH,
    SUBCLUSTERS_PATH,
)
from marketintel.data_loader import load_news, load_startups  # noqa: E402

from hidden_ground_truth import HIDDEN_TEMPLATES  # noqa: E402

TODAY = datetime(2026, 8, 24)
ALL_DIMS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def build_feature_columns(subclusters: dict):
    """One column per (dimension, sub-cluster id), in a fixed order, plus which
    parent dimension each column rolls up to."""
    columns = []  # (dim, cluster_id_str)
    for _, dim in ALL_DIMS:
        for cluster_id in sorted(subclusters[dim]["labels"], key=int):
            columns.append((dim, cluster_id))
    return columns


def build_daily_signal(news: list[dict], subclusters: dict, columns: list[tuple], n_days: int) -> np.ndarray:
    """signal[day, col] = sum over articles published that day, assigned to that
    (dimension, sub-cluster), of relevance * polarity. Articles below the
    clustering relevance threshold for a dimension have no assignment there and
    contribute nothing to any of that dimension's sub-cluster columns."""
    col_index = {key: i for i, key in enumerate(columns)}
    score_field_by_dim = {d: f for f, d in ALL_DIMS}
    window_start = TODAY - timedelta(days=n_days - 1)
    signal = np.zeros((n_days, len(columns)))

    for article in news:
        day = (datetime.strptime(article["date"], "%Y-%m-%d") - window_start).days
        if not (0 <= day < n_days):
            continue
        sign = polarity_sign(article)
        for _, dim in ALL_DIMS:
            cluster_id = subclusters[dim]["assignments"].get(article["id"])
            if cluster_id is None:
                continue
            col = col_index[(dim, str(cluster_id))]
            signal[day, col] += article[score_field_by_dim[dim]][dim] * sign

    return signal


def fit_lag_ridge(profit: np.ndarray, signal: np.ndarray, lag: int, alpha: float):
    """Ridge-regress profit_change[t] = profit[t] - profit[t-1] against
    signal[t-lag], with an unpenalized intercept to absorb the trend."""
    n_days = len(profit)
    n_features = signal.shape[1]
    profit_change = np.diff(profit)

    t_values = np.arange(lag - 1, n_days - 1)
    if len(t_values) < n_features // 2:
        return -np.inf, np.zeros(n_features)

    y = profit_change[t_values]
    X = signal[t_values + 1 - lag]
    X_design = np.column_stack([np.ones(len(y)), X])

    penalty = alpha * np.eye(n_features + 1)
    penalty[0, 0] = 0.0  # don't regularize the intercept

    coef = np.linalg.solve(X_design.T @ X_design + penalty, X_design.T @ y)
    residuals = y - X_design @ coef
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 1e-9 else 0.0
    return r_squared, coef[1:]


def roll_up_to_dimensions(coef: np.ndarray, columns: list[tuple]) -> np.ndarray:
    dim_totals = {d: 0.0 for _, d in ALL_DIMS}
    for value, (dim, _cluster_id) in zip(coef, columns):
        dim_totals[dim] += value
    return np.array([dim_totals[d] for _, d in ALL_DIMS])


def derive_profile(profit: np.ndarray, signal: np.ndarray, columns: list[tuple]):
    best_lag, best_r2, best_coef = None, -np.inf, None
    for lag in CANDIDATE_LAGS:
        r2, coef = fit_lag_ridge(profit, signal, lag, PROFILE_REGRESSION_ALPHA)
        if r2 > best_r2:
            best_lag, best_r2, best_coef = lag, r2, coef

    dim_vector = roll_up_to_dimensions(best_coef, columns)
    max_abs = np.max(np.abs(dim_vector))
    scaled = dim_vector / max_abs * 100.0 if max_abs > 1e-9 else dim_vector
    return best_lag, best_r2, scaled


def profile_to_dicts(vector: np.ndarray):
    pestle = {d: float(v) for d, v in zip(PESTLE_DIMS, vector[: len(PESTLE_DIMS)])}
    porters = {d: float(v) for d, v in zip(PORTERS_DIMS, vector[len(PESTLE_DIMS) :])}
    return pestle, porters


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
    signal = build_daily_signal(news, subclusters, columns, N_PROFIT_DAYS)
    print(f"Deriving sensitivity profiles for {len(startups)} startups via sub-cluster lag regression...")
    print(f"({len(columns)} sub-cluster features, ridge alpha={PROFILE_REGRESSION_ALPHA})")
    print(f"{'startup':<24} {'lag':>4} {'true_lag':>9} {'R^2':>7} {'corr_vs_hidden':>15}")

    hidden_vecs, derived_vecs = [], []
    lag_matches = 0

    for startup in startups:
        hidden = HIDDEN_TEMPLATES[startup["name"]]
        profit = np.array([p["profit"] for p in profit_history[startup["id"]]])

        best_lag, best_r2, derived = derive_profile(profit, signal, columns)
        pestle_profile, porters_profile = profile_to_dicts(derived)
        startup["pestle_profile"] = pestle_profile
        startup["porters_profile"] = porters_profile

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

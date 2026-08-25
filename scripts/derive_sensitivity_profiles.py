"""Derive each startup's PESTLE/Porter's sensitivity profile from its fabricated
profit history (data/profit_history.json), replacing hand-authored ground truth.

For each of a handful of candidate lag windows, regress the startup's daily
profit changes against the preceding day's news relevance-times-polarity signal
(summed per dimension across whatever articles ran that day) plus an intercept
(to absorb trend/drift). The lag with the highest explained variance (R^2) is
kept, and its 11 fitted dimension coefficients - rescaled so the largest
magnitude hits 100, sign preserved - become that startup's derived sensitivity
profile. This overwrites the pestle_profile/porters_profile fields in
data/startups.json.

Then validates the recovery: compares each derived profile against its hidden
generation template (hidden_ground_truth.py, never seen by the regression) and
reports the correlation, plus how often the recovered lag matches the true one.
This is a sanity check on the recovery pipeline itself - if it doesn't hold up,
the shared matrix W has no business being trained on top of it.

Must run AFTER simulate_profit_history.py.
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
    PROFIT_HISTORY_PATH,
    STARTUPS_PATH,
)
from marketintel.data_loader import load_news, load_startups  # noqa: E402

from hidden_ground_truth import HIDDEN_TEMPLATES  # noqa: E402

TODAY = datetime(2026, 8, 24)
ALL_DIMS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]
DIM_NAMES = [d for _, d in ALL_DIMS]


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def build_daily_signal(news: list[dict], n_days: int) -> np.ndarray:
    """signal[day, dim] = sum over articles published that day of relevance * polarity."""
    window_start = TODAY - timedelta(days=n_days - 1)
    signal = np.zeros((n_days, len(DIM_NAMES)))
    for article in news:
        day = (datetime.strptime(article["date"], "%Y-%m-%d") - window_start).days
        if not (0 <= day < n_days):
            continue
        sign = polarity_sign(article)
        for j, (score_field, dim) in enumerate(ALL_DIMS):
            signal[day, j] += article[score_field][dim] * sign
    return signal


def fit_lag(profit: np.ndarray, signal: np.ndarray, lag: int):
    """Regress profit_change[t] = profit[t] - profit[t-1] against signal[t-lag],
    with an intercept to absorb the trend. Returns (r_squared, dim_coefficients)."""
    n_days = len(profit)
    profit_change = np.diff(profit)  # index t -> change on day (t+1)

    t_values = np.arange(lag - 1, n_days - 1)  # day (t+1) needs t+1-lag >= 0 -> t >= lag-1
    if len(t_values) < len(DIM_NAMES) + 5:
        return -np.inf, np.zeros(len(DIM_NAMES))

    y = profit_change[t_values]
    X = signal[t_values + 1 - lag]
    X_design = np.column_stack([np.ones(len(y)), X])

    coef, *_ = np.linalg.lstsq(X_design, y, rcond=None)
    residuals = y - X_design @ coef
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 1e-9 else 0.0
    return r_squared, coef[1:]


def derive_profile(profit: np.ndarray, signal: np.ndarray):
    best_lag, best_r2, best_coef = None, -np.inf, None
    for lag in CANDIDATE_LAGS:
        r2, coef = fit_lag(profit, signal, lag)
        if r2 > best_r2:
            best_lag, best_r2, best_coef = lag, r2, coef

    max_abs = np.max(np.abs(best_coef))
    scaled = best_coef / max_abs * 100.0 if max_abs > 1e-9 else best_coef
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

    with open(PROFIT_HISTORY_PATH, encoding="utf-8") as f:
        profit_history = json.load(f)

    signal = build_daily_signal(news, N_PROFIT_DAYS)

    print(f"Deriving sensitivity profiles for {len(startups)} startups via lag regression...")
    print(f"{'startup':<24} {'lag':>4} {'true_lag':>9} {'R^2':>7} {'corr_vs_hidden':>15}")

    hidden_vecs, derived_vecs = [], []
    lag_matches = 0

    for startup in startups:
        hidden = HIDDEN_TEMPLATES[startup["name"]]
        profit = np.array([p["profit"] for p in profit_history[startup["id"]]])

        best_lag, best_r2, derived = derive_profile(profit, signal)
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

    print("\n=== VALIDATION: derived profile vs. hidden generation template ===")
    print(f"Pooled correlation across all {len(startups)} startups x 11 dimensions: {pooled_corr:.3f}")
    print(f"Mean per-startup correlation: {np.mean(per_startup_corrs):.3f}")
    print(f"Recovered lag matched the true hidden lag for {lag_matches}/{len(startups)} startups.")
    if pooled_corr < 0.4:
        print(
            "WARNING: weak recovery - check shock/noise scale in simulate_profit_history.py "
            "before training the shared matrix W on these profiles."
        )


if __name__ == "__main__":
    main()

"""Core lagged-ridge-regression mechanism for recovering a PESTLE/Porter's
sensitivity profile from a daily profit/revenue series and a news/fact pool -
extracted out of scripts/derive_sensitivity_profiles.py (originally written
only for the 20-then-50 fabricated startups) so the SAME mechanism can be
reused for a real company's uploaded sales history against the real news
corpus (see sales_upload.py), instead of a second, forked implementation.

The math is completely agnostic to what "profit" and "news" actually are:
  - `profit`: any daily numeric series (fabricated simulated profit, or a
    real uploaded revenue series resampled to one value per day).
  - the news/fact pool: any list of dicts shaped like a fabricated seed
    article or a real fact record (both already share the same shape -
    "date" or normalized-to-"date", "pestle_scores", "porters_scores",
    "polarity", "id") together with a `subclusters` dict describing which
    (dimension, sub-cluster) each item is assigned to.

For each of a handful of candidate lag windows, this ridge-regresses daily
profit CHANGES against the PRECEDING day's per-(dimension, sub-cluster)
relevance-times-polarity signal, keeps the lag with the best fit, and rolls
the winning lag's sub-cluster coefficients back up to their 11 parent
dimensions (rescaled so the largest magnitude hits 100, sign preserved).
"""
from datetime import datetime

import numpy as np

from .config import CANDIDATE_LAGS, PESTLE_DIMS, PORTERS_DIMS, PROFILE_REGRESSION_ALPHA

ALL_DIMS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]


def polarity_sign(item: dict) -> float:
    return 1.0 if item["polarity"] == "positive" else -1.0


def build_feature_columns(subclusters: dict, dims: list[str] | None = None) -> list[tuple]:
    """One column per (dimension, sub-cluster id), in a fixed order. `dims`
    optionally restricts this to a SUBSET of the 11 dimensions - used by the
    real-data path to only build features for dimensions that have passed
    real_data_inference.assess_dimension_coverage(), rather than regressing
    against sub-clusters fed by a reference pool judged too thin to trust
    for that dimension."""
    allowed = set(dims) if dims is not None else {d for _, d in ALL_DIMS}
    columns = []
    for _, dim in ALL_DIMS:
        if dim not in allowed:
            continue
        for cluster_id in sorted(subclusters[dim]["labels"], key=int):
            columns.append((dim, cluster_id))
    return columns


def build_daily_signal(
    items: list[dict], subclusters: dict, columns: list[tuple], window_start: datetime, n_days: int
) -> np.ndarray:
    """signal[day, col] = sum over items dated that day, assigned to that
    (dimension, sub-cluster), of relevance * polarity. `window_start` is the
    calendar date of day 0 - explicit rather than a hardcoded "today"
    constant, so this same function works for a fabricated 180-day window
    anchored on a fixed date AND a real news corpus's own (much shorter,
    recent) coverage window."""
    col_index = {key: i for i, key in enumerate(columns)}
    score_field_by_dim = {d: f for f, d in ALL_DIMS}
    signal = np.zeros((n_days, len(columns)))

    for item in items:
        day = (datetime.strptime(item["date"], "%Y-%m-%d") - window_start).days
        if not (0 <= day < n_days):
            continue
        sign = polarity_sign(item)
        for _, dim in ALL_DIMS:
            cluster_id = subclusters.get(dim, {}).get("assignments", {}).get(item["id"])
            if cluster_id is None:
                continue
            key = (dim, str(cluster_id))
            if key not in col_index:
                continue  # this dimension was excluded from `columns` (e.g. failed coverage) - skip it
            signal[day, col_index[key]] += item[score_field_by_dim[dim]][dim] * sign

    return signal


def fit_lag_ridge(profit: np.ndarray, signal: np.ndarray, lag: int, alpha: float):
    """Ridge-regress profit_change[t] = profit[t] - profit[t-1] against
    signal[t-lag], with an unpenalized intercept to absorb the trend.
    Returns (r_squared, coefficients) - coefficients exclude the intercept."""
    n_days = len(profit)
    n_features = signal.shape[1]
    profit_change = np.diff(profit)

    t_values = np.arange(lag - 1, n_days - 1)
    if len(t_values) < max(n_features // 2, 5):
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


def roll_up_to_dimensions(coef: np.ndarray, columns: list[tuple], dims: list[str] | None = None) -> dict:
    """Sums sub-cluster coefficients up to their parent dimension. Returns a
    dict keyed by dimension name (only dimensions present in `columns`, or
    all 11 if `dims` is None and columns cover all of them) rather than a
    fixed-length vector, since the real-data path may only have columns for
    a subset of dimensions."""
    present_dims = dims if dims is not None else sorted({d for d, _ in columns})
    dim_totals = {d: 0.0 for d in present_dims}
    for value, (dim, _cluster_id) in zip(coef, columns):
        dim_totals[dim] += value
    return dim_totals


def derive_profile(
    profit: np.ndarray,
    signal: np.ndarray,
    columns: list[tuple],
    dims: list[str] | None = None,
    candidate_lags: list[int] = CANDIDATE_LAGS,
    alpha: float = PROFILE_REGRESSION_ALPHA,
):
    """Tries every candidate lag, keeps the best-fitting one, rolls its
    coefficients up to parent dimensions, and rescales so the largest
    magnitude hits 100 (sign preserved). Returns (best_lag, best_r2,
    dim_totals: dict[str, float]) - dim_totals covers only the dimensions
    present in `columns` (see build_feature_columns's `dims` filter)."""
    best_lag, best_r2, best_coef = None, -np.inf, np.zeros(signal.shape[1])
    for lag in candidate_lags:
        r2, coef = fit_lag_ridge(profit, signal, lag, alpha)
        if r2 > best_r2:
            best_lag, best_r2, best_coef = lag, r2, coef

    dim_totals = roll_up_to_dimensions(best_coef, columns, dims)
    max_abs = max((abs(v) for v in dim_totals.values()), default=0.0)
    if max_abs > 1e-9:
        dim_totals = {d: v / max_abs * 100.0 for d, v in dim_totals.items()}
    return best_lag, best_r2, dim_totals


def profile_to_dicts(dim_totals: dict) -> tuple[dict, dict]:
    """Splits a dimension->value dict back into (pestle_profile, porters_profile)
    dicts, using whatever subset of PESTLE_DIMS/PORTERS_DIMS is present."""
    pestle = {d: float(dim_totals[d]) for d in PESTLE_DIMS if d in dim_totals}
    porters = {d: float(dim_totals[d]) for d in PORTERS_DIMS if d in dim_totals}
    return pestle, porters

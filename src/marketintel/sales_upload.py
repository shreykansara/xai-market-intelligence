"""Optional, second analysis mode: derive a company's own PESTLE/Porter's
sensitivity profile from its ACTUAL uploaded sales/revenue history, regressed
against the REAL news corpus - instead of (or alongside) the existing
CVP-similarity estimate, which infers sensitivity by comparing a business's
text description to comparable fabricated startups via the trained matrix W.

CVP input remains the required, unchanged default path (see server.py) - this
is a strictly additive second mode, only engaged when a caller provides a
sales upload AND that upload clears the validation bar in this module.

Reuses the exact same lagged-ridge-regression mechanism as the fabricated
offline pipeline (src/marketintel/sensitivity_regression.py, extracted out of
scripts/derive_sensitivity_profiles.py for this purpose) - the only things
that differ are: (a) the profit series is real, uploaded data instead of a
fabricated simulation, and (b) which news pool it's regressed against, and
whether that pool gates by per-dimension coverage - see derive_sales_profile()
below, the single entry point that dispatches on config.SALES_REGRESSION_NEWS_SOURCE:

  - "real" (the production path): regressed against the accumulated real-fact
    corpus (data/real_facts.json), restricted to only the PESTLE/Porter's
    dimensions that currently pass real_data_inference.assess_dimension_coverage()
    - the same per-dimension coverage gate live ingestion already respects,
    so a company's derived profile is never quietly backed by a dimension too
    thin in real news volume to trust. Can legitimately return "not enough
    data yet" (see compute_coverage_overlap) - this is the honest, thin-real-
    data-aware path and callers must keep falling back to CVP-only when it does.
  - "fabricated" (today's TIME-BOXED demo default - see config.py): regressed
    against the fabricated seed corpus instead, so the regression runs and
    produces output regardless of real-news volume. Every result this
    produces MUST be labeled to the caller as demo/sample-data, never
    presented as derived from the user's live news feed (see server.py /
    web/index.html's mandatory banner).

Explicitly out of scope (see CLAUDE.md): uploaded data is never folded into
the shared real/fabricated reference pool other users' CVP-similarity
analysis draws on, and never used to retrain the shared matrix W. Both would
require a real data-use/consent decision this pass does not make.
"""
import io
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd

from .config import CANDIDATE_LAGS, N_PROFIT_DAYS, PROFILE_REGRESSION_ALPHA, SALES_REGRESSION_NEWS_SOURCE
from .sensitivity_regression import ALL_DIMS, build_daily_signal, build_feature_columns, derive_profile, profile_to_dicts

MIN_OBSERVATIONS = 90  # distinct valid (date, value) rows required after cleaning
MAX_DUPLICATE_FRACTION = 0.05  # at most 5% of rows may be exact duplicate dates before we reject rather than aggregate
MIN_DATE_DENSITY = 0.5  # observations / calendar-day-span of the upload - below this, "excessive gaps"
MIN_OVERLAP_DAYS = 90  # the SAME bar, applied to the upload<->real-news-coverage overlap window specifically

DATE_NAME_HINTS = ("date", "day", "period", "month", "week", "timestamp", "time")
VALUE_NAME_HINTS = ("revenue", "sales", "profit", "income", "amount", "value", "turnover", "earnings")


@dataclass
class ColumnGuess:
    columns: list[str]
    guessed_date_col: str | None
    guessed_value_col: str | None
    preview_rows: list[dict]


@dataclass
class ValidationResult:
    valid: bool
    reason: str = ""
    daily_series: pd.Series | None = field(default=None, repr=False)  # date-indexed, one value per calendar day
    stats: dict = field(default_factory=dict)


def parse_upload(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """Parses a CSV or XLSX upload into a DataFrame. Raises ValueError for an
    unrecognized extension or a file pandas can't parse at all - callers
    should treat that as a 400, distinct from the richer validation below."""
    lower = filename.lower()
    try:
        if lower.endswith(".csv"):
            return pd.read_csv(io.BytesIO(file_bytes))
        if lower.endswith((".xlsx", ".xls")):
            return pd.read_excel(io.BytesIO(file_bytes))
    except Exception as exc:
        raise ValueError(f"Could not parse {filename!r} as a spreadsheet: {exc}") from exc
    raise ValueError(f"Unrecognized file type: {filename!r} (expected .csv or .xlsx)")


def _looks_like_dates(series: pd.Series, sample_size: int = 30) -> float:
    """Fraction of a sampled subset that parses as a date - used to guess the
    date column by CONTENT when the column name doesn't give it away."""
    sample = series.dropna().head(sample_size)
    if len(sample) == 0:
        return 0.0
    parsed = pd.to_datetime(sample, errors="coerce")
    return float(parsed.notna().mean())


def guess_columns(df: pd.DataFrame) -> ColumnGuess:
    """Best-guess which column is the date column and which is the revenue/
    sales metric column - by name first, then by content. This is ALWAYS a
    guess to be confirmed or corrected by the caller before anything is
    computed (see validate_upload) - never trusted silently."""
    columns = list(df.columns)

    date_col = next((c for c in columns if any(h in str(c).lower() for h in DATE_NAME_HINTS)), None)
    if date_col is None:
        date_col = max(columns, key=lambda c: _looks_like_dates(df[c]), default=None)
        if date_col is not None and _looks_like_dates(df[date_col]) < 0.5:
            date_col = None  # nothing in the sheet looks like a date column at all

    value_col = next(
        (c for c in columns if c != date_col and any(h in str(c).lower() for h in VALUE_NAME_HINTS)), None
    )
    if value_col is None:
        numeric_cols = [c for c in columns if c != date_col and pd.api.types.is_numeric_dtype(df[c])]
        value_col = numeric_cols[0] if numeric_cols else None

    preview = df.head(5).to_dict(orient="records")
    return ColumnGuess(columns=columns, guessed_date_col=date_col, guessed_value_col=value_col, preview_rows=preview)


def validate_upload(df: pd.DataFrame, date_col: str, value_col: str) -> ValidationResult:
    """Cleans and validates a (date_col, value_col) mapping the caller has
    confirmed. Requires MIN_OBSERVATIONS distinct valid days, rejects if
    duplicate-date rows exceed MAX_DUPLICATE_FRACTION, and rejects if the
    date range is too sparse (MIN_DATE_DENSITY) - "reasonable data quality"
    per the spec, not just a row count. Returns a daily-indexed Series
    (forward-filled to one value per calendar day across the observed range)
    on success; ValidationResult.valid=False with a plain-language `reason`
    on failure - callers must fall back to CVP-only analysis, not run the
    regression anyway or fail silently."""
    if date_col not in df.columns or value_col not in df.columns:
        return ValidationResult(valid=False, reason="The selected columns don't exist in the uploaded file.")

    working = df[[date_col, value_col]].copy()
    working.columns = ["date", "value"]
    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working["value"] = pd.to_numeric(working["value"], errors="coerce")

    total_rows = len(working)
    working = working.dropna(subset=["date", "value"])
    if len(working) == 0:
        return ValidationResult(
            valid=False,
            reason="None of the rows had both a parseable date and a numeric value in the selected columns.",
        )

    duplicate_count = int(working["date"].duplicated().sum())
    if total_rows > 0 and duplicate_count / total_rows > MAX_DUPLICATE_FRACTION:
        return ValidationResult(
            valid=False,
            reason=(
                f"{duplicate_count}/{total_rows} rows share a duplicate date ("
                f"more than {MAX_DUPLICATE_FRACTION:.0%}) - this doesn't look like one observation per day. "
                "Please upload one revenue/sales figure per date."
            ),
        )
    # Duplicates within tolerance: aggregate by summing same-day values (e.g. multiple
    # transactions on one day), which is the natural aggregation for a revenue metric.
    working = working.groupby("date", as_index=False)["value"].sum()

    n_valid_days = len(working)
    if n_valid_days < MIN_OBSERVATIONS:
        return ValidationResult(
            valid=False,
            reason=(
                f"Only {n_valid_days} valid daily observation(s) after cleaning - "
                f"need at least {MIN_OBSERVATIONS} days of historical sales data for a reliable regression. "
                "Falling back to the CVP-based estimate."
            ),
        )

    date_min, date_max = working["date"].min(), working["date"].max()
    span_days = (date_max - date_min).days + 1
    density = n_valid_days / span_days if span_days > 0 else 0.0
    if density < MIN_DATE_DENSITY:
        return ValidationResult(
            valid=False,
            reason=(
                f"Your upload spans {span_days} days but only has data for {n_valid_days} of them "
                f"({density:.0%} coverage) - too many gaps to trust a daily regression. "
                "Falling back to the CVP-based estimate."
            ),
        )

    daily_series = working.set_index("date")["value"].asfreq("D").ffill()
    return ValidationResult(
        valid=True,
        daily_series=daily_series,
        stats={
            "n_valid_days": n_valid_days,
            "span_days": span_days,
            "density": density,
            "date_min": date_min.strftime("%Y-%m-%d"),
            "date_max": date_max.strftime("%Y-%m-%d"),
            "duplicate_rows_aggregated": duplicate_count,
        },
    )


def compute_coverage_overlap(daily_series: pd.Series, real_facts: list[dict]) -> dict:
    """Compares the uploaded sales date range against the real news corpus's
    ACTUAL coverage range and reports the overlap explicitly - a regression
    can only use the window where both signals exist at once, which may be a
    small fraction of the full upload history."""
    upload_start, upload_end = daily_series.index.min(), daily_series.index.max()

    if not real_facts:
        return {
            "upload_start": upload_start.strftime("%Y-%m-%d"),
            "upload_end": upload_end.strftime("%Y-%m-%d"),
            "real_news_start": None,
            "real_news_end": None,
            "overlap_start": None,
            "overlap_end": None,
            "overlap_days": 0,
            "sufficient": False,
        }

    real_dates = [datetime.fromisoformat(f["published"]) for f in real_facts]
    real_start, real_end = min(real_dates).replace(tzinfo=None), max(real_dates).replace(tzinfo=None)

    overlap_start = max(upload_start, pd.Timestamp(real_start.date()))
    overlap_end = min(upload_end, pd.Timestamp(real_end.date()))
    overlap_days = max((overlap_end - overlap_start).days + 1, 0)

    return {
        "upload_start": upload_start.strftime("%Y-%m-%d"),
        "upload_end": upload_end.strftime("%Y-%m-%d"),
        "upload_span_days": (upload_end - upload_start).days + 1,
        "real_news_start": real_start.strftime("%Y-%m-%d"),
        "real_news_end": real_end.strftime("%Y-%m-%d"),
        "overlap_start": overlap_start.strftime("%Y-%m-%d") if overlap_days > 0 else None,
        "overlap_end": overlap_end.strftime("%Y-%m-%d") if overlap_days > 0 else None,
        "overlap_days": overlap_days,
        "sufficient": overlap_days >= MIN_OVERLAP_DAYS,
    }


def _derive_profile_from_real_data(
    daily_series: pd.Series,
    real_facts: list[dict],
    dimension_coverage: dict[str, bool],
    subclusters: dict,
    real_assignments: dict,
):
    """Runs the shared lagged-ridge-regression mechanism (sensitivity_regression.py)
    against the REAL news corpus over the upload<->real-news overlap window,
    restricted to only the dimensions real_data_inference.assess_dimension_coverage()
    currently trusts. Returns None if the overlap is too thin (per
    compute_coverage_overlap's MIN_OVERLAP_DAYS bar) - callers must fall back
    to the CVP-based estimate in that case, with the overlap stats surfaced
    so the caller can explain why.

    `real_assignments` is real_data's own per-dimension sub-cluster assignment
    (from live_facts.assign_fact_subclusters against the EXISTING fabricated-
    discovered centroids - the sub-cluster STRUCTURE itself is not migrated,
    see CLAUDE.md) - passed in rather than recomputed here so callers that
    already computed it for live scoring don't pay for it twice.

    This is the intended, production path (see SALES_REGRESSION_NEWS_SOURCE
    in config.py) - call derive_sales_profile() below rather than this
    function directly, so the news-source choice stays a single config flag
    rather than being hardcoded at each call site.
    """
    overlap = compute_coverage_overlap(daily_series, real_facts)
    if not overlap["sufficient"]:
        return None, overlap

    covered_dims = [d for d, ok in dimension_coverage.items() if ok]
    if not covered_dims:
        overlap["sufficient"] = False
        overlap["reason"] = "No PESTLE/Porter's dimension currently has enough real news coverage to regress against."
        return None, overlap

    overlap_start = pd.Timestamp(overlap["overlap_start"])
    overlap_end = pd.Timestamp(overlap["overlap_end"])
    n_days = overlap["overlap_days"]

    window_series = daily_series.reindex(pd.date_range(overlap_start, overlap_end, freq="D")).ffill().bfill()
    profit = window_series.to_numpy()

    real_as_items = [
        {**f, "date": f["published"][:10]}
        for f in real_facts
        if overlap_start <= pd.Timestamp(f["published"][:10]) <= overlap_end
    ]
    real_only_subclusters = {
        dim: {"labels": subclusters[dim]["labels"], "assignments": real_assignments.get(dim, {})}
        for dim in covered_dims
    }

    columns = build_feature_columns(real_only_subclusters, dims=covered_dims)
    if not columns:
        overlap["sufficient"] = False
        overlap["reason"] = "No sub-cluster features available for the covered dimensions in this window."
        return None, overlap

    signal = build_daily_signal(real_as_items, real_only_subclusters, columns, overlap_start.to_pydatetime(), n_days)
    best_lag, best_r2, dim_totals = derive_profile(
        profit, signal, columns, dims=covered_dims, candidate_lags=CANDIDATE_LAGS, alpha=PROFILE_REGRESSION_ALPHA
    )
    pestle_profile, porters_profile = profile_to_dicts(dim_totals)

    result = {
        "pestle_profile": pestle_profile,
        "porters_profile": porters_profile,
        "covered_dimensions": covered_dims,
        "uncovered_dimensions": [d for d, ok in dimension_coverage.items() if not ok],
        "lag_days": best_lag,
        "r_squared": best_r2,
        "news_source": "real",
    }
    return result, overlap


def _fabricated_window(fabricated_news: list[dict]) -> tuple[datetime, int]:
    """The fabricated seed corpus's own fixed synthetic calendar span, read
    directly off its articles' own dates rather than duplicating the
    TODAY/WINDOW_START constants scripts/derive_sensitivity_profiles.py
    hardcodes for itself - so this stays correct even if that corpus is ever
    regenerated on a different date."""
    dates = [datetime.strptime(item["date"], "%Y-%m-%d") for item in fabricated_news]
    window_start = min(dates)
    span_days = (max(dates) - window_start).days + 1
    return window_start, span_days


def _derive_profile_from_fabricated_data(daily_series: pd.Series, fabricated_news: list[dict], subclusters: dict):
    """TIME-BOXED DEMO PATH (see SALES_REGRESSION_NEWS_SOURCE in config.py):
    runs the exact same lagged-ridge-regression mechanism as the production
    real-news path above, but against the fabricated seed corpus (the same
    1000 articles scripts/derive_sensitivity_profiles.py already regresses
    the 50 fabricated startups against) instead of the sparse real-news
    corpus - so the regression runs end to end and produces output today,
    rather than falling back to CVP-only every time real coverage is thin.

    The fabricated corpus's dates are a fixed, representative synthetic
    timeline with no relationship to the upload's actual calendar, so the
    upload's most recent days of history are aligned onto that timeline by
    POSITION only, never by real date correspondence - this is a
    representative-sample demo run, not a claim that these specific fabricated
    articles happened on the same days as the uploaded revenue. Every caller
    MUST label a result produced by this path as demo/sample-data - see
    server.py's `news_source` field and web/index.html's mandatory banner.

    All 11 dimensions are used (unlike the real-data path, the fabricated
    corpus is the fully-discovered taxonomy itself, so there is no thin-
    coverage dimension to gate on here)."""
    all_dims = [d for _, d in ALL_DIMS]
    window_start, fabricated_span = _fabricated_window(fabricated_news)
    n_days = min(fabricated_span, N_PROFIT_DAYS, len(daily_series))

    profit = daily_series.iloc[-n_days:].to_numpy()

    columns = build_feature_columns(subclusters, dims=all_dims)
    signal = build_daily_signal(fabricated_news, subclusters, columns, window_start, n_days)
    best_lag, best_r2, dim_totals = derive_profile(
        profit, signal, columns, dims=all_dims, candidate_lags=CANDIDATE_LAGS, alpha=PROFILE_REGRESSION_ALPHA
    )
    pestle_profile, porters_profile = profile_to_dicts(dim_totals)

    return {
        "pestle_profile": pestle_profile,
        "porters_profile": porters_profile,
        "covered_dimensions": all_dims,
        "uncovered_dimensions": [],
        "lag_days": best_lag,
        "r_squared": best_r2,
        "news_source": "fabricated",
    }


def derive_sales_profile(
    daily_series: pd.Series,
    real_facts: list[dict],
    dimension_coverage: dict[str, bool],
    subclusters: dict,
    real_assignments: dict,
    fabricated_news: list[dict],
    news_source: str = SALES_REGRESSION_NEWS_SOURCE,
) -> tuple[dict | None, dict]:
    """Single entry point for the sales-history regression - callers should
    use this instead of either underlying implementation directly, so which
    news pool gets used is controlled by one config flag
    (SALES_REGRESSION_NEWS_SOURCE), not hardcoded per call site. Returns
    (derived_profile_or_None, overlap_or_status_dict) either way, so a
    caller can pattern-match the result the same way regardless of source.

    news_source="fabricated" (today's demo default) always "succeeds" if the
    fabricated corpus and a validated upload are both present - there is no
    real coverage to be thin on. news_source="real" is the unchanged,
    honest production path: it can legitimately return None when the
    upload<->real-news overlap or per-dimension coverage isn't there yet
    (see _derive_profile_from_real_data), and callers must keep falling back
    to the CVP-only estimate in that case exactly as before.
    """
    if news_source == "fabricated":
        derived = _derive_profile_from_fabricated_data(daily_series, fabricated_news, subclusters)
        overlap = {"news_source": "fabricated", "sufficient": True}
        return derived, overlap

    derived, overlap = _derive_profile_from_real_data(
        daily_series, real_facts, dimension_coverage, subclusters, real_assignments
    )
    overlap["news_source"] = "real"
    return derived, overlap

"""Simulate a fabricated daily profit/revenue history per startup over the last
6 months: a baseline trend plus noise, with realistic shocks injected using each
startup's HIDDEN sensitivity template (see hidden_ground_truth.py) - when a news
article is highly relevant to a dimension the startup is hidden-sensitive to, a
profit shock lands some days later (that startup's hidden shock_lag_days), sized
by the article's relevance and polarity times the hidden sensitivity weight.

This is the "observed" dataset: derive_sensitivity_profiles.py later mines it to
recover each startup's sensitivity profile without ever seeing the hidden
template that generated it.

Must run AFTER generate_news.py and generate_startups.py.
Run: python scripts/simulate_profit_history.py
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    N_PROFIT_DAYS,
    PESTLE_DIMS,
    PORTERS_DIMS,
    PROFIT_HISTORY_PATH,
)
from marketintel.data_loader import load_news, load_startups  # noqa: E402

from hidden_ground_truth import HIDDEN_TEMPLATES  # noqa: E402

SEED = 123
TODAY = datetime(2026, 8, 24)

ALL_DIMS = [("pestle_scores", "pestle", d) for d in PESTLE_DIMS] + [
    ("porters_scores", "porters", d) for d in PORTERS_DIMS
]


def polarity_sign(article: dict) -> float:
    return 1.0 if article["polarity"] == "positive" else -1.0


def simulate_one(hidden: dict, news: list[dict], rng: np.random.Generator) -> list[dict]:
    lag = hidden["shock_lag_days"]

    baseline_level = rng.uniform(80_000, 250_000)
    daily_growth = rng.uniform(-150, 400)
    noise_std = baseline_level * 0.04
    shock_scale = baseline_level * 0.35

    profit = baseline_level + daily_growth * np.arange(N_PROFIT_DAYS)
    profit = profit + rng.normal(0, noise_std, size=N_PROFIT_DAYS)

    window_start = TODAY - timedelta(days=N_PROFIT_DAYS - 1)
    for article in news:
        article_day = (datetime.strptime(article["date"], "%Y-%m-%d") - window_start).days
        target_day = article_day + lag
        if not (0 <= target_day < N_PROFIT_DAYS):
            continue
        shock = 0.0
        for score_field, profile_key, dim in ALL_DIMS:
            shock += article[score_field][dim] * (hidden[profile_key][dim] / 100.0)
        shock *= polarity_sign(article)
        if abs(shock) > 1e-9:
            profit[target_day] += shock * shock_scale

    dates = [(window_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(N_PROFIT_DAYS)]
    return [{"date": d, "profit": round(float(p), 2)} for d, p in zip(dates, profit)]


def main():
    news, _ = load_news()
    startups, _ = load_startups()
    rng = np.random.default_rng(SEED)

    histories = {}
    for startup in startups:
        hidden = HIDDEN_TEMPLATES[startup["name"]]
        histories[startup["id"]] = simulate_one(hidden, news, rng)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROFIT_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(histories, f, indent=2)
    print(f"Wrote {PROFIT_HISTORY_PATH} ({len(histories)} startups x {N_PROFIT_DAYS} days)")


if __name__ == "__main__":
    main()

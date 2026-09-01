"""Read-only browse/inspect layer over EVERY news item the system currently
holds, across both corpora, so what's actually been collected is visible in
the UI instead of only inferrable from file sizes on disk.

The two corpora are deliberately NOT merged into one undifferentiated list -
they have genuinely different provenance:

  - "seed" - the 1000 fabricated articles (data/news.json).
  - "live" - real facts from ingestion_service.py (data/real_facts.json),
             decomposed from real articles by Ollama.

Both are scored by /api/analyze today (see live_facts.py); each item still
carries an explicit in_scoring flag so a future corpus that ISN'T wired into
the serving path can't quietly look equivalent to one that is.

Nothing here computes, mutates, or re-scores anything - it only reads what
already exists on disk and normalizes the two record shapes into one
display shape. This module is intentionally free of any dependency on the
scoring pipeline so browsing can never perturb analysis.
"""
import json
from pathlib import Path

from .config import (
    NEWS_PATH,
    PESTLE_DIMS,
    PESTLE_LABELS,
    PORTERS_DIMS,
    PORTERS_LABELS,
    REAL_ARTICLES_PATH,
    REAL_FACTS_PATH,
)

ALL_DIM_LABELS = {**PESTLE_LABELS, **PORTERS_LABELS}
SOURCES = ("seed", "live")

# Cache keyed by (path -> mtime) so a browse request is cheap, but a corpus
# that grew since the last request (live ingestion appending to real_facts.json
# from its own process) is picked up without restarting the server.
_cache: dict = {}


def _top_dimension(item: dict) -> tuple[str, float]:
    """The single dimension this item scores highest on, across both
    frameworks - what the item is "mostly about", for at-a-glance scanning.
    The full 11-dimension vector is returned separately for the detail view."""
    scores = {**item.get("pestle_scores", {}), **item.get("porters_scores", {})}
    if not scores:
        return "", 0.0
    dim, value = max(scores.items(), key=lambda kv: kv[1])
    return dim, float(value)


def _all_scores(item: dict) -> dict:
    scores = {**item.get("pestle_scores", {}), **item.get("porters_scores", {})}
    return {d: round(float(scores.get(d, 0.0)), 3) for d in PESTLE_DIMS + PORTERS_DIMS}


def _load_json(path: Path) -> list:
    """Any unreadable/corrupt corpus degrades to "nothing from this source"
    rather than breaking the whole browse page - same posture as
    data_loader.load_real_facts(), for the same reason (these files are
    written by other processes that may be mid-write or absent entirely)."""
    try:
        if not path.exists() or path.stat().st_size == 0:
            return []
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError, OSError, EOFError):
        return []


def _normalize_seed(article: dict) -> dict:
    dim, score = _top_dimension(article)
    return {
        "id": article["id"],
        "source": "seed",
        "origin": "fabricated",
        "text": article.get("title", ""),
        "detail": article.get("body", ""),
        "date": str(article.get("date", ""))[:10],
        "scope": article.get("scope", ""),
        "polarity": article.get("polarity", ""),
        "top_dimension": dim,
        "top_dimension_label": ALL_DIM_LABELS.get(dim, dim),
        "top_dimension_score": round(score, 3),
        "scores": _all_scores(article),
        "link": None,
        "mention_count": 1,
        "in_scoring": True,
    }


def _normalize_fact(fact: dict, source: str, articles_by_id: dict, in_scoring: bool) -> dict:
    dim, score = _top_dimension(fact)
    parent = articles_by_id.get(fact.get("parent_article_id"), {})
    return {
        "id": fact["id"],
        "source": source,
        # The feed an article came from, shown as-is rather than flattened
        # into a generic "real" label - provenance is the whole point here.
        "origin": parent.get("source", "unknown"),
        "text": fact.get("fact_text", ""),
        "detail": parent.get("title", ""),
        "date": str(fact.get("published", ""))[:10],
        "scope": fact.get("scope", ""),
        "polarity": fact.get("polarity", ""),
        "top_dimension": dim,
        "top_dimension_label": ALL_DIM_LABELS.get(dim, dim),
        "top_dimension_score": round(score, 3),
        "scores": _all_scores(fact),
        "link": parent.get("link") or parent.get("url"),
        "mention_count": int(fact.get("mention_count", 1) or 1),
        "in_scoring": in_scoring,
    }


def load_all_items() -> list[dict]:
    """Every item from both corpora, normalized to one display shape and
    sorted newest-first. Cached per (file, mtime) so repeat browsing is cheap
    while a corpus still being written to is picked up on its next change."""
    paths = [NEWS_PATH, REAL_FACTS_PATH, REAL_ARTICLES_PATH]
    stamp = tuple((p.stat().st_mtime_ns if p.exists() else 0) for p in paths)
    if _cache.get("stamp") == stamp:
        return _cache["items"]

    seed = _load_json(NEWS_PATH)
    live_facts = _load_json(REAL_FACTS_PATH)
    live_articles = {a["id"]: a for a in _load_json(REAL_ARTICLES_PATH)}
    items = [_normalize_seed(a) for a in seed]
    items += [_normalize_fact(f, "live", live_articles, in_scoring=True) for f in live_facts]

    items.sort(key=lambda i: (i["date"], i["id"]), reverse=True)
    _cache["stamp"] = stamp
    _cache["items"] = items
    return items


def summarize(items: list[dict]) -> dict:
    """Per-corpus totals and date coverage - the "what do we actually have"
    answer, which is the main reason this page exists."""
    summary = {}
    for source in SOURCES:
        subset = [i for i in items if i["source"] == source]
        dates = sorted({i["date"] for i in subset if i["date"]})
        summary[source] = {
            "count": len(subset),
            "start": dates[0] if dates else None,
            "end": dates[-1] if dates else None,
            "distinct_days": len(dates),
            "in_scoring": bool(subset and subset[0]["in_scoring"]),
        }
    return summary


def filter_items(
    items: list[dict],
    source: str = "all",
    q: str = "",
    scope: str = "all",
    polarity: str = "all",
    dimension: str = "all",
) -> list[dict]:
    """Plain substring/equality filtering - no ranking, no embedding search.
    This is an inspection view over what's stored, deliberately not a second
    (and potentially divergent) retrieval mechanism next to the real one."""
    needle = q.strip().lower()
    result = items
    if source != "all":
        result = [i for i in result if i["source"] == source]
    if scope != "all":
        result = [i for i in result if i["scope"] == scope]
    if polarity != "all":
        result = [i for i in result if i["polarity"] == polarity]
    if dimension != "all":
        result = [i for i in result if i["top_dimension"] == dimension]
    if needle:
        result = [i for i in result if needle in i["text"].lower() or needle in (i["detail"] or "").lower()]
    return result


def facet_values(items: list[dict]) -> dict:
    """The scope values actually present, so the UI's filter dropdown offers
    real options rather than a hardcoded list that can drift from the data."""
    return {
        "scopes": sorted({i["scope"] for i in items if i["scope"]}),
        "dimensions": [{"value": d, "label": ALL_DIM_LABELS.get(d, d)} for d in PESTLE_DIMS + PORTERS_DIMS],
    }

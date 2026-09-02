"""Read-only browse/inspect layer over every news item the system currently
holds, so what's actually been collected is visible in the UI instead of only
inferrable from file sizes on disk.

There is now exactly ONE corpus: "lpu" - atomic facts decomposed from the real
LPU announcements in data/lpudata/ (see lpu_ingestion.py), stored in
data/lpu_facts.json with their parent announcements in
data/lpu_announcements.json. The fabricated seed corpus and the live-ingested
news feed were both removed, so nothing else is left to browse.

Each item still carries an explicit in_scoring flag rather than that being
assumed: a corpus that is stored but NOT wired into /api/analyze must never
look equivalent to one that is.

Two quality flags come straight from ingestion and are surfaced rather than
hidden, because both are ways a record can be less trustworthy than it looks:
  - decomposition_ok=False - Ollama timed out or returned unparseable JSON, so
    this record is the WHOLE announcement stored unsplit, not an atomic fact.
  - classification_ok=False - the relevance/polarity call failed, so the
    all-zero scores mean "not scored", not "genuinely no market relevance".

Nothing here computes, mutates, or re-scores anything - it only reads what
already exists on disk and normalizes it into one display shape. This module
is intentionally free of any dependency on the scoring pipeline so browsing
can never perturb analysis, and it is safe to read a corpus that ingestion is
still actively writing to (every write is temp-file-then-rename).
"""
import json
from pathlib import Path

from .config import (
    LPU_ANNOUNCEMENTS_PATH,
    LPU_FACTS_PATH,
    PESTLE_DIMS,
    PESTLE_LABELS,
    PORTERS_DIMS,
    PORTERS_LABELS,
)

ALL_DIM_LABELS = {**PESTLE_LABELS, **PORTERS_LABELS}
SOURCES = ("lpu",)

# Cache keyed by (path -> mtime) so repeat browsing is cheap, while a corpus
# that grew since the last request (the ingestion run flushing a checkpoint
# every 25 announcements from its own process) is picked up automatically
# without restarting the server.
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
    rather than breaking the whole browse page - the same posture
    data_loader.load_real_facts() takes, for the same reason (this file is
    written by a separate long-running process)."""
    try:
        if not path.exists() or path.stat().st_size == 0:
            return []
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError, OSError, EOFError):
        return []


def _normalize_lpu_fact(fact: dict, announcements_by_id: dict) -> dict:
    dim, score = _top_dimension(fact)
    parent = announcements_by_id.get(fact.get("parent_announcement_id"), {})
    links = parent.get("links") or []
    return {
        "id": fact["id"],
        "source": "lpu",
        # Who posted the notice - the LPU equivalent of a news outlet, and the
        # closest thing this corpus has to provenance beyond the file it came from.
        "origin": (parent.get("uploaded_by") or "LPU").split("*")[0].strip() or "LPU",
        "text": fact.get("fact_text", ""),
        "detail": parent.get("title", ""),
        "date": (fact.get("published") or "")[:10],
        "scope": fact.get("scope", ""),
        "polarity": fact.get("polarity", ""),
        "top_dimension": dim,
        "top_dimension_label": ALL_DIM_LABELS.get(dim, dim),
        "top_dimension_score": round(score, 3),
        "scores": _all_scores(fact),
        "link": links[0] if links and isinstance(links[0], str) else None,
        "mention_count": int(fact.get("mention_count", 1) or 1),
        # Absent on records written before these flags existed - treated as
        # unknown-but-assumed-ok rather than silently reported as failures.
        "decomposition_ok": bool(fact.get("decomposition_ok", True)),
        "classification_ok": bool(fact.get("classification_ok", True)),
        "is_lpu": bool(fact.get("is_lpu", True)),
        # The LPU corpus is not yet wired into /api/analyze's scoring path.
        "in_scoring": False,
    }


def load_all_items() -> list[dict]:
    """Every stored fact, normalized to one display shape and sorted
    newest-first. Cached per (file, mtime) so repeat browsing is cheap while an
    actively-growing corpus is still picked up on its next change."""
    paths = [LPU_FACTS_PATH, LPU_ANNOUNCEMENTS_PATH]
    stamp = tuple((p.stat().st_mtime_ns if p.exists() else 0) for p in paths)
    if _cache.get("stamp") == stamp:
        return _cache["items"]

    facts = _load_json(LPU_FACTS_PATH)
    announcements = {a["id"]: a for a in _load_json(LPU_ANNOUNCEMENTS_PATH)}
    items = [_normalize_lpu_fact(f, announcements) for f in facts]

    # Undated facts sort last rather than being dropped - the announcement is
    # real, its date just couldn't be parsed from the source.
    items.sort(key=lambda i: (i["date"] == "", i["date"], i["id"]), reverse=True)
    _cache["stamp"] = stamp
    _cache["items"] = items
    return items


def summarize(items: list[dict]) -> dict:
    """Per-corpus totals, date coverage and ingestion-quality counts - the
    "what do we actually have, and how much of it is trustworthy" answer that
    is the main reason this page exists."""
    summary = {}
    for source in SOURCES:
        subset = [i for i in items if i["source"] == source]
        dates = sorted({i["date"] for i in subset if i["date"]})
        summary[source] = {
            "count": len(subset),
            "start": dates[0] if dates else None,
            "end": dates[-1] if dates else None,
            "distinct_days": len(dates),
            "in_scoring": bool(subset) and subset[0]["in_scoring"],
            "not_atomic": sum(1 for i in subset if not i["decomposition_ok"]),
            "unclassified": sum(1 for i in subset if not i["classification_ok"]),
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

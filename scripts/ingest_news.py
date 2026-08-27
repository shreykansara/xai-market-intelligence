"""Real-world news ingestion: fetches world-level headlines from a small set of
free, no-key sources, deduplicates near-identical headlines via embedding
similarity, and infers PESTLE/Porter's relevance, polarity, and (for articles
that clear a relevance gate) geographic scope - all by looking up the
fabricated seed corpus, see src/marketintel/seed_inference.py. No per-source
scope tagging, no trained classifier.

Two safeguards on top of the original nearest-neighbor design, added after a
live run came back scope-distributed India=47/World=36/Punjab=25 - including
tagging an NFL brain-injury study and a Nigerian kidnapping story as "India":
  1. A relevance gate runs before scope classification. An article whose max
     relevance across all 11 dimensions falls below the 5th percentile of the
     fabricated seed corpus's own max-relevance distribution isn't
     meaningfully close to anything this system models - it's excluded
     entirely (no scope, not stored, not used downstream) and logged to
     data/ingestion_excluded.jsonl instead of silently dropped.
  2. Articles that pass the gate get scope from a per-class-best-match rule,
     not pooled top-k plurality voting: for each of the 7 scope classes, only
     that class's single closest seed article competes. This is what
     actually fixes the bias - pooled voting let India/Punjab win purely by
     having more seed articles nearby, regardless of how well any one of
     them matched.

Sources (all free, no API key, no paid tier):
  - BBC World RSS and Al Jazeera RSS - standard publisher feeds.
  - Google News RSS, queried by topic (WORLD), not scoped to any one outlet.
  - GDELT DOC 2.0 API via the open-source `gdeltdoc` package - NOT "GDELT
    Cloud" (gdeltcloud.com), which is a separate paid product requiring a key.
Reuters is not used: its public RSS was discontinued in 2020 and programmatic
access now requires a paid license.

Only title, publish timestamp, link, and the inferred tags are stored - no
article body text, and no vector database. This appends to the same flat
JSON + .npy embedding structure the fabricated dataset already uses, kept in
a separate pair of files (data/real_news.json / real_news_embeddings.npy) so
real headlines never mix into the fabricated startups' training data.

Designed to be re-run on a schedule (every 1-4 hours is plenty for global
wires): each run only fetches items newer than that source's last successful
fetch (data/ingestion_state.json), and is safe to re-run or have overlapping
windows, since the embedding-similarity dedup pass catches repeats regardless
of the incremental cursor.

Run: python scripts/ingest_news.py

Schedule examples:
  cron (Linux/Mac):       0 */2 * * *  cd /path/to/project && .venv/bin/python scripts/ingest_news.py
  Windows Task Scheduler: trigger "every 2 hours", action = .venv\\Scripts\\python.exe scripts\\ingest_news.py
"""
import calendar
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import numpy as np

# Global wires (especially GDELT) regularly include non-English headlines; Windows'
# default console codepage can't encode a lot of that, and this is meant to run
# unattended on a schedule, so a stray character shouldn't take the whole run down.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    DEDUP_SIMILARITY_THRESHOLD,
    DEDUP_WINDOW_HOURS,
    INGESTION_EXCLUDED_LOG_PATH,
    INGESTION_SAMPLE_LOG_PATH,
    INGESTION_STATE_PATH,
    PESTLE_DIMS,
    PORTERS_DIMS,
    REAL_NEWS_EMBEDDINGS_PATH,
    REAL_NEWS_PATH,
)
from marketintel.data_loader import load_news  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.seed_inference import (  # noqa: E402
    calibrate_relevance_threshold,
    group_indices_by_scope,
    infer_categorical,
    infer_relevance,
    infer_scope_best_match,
    nearest_neighbors,
)

USER_AGENT = "Mozilla/5.0 (compatible; MarketIntelBot/0.1)"
SAMPLE_LOG_SIZE = 8
GDELT_LOOKBACK_HOURS = 6  # first-run-only fallback window; later runs use the state cursor
GDELT_KEYWORD = "world"

RSS_FEEDS = {
    "bbc_world": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "google_news_world": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
}


def load_state() -> dict:
    if INGESTION_STATE_PATH.exists():
        with open(INGESTION_STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state: dict):
    with open(INGESTION_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def load_existing():
    if REAL_NEWS_PATH.exists() and REAL_NEWS_EMBEDDINGS_PATH.exists():
        with open(REAL_NEWS_PATH, encoding="utf-8") as f:
            records = json.load(f)
        embeddings = list(np.load(REAL_NEWS_EMBEDDINGS_PATH))
        return records, embeddings
    return [], []


def save_existing(records: list[dict], embeddings: list[np.ndarray]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REAL_NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    np.save(REAL_NEWS_EMBEDDINGS_PATH, np.array(embeddings))


def parse_published(entry) -> datetime:
    if entry.get("published_parsed"):
        return datetime.fromtimestamp(calendar.timegm(entry.published_parsed), tz=timezone.utc)
    return datetime.now(timezone.utc)


def fetch_rss(url: str, since: datetime | None) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    raw = urllib.request.urlopen(req, timeout=20).read()
    parsed = feedparser.parse(raw)

    items = []
    for entry in parsed.entries:
        published = parse_published(entry)
        if since is not None and published <= since:
            continue
        title = entry.get("title", "").strip()
        if not title:
            continue
        items.append({"title": title, "link": entry.get("link", ""), "published": published})
    return items


def parse_gdelt_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return datetime.now(timezone.utc)


def fetch_gdelt(since: datetime | None) -> list[dict]:
    """GDELT DOC 2.0 API (free, no key) via the open-source `gdeltdoc` package -
    not GDELT Cloud, which is a separate paid product."""
    from gdeltdoc import Filters, GdeltDoc

    now = datetime.now(timezone.utc)
    start = since or (now - timedelta(hours=GDELT_LOOKBACK_HOURS))
    filters = Filters(
        keyword=GDELT_KEYWORD,
        start_date=start.replace(tzinfo=None),
        end_date=now.replace(tzinfo=None),
        num_records=250,
    )
    df = GdeltDoc().article_search(filters)

    items = []
    for _, row in df.iterrows():
        title = str(row.get("title") or "").strip()
        if not title:
            continue
        published = parse_gdelt_date(row.get("seendate"))
        if since is not None and published <= since:
            continue
        items.append({"title": title, "link": str(row.get("url") or ""), "published": published})
    return items


def make_rss_fetcher(url: str):
    return lambda since: fetch_rss(url, since)


SOURCES = {
    "bbc_world": make_rss_fetcher(RSS_FEEDS["bbc_world"]),
    "aljazeera": make_rss_fetcher(RSS_FEEDS["aljazeera"]),
    "google_news_world": make_rss_fetcher(RSS_FEEDS["google_news_world"]),
    "gdelt_world": fetch_gdelt,
}


def find_duplicate(new_embedding: np.ndarray, records: list[dict], embeddings: list[np.ndarray], now: datetime):
    """Cosine similarity against every record published within the dedup window
    (embeddings are already L2-normalized, so dot product = cosine similarity)."""
    cutoff = now - timedelta(hours=DEDUP_WINDOW_HOURS)
    candidate_idx = [i for i, r in enumerate(records) if datetime.fromisoformat(r["published"]) >= cutoff]
    if not candidate_idx:
        return None, 0.0

    candidate_matrix = np.array([embeddings[i] for i in candidate_idx])
    sims = candidate_matrix @ new_embedding
    best_local = int(np.argmax(sims))
    best_sim = float(sims[best_local])
    if best_sim >= DEDUP_SIMILARITY_THRESHOLD:
        return candidate_idx[best_local], best_sim
    return None, best_sim


def main():
    seed_news, seed_embeddings = load_news()
    relevance_threshold = calibrate_relevance_threshold(seed_news)
    scope_indices = group_indices_by_scope(seed_news)
    print(f"Relevance gate threshold (5th percentile of seed corpus): {relevance_threshold:.4f}\n")

    state = load_state()
    records, embeddings = load_existing()
    next_id = len(records) + 1
    now = datetime.now(timezone.utc)

    new_count, dup_count, excluded_count = 0, 0, 0
    sample_log = []
    excluded_log = []

    for source_id, fetch in SOURCES.items():
        since_str = state.get(source_id, {}).get("last_published")
        since = datetime.fromisoformat(since_str) if since_str else None

        try:
            items = fetch(since)
        except Exception as exc:
            print(f"[{source_id}] fetch failed: {exc}")
            continue

        latest_published = since
        for item in items:
            embedding = embed_text(item["title"])
            dup_idx, sim = find_duplicate(embedding, records, embeddings, now)

            if dup_idx is not None:
                records[dup_idx]["mention_count"] += 1
                records[dup_idx]["last_seen"] = now.isoformat()
                dup_count += 1
                if latest_published is None or item["published"] > latest_published:
                    latest_published = item["published"]
                continue

            top_idx, weights = nearest_neighbors(embedding, seed_embeddings)
            relevance = infer_relevance(seed_news, top_idx, weights)
            max_relevance = max(relevance.values())

            if max_relevance < relevance_threshold:
                excluded_count += 1
                excluded_log.append({
                    "title": item["title"],
                    "published": item["published"].isoformat(),
                    "max_relevance": max_relevance,
                })
            else:
                polarity = infer_categorical(seed_news, top_idx, weights, "polarity")
                scope, _ = infer_scope_best_match(embedding, seed_embeddings, scope_indices)
                pestle_scores = {d: relevance[d] for d in PESTLE_DIMS}
                porters_scores = {d: relevance[d] for d in PORTERS_DIMS}

                records.append({
                    "id": f"real_{next_id:05d}",
                    "title": item["title"],
                    "link": item["link"],
                    "published": item["published"].isoformat(),
                    "source": source_id,
                    "scope": scope,
                    "pestle_scores": pestle_scores,
                    "porters_scores": porters_scores,
                    "polarity": polarity,
                    "mention_count": 1,
                    "first_seen": now.isoformat(),
                    "last_seen": now.isoformat(),
                })
                embeddings.append(embedding)
                next_id += 1
                new_count += 1

                if len(sample_log) < SAMPLE_LOG_SIZE:
                    sample_log.append({
                        "title": item["title"],
                        "relevance": relevance,
                        "polarity": polarity,
                        "scope": scope,
                    })

            if latest_published is None or item["published"] > latest_published:
                latest_published = item["published"]

        state[source_id] = {
            "last_published": (latest_published or now).isoformat(),
            "last_run": now.isoformat(),
        }
        print(f"[{source_id}] fetched {len(items)} item(s) newer than {since}")

    save_existing(records, embeddings)
    save_state(state)

    print(
        f"\n{new_count} new headline(s) stored, {dup_count} deduplicated into existing records, "
        f"{excluded_count} excluded by the relevance gate."
    )
    print(f"Total real_news records: {len(records)}\n")

    if excluded_log:
        with open(INGESTION_EXCLUDED_LOG_PATH, "a", encoding="utf-8") as log_file:
            for entry in excluded_log:
                log_file.write(json.dumps({"logged_at": now.isoformat(), **entry}) + "\n")
        print(f"({len(excluded_log)} excluded headline(s) appended to {INGESTION_EXCLUDED_LOG_PATH})\n")

    if sample_log:
        print("Sample for spot-checking (scope now uses per-class-best-match, not pooled voting):")
        with open(INGESTION_SAMPLE_LOG_PATH, "a", encoding="utf-8") as log_file:
            for entry in sample_log:
                top_dims = sorted(entry["relevance"].items(), key=lambda kv: -kv[1])[:2]
                top_str = ", ".join(f"{d}={v:.2f}" for d, v in top_dims)
                print(f"  [{entry['polarity']:>8} | {entry['scope']:>11}] {entry['title']}")
                print(f"             top relevance: {top_str}")
                log_file.write(json.dumps({"logged_at": now.isoformat(), **entry}) + "\n")
        print(f"\n(appended to {INGESTION_SAMPLE_LOG_PATH} for later review)")


if __name__ == "__main__":
    main()

"""Real-world news ingestion: fetches world-level headlines from a small set of
global RSS feeds, deduplicates near-identical headlines via embedding similarity,
and tags each with PESTLE/Porter's relevance (nearest sub-cluster centroid from
the existing fabricated-data clustering) and polarity (an existing pretrained
sentiment classifier) - no new classifier is trained here.

Only title, publish timestamp, link, and the derived tags are stored - no
article body text, and no vector database. This appends to the same flat
JSON + .npy embedding structure the fabricated dataset already uses, kept in
a separate pair of files (data/real_news.json / real_news_embeddings.npy) so
real headlines never mix into the fabricated startups' training data.

Designed to be re-run on a schedule (every 1-4 hours is plenty for global
wires): each run only fetches items newer than that feed's last successful
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from marketintel.config import (  # noqa: E402
    DATA_DIR,
    DEDUP_SIMILARITY_THRESHOLD,
    DEDUP_WINDOW_HOURS,
    INGESTION_SAMPLE_LOG_PATH,
    INGESTION_STATE_PATH,
    REAL_NEWS_EMBEDDINGS_PATH,
    REAL_NEWS_PATH,
)
from marketintel.data_loader import load_news, load_subclusters  # noqa: E402
from marketintel.embeddings import embed_text  # noqa: E402
from marketintel.relevance import compute_subcluster_centroids, relevance_from_centroids, split_relevance  # noqa: E402
from marketintel.sentiment import classify_polarity  # noqa: E402

USER_AGENT = "Mozilla/5.0 (compatible; MarketIntelBot/0.1)"
SAMPLE_LOG_SIZE = 8

# Reuters and AP both stopped offering direct public RSS feeds some years back;
# routing through Google News' per-site RSS search is the practical way to keep
# both wires in the mix without a paid syndication agreement. BBC and Al
# Jazeera still publish their own feeds directly, so those are used as-is.
FEEDS = {
    "bbc_world": {
        "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "scope": "World",
        "title_suffix": None,
    },
    "aljazeera": {
        "url": "https://www.aljazeera.com/xml/rss/all.xml",
        "scope": "World",
        "title_suffix": None,
    },
    "reuters_world": {
        "url": "https://news.google.com/rss/search?q=site:reuters.com+when:1d&hl=en-US&gl=US&ceid=US:en",
        "scope": "World",
        "title_suffix": " - Reuters",
    },
    "ap_world": {
        "url": "https://news.google.com/rss/search?q=site:apnews.com+when:1d&hl=en-US&gl=US&ceid=US:en",
        "scope": "World",
        "title_suffix": " - AP News",
    },
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


def clean_title(title: str, suffix: str | None) -> str:
    title = title.strip()
    if suffix and title.endswith(suffix):
        return title[: -len(suffix)].strip()
    return title


def parse_published(entry) -> datetime:
    if entry.get("published_parsed"):
        return datetime.fromtimestamp(calendar.timegm(entry.published_parsed), tz=timezone.utc)
    return datetime.now(timezone.utc)


def fetch_feed(config: dict, since: datetime | None) -> list[dict]:
    req = urllib.request.Request(config["url"], headers={"User-Agent": USER_AGENT})
    raw = urllib.request.urlopen(req, timeout=20).read()
    parsed = feedparser.parse(raw)

    items = []
    for entry in parsed.entries:
        published = parse_published(entry)
        if since is not None and published <= since:
            continue
        title = clean_title(entry.get("title", ""), config["title_suffix"])
        if not title:
            continue
        items.append({"title": title, "link": entry.get("link", ""), "published": published})
    return items


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
    fabricated_news, fabricated_embeddings = load_news()
    subclusters = load_subclusters()
    centroids = compute_subcluster_centroids(fabricated_news, fabricated_embeddings, subclusters)

    state = load_state()
    records, embeddings = load_existing()
    next_id = len(records) + 1
    now = datetime.now(timezone.utc)

    new_count, dup_count = 0, 0
    sample_log = []

    for feed_id, config in FEEDS.items():
        since_str = state.get(feed_id, {}).get("last_published")
        since = datetime.fromisoformat(since_str) if since_str else None

        try:
            items = fetch_feed(config, since)
        except Exception as exc:
            print(f"[{feed_id}] fetch failed: {exc}")
            continue

        latest_published = since
        for item in items:
            embedding = embed_text(item["title"])
            dup_idx, sim = find_duplicate(embedding, records, embeddings, now)

            if dup_idx is not None:
                records[dup_idx]["mention_count"] += 1
                records[dup_idx]["last_seen"] = now.isoformat()
                dup_count += 1
            else:
                relevance, nearest_cluster = relevance_from_centroids(embedding, centroids)
                pestle_scores, porters_scores = split_relevance(relevance)
                polarity = classify_polarity(item["title"])

                records.append({
                    "id": f"real_{next_id:05d}",
                    "title": item["title"],
                    "link": item["link"],
                    "published": item["published"].isoformat(),
                    "source": feed_id,
                    "scope": config["scope"],
                    "pestle_scores": pestle_scores,
                    "porters_scores": porters_scores,
                    "nearest_subcluster": nearest_cluster,
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
                    })

            if latest_published is None or item["published"] > latest_published:
                latest_published = item["published"]

        state[feed_id] = {
            "last_published": (latest_published or now).isoformat(),
            "last_run": now.isoformat(),
        }
        print(f"[{feed_id}] fetched {len(items)} item(s) newer than {since}")

    save_existing(records, embeddings)
    save_state(state)

    print(f"\n{new_count} new headline(s) stored, {dup_count} deduplicated into existing records.")
    print(f"Total real_news records: {len(records)}\n")

    if sample_log:
        print("Sample for spot-checking:")
        with open(INGESTION_SAMPLE_LOG_PATH, "a", encoding="utf-8") as log_file:
            for entry in sample_log:
                top_dims = sorted(entry["relevance"].items(), key=lambda kv: -kv[1])[:2]
                top_str = ", ".join(f"{d}={v:.2f}" for d, v in top_dims)
                print(f"  [{entry['polarity']:>8}] {entry['title']}")
                print(f"             top relevance: {top_str}")
                log_file.write(json.dumps({"logged_at": now.isoformat(), **entry}) + "\n")
        print(f"\n(appended to {INGESTION_SAMPLE_LOG_PATH} for later review)")


if __name__ == "__main__":
    main()

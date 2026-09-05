#!/usr/bin/env python3
"""
GDELT 2.0 News Downloader Script
--------------------------------
Fetches news articles from GDELT DOC 2.0 API between a given start and end date
(default: Jan 1, 2026 to Aug 31, 2026).

Features:
  - Overcomes 250-record response limit using timestamp-based pagination (startdatetime advancing).
  - Broad coverage query (default: 'sourcelang:eng' to ingest all English news items).
  - Memory-efficient deduplication based on article URL MD5 hashes.
  - Updates and saves output JSON file immediately after EVERY ingestion batch.
  - Graceful KeyboardInterrupt (Ctrl+C) handling preserving all downloaded data.
  - Stagnant loop protection automatically jumping forward when duplicate batches occur.
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("GDELTFetcher")

GDELT_DOC_API_URL = "https://api.gdeltproject.org/api/v2/doc/doc"


def parse_seendate_to_gdelt_format(seendate_str: str) -> str:
    """
    Converts GDELT seendate format (e.g., '20260101T123000Z' or '20260101123000')
    to standard YYYYMMDDHHMMSS string for API startdatetime parameter.
    """
    if not seendate_str:
        return ""
    clean_str = seendate_str.replace("T", "").replace("Z", "").replace("-", "").replace(":", "").strip()
    if len(clean_str) >= 14:
        return clean_str[:14]
    return clean_str


def get_url_hash(url: str) -> str:
    """Generate MD5 hash for a URL for fast in-memory deduplication."""
    return hashlib.md5(url.strip().lower().encode("utf-8")).hexdigest()


class GDELTFetcher:
    def __init__(
        self,
        query: str = "sourcelang:eng",
        start_date: str = "20260101000000",
        end_date: str = "20260831235959",
        output_file: str = "gdelt_news_20260101_20260831.json",
        request_delay: float = 3.0,
        max_retries: int = 5,
        max_articles: int = None,
    ):
        self.query = query
        self.current_start = parse_seendate_to_gdelt_format(start_date)
        self.end_date = parse_seendate_to_gdelt_format(end_date)
        self.output_file = Path(output_file)
        self.request_delay = request_delay
        self.max_retries = max_retries
        self.max_articles = max_articles

        self.articles = []
        self.seen_hashes = set()

        # Load existing output file if present to resume
        self._load_existing_checkpoint()

    def _load_existing_checkpoint(self):
        """Loads existing articles and seen hashes from output file if it exists."""
        if self.output_file.exists():
            try:
                logger.info(f"Existing file found at '{self.output_file}'. Loading checkpoint...")
                with open(self.output_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.articles = data
                    elif isinstance(data, dict) and "articles" in data:
                        self.articles = data.get("articles", [])

                for art in self.articles:
                    url = art.get("url")
                    if url:
                        self.seen_hashes.add(get_url_hash(url))

                logger.info(
                    f"Resumed checkpoint: {len(self.articles)} unique articles already loaded."
                )

                # Update current_start to the latest seendate if available
                if self.articles:
                    latest_date = None
                    for art in reversed(self.articles):
                        sdate = parse_seendate_to_gdelt_format(art.get("seendate", ""))
                        if sdate and len(sdate) == 14:
                            latest_date = sdate
                            break
                    if latest_date and latest_date > self.current_start:
                        self.current_start = latest_date
                        logger.info(f"Advancing start timestamp to last checkpoint date: {self.current_start}")
            except Exception as e:
                logger.warning(f"Failed to read existing checkpoint file: {e}. Starting fresh.")

    def save_to_json(self):
        """Saves ingested articles safely into output JSON file immediately."""
        temp_file = self.output_file.with_suffix(".json.tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.articles, f, ensure_ascii=False, indent=2)
            temp_file.replace(self.output_file)
            logger.info(f"Updated stored file: {len(self.articles)} total unique articles in '{self.output_file}'")
        except Exception as e:
            logger.error(f"Error saving output JSON: {e}")

    def fetch_batch(self, start_ts: str) -> dict:
        """
        Executes a single API request to GDELT DOC 2.0 API with exponential backoff on errors.
        """
        params = {
            "query": self.query,
            "mode": "artlist",
            "maxrecords": "250",
            "format": "json",
            "sort": "dateasc",
            "startdatetime": start_ts,
            "enddatetime": self.end_date,
        }

        query_str = urllib.parse.urlencode(params)
        request_url = f"{GDELT_DOC_API_URL}?{query_str}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            )
        }

        retry_count = 0
        backoff_delay = 5.0

        while retry_count <= self.max_retries:
            try:
                req = urllib.request.Request(request_url, headers=headers)
                with urllib.request.urlopen(req, timeout=30) as resp:
                    if resp.status == 200:
                        raw_data = resp.read().decode("utf-8")
                        if not raw_data.strip():
                            return {}
                        return json.loads(raw_data)
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504):
                    retry_count += 1
                    logger.warning(
                        f"HTTP {e.code} ({e.reason}) encountered. Retrying in {backoff_delay:.1f}s... "
                        f"(Attempt {retry_count}/{self.max_retries})"
                    )
                    time.sleep(backoff_delay)
                    backoff_delay *= 2.0  # Exponential backoff
                else:
                    logger.error(f"HTTP Error {e.code}: {e.reason}")
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                retry_count += 1
                logger.warning(
                    f"Network issue: {e}. Retrying in {backoff_delay:.1f}s... "
                    f"(Attempt {retry_count}/{self.max_retries})"
                )
                time.sleep(backoff_delay)
                backoff_delay *= 2.0
            except Exception as e:
                logger.error(f"Unexpected error fetching batch: {e}")
                break

        logger.error(f"Failed to fetch batch starting at {start_ts} after {self.max_retries} retries.")
        return {}

    def _advance_timestamp(self, ts_str: str, add_seconds: int = 1) -> str:
        """Helper to safely add seconds/hours to a YYYYMMDDHHMMSS timestamp string."""
        try:
            dt = datetime.strptime(ts_str, "%Y%m%d%H%M%S")
            new_dt = dt + timedelta(seconds=add_seconds)
            return new_dt.strftime("%Y%m%d%H%M%S")
        except Exception:
            return ts_str

    def run(self):
        """Main execution loop for timestamp pagination and ingestion."""
        logger.info(f"Starting GDELT ingestion...")
        logger.info(f"Query: '{self.query}'")
        logger.info(f"Date Range: {self.current_start} to {self.end_date}")
        logger.info(f"Output File: {self.output_file.resolve()}")

        batch_count = 0
        consecutive_zero_new = 0

        try:
            while True:
                if self.current_start >= self.end_date:
                    logger.info("Reached target end date. Ingestion complete!")
                    break

                if self.max_articles and len(self.articles) >= self.max_articles:
                    logger.info(f"Reached maximum requested articles limit ({self.max_articles}). Stopping.")
                    break

                logger.info(f"Fetching batch starting at timestamp: {self.current_start}...")
                data = self.fetch_batch(self.current_start)

                batch_articles = data.get("articles", []) if isinstance(data, dict) else []
                if not batch_articles:
                    logger.info("No more articles returned for this window or query.")
                    # If API returns empty, jump 1 hour forward to continue scanning
                    logger.info("Advancing window forward by 1 hour...")
                    self.current_start = self._advance_timestamp(self.current_start, 3600)
                    time.sleep(self.request_delay)
                    continue

                batch_count += 1
                new_articles_count = 0
                latest_timestamp_in_batch = self.current_start

                for art in batch_articles:
                    url = art.get("url")
                    if not url:
                        continue

                    url_hash = get_url_hash(url)
                    if url_hash not in self.seen_hashes:
                        self.seen_hashes.add(url_hash)
                        self.articles.append(art)
                        new_articles_count += 1

                    seendate_raw = art.get("seendate")
                    parsed_ts = parse_seendate_to_gdelt_format(seendate_raw)
                    if parsed_ts and len(parsed_ts) == 14 and parsed_ts > latest_timestamp_in_batch:
                        latest_timestamp_in_batch = parsed_ts

                logger.info(
                    f"Batch {batch_count}: Received {len(batch_articles)} articles, "
                    f"{new_articles_count} new unique added. Total collected: {len(self.articles)}"
                )

                # Update output file IMMEDIATELY after every ingestion batch
                self.save_to_json()

                # Handle loop stagnation / duplicate batches
                if new_articles_count == 0:
                    consecutive_zero_new += 1
                    logger.warning(
                        f"Batch yielded 0 new articles ({consecutive_zero_new} consecutive zero-new batch)."
                    )
                    if consecutive_zero_new >= 2:
                        # Force jump 1 hour forward to break stagnant duplicate loops
                        logger.warning("Stagnant loop detected. Force-advancing timestamp by 1 hour...")
                        self.current_start = self._advance_timestamp(self.current_start, 3600)
                        consecutive_zero_new = 0
                    else:
                        self.current_start = self._advance_timestamp(self.current_start, 1)
                else:
                    consecutive_zero_new = 0
                    if latest_timestamp_in_batch <= self.current_start:
                        self.current_start = self._advance_timestamp(self.current_start, 1)
                    else:
                        self.current_start = latest_timestamp_in_batch

                # Respect rate limit delay
                time.sleep(self.request_delay)

        except KeyboardInterrupt:
            logger.info("Execution interrupted by user (Ctrl+C). Saving all progress before exit...")
        except Exception as e:
            logger.error(f"Unexpected error during ingestion execution: {e}")
        finally:
            self.save_to_json()
            logger.info(f"Ingestion process finished. Final unique articles saved: {len(self.articles)}")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest all news items from GDELT 2.0 API between 1 Jan 2026 and 31 Aug 2026."
    )
    parser.add_argument(
        "--query",
        type=str,
        default="sourcelang:eng",
        help="GDELT search query (default: 'sourcelang:eng' to ingest all English news without restriction).",
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="20260101000000",
        help="Start datetime YYYYMMDDHHMMSS (default: 20260101000000).",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="20260831235959",
        help="End datetime YYYYMMDDHHMMSS (default: 20260831235959).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="gdelt_news_20260101_20260831.json",
        help="Output JSON filename (default: gdelt_news_20260101_20260831.json).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="Delay in seconds between requests to respect rate limits (default: 3.0).",
    )
    parser.add_argument(
        "--max-articles",
        type=int,
        default=None,
        help="Optional maximum number of total articles to ingest (default: unlimited).",
    )

    args = parser.parse_args()

    fetcher = GDELTFetcher(
        query=args.query,
        start_date=args.start_date,
        end_date=args.end_date,
        output_file=args.output,
        request_delay=args.delay,
        max_articles=args.max_articles,
    )
    fetcher.run()


if __name__ == "__main__":
    main()

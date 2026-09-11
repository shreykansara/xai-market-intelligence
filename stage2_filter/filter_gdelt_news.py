#!/usr/bin/env python3
"""
STAGE 2: GDELT Web Scraping & Irrelevant News Filtering Engine
----------------------------------------------------------------
Reads raw GDELT zipped or unzipped CSV files from Stage 1, fetches page headlines & body content,
and filters out irrelevant, noisy, duplicate, or non-business news stories.

Output: Clean filtered CSV (`filtered_news_YYYYMM.csv`) ready for Stage 3 11-D Projection.

Usage Examples:
  # Process a raw GDELT zip file:
  python filter_gdelt_news.py --input ../gdelt_data/20260101.export.CSV.zip --output filtered_news_20260101.csv

  # Process all files in a folder:
  python filter_gdelt_news.py --input-dir ../gdelt_data --output filtered_news_202608.csv --limit 2000
"""

import argparse
import csv
import hashlib
import html.parser
import json
import logging
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("Stage2Filter")

VALID_LOCATIONS = ["LPU", "Kapurthala", "Punjab", "India", "World"]

# Key relevance concept terms to keep business, policy, tech, legal, and economic news
RELEVANT_CONCEPT_KEYWORDS = {
    "tariff", "sanction", "government", "policy", "trade", "regulation", "subsidy",
    "inflation", "interest rate", "gdp", "recession", "bank", "currency", "spending",
    "stock", "market", "revenue", "price", "ipo", "profit", "quarterly", "investor",
    "ai", "tech", "software", "semiconductor", "chip", "cloud", "data center", "digital",
    "lawsuit", "court", "antitrust", "compliance", "litigation", "verdict", "legal",
    "climate", "carbon", "emissions", "esg", "energy", "renewable", "disaster",
    "company", "firm", "industry", "merger", "acquisition", "rivalry", "competitor", "business"
}


class SimpleHTMLParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta_desc = ""
        self.paragraphs = []
        self._in_title = False
        self._in_p = False
        self._current_p = []

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = True
        elif tag_lower == "p":
            self._in_p = True
            self._current_p = []
        elif tag_lower == "meta":
            attr_dict = {k.lower(): v for k, v in attrs if k and v}
            prop = attr_dict.get("property", "").lower()
            name = attr_dict.get("name", "").lower()
            content = attr_dict.get("content", "")
            if (prop == "og:title" or name == "title") and not self.title and content:
                self.title = content.strip()
            elif (prop == "og:description" or name == "description") and not self.meta_desc and content:
                self.meta_desc = content.strip()

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower == "title":
            self._in_title = False
        elif tag_lower == "p":
            self._in_p = False
            if self._current_p:
                p_text = "".join(self._current_p).strip()
                if len(p_text) > 30:
                    self.paragraphs.append(p_text)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_p:
            self._current_p.append(data)


def fetch_article_content(url: str, timeout: int = 6) -> dict:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }
    result = {"title": "", "text": "", "success": False}
    if not url or not url.startswith("http"):
        return result

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" in content_type or "xml" in content_type or not content_type:
                raw_bytes = resp.read(200000)
                html_text = raw_bytes.decode("utf-8", errors="ignore")
                parser = SimpleHTMLParser()
                parser.feed(html_text)

                title = parser.title.strip() if parser.title else ""
                body = " ".join(parser.paragraphs[:10]).strip()
                if not body and parser.meta_desc:
                    body = parser.meta_desc

                title = re.sub(r"\s+", " ", title)
                title = re.sub(r"\s*[-|]\s*[^|-]{2,30}$", "", title).strip()

                result["title"] = title
                result["text"] = body[:2000]
                result["success"] = bool(title or body)
    except Exception:
        pass
    return result


def is_relevant_news(headline: str, body: str) -> bool:
    """Filters out irrelevant news (e.g. clickbait, celebrity gossip, local scores)."""
    combined = f"{headline} {body}".lower()
    words = set(re.findall(r"\w+", combined))
    
    # Check if text contains at least one strategic market/business keyword
    match_count = sum(1 for kw in RELEVANT_CONCEPT_KEYWORDS if kw in words or kw in combined)
    return match_count >= 1


def deterministic_location(full_text: str) -> str:
    text_lower = full_text.lower()
    if any(k in text_lower for k in ["lpu", "lovely professional university"]):
        return "LPU"
    if "kapurthala" in text_lower:
        return "Kapurthala"
    if any(k in text_lower for k in ["punjab", "jalandhar", "phagwara"]):
        return "Punjab"
    if any(k in text_lower for k in ["india", "indian", "delhi", "mumbai", "modi"]):
        return "India"
    return "World"


def process_single_gdelt_row(row: list) -> dict:
    event_id = row[0] if len(row) > 0 else ""
    raw_date = row[1] if len(row) > 1 else ""
    actor1_name = row[6] if len(row) > 6 else ""
    actor2_name = row[16] if len(row) > 16 else ""
    action_geo = row[52] if len(row) > 52 else ""
    source_url = row[-1] if len(row) > 0 else ""

    formatted_date = ""
    if len(raw_date) == 8:
        formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"

    record_id = f"gdelt_{raw_date}_e{event_id}" if event_id else f"gdelt_{hashlib.md5(source_url.encode('utf-8')).hexdigest()[:12]}"

    scraped = fetch_article_content(source_url)
    headline = scraped.get("title", "")
    body_text = scraped.get("text", "")

    if not headline:
        domain = urllib.parse.urlparse(source_url).netloc.replace("www.", "")
        headline = f"News update from {domain}: {actor1_name} {action_geo}".strip()

    # Irrelevance Filter
    if not is_relevant_news(headline, body_text):
        return None  # Discard irrelevant news

    combined_context = f"{headline} {body_text} Actors: {actor1_name}, {actor2_name} Location: {action_geo}".strip()
    location_affected = deterministic_location(combined_context)

    return {
        "id": record_id,
        "date": formatted_date,
        "headline": headline,
        "text": body_text[:1500],
        "source_link": source_url,
        "location_affected": location_affected
    }


def read_gdelt_rows_from_file(file_path: Path) -> list:
    """Reads rows from raw .csv, .tsv, or .csv.zip files."""
    rows = []
    if file_path.suffix == ".zip":
        with zipfile.ZipFile(file_path, "r") as z:
            for name in z.namelist():
                if name.endswith(".CSV") or name.endswith(".tsv") or name.endswith(".csv"):
                    with z.open(name) as f:
                        lines = [line.decode("utf-8", errors="ignore") for line in f.readlines()]
                        reader = csv.reader(lines, delimiter="\t")
                        for r in reader:
                            if len(r) > 2:
                                rows.append(r)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.reader(f, delimiter="\t")
            for r in reader:
                if len(r) > 2:
                    rows.append(r)
    return rows


def main():
    parser = argparse.ArgumentParser(
        description="Stage 2: Filter irrelevant news from raw GDELT CSV exports."
    )
    parser.add_argument("--input", type=str, help="Input single GDELT CSV/ZIP file path.")
    parser.add_argument("--input-dir", type=str, help="Input directory containing raw GDELT zip files.")
    parser.add_argument("--output", type=str, default="filtered_news.csv", help="Output filtered CSV path.")
    parser.add_argument("--workers", type=int, default=8, help="Number of scraping threads.")
    parser.add_argument("--limit", type=int, default=None, help="Optional max records limit.")

    parser.add_argument("--purge-processed-inputs", action="store_true", help="Automatically delete Stage 1 raw zip/csv files after Stage 2 filtering succeeds.")

    args = parser.parse_args()
    output_path = Path(args.output).resolve()

    raw_files = []
    if args.input:
        raw_files.append(Path(args.input))
    elif args.input_dir:
        input_dir = Path(args.input_dir)
        raw_files = list(input_dir.glob("*.zip")) + list(input_dir.glob("*.CSV")) + list(input_dir.glob("*.csv"))

    if not raw_files:
        logger.error("No input files found! Pass --input or --input-dir.")
        sys.exit(1)

    logger.info(f"=== STAGE 2: IRRELEVANT NEWS FILTERING ===")
    logger.info(f"Input Files : {len(raw_files)} files")
    logger.info(f"Output CSV  : {output_path}")

    # Read raw rows
    all_rows = []
    for f in raw_files:
        all_rows.extend(read_gdelt_rows_from_file(f))

    logger.info(f"Loaded {len(all_rows)} total raw GDELT records across files.")

    seen_urls = set()
    unique_rows = []
    for r in all_rows:
        url = r[-1] if len(r) > 0 else ""
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_rows.append(r)

    if args.limit and args.limit > 0:
        unique_rows = unique_rows[:args.limit]

    logger.info(f"Filtered {len(unique_rows)} unique articles for web scraping & relevance filter...")

    filtered_records = []
    eliminated_count = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_single_gdelt_row, row): row for row in unique_rows}
        for future in as_completed(futures):
            res = future.result()
            if res:
                filtered_records.append(res)
            else:
                eliminated_count += 1

    # Save to clean filtered CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "headline", "text", "source_link", "location_affected"])
        for r in filtered_records:
            writer.writerow([r["id"], r["date"], r["headline"], r["text"], r["source_link"], r["location_affected"]])

    logger.info(
        f"SUCCESS: Stage 2 Complete! Retained {len(filtered_records)} clean news records in '{output_path}'. "
        f"Strictly eliminated {eliminated_count} irrelevant/off-topic news items."
    )

    # Auto-Purge Stage 1 raw files if requested
    if args.purge_processed_inputs:
        logger.info("Purging processed Stage 1 raw zip/csv files...")
        purged_count = 0
        for f in raw_files:
            try:
                if f.exists():
                    f.unlink()
                    purged_count += 1
            except Exception as e:
                logger.warning(f"Could not delete input file '{f}': {e}")
        logger.info(f"AUTO-PURGE COMPLETE: Deleted {purged_count} Stage 1 raw file(s). Space freed up!")


if __name__ == "__main__":
    main()

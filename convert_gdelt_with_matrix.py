#!/usr/bin/env python3
"""
GDELT to Enriched News Converter (Matrix Projection Edition)
------------------------------------------------------------
Converts raw GDELT TSV/CSV news files into enriched news CSV datasets using
the pre-trained Linear Projection Matrix model (W in R^{768x11}, b in R^{11}).

Features:
  - Instant 11-D Strategic Vector Inference via matrix multiplication: y = clip(x * W + b, 0.05, 0.95)
  - Full Chunking & Auto-Resume Support: Reads target CSV first, detects processed record IDs,
    skips completed rows, and appends new records. Safe to run in small chunks or stop at any time.
  - Multi-threaded Web Scraping & Context Embedding.

Usage Examples:
  # Convert next 500 records from gdelt_202608.csv:
  python convert_gdelt_with_matrix.py --input gdelt_data/gdelt_202608.csv --output enriched_news_202608.csv --limit 500

  # Convert entire file:
  python convert_gdelt_with_matrix.py --input gdelt_data/gdelt_202608.csv --output enriched_news_202608.csv
"""

import argparse
import csv
import hashlib
import html.parser
import json
import logging
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import numpy as np

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("GDELTMatrixConverter")

OLLAMA_BASE_URL = "http://localhost:11434"
VALID_LOCATIONS = ["LPU", "Kapurthala", "Punjab", "India", "World"]
DIM_NAMES = [
    "political", "economic", "social", "technological", "legal", "environmental",
    "threat_of_new_entrants", "bargaining_power_of_buyers",
    "bargaining_power_of_suppliers", "threat_of_substitutes", "competitive_rivalry"
]


class SimpleHTMLParser(html.parser.HTMLParser):
    """Basic HTML parser to extract page title, meta description, and paragraph text."""
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
    """Fetches article content and title from URL with fallback parsing."""
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
    except Exception as e:
        logger.debug(f"Fetch failed for {url}: {e}")

    return result


def compute_local_text_embedding(text: str, dim: int = 768) -> list:
    """Computes a deterministic 768-dim dense feature vector fallback."""
    if not text:
        return [0.0] * dim
    vec = [0.0] * dim
    words = re.findall(r"\w+", text.lower())
    if not words:
        return [0.0] * dim

    features = words + [f"{words[i]}_{words[i+1]}" for i in range(len(words)-1)]
    for feat in features:
        h = int(hashlib.md5(feat.encode("utf-8")).hexdigest(), 16)
        idx = h % dim
        val = 1.0 if (h & 1) else -1.0
        vec[idx] += val

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [round(v / norm, 6) for v in vec]
    return vec


def call_ollama_embedding(text: str, model: str = "nomic-embed-text", dim: int = 768) -> list:
    """Calls Ollama embeddings API endpoint with local fallback."""
    if model:
        url = f"{OLLAMA_BASE_URL}/api/embed"
        payload = {"model": model, "input": text[:2000]}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                res_json = json.loads(resp.read().decode("utf-8"))
                embeddings = res_json.get("embeddings", [])
                if embeddings and isinstance(embeddings[0], list):
                    return embeddings[0]
        except Exception:
            try:
                url_legacy = f"{OLLAMA_BASE_URL}/api/embeddings"
                payload_legacy = {"model": model, "prompt": text[:2000]}
                req_legacy = urllib.request.Request(
                    url_legacy,
                    data=json.dumps(payload_legacy).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req_legacy, timeout=15) as resp2:
                    res_json2 = json.loads(resp2.read().decode("utf-8"))
                    emb = res_json2.get("embedding", [])
                    if emb:
                        return emb
            except Exception:
                pass

    return compute_local_text_embedding(text, dim=dim)


def deterministic_fallback_location(full_text: str) -> str:
    """Rule-based location classifier."""
    text_lower = full_text.lower()
    if any(k in text_lower for k in ["lpu", "lovely professional university", "lovely professional"]):
        return "LPU"
    if "kapurthala" in text_lower:
        return "Kapurthala"
    if any(k in text_lower for k in ["punjab", "punjabi", "jalandhar", "phagwara", "in23"]):
        return "Punjab"
    if any(k in text_lower for k in ["india", "indian", "bharat", "delhi", "mumbai", "modi"]):
        return "India"
    return "World"


def predict_11d_strategic_vector(contextual_embedding: list, W: np.ndarray, b: np.ndarray) -> list:
    """
    Predicts 11-D PESTLE & Porter's 5 Forces scores using trained Matrix Projection:
      y = clip(x * W + b, 0.05, 0.95)
    """
    x = np.array(contextual_embedding, dtype=np.float32)
    # Ensure input matches model input dim
    if x.shape[0] != W.shape[0]:
        if x.shape[0] < W.shape[0]:
            x = np.pad(x, (0, W.shape[0] - x.shape[0]))
        else:
            x = x[:W.shape[0]]

    y_raw = np.dot(x, W) + b
    y_clipped = np.clip(y_raw, 0.05, 0.95)
    return [round(float(val), 4) for val in y_clipped]


def process_single_row(row: list, embed_model: str, W: np.ndarray, b: np.ndarray) -> dict:
    """Processes a single raw GDELT row into an enriched record dict using the matrix model."""
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

    # Step 1: Web Scraping
    scraped = fetch_article_content(source_url)
    scraped_title = scraped.get("title", "")
    scraped_text = scraped.get("text", "")

    geo_context = f"Actors: {actor1_name}, {actor2_name}. Location: {action_geo}."
    combined_content = f"{scraped_title} {scraped_text} {geo_context}".strip()

    headline = scraped_title
    if not headline:
        domain = urllib.parse.urlparse(source_url).netloc.replace("www.", "")
        headline = f"News update from {domain}: {actor1_name} {action_geo}".strip()

    location_affected = deterministic_fallback_location(combined_content)
    summary = scraped_text[:300] if scraped_text else f"Event involving {actor1_name} at {action_geo}."

    # Step 2: Contextual Embedding (768-D)
    contextual_text = f"Headline: {headline}\nLocation: {location_affected}\nSummary: {summary}\nContent: {combined_content[:1000]}"
    c_emb = call_ollama_embedding(contextual_text, model=embed_model, dim=W.shape[0])

    # Step 3: Matrix Projection Inference (11-D)
    s_emb = predict_11d_strategic_vector(c_emb, W, b)

    return {
        "id": record_id,
        "date": formatted_date,
        "headline": headline,
        "contextual_embedding": c_emb,
        "strategic_embedding": s_emb,
        "source_link": source_url,
        "location_affected": location_affected,
    }


def save_checkpoint(output_path: Path, all_records: list):
    """Saves output CSV atomically."""
    temp_path = output_path.with_suffix(".csv.tmp")
    with open(temp_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "date", "headline", "contextual_embedding",
            "strategic_embedding", "source_link", "location_affected"
        ])
        for r in all_records:
            writer.writerow([
                r["id"],
                r["date"],
                r["headline"],
                json.dumps(r["contextual_embedding"]),
                json.dumps(r["strategic_embedding"]),
                r["source_link"],
                r["location_affected"]
            ])
    temp_path.replace(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Convert raw GDELT CSV to Enriched News CSV using trained Matrix Model."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="gdelt_data/gdelt_202608.csv",
        help="Path to raw input GDELT CSV file (default: gdelt_data/gdelt_202608.csv).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="enriched_news_202608.csv",
        help="Path to target output enriched CSV file (default: enriched_news_202608.csv).",
    )
    parser.add_argument(
        "--matrix-weights",
        type=str,
        default="strategic_projection_matrix.npz",
        help="Path to trained matrix projection weights (.npz or .json).",
    )
    parser.add_argument(
        "--embed-model",
        type=str,
        default="nomic-embed-text",
        help="Embedding model for contextual 768-D vector (default: nomic-embed-text).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of new records to process in this run (e.g. 500 or 1000).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of concurrent worker threads for fetching headlines (default: 8).",
    )
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=50,
        help="Save CSV checkpoint every N records (default: 50).",
    )

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)
    matrix_path = Path(args.matrix_weights)

    if not input_path.exists():
        logger.error(f"Input file '{input_path}' does not exist.")
        sys.exit(1)

    # 1. Load Matrix Weights
    if not matrix_path.exists():
        logger.error(f"Matrix weights file '{matrix_path}' does not exist.")
        sys.exit(1)

    logger.info(f"Loading trained projection matrix from '{matrix_path}'...")
    if matrix_path.suffix == ".npz":
        data = np.load(matrix_path)
        W = data["W"].astype(np.float32)
        b = data["b"].astype(np.float32)
    else:
        with open(matrix_path, "r", encoding="utf-8") as f:
            m_json = json.load(f)
            W = np.array(m_json["weight_matrix"], dtype=np.float32)
            b = np.array(m_json["bias"], dtype=np.float32)

    logger.info(f"Loaded Projection Matrix W: {W.shape}, Bias b: {b.shape}")

    # 2. Check Existing Output Checkpoint & Resume
    existing_records = []
    seen_ids = set()

    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    rec_id = r.get("id")
                    if rec_id:
                        seen_ids.add(rec_id)
                        try:
                            c_emb = json.loads(r.get("contextual_embedding", "[]"))
                        except Exception:
                            c_emb = []
                        try:
                            s_emb = json.loads(r.get("strategic_embedding", "[]"))
                        except Exception:
                            s_emb = []

                        existing_records.append({
                            "id": rec_id,
                            "date": r.get("date", ""),
                            "headline": r.get("headline", ""),
                            "contextual_embedding": c_emb,
                            "strategic_embedding": s_emb,
                            "source_link": r.get("source_link", ""),
                            "location_affected": r.get("location_affected", ""),
                        })
            logger.info(f"Loaded existing checkpoint: {len(existing_records)} records already in '{output_path}'")
        except Exception as e:
            logger.warning(f"Could not read existing checkpoint file: {e}")

    # 3. Read Input GDELT file and filter un-processed rows
    rows_to_process = []
    total_input = 0
    with open(input_path, "r", encoding="utf-8") as f:
        delimiter = "\t" if input_path.suffix in [".tsv", ".csv"] else ","
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            if not row or len(row) < 2:
                continue
            total_input += 1
            event_id = row[0]
            raw_date = row[1]
            source_url = row[-1] if len(row) > 0 else ""
            record_id = f"gdelt_{raw_date}_e{event_id}" if event_id else f"gdelt_{hashlib.md5(source_url.encode('utf-8')).hexdigest()[:12]}"

            if record_id not in seen_ids:
                rows_to_process.append(row)

    already_done = len(seen_ids)
    logger.info(f"Resume Status: {already_done}/{total_input} items already processed in '{output_path}'.")

    if not rows_to_process:
        logger.info(f"All {total_input} records in '{input_path}' are already enriched. Nothing to do!")
        sys.exit(0)

    if args.limit and args.limit > 0:
        rows_to_process = rows_to_process[:args.limit]
        logger.info(f"Processing next chunk of {len(rows_to_process)} records (Limit: {args.limit})...")
    else:
        logger.info(f"Processing all remaining {len(rows_to_process)} records...")

    # 4. Multithreaded Processing
    processed_count = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_row = {
            executor.submit(process_single_row, row, args.embed_model, W, b): row
            for row in rows_to_process
        }

        for future in as_completed(future_to_row):
            try:
                rec = future.result()
                existing_records.append(rec)
                seen_ids.add(rec["id"])
                processed_count += 1

                if processed_count % args.checkpoint_every == 0 or processed_count == len(rows_to_process):
                    save_checkpoint(output_path, existing_records)
                    elapsed = time.time() - start_time
                    rate = processed_count / max(0.001, elapsed)
                    logger.info(
                        f"Checkpoint Saved: {len(existing_records)} total records in '{output_path}' "
                        f"({processed_count}/{len(rows_to_process)} in this batch, {rate:.1f} rec/sec)"
                    )
            except Exception as e:
                logger.error(f"Error processing row: {e}")

    save_checkpoint(output_path, existing_records)
    logger.info(f"SUCCESS: Conversion completed! Enriched CSV stored at '{output_path}' with {len(existing_records)} total records.")


if __name__ == "__main__":
    main()

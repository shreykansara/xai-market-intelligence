#!/usr/bin/env python3
"""
GDELT Local Ollama News Enrichment & Embedding Script
------------------------------------------------------
Enriches filtered GDELT CSV records into a standard target format with an 11-dimensional strategic embedding vector:
  1. id
  2. date (YYYY-MM-DD)
  3. headline
  4. embedding (11-dimensional float vector representing PESTLE + Porter's 5 Forces)
     - Dim 0: Political (PESTLE)
     - Dim 1: Economic (PESTLE)
     - Dim 2: Social (PESTLE)
     - Dim 3: Technological (PESTLE)
     - Dim 4: Legal (PESTLE)
     - Dim 5: Environmental (PESTLE)
     - Dim 6: Threat of New Entrants (Porter)
     - Dim 7: Bargaining Power of Buyers (Porter)
     - Dim 8: Bargaining Power of Suppliers (Porter)
     - Dim 9: Threat of Substitutes (Porter)
     - Dim 10: Competitive Rivalry (Porter)
  5. source_link
  6. location_affected (strictly one of: "LPU", "Kapurthala", "Punjab", "India", "World")

Uses local Ollama LLM endpoints for structured extraction, classification, and 11-D strategic scoring.
Zero external pip dependencies (uses Python standard library).
"""

import argparse
import csv
import hashlib
import html.parser
import json
import logging
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("OllamaEnricher")

OLLAMA_BASE_URL = "http://localhost:11434"
VALID_LOCATIONS = ["LPU", "Kapurthala", "Punjab", "India", "World"]


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


def fetch_article_content(url: str, timeout: int = 8) -> dict:
    """
    Fetches article content and title from URL with fallback parsing.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }
    result = {
        "title": "",
        "text": "",
        "success": False
    }

    if not url or not url.startswith("http"):
        return result

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" in content_type or "xml" in content_type or not content_type:
                raw_bytes = resp.read(200000)  # Read up to ~200KB
                html_text = raw_bytes.decode("utf-8", errors="ignore")
                
                parser = SimpleHTMLParser()
                parser.feed(html_text)

                title = parser.title.strip() if parser.title else ""
                body = " ".join(parser.paragraphs[:10]).strip()
                if not body and parser.meta_desc:
                    body = parser.meta_desc

                # Clean title
                title = re.sub(r"\s+", " ", title)
                title = re.sub(r"\s*[-|]\s*[^|-]{2,30}$", "", title).strip()

                result["title"] = title
                result["text"] = body[:2000]
                result["success"] = bool(title or body)
    except Exception as e:
        logger.debug(f"Fetch failed for {url}: {e}")

    return result


def call_ollama_generate(prompt: str, model: str = "llama3.2") -> str:
    """Calls Ollama generate API endpoint."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_predict": 500}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("response", "").strip()
    except Exception as e:
        logger.warning(f"Ollama generate request failed: {e}")
        return ""


def deterministic_fallback_location(full_text: str) -> str:
    """Rule-based fallback for strict location classification."""
    text_lower = full_text.lower()
    
    # 1. LPU
    if any(k in text_lower for k in ["lpu", "lovely professional university", "lovely professional"]):
        return "LPU"
    # 2. Kapurthala
    if "kapurthala" in text_lower:
        return "Kapurthala"
    # 3. Punjab
    if any(k in text_lower for k in ["punjab", "punjabi", "jalandhar", "phagwara", "in23"]):
        return "Punjab"
    # 4. India
    if any(k in text_lower for k in ["india", "indian", "bharat", "delhi", "mumbai", "modi"]):
        return "India"
    # 5. World
    return "World"


def compute_fallback_pestle_and_porter(text: str) -> tuple:
    """
    Computes heuristic baseline PESTLE and Porter's 5 Forces scores (0.0 to 1.0)
    based on keyword density and domain indicators.
    """
    t = text.lower()
    
    pestle_keywords = {
        "political": ["government", "policy", "election", "minister", "tariff", "law", "sanction", "parliament", "tax", "state", "diplomatic"],
        "economic": ["market", "economy", "price", "inflation", "bank", "export", "trade", "growth", "investment", "finance", "dollar", "stock"],
        "social": ["people", "student", "education", "health", "society", "culture", "population", "community", "public", "job", "employment"],
        "technological": ["technology", "ai", "software", "digital", "research", "innovation", "automation", "tech", "cyber", "data"],
        "legal": ["court", "legal", "rights", "compliance", "regulation", "lawsuit", "justice", "verdict", "patent", "clause"],
        "environmental": ["climate", "environment", "pollution", "green", "solar", "energy", "carbon", "weather", "emission", "waste"]
    }
    
    pestle_scores = {}
    for factor, kws in pestle_keywords.items():
        hits = sum(1 for kw in kws if kw in t)
        score = min(1.0, round(hits * 0.25, 2))
        pestle_scores[factor] = score

    porter_keywords = {
        "threat_of_new_entrants": ["startup", "new entrant", "barrier", "expansion", "launch", "license", "market access"],
        "bargaining_power_of_buyers": ["customer", "buyer", "consumer", "demand", "price sensitivity", "choice", "discount"],
        "bargaining_power_of_suppliers": ["supplier", "supply chain", "raw material", "semiconductor", "chip", "cost", "vendor"],
        "threat_of_substitutes": ["substitute", "alternative", "replacement", "disrupt", "competing solution"],
        "competitive_rivalry": ["competitor", "rival", "market share", "competition", "race", "industry leader", "contest"]
    }
    
    porter_scores = {}
    for force, kws in porter_keywords.items():
        hits = sum(1 for kw in kws if kw in t)
        score = min(1.0, round(hits * 0.30, 2))
        porter_scores[force] = score
        
    return pestle_scores, porter_scores


def process_record(row: list, llm_model: str) -> dict:
    """Processes a single GDELT CSV record into enriched target schema with 11-D embedding vector."""
    event_id = row[0] if len(row) > 0 else ""
    raw_date = row[1] if len(row) > 1 else ""
    actor1_name = row[6] if len(row) > 6 else ""
    actor2_name = row[16] if len(row) > 16 else ""
    action_geo = row[52] if len(row) > 52 else ""
    source_url = row[-1] if len(row) > 0 else ""

    # Format date YYYY-MM-DD
    formatted_date = ""
    if len(raw_date) == 8:
        formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"

    # Generate unique ID
    record_id = f"gdelt_{raw_date}_e{event_id}" if event_id else f"gdelt_{hashlib.md5(source_url.encode('utf-8')).hexdigest()[:12]}"

    # Step 1: Fetch article content
    scraped = fetch_article_content(source_url)
    scraped_title = scraped.get("title", "")
    scraped_text = scraped.get("text", "")

    # Construct context
    geo_context = f"Actors: {actor1_name}, {actor2_name}. Location: {action_geo}."
    combined_content = f"{scraped_title} {scraped_text} {geo_context}".strip()

    # Default headline fallback if scraping fails
    headline = scraped_title
    if not headline:
        domain = urllib.parse.urlparse(source_url).netloc.replace("www.", "")
        headline = f"News update from {domain}: {actor1_name} {action_geo}".strip()

    # Step 2: Fallback Location, PESTLE, and Porter analysis
    location_affected = deterministic_fallback_location(combined_content)
    summary = scraped_text[:300] if scraped_text else f"Event involving {actor1_name} at {action_geo}."
    fallback_pestle, fallback_porter = compute_fallback_pestle_and_porter(combined_content)

    pestle_analysis = fallback_pestle
    porter_analysis = fallback_porter

    if llm_model:
        prompt = f"""You are an expert strategic business intelligence AI. Analyze this news item:

Headline: {headline}
URL: {source_url}
Context: {combined_content[:1500]}

Tasks:
1. Refine the headline.
2. Provide a 2-sentence summary.
3. Classify location_affected strictly as ONE of: "LPU", "Kapurthala", "Punjab", "India", "World".
4. Score PESTLE impact (0.0 to 1.0) for: political, economic, social, technological, legal, environmental.
5. Score Porter's Five Forces impact (0.0 to 1.0) for: threat_of_new_entrants, bargaining_power_of_buyers, bargaining_power_of_suppliers, threat_of_substitutes, competitive_rivalry.

Respond ONLY with valid JSON in this exact structure:
{{
  "headline": "...",
  "summary": "...",
  "location_affected": "LPU" | "Kapurthala" | "Punjab" | "India" | "World",
  "pestle_analysis": {{
    "political": 0.0,
    "economic": 0.0,
    "social": 0.0,
    "technological": 0.0,
    "legal": 0.0,
    "environmental": 0.0
  }},
  "porter_analysis": {{
    "threat_of_new_entrants": 0.0,
    "bargaining_power_of_buyers": 0.0,
    "bargaining_power_of_suppliers": 0.0,
    "threat_of_substitutes": 0.0,
    "competitive_rivalry": 0.0
  }}
}}"""
        llm_response = call_ollama_generate(prompt, model=llm_model)
        if llm_response:
            try:
                json_match = re.search(r"\{.*\}", llm_response, re.DOTALL)
                if json_match:
                    res_json = json.loads(json_match.group(0))
                    if res_json.get("headline"):
                        headline = res_json["headline"]
                    if res_json.get("summary"):
                        summary = res_json["summary"]
                    loc = res_json.get("location_affected", "").strip()
                    if loc in VALID_LOCATIONS:
                        location_affected = loc
                    if isinstance(res_json.get("pestle_analysis"), dict):
                        pestle_analysis.update(res_json["pestle_analysis"])
                    if isinstance(res_json.get("porter_analysis"), dict):
                        porter_analysis.update(res_json["porter_analysis"])
            except Exception:
                pass

    # Step 3: Construct Single 11-Dimensional Strategic Embedding Vector
    # Vector layout: [Political, Economic, Social, Technological, Legal, Environmental,
    #                 Threat_New_Entrants, Power_Buyers, Power_Suppliers, Threat_Substitutes, Competitive_Rivalry]
    strategic_11d_embedding = [
        float(pestle_analysis.get("political", 0.0)),
        float(pestle_analysis.get("economic", 0.0)),
        float(pestle_analysis.get("social", 0.0)),
        float(pestle_analysis.get("technological", 0.0)),
        float(pestle_analysis.get("legal", 0.0)),
        float(pestle_analysis.get("environmental", 0.0)),
        float(porter_analysis.get("threat_of_new_entrants", 0.0)),
        float(porter_analysis.get("bargaining_power_of_buyers", 0.0)),
        float(porter_analysis.get("bargaining_power_of_suppliers", 0.0)),
        float(porter_analysis.get("threat_of_substitutes", 0.0)),
        float(porter_analysis.get("competitive_rivalry", 0.0)),
    ]

    return {
        "id": record_id,
        "date": formatted_date,
        "headline": headline,
        "embedding": strategic_11d_embedding,
        "source_link": source_url,
        "location_affected": location_affected,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Enrich GDELT CSV news records using local Ollama LLM into standard format with 11-D strategic embedding vector."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="gdelt_data/gdelt_202601.csv",
        help="Input filtered GDELT CSV file path.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="enriched_news_202601.json",
        help="Output JSON file path.",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default="llama3.2",
        help="Ollama model for structured classification (default: llama3.2). Pass '' to skip LLM.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of concurrent worker threads for scraping/Ollama calls (default: 4).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on total records to process (default: unlimited).",
    )

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.exists():
        logger.error(f"Input CSV file '{input_path}' does not exist.")
        sys.exit(1)

    output_path = Path(args.output)
    enriched_records = []
    seen_ids = set()

    # Load existing output checkpoint if available
    if output_path.exists():
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    enriched_records = data
                    seen_ids = {r["id"] for r in enriched_records if "id" in r}
            logger.info(f"Loaded existing checkpoint: {len(enriched_records)} records from '{output_path}'")
        except Exception:
            pass

    # Read input CSV
    rows_to_process = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if not row or len(row) < 2:
                continue
            event_id = row[0]
            raw_date = row[1]
            source_url = row[-1] if len(row) > 0 else ""
            record_id = f"gdelt_{raw_date}_e{event_id}" if event_id else f"gdelt_{hashlib.md5(source_url.encode('utf-8')).hexdigest()[:12]}"
            
            if record_id not in seen_ids:
                rows_to_process.append(row)

    if args.limit:
        rows_to_process = rows_to_process[:args.limit]

    logger.info(f"Starting news enrichment for {len(rows_to_process)} records using Ollama...")
    logger.info(f"LLM Model: '{args.llm_model}' | Workers: {args.workers}")

    processed_count = 0

    def save_checkpoint():
        temp_file = output_path.with_suffix(".json.tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(enriched_records, f, ensure_ascii=False, indent=2)
        temp_file.replace(output_path)
        logger.info(f"Updated output checkpoint: {len(enriched_records)} records in '{output_path}'")

    try:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_row = {
                executor.submit(process_record, row, args.llm_model): row
                for row in rows_to_process
            }

            for future in as_completed(future_to_row):
                processed_count += 1
                try:
                    result = future.result()
                    if result and result.get("id"):
                        enriched_records.append(result)
                        seen_ids.add(result["id"])

                    if processed_count % 10 == 0:
                        logger.info(f"Progress: {processed_count}/{len(rows_to_process)} records processed.")
                        save_checkpoint()
                except Exception as e:
                    logger.warning(f"Error processing record: {e}")

    except KeyboardInterrupt:
        logger.info("Enrichment interrupted by user (Ctrl+C). Saving progress before exit...")
    finally:
        save_checkpoint()
        logger.info(f"Enrichment completed! Total enriched news records saved: {len(enriched_records)}")


if __name__ == "__main__":
    main()

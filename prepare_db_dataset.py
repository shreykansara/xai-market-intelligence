#!/usr/bin/env python3
"""
Database Dataset Preparation Script
------------------------------------
Processes raw enriched CSV files (enriched_news_202607.csv & enriched_news_202608.csv),
strips heavy 768-D text embeddings, computes 11-D strategic impact scores, and exports
lightweight, SQL-ready CSV files ready for PostgreSQL / pgvector deployment.

Input files : ~1.4 GB (with 768-D text embeddings)
Output files: ~60-80 MB (with ONLY 11-D vectors + metadata)

Usage:
  python prepare_db_dataset.py --input enriched_news_202607.csv --output stage3_enrich_and_store/db_ready_news_202607.csv
  python prepare_db_dataset.py --input enriched_news_202608.csv --output stage3_enrich_and_store/db_ready_news_202608.csv
"""

import argparse
import csv
import json
import logging
import os
import sys
from pathlib import Path
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("DBDatasetPreparer")


def compute_strategic_impact_score(s_11d: list) -> float:
    """Computes Strategic Impact Score (0.00 to 1.00) from 11-D vector."""
    if not s_11d or len(s_11d) < 11:
        return 0.05
    s_arr = np.array(s_11d, dtype=np.float32)
    sorted_s = np.sort(s_arr)[::-1]
    peak = float(sorted_s[0])
    top2_mean = float(np.mean(sorted_s[:2]))
    active_count = float(np.sum(s_arr > 0.20))
    impact = (peak * 0.60) + (top2_mean * 0.30) + min(0.10, active_count * 0.02)
    return round(float(impact), 4)


def process_csv_file(input_path: Path, output_path: Path, min_impact_threshold: float = 0.20):
    if not input_path.exists():
        logger.error(f"Input CSV file '{input_path}' does not exist.")
        sys.exit(1)

    logger.info(f"Processing '{input_path.name}' (File size: {input_path.stat().st_size / (1024*1024):.2f} MB)...")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    retained_records = []
    skipped_low_impact = 0
    total_processed = 0

    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            total_processed += 1
            if total_processed % 10000 == 0:
                logger.info(f"Loaded {total_processed} rows from '{input_path.name}'...")

            s_emb = []
            try:
                s_emb = json.loads(row.get("strategic_embedding", "[]"))
            except Exception:
                pass

            if not s_emb or len(s_emb) != 11:
                skipped_low_impact += 1
                continue

            impact_score = compute_strategic_impact_score(s_emb)
            if impact_score < min_impact_threshold:
                skipped_low_impact += 1
                continue

            # Format vector as PostgreSQL vector string e.g. "[0.1,0.2,...]"
            vector_str = f"[{','.join(f'{v:.4f}' for v in s_emb)}]"

            retained_records.append([
                row.get("id"),
                row.get("date"),
                row.get("headline", "").strip(),
                vector_str,
                row.get("source_link", "").strip(),
                row.get("location_affected", "World").strip(),
                impact_score
            ])

    # Save to SQL-ready CSV file
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "date", "headline", "strategic_embedding_11d", "source_link", "location_affected", "impact_score"
        ])
        writer.writerows(retained_records)

    out_size_mb = output_path.stat().st_size / (1024 * 1024)
    logger.info(
        f"SUCCESS: Saved {len(retained_records)} DB-ready records to '{output_path.name}' ({out_size_mb:.2f} MB). "
        f"Strictly eliminated {skipped_low_impact} low-impact noise items."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Prepare enriched news CSVs for PostgreSQL pgvector deployment by stripping 768-D vectors."
    )
    parser.add_argument("--input", type=str, required=True, help="Input raw enriched CSV file path.")
    parser.add_argument("--output", type=str, required=True, help="Output DB-ready CSV file path.")
    parser.add_argument(
        "--min-impact", type=float, default=0.20, help="Minimum strategic impact threshold (default: 0.20)."
    )

    args = parser.parse_args()
    process_csv_file(Path(args.input), Path(args.output), min_impact_threshold=args.min_impact)


if __name__ == "__main__":
    main()

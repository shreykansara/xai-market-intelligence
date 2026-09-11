#!/usr/bin/env python3
"""
STAGE 3: 11-D Strategic Vector Projection & DB Export Engine
--------------------------------------------------------------
Takes filtered news records from Stage 2, computes the 768-D contextual text embedding,
applies the trained Linear Projection Matrix model (W in R^{768x11}, b in R^{11}) to generate
the 11-D PESTLE & Porter's 5 Forces scores, DISCARDS the heavy 768-D text embedding vector,
and saves ONLY the lightweight 11-D strategic vector + metadata ready for DB upload!

Output schema:
  1. id
  2. date
  3. headline
  4. strategic_embedding (11-dimensional vector: [Political, Economic, Social, Tech, Legal, Env, Entrants, Buyers, Suppliers, Substitutes, Rivalry])
  5. source_link
  6. location_affected
  7. impact_score

Usage Examples:
  python enrich_and_store.py --input ../stage2_filter/filtered_news_202608.csv --output enriched_11d_news_202608.csv
"""

import argparse
import csv
import hashlib
import json
import logging
import math
import re
import sys
import urllib.request
from pathlib import Path
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("Stage3EnrichStore")

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_WEIGHTS_PATH = Path(__file__).parent / "projection_matrix" / "strategic_projection_matrix.npz"
FALLBACK_WEIGHTS_PATH = Path(__file__).parent.parent / "strategic_projection_matrix.npz"


def compute_local_text_embedding(text: str, dim: int = 768) -> list:
    """Deterministic 768-dim text feature vector fallback."""
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
            pass

    return compute_local_text_embedding(text, dim=dim)


def project_11d_vector(c_emb: list, W: np.ndarray, b: np.ndarray) -> list:
    """
    Applies trained Matrix Projection to generate 11-D Strategic Vector:
    y = clip(x * W + b, 0.05, 0.95)
    """
    x = np.array(c_emb, dtype=np.float32)
    if x.shape[0] != W.shape[0]:
        if x.shape[0] < W.shape[0]:
            x = np.pad(x, (0, W.shape[0] - x.shape[0]))
        else:
            x = x[:W.shape[0]]

    y_raw = np.dot(x, W) + b
    y_clipped = np.clip(y_raw, 0.05, 0.95)
    return [round(float(val), 4) for val in y_clipped]


def compute_impact_score(s_11d: list) -> float:
    """Computes Strategic Impact Score from 11-D vector."""
    if not s_11d or len(s_11d) < 11:
        return 0.05
    peak = max(s_11d)
    top2_mean = sum(sorted(s_11d, reverse=True)[:2]) / 2.0
    return round(float((peak * 0.60) + (top2_mean * 0.40)), 3)


def load_matrix_weights(weights_path: Path) -> tuple:
    """Loads weight matrix W (768, 11) and bias b (11)."""
    if not weights_path.exists():
        if FALLBACK_WEIGHTS_PATH.exists():
            weights_path = FALLBACK_WEIGHTS_PATH
        else:
            logger.error(f"Matrix weights file '{weights_path}' does not exist.")
            sys.exit(1)

    logger.info(f"Loading projection matrix weights from '{weights_path}'...")
    if weights_path.suffix == ".npz":
        data = np.load(weights_path)
        W = data["W"].astype(np.float32)
        b = data["b"].astype(np.float32)
    else:
        with open(weights_path, "r", encoding="utf-8") as f:
            m_json = json.load(f)
            W = np.array(m_json["weight_matrix"], dtype=np.float32)
            b = np.array(m_json["bias"], dtype=np.float32)

    logger.info(f"Loaded Weight Matrix W: {W.shape}, Bias b: {b.shape}")
    return W, b


def main():
    parser = argparse.ArgumentParser(
        description="Stage 3: Project news into 11-D strategic vectors, discard heavy embeddings, and save for DB."
    )
    parser.add_argument(
        "--input",
        type=str,
        default="../stage2_filter/filtered_news_202608.csv",
        help="Input filtered news CSV path from Stage 2.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="enriched_11d_news_202608.csv",
        help="Output CSV path containing ONLY 11-D vectors + metadata.",
    )
    parser.add_argument(
        "--weights",
        type=str,
        default=str(DEFAULT_WEIGHTS_PATH),
        help="Path to strategic projection matrix weights (.npz or .json).",
    )
    parser.add_argument(
        "--embed-model",
        type=str,
        default="nomic-embed-text",
        help="Ollama embedding model (default: nomic-embed-text).",
    )
    parser.add_argument(
        "--min-impact",
        type=float,
        default=0.25,
        help="Minimum strategic impact threshold to retain in final DB export (default: 0.25).",
    )

    args = parser.parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    weights_path = Path(args.weights)

    if not input_path.exists():
        logger.error(f"Input file '{input_path}' does not exist.")
        sys.exit(1)

    W, b = load_matrix_weights(weights_path)

    logger.info(f"=== STAGE 3: 11-D STRATEGIC PROJECTION & DB EXPORT ===")
    logger.info(f"Input File : {input_path}")
    logger.info(f"Output File: {output_path}")

    records_to_process = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            records_to_process.append(r)

    logger.info(f"Loaded {len(records_to_process)} filtered records from Stage 2.")

    enriched_11d_records = []
    discarded_low_impact = 0

    for idx, r in enumerate(records_to_process):
        headline = r.get("headline", "")
        text_body = r.get("text", "")
        loc = r.get("location_affected", "World")
        combined_text = f"Headline: {headline}\nLocation: {loc}\nBody: {text_body[:1000]}"

        # Step 1: Intermediate 768-D Contextual Embedding
        c_emb_768d = call_ollama_embedding(combined_text, model=args.embed_model, dim=W.shape[0])

        # Step 2: 11-D Strategic Projection Matrix Multiplication
        s_emb_11d = project_11d_vector(c_emb_768d, W, b)

        # Step 3: Compute Impact Score & Filter
        impact = compute_impact_score(s_emb_11d)
        if impact < args.min_impact:
            discarded_low_impact += 1
            continue

        # Step 4: DISCARD heavy 768-D embedding! Retain ONLY 11-D strategic vector + metadata
        enriched_11d_records.append({
            "id": r.get("id"),
            "date": r.get("date"),
            "headline": headline,
            "strategic_embedding": s_emb_11d,  # ONLY 11-D Vector stored
            "source_link": r.get("source_link"),
            "location_affected": loc,
            "impact_score": impact
        })

        if (idx + 1) % 500 == 0 or (idx + 1) == len(records_to_process):
            logger.info(f"Processed {idx + 1}/{len(records_to_process)} news items...")

    # Save final clean 11-D dataset
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "date", "headline", "strategic_embedding", "source_link", "location_affected", "impact_score"
        ])
        for rec in enriched_11d_records:
            writer.writerow([
                rec["id"],
                rec["date"],
                rec["headline"],
                json.dumps(rec["strategic_embedding"]),  # 11-D Vector JSON
                rec["source_link"],
                rec["location_affected"],
                rec["impact_score"]
            ])

    logger.info(
        f"SUCCESS: Stage 3 Complete! Saved {len(enriched_11d_records)} clean 11-D enriched records in '{output_path}'. "
        f"768-D embeddings discarded. Eliminated {discarded_low_impact} low-impact stories below threshold ({args.min_impact})."
    )


if __name__ == "__main__":
    main()

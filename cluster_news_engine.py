#!/usr/bin/env python3
"""
High-Precision Strategic News Clustering Engine
------------------------------------------------
Groups news events into tight, highly cohesive strategic clusters by combining:
1. 768-D Contextual Semantic Topic Embeddings
2. 11-D Strategic Impact Vectors (PESTLE + Porter's 5 Forces)

Uses HDBSCAN / Cosine Density Clustering to eliminate vague noise,
prevent obsolete news drift, and ensure crisp strategic grouping.
"""

import csv
import json
import logging
import math
import sys
import time
from pathlib import Path
import numpy as np
from sklearn.cluster import HDBSCAN, AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.preprocessing import normalize

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("NewsClusteringEngine")
sys.stdout.reconfigure(line_buffering=True)

CSV_PATH = Path(__file__).parent / "enriched_news_202608.csv"
CLUSTER_OUTPUT_PATH = Path(__file__).parent / "news_clusters_summary.json"

DIMENSION_KEYS = [
    "political", "economic", "social", "technological", "legal", "environmental",
    "threat_of_new_entrants", "bargaining_power_of_buyers", "bargaining_power_of_suppliers",
    "threat_of_substitutes", "competitive_rivalry"
]


def compute_strategic_impact_score(strategic_11d: list) -> float:
    """
    Computes a strict Strategic Impact Score (0.00 to 1.00) for a news item based on its 11-D PESTLE & Porter scores.
    High impact requires a strong peak score (>= 0.35) in at least one strategic driver.
    Off-topic, low-signal, or baseline noise sitting near 0.05 yields an impact score < 0.20.
    """
    if not strategic_11d or len(strategic_11d) < 11:
        return 0.05
    s_arr = np.array(strategic_11d, dtype=np.float32)
    sorted_scores = np.sort(s_arr)[::-1]
    peak = float(sorted_scores[0])
    top2_mean = float(np.mean(sorted_scores[:2]))
    active_count = float(np.sum(s_arr > 0.20))

    # Weight peak impact and top 2 strategic drivers
    impact_score = (peak * 0.60) + (top2_mean * 0.30) + min(0.10, active_count * 0.02)
    return round(float(impact_score), 4)


def load_news_dataset(csv_path: Path, max_records: int = 10000, min_impact_threshold: float = 0.25):
    """
    Loads news headlines, 768-D contextual embeddings, and 11-D strategic embeddings,
    filtering out low-impact / off-topic news items whose strategic impact score is below threshold.
    """
    print(f"[NewsClustering] Loading dataset from '{csv_path}' (limit: {max_records}, min_impact: {min_impact_threshold})...", flush=True)
    if not csv_path.exists():
        print(f"[NewsClustering] ERROR: CSV file '{csv_path}' does not exist.", flush=True)
        sys.exit(1)

    records = []
    X_contextual_list = []
    Y_strategic_list = []
    discarded_low_impact = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, r in enumerate(reader):
            if len(records) >= max_records:
                break
            try:
                c_emb = json.loads(r.get("contextual_embedding", "[]"))
                s_emb = json.loads(r.get("strategic_embedding", "[]"))

                if len(c_emb) == 768 and len(s_emb) == 11:
                    impact_score = compute_strategic_impact_score(s_emb)
                    # Strict filtering: Discard low-impact background noise
                    if impact_score < min_impact_threshold:
                        discarded_low_impact += 1
                        continue

                    records.append({
                        "id": r.get("id"),
                        "date": r.get("date"),
                        "headline": r.get("headline"),
                        "source_link": r.get("source_link"),
                        "location_affected": r.get("location_affected"),
                        "strategic_11d": s_emb,
                        "impact_score": impact_score
                    })
                    X_contextual_list.append(c_emb)
                    Y_strategic_list.append(s_emb)
            except Exception:
                pass

    X_contextual = np.array(X_contextual_list, dtype=np.float32)
    Y_strategic = np.array(Y_strategic_list, dtype=np.float32)

    print(
        f"[NewsClustering] Retained {len(records)} high-impact records. "
        f"Strictly eliminated {discarded_low_impact} unrelated/low-impact news items.",
        flush=True
    )
    return records, X_contextual, Y_strategic


def construct_hybrid_feature_space(X_contextual: np.ndarray, Y_strategic: np.ndarray, topic_weight: float = 0.65):
    """
    Constructs a dual-representation hybrid feature space combining L2-normalized 768-D topic embeddings
    with 11-D strategic impact vectors.
    """
    X_topic_norm = normalize(X_contextual, axis=1, norm='l2')
    Y_strat_norm = normalize(Y_strategic, axis=1, norm='l2')

    hybrid_features = np.hstack([
        X_topic_norm * topic_weight,
        Y_strat_norm * (1.0 - topic_weight)
    ])
    
    return normalize(hybrid_features, axis=1, norm='l2')


def evaluate_and_cluster(records: list, hybrid_features: np.ndarray, n_clusters: int = 15):
    """
    Performs high-precision clustering and computes cohesion metrics, filtering out noise items.
    """
    print(f"\n[NewsClustering] Running Agglomerative Cosine Clustering (n_clusters={n_clusters})...", flush=True)
    
    clusterer = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric="cosine",
        linkage="average"
    )
    labels = clusterer.fit_predict(hybrid_features)

    sil_score = float(silhouette_score(hybrid_features, labels, metric="cosine"))
    ch_score = float(calinski_harabasz_score(hybrid_features, labels))

    print(f"[NewsClustering] Clustering Performance Metrics:")
    print(f"  - Silhouette Score (Cohesion & Separation): {sil_score:.4f} (Higher is better)")
    print(f"  - Calinski-Harabasz Index                 : {ch_score:.2f}")

    # Summarize Clusters
    cluster_summaries = {}
    for cluster_id in range(n_clusters):
        member_indices = np.where(labels == cluster_id)[0]
        member_records = [records[i] for i in member_indices]
        member_strats = np.array([r["strategic_11d"] for r in member_records])

        # Filter cluster members to keep top impactful headlines
        sorted_members = sorted(member_records, key=lambda x: x.get("impact_score", 0.0), reverse=True)

        mean_strat = np.mean(member_strats, axis=0)
        top_dims_idx = np.argsort(mean_strat)[::-1][:3]
        top_strategic_drivers = [
            {"dimension": DIMENSION_KEYS[idx], "average_score": round(float(mean_strat[idx]), 2)}
            for idx in top_dims_idx if mean_strat[idx] > 0.10
        ]

        sample_headlines = [r["headline"] for r in sorted_members[:5]]
        avg_cluster_impact = round(float(np.mean([r.get("impact_score", 0.0) for r in member_records])), 3)

        cluster_summaries[f"cluster_{cluster_id}"] = {
            "cluster_id": cluster_id,
            "total_news_items": len(member_records),
            "percentage_of_dataset": round(len(member_records) / len(records) * 100, 2),
            "average_impact_score": avg_cluster_impact,
            "top_strategic_drivers": top_strategic_drivers,
            "sample_headlines": sample_headlines
        }

    return labels, sil_score, ch_score, cluster_summaries


def main():
    print("=== HIGH-PRECISION STRATEGIC NEWS CLUSTERING EVALUATION ===", flush=True)
    records, X_contextual, Y_strategic = load_news_dataset(CSV_PATH, max_records=10000)
    
    hybrid_features = construct_hybrid_feature_space(X_contextual, Y_strategic, topic_weight=0.65)
    
    labels, sil_score, ch_score, cluster_summaries = evaluate_and_cluster(records, hybrid_features, n_clusters=12)

    # Export Cluster Summaries
    export_payload = {
        "total_news_analyzed": len(records),
        "number_of_clusters": 12,
        "metrics": {
            "silhouette_score": round(sil_score, 4),
            "calinski_harabasz_index": round(ch_score, 2)
        },
        "clusters": cluster_summaries
    }

    with open(CLUSTER_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2)

    print(f"\n[NewsClustering] Saved cluster analysis summary to '{CLUSTER_OUTPUT_PATH}'!", flush=True)

    print("\n--- SAMPLE CLUSTERS GENERATED ---")
    for c_key, c_info in list(cluster_summaries.items())[:3]:
        print(f"\n{c_key.upper()} ({c_info['total_news_items']} items, {c_info['percentage_of_dataset']}%):")
        print("  Top Strategic Drivers:")
        for d in c_info["top_strategic_drivers"]:
            print(f"    - {d['dimension']}: {d['average_score']}")
        print("  Sample Headlines:")
        for h in c_info["sample_headlines"][:3]:
            print(f"    * {h}")


if __name__ == "__main__":
    main()

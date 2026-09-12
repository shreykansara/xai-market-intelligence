#!/usr/bin/env python3
"""
Cloud Embedding Provider via Hugging Face Inference API
--------------------------------------------------------
Computes text embeddings via Hugging Face's Cloud API without loading local PyTorch / Ollama models.
Model: BAAI/bge-base-en-v1.5 (768-D) or sentence-transformers/all-MiniLM-L6-v2 (384-D)
Memory Footprint: < 5 MB RAM (100% cloud API based)
"""

import json
import os
import urllib.request
import logging

logger = logging.getLogger("CloudEmbeddings")

# Hugging Face Free Inference API Endpoint
DEFAULT_HF_MODEL = "BAAI/bge-base-en-v1.5"  # 768-D native embedding model
HF_API_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{DEFAULT_HF_MODEL}"


def get_cloud_text_embedding(text: str, hf_token: str = None, model: str = DEFAULT_HF_MODEL) -> list:
    """
    Fetches text embedding vector via Hugging Face Cloud API.
    Returns 768-dimensional float list.
    """
    if not text or not text.strip():
        return [0.0] * 768

    token = hf_token or os.environ.get("HF_TOKEN", "") or os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
    url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}"

    payload = {
        "inputs": text[:1500],
        "options": {"wait_for_model": True}
    }
    data = json.dumps(payload).encode("utf-8")

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            
            # Feature extraction API returns list of floats or list of token embeddings
            if isinstance(res_json, list):
                if len(res_json) > 0 and isinstance(res_json[0], float):
                    return res_json
                elif len(res_json) > 0 and isinstance(res_json[0], list):
                    # Mean pooling over token embeddings
                    matrix = [row for row in res_json if isinstance(row, list)]
                    if matrix:
                        dim = len(matrix[0])
                        mean_vec = [sum(row[i] for row in matrix) / len(matrix) for i in range(dim)]
                        return mean_vec
    except Exception as e:
        logger.warning(f"Hugging Face Cloud Embedding API call failed: {e}. Using lightweight fallback vector.")

    # Lightweight zero-dependency fallback feature vector (768-D)
    import hashlib, math, re
    vec = [0.0] * 768
    words = re.findall(r"\w+", text.lower())
    for w in words:
        h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
        idx = h % 768
        vec[idx] += 1.0 if (h & 1) else -1.0
    norm = math.sqrt(sum(v * v for v in vec)) + 1e-8
    return [round(v / norm, 6) for v in vec]


if __name__ == "__main__":
    print("Testing Hugging Face Cloud Embedding API...")
    sample_text = "India monitoring trade tariffs on foreign imports and corporate finance."
    emb = get_cloud_text_embedding(sample_text)
    print(f"Generated Vector Dim: {len(emb)}")
    print(f"Sample 5 dimensions: {emb[:5]}")

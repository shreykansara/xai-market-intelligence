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

# Supported Cloud Embedding Endpoints
DEFAULT_HF_MODEL = "BAAI/bge-base-en-v1.5"  # 768-D native model


def _call_openai_embeddings(text: str, api_key: str) -> list:
    """Fetches text embedding via OpenAI REST API (zero dependencies)."""
    url = "https://api.openai.com/v1/embeddings"
    payload = json.dumps({
        "input": text[:2000],
        "model": os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    }).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=3.0) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        raw_vec = res["data"][0]["embedding"]
        # Project or truncate/pad to 768 dimensions if needed
        if len(raw_vec) == 768:
            return raw_vec
        elif len(raw_vec) > 768:
            return raw_vec[:768]
        else:
            return raw_vec + [0.0] * (768 - len(raw_vec))


def _call_huggingface_embeddings(text: str, token: str, model: str = DEFAULT_HF_MODEL) -> list:
    """Fetches text embedding via Hugging Face Inference API (zero dependencies)."""
    url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}"
    payload = json.dumps({
        "inputs": text[:1500],
        "options": {"wait_for_model": True}
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=payload, headers=headers)
    with urllib.request.urlopen(req, timeout=3.0) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        if isinstance(res_json, list):
            if len(res_json) > 0 and isinstance(res_json[0], (float, int)):
                return [float(v) for v in res_json]
            elif len(res_json) > 0 and isinstance(res_json[0], list):
                matrix = [row for row in res_json if isinstance(row, list)]
                if matrix:
                    dim = len(matrix[0])
                    return [sum(row[i] for row in matrix) / len(matrix) for i in range(dim)]
    return None


def get_cloud_text_embedding(text: str, hf_token: str = None, model: str = DEFAULT_HF_MODEL) -> list:
    """
    Computes text embeddings via Cloud APIs without any local heavy ML packages (no PyTorch, no Transformers).
    Order of preference:
      1. OpenAI API (if OPENAI_API_KEY is configured)
      2. Hugging Face Inference API (if HF_TOKEN or free inference endpoint is available)
      3. Zero-dependency deterministic mathematical projection (fallback)
    Returns a 768-dimensional float list.
    """
    if not text or not text.strip():
        return [0.0] * 768

    # 1. Try OpenAI Embeddings API if key is present
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            return _call_openai_embeddings(text, openai_key)
        except Exception as e:
            logger.warning(f"OpenAI Embedding API call failed: {e}. Trying fallback.")

    # 2. Try Hugging Face Inference API
    hf_tok = hf_token or os.environ.get("HF_TOKEN", "") or os.environ.get("HUGGINGFACE_HUB_TOKEN", "")
    try:
        vec = _call_huggingface_embeddings(text, hf_tok, model)
        if vec:
            return vec
    except Exception as e:
        logger.warning(f"Hugging Face Cloud Embedding API call failed: {e}. Using lightweight fallback vector.")

    # 3. Lightweight zero-dependency fallback feature vector (768-D)
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

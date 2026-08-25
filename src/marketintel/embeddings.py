from functools import lru_cache

import numpy as np

from .config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL_NAME)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a list of texts into L2-normalized vectors (cosine similarity = dot product)."""
    model = get_model()
    return np.asarray(model.encode(list(texts), show_progress_bar=True, normalize_embeddings=True))


def embed_text(text: str) -> np.ndarray:
    model = get_model()
    return np.asarray(model.encode([text], show_progress_bar=False, normalize_embeddings=True))[0]

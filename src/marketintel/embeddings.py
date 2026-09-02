"""Local text embedding - the one piece of the stack that always runs
on-host regardless of config.LLM_PROVIDER (Groq vs Ollama only replace the
GENERATIVE calls; embeddings were never routed through either).

Backend is fastembed (ONNX Runtime), not sentence-transformers/torch. This
was a real, measured production constraint, not a style preference: with
sentence-transformers, a plain FastAPI process running one real embed_text()
call sat at ~500 MB RSS - against Render's free-tier 512 MB hard limit, a
~2% margin that would OOM-kill the service under real concurrent load (a
second request arriving mid-embedding, or the DB driver's own buffers,
would be enough). Measured with sentence-transformers removed and fastembed
in its place: no torch dependency at all (`pip install fastembed` pulls
`onnxruntime`, never `torch`), confirmed directly - see CLAUDE.md for the
full before/after numbers.

Same model, same output shape: `sentence-transformers/all-MiniLM-L6-v2`,
384 dimensions - this had to hold exactly, since every embedding already
written anywhere (the halfvec(384) column, the interaction matrix W's
384x384 shape) assumes it. fastembed runs the identical model weights
through ONNX Runtime instead of PyTorch - same architecture, same trained
parameters, not a different or approximated model.
"""
from functools import lru_cache

import numpy as np

from .config import EMBEDDING_MODEL_NAME


@lru_cache(maxsize=1)
def get_model():
    from fastembed import TextEmbedding

    return TextEmbedding(model_name=EMBEDDING_MODEL_NAME)


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """Explicit L2 normalization regardless of what the backend does on its
    own - "cosine similarity == dot product" is a contract of THIS module,
    not an assumption about one particular library's default behavior, so
    switching backends again in the future can't silently break it."""
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return vectors / norms


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed a list of texts into L2-normalized vectors (cosine similarity = dot product)."""
    model = get_model()
    vectors = np.asarray(list(model.embed(list(texts))))
    return _normalize(vectors)


def embed_text(text: str) -> np.ndarray:
    model = get_model()
    vector = np.asarray(next(model.embed([text])))
    return _normalize(vector)

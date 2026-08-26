from functools import lru_cache

from .config import SENTIMENT_MODEL_NAME


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    """An existing pretrained sentiment classifier (not fine-tuned here) - used as-is
    for real headline polarity, per CLAUDE.md's 'do not train one from scratch yet'."""
    from transformers import pipeline

    return pipeline("sentiment-analysis", model=SENTIMENT_MODEL_NAME)


def classify_polarity(text: str) -> str:
    result = get_sentiment_pipeline()(text[:512])[0]
    return "positive" if result["label"] == "POSITIVE" else "negative"

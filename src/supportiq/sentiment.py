"""Optional Hugging Face sentiment adapter.

Banking77 contains no sentiment labels. Configure SUPPORTIQ_SENTIMENT_MODEL to
enable a separately sourced general sentiment model; domain validation is still
required before operational use.
"""
import os
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_pipeline():
    model_name = os.getenv("SUPPORTIQ_SENTIMENT_MODEL", "").strip()
    if not model_name:
        return None
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError("Install the transformers extra to enable sentiment analysis") from exc
    return pipeline("sentiment-analysis", model=model_name)


def analyze_sentiment(text: str) -> str:
    analyzer = _load_pipeline()
    if analyzer is None:
        return "Not configured"
    result = analyzer(text[:4000], truncation=True)[0]
    label = str(result.get("label", "unknown")).upper()
    if "POSITIVE" in label:
        return "Positive"
    if "NEGATIVE" in label:
        return "Negative"
    return "Unknown"

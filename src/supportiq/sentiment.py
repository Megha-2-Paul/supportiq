"""Sentiment adapter.

Banking77 has no sentiment labels. This conservative placeholder does not claim
model-derived sentiment; replace it with a separately evaluated sentiment model.
"""


def analyze_sentiment(text: str) -> str:
    """Return an explicit not-configured state until a validated model is installed."""
    del text
    return "Not configured"

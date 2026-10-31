"""Sentiment adapter. Banking77 has no sentiment annotations."""
def analyze_sentiment(text: str) -> str:
    """Do not fabricate sentiment: return explicit status until a model is configured."""
    del text
    return "Not configured"

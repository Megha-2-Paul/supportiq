from supportiq.sentiment import analyze_sentiment

def test_sentiment_is_explicitly_unconfigured_without_model(monkeypatch):
    monkeypatch.delenv("SUPPORTIQ_SENTIMENT_MODEL", raising=False)
    analyze_sentiment.cache_clear() if hasattr(analyze_sentiment, "cache_clear") else None
    assert analyze_sentiment("A sample banking support message") == "Not configured"

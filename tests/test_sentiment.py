from supportiq.sentiment import _load_pipeline, analyze_sentiment


def test_sentiment_is_explicitly_unconfigured_without_model(monkeypatch):
    monkeypatch.delenv("SUPPORTIQ_SENTIMENT_MODEL", raising=False)
    _load_pipeline.cache_clear()
    assert analyze_sentiment("A sample banking support message") == "Not configured"

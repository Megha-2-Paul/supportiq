import pytest

from supportiq.config import Settings


def test_settings_read_environment(monkeypatch):
    monkeypatch.setenv("SUPPORTIQ_CONFIDENCE_THRESHOLD", "0.7")
    monkeypatch.setenv("SUPPORTIQ_MAX_BATCH_ROWS", "25")
    monkeypatch.setenv("SUPPORTIQ_MODEL_PATH", "models/demo.joblib")

    settings = Settings.from_env()

    assert settings.confidence_threshold == 0.7
    assert settings.max_batch_rows == 25
    assert settings.model_path == "models/demo.joblib"


@pytest.mark.parametrize("value", ["-0.1", "1.1", "not-a-number"])
def test_settings_reject_invalid_confidence_threshold(monkeypatch, value):
    monkeypatch.setenv("SUPPORTIQ_CONFIDENCE_THRESHOLD", value)

    with pytest.raises(ValueError):
        Settings.from_env()


@pytest.mark.parametrize("value", ["0", "-1"])
def test_settings_reject_non_positive_batch_limit(monkeypatch, value):
    monkeypatch.setenv("SUPPORTIQ_MAX_BATCH_ROWS", value)

    with pytest.raises(ValueError):
        Settings.from_env()

def test_settings_reject_batch_limit_above_schema_max(monkeypatch):
    monkeypatch.setenv("SUPPORTIQ_MAX_BATCH_ROWS", "1001")

    with pytest.raises(ValueError):
        Settings.from_env()

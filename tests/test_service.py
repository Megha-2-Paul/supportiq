from supportiq.service import SupportIQService


class FakeModel:
    def predict(self, texts):
        return ["cash_withdrawal"]

    def predict_proba(self, texts):
        return [[0.08, 0.92]]


def test_service_combines_intent_and_rules():
    service = SupportIQService(threshold=0.8)
    service._model = FakeModel()
    result = service.classify("My cash withdrawal was debited but no cash came out")
    assert result["intent"] == "cash_withdrawal"
    assert result["confidence"] == 0.92
    assert result["priority"] == "Normal"
    assert result["priority_reasons"]
    assert result["needs_human_review"] is False


def test_service_rejects_blank_text():
    service = SupportIQService()
    try:
        service.classify("  ")
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid ticket text to be rejected")

from fastapi.testclient import TestClient

from supportiq.api import create_app


class FakeService:
    _model = object()

    def classify(self, text):
        return {
            "intent": "cash_withdrawal",
            "confidence": 0.91,
            "department": "Cash Services",
            "priority": "Normal",
            "priority_reasons": ["No configured urgency phrase matched"],
            "sentiment": "Not configured",
            "needs_human_review": False,
            "model_version": "test",
        }


def make_client():
    return TestClient(create_app(FakeService()))


def test_health_endpoint():
    response = make_client().get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_includes_priority_explanation():
    response = make_client().post(
        "/api/v1/predict", json={"text": "Cash was not dispensed"}
    )
    assert response.status_code == 200
    assert response.json()["intent"] == "cash_withdrawal"
    assert response.json()["priority_reasons"] == [
        "No configured urgency phrase matched"
    ]


def test_invalid_message_is_rejected():
    assert make_client().post(
        "/api/v1/predict", json={"text": " "}
    ).status_code == 422


def test_batch_prediction_returns_each_ticket():
    response = make_client().post(
        "/api/v1/predict/batch",
        json={"tickets": [{"text": "Cash was not dispensed"}, {"text": "Need help with cash"}]},
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
    assert all(item["intent"] == "cash_withdrawal" for item in response.json()["results"])


def test_batch_rejects_empty_ticket_list():
    response = make_client().post("/api/v1/predict/batch", json={"tickets": []})
    assert response.status_code == 422


def test_history_rejects_out_of_range_limit():
    response = make_client().get("/api/v1/history?limit=0")
    assert response.status_code == 422


def test_batch_rejects_configured_row_limit(monkeypatch):
    monkeypatch.setenv("SUPPORTIQ_MAX_BATCH_ROWS", "1")
    response = make_client().post(
        "/api/v1/predict/batch",
        json={"tickets": [{"text": "Cash was not dispensed"}, {"text": "Need cash help"}]},
    )
    assert response.status_code == 413


def test_batch_converts_classifier_value_error_to_422():
    class InvalidService(FakeService):
        def classify(self, text):
            raise ValueError("Invalid message")

    response = TestClient(create_app(InvalidService())).post(
        "/api/v1/predict/batch",
        json={"tickets": [{"text": "Cash was not dispensed"}]},
    )
    assert response.status_code == 422

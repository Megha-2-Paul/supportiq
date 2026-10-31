from fastapi.testclient import TestClient

from supportiq.api import create_app
from supportiq.storage import TicketStore


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


def make_client(tmp_path, service=None):
    store = TicketStore(str(tmp_path / "history.sqlite"))
    return TestClient(create_app(service or FakeService(), store))


def test_health_endpoint(tmp_path):
    response = make_client(tmp_path).get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict_endpoint_includes_priority_explanation(tmp_path):
    response = make_client(tmp_path).post(
        "/api/v1/predict", json={"text": "Cash was not dispensed"}
    )
    assert response.status_code == 200
    assert response.json()["intent"] == "cash_withdrawal"
    assert response.json()["priority_reasons"] == [
        "No configured urgency phrase matched"
    ]


def test_invalid_message_is_rejected(tmp_path):
    response = make_client(tmp_path).post("/api/v1/predict", json={"text": " "})
    assert response.status_code == 422


def test_batch_prediction_returns_each_ticket(tmp_path):
    response = make_client(tmp_path).post(
        "/api/v1/predict/batch",
        json={
            "tickets": [
                {"text": "Cash was not dispensed"},
                {"text": "Need help with cash"},
            ]
        },
    )
    assert response.status_code == 200
    assert len(response.json()["results"]) == 2
    assert all(
        item["intent"] == "cash_withdrawal"
        for item in response.json()["results"]
    )


def test_batch_rejects_empty_ticket_list(tmp_path):
    response = make_client(tmp_path).post(
        "/api/v1/predict/batch", json={"tickets": []}
    )
    assert response.status_code == 422


def test_history_rejects_out_of_range_limit(tmp_path):
    response = make_client(tmp_path).get("/api/v1/history?limit=0")
    assert response.status_code == 422


def test_batch_rejects_configured_row_limit(tmp_path, monkeypatch):
    monkeypatch.setenv("SUPPORTIQ_MAX_BATCH_ROWS", "1")
    response = make_client(tmp_path).post(
        "/api/v1/predict/batch",
        json={
            "tickets": [
                {"text": "Cash was not dispensed"},
                {"text": "Need cash help"},
            ]
        },
    )
    assert response.status_code == 413


def test_batch_converts_classifier_value_error_to_422(tmp_path):
    class InvalidService(FakeService):
        def classify(self, text):
            raise ValueError("Invalid message")

    response = make_client(tmp_path, InvalidService()).post(
        "/api/v1/predict/batch",
        json={"tickets": [{"text": "Cash was not dispensed"}]},
    )
    assert response.status_code == 422


def test_prediction_is_saved_to_history(tmp_path):
    client = make_client(tmp_path)
    prediction = client.post(
        "/api/v1/predict", json={"text": "Cash was not dispensed"}
    )
    history = client.get("/api/v1/history")

    assert prediction.status_code == 200
    assert history.status_code == 200
    assert len(history.json()["items"]) == 1
    assert history.json()["items"][0]["intent"] == "cash_withdrawal"

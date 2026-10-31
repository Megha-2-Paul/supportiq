from fastapi.testclient import TestClient
from supportiq.api import create_app

class FakeService:
    _model = object()
    def classify(self, text):
        return {"intent":"cash_withdrawal","confidence":0.91,"department":"Cash Services",
                "priority":"Normal","sentiment":"Not configured",
                "needs_human_review":False,"model_version":"test"}

def test_health_endpoint():
    client = TestClient(create_app(FakeService()))
    assert client.get("/health").json()["status"] == "ok"

def test_predict_endpoint():
    client = TestClient(create_app(FakeService()))
    response = client.post("/api/v1/predict", json={"text":"Cash was not dispensed"})
    assert response.status_code == 200
    assert response.json()["intent"] == "cash_withdrawal"

def test_invalid_message_is_rejected():
    client = TestClient(create_app(FakeService()))
    assert client.post("/api/v1/predict", json={"text":" "}).status_code == 422

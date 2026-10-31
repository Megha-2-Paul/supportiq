from supportiq.classifier import ModelNotReadyError, load_model, predict_intent


class LabelOnlyModel:
    def predict(self, messages):
        return ["cash_withdrawal"]


class ProbabilityModel:
    def predict(self, messages):
        return ["cash_withdrawal"]

    def predict_proba(self, messages):
        return [[0.2, 0.8]]


def test_load_model_reports_missing_artifact(tmp_path):
    try:
        load_model(tmp_path / "missing.joblib")
    except ModelNotReadyError as exc:
        assert "train it first" in str(exc)
    else:
        raise AssertionError("Expected missing model artifact to be reported")


def test_prediction_without_probabilities_is_zero_confidence():
    label, confidence = predict_intent(LabelOnlyModel(), "cash not dispensed")

    assert label == "cash_withdrawal"
    assert confidence == 0.0


def test_prediction_probability_is_bounded_and_returned():
    label, confidence = predict_intent(ProbabilityModel(), "cash not dispensed")

    assert label == "cash_withdrawal"
    assert confidence == 0.8

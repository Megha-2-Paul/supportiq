"""Load and run a persisted scikit-learn intent pipeline."""
from pathlib import Path

import joblib


class ModelNotReadyError(RuntimeError):
    """No trained model artifact is available."""


def load_model(path: str | Path):
    model_path = Path(path)
    if not model_path.is_file():
        raise ModelNotReadyError(f"Intent model not found at {model_path}; train it first.")
    return joblib.load(model_path)


def predict_intent(model, text: str) -> tuple[str, float]:
    label = str(model.predict([text])[0])
    # Only probability-capable estimators produce a probability-like score here.
    confidence = (
        float(max(model.predict_proba([text])[0]))
        if hasattr(model, "predict_proba")
        else 0.0
    )
    return label, max(0.0, min(1.0, confidence))

"""Intent model loading and prediction helpers."""
from pathlib import Path
from typing import Any
import joblib


class ModelNotReadyError(RuntimeError):
    """Raised when no trained intent model artifact is available."""


def load_model(path: str | Path) -> Any:
    model_path = Path(path)
    if not model_path.is_file():
        raise ModelNotReadyError(
            f"Intent model not found at {model_path}. Run the documented training script first."
        )
    return joblib.load(model_path)


def predict_intent(model: Any, text: str) -> tuple[str, float]:
    """Predict one intent and return the best available confidence estimate."""
    label = str(model.predict([text])[0])
    confidence = 0.0
    if hasattr(model, "predict_proba"):
        confidence = float(max(model.predict_proba([text])[0]))
    elif hasattr(model, "decision_function"):
        # A decision score is not a calibrated probability. Use a neutral sentinel
        # and let the API mark it for human review rather than mislabel it confidence.
        confidence = 0.0
    return label, max(0.0, min(1.0, confidence))

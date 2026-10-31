"""Application service that combines the model and transparent rules."""
from pathlib import Path
from .classifier import ModelNotReadyError, load_model, predict_intent
from .priority import recommend_priority
from .routing import route_intent
from .sentiment import analyze_sentiment


class SupportIQService:
    def __init__(self, model_path: str = "artifacts/intent_model.joblib", threshold: float = 0.55):
        self.model_path = model_path
        self.threshold = threshold
        self._model = None

    def _get_model(self):
        if self._model is None:
            self._model = load_model(Path(self.model_path))
        return self._model

    def classify(self, text: str) -> dict:
        cleaned = text.strip()
        if len(cleaned) < 3:
            raise ValueError("Ticket text must contain at least 3 non-whitespace characters")
        intent, confidence = predict_intent(self._get_model(), cleaned)
        priority, reasons = recommend_priority(cleaned)
        return {
            "intent": intent,
            "confidence": confidence,
            "department": route_intent(intent),
            "priority": priority,
            "priority_reasons": reasons,
            "sentiment": analyze_sentiment(cleaned),
            "needs_human_review": confidence < self.threshold,
            "model_version": "local-artifact",
        }

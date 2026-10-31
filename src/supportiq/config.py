"""Environment-backed application configuration."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = "development"
    database_path: str = "supportiq.db"
    model_path: str = "artifacts/intent_model.joblib"
    confidence_threshold: float = 0.55
    max_batch_rows: int = 1000

    @classmethod
    def from_env(cls) -> "Settings":
        threshold = float(os.getenv("SUPPORTIQ_CONFIDENCE_THRESHOLD", "0.55"))
        max_rows = int(os.getenv("SUPPORTIQ_MAX_BATCH_ROWS", "1000"))
        if not 0 <= threshold <= 1:
            raise ValueError("SUPPORTIQ_CONFIDENCE_THRESHOLD must be between 0 and 1")
        if not 1 <= max_rows <= 1000:
            raise ValueError("SUPPORTIQ_MAX_BATCH_ROWS must be between 1 and 1000")
        return cls(
            environment=os.getenv("SUPPORTIQ_ENV", "development"),
            database_path=os.getenv("SUPPORTIQ_DATABASE_PATH", "supportiq.db"),
            model_path=os.getenv("SUPPORTIQ_MODEL_PATH", "artifacts/intent_model.joblib"),
            confidence_threshold=threshold,
            max_batch_rows=max_rows,
        )

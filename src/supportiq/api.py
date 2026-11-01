"""FastAPI application factory with prediction history persistence."""
from fastapi import FastAPI, HTTPException, Query

from .classifier import ModelNotReadyError
from .config import Settings
from .schemas import (
    BatchPredictionResponse,
    BatchTicketRequest,
    PredictionResponse,
    TicketRequest,
)
from .service import SupportIQService
from .storage import TicketStore


def create_app(service=None, store=None):
    settings = Settings.from_env()
    predictor = service or SupportIQService(
        settings.model_path, settings.confidence_threshold
    )
    history = store or TicketStore(settings.database_path)
    app = FastAPI(
        title="SupportIQ API",
        version="0.1.0",
        description="Banking support ticket classification decision support",
    )

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "model_loaded": getattr(predictor, "_model", None) is not None,
        }

    @app.post("/api/v1/predict", response_model=PredictionResponse)
    def predict(payload: TicketRequest):
        try:
            result = predictor.classify(payload.text)
            history.add(payload.text, result)
            return result
        except ModelNotReadyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post(
        "/api/v1/predict/batch",
        response_model=BatchPredictionResponse,
    )
    def predict_batch(payload: BatchTicketRequest):
        if len(payload.tickets) > settings.max_batch_rows:
            raise HTTPException(
                status_code=413,
                detail="Batch exceeds configured row limit",
            )
        try:
            results = []
            for ticket in payload.tickets:
                result = predictor.classify(ticket.text)
                history.add(ticket.text, result)
                results.append(result)
            return {"results": results}
        except ModelNotReadyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.get("/api/v1/history")
    def get_history(limit: int = Query(default=100, ge=1, le=1000)):
        try:
            return {"items": history.list_recent(limit)}
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    return app


app = create_app()

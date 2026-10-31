"""FastAPI application factory."""
from fastapi import FastAPI, HTTPException
from .config import Settings
from .schemas import BatchTicketRequest, PredictionResponse, TicketRequest
from .service import SupportIQService
from .classifier import ModelNotReadyError


def create_app(service: SupportIQService | None = None) -> FastAPI:
    settings = Settings.from_env()
    predictor = service or SupportIQService(settings.model_path, settings.confidence_threshold)
    app = FastAPI(title="SupportIQ API", version="0.1.0", description="Banking support ticket decision support")

    @app.get("/health")
    def health():
        return {"status": "ok", "model_loaded": predictor._model is not None}

    @app.post("/api/v1/predict", response_model=PredictionResponse)
    def predict(payload: TicketRequest):
        try:
            return predictor.classify(payload.text)
        except ModelNotReadyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    @app.post("/api/v1/predict/batch")
    def predict_batch(payload: BatchTicketRequest):
        if len(payload.tickets) > settings.max_batch_rows:
            raise HTTPException(status_code=413, detail="Batch exceeds configured row limit")
        try:
            return {"results": [predictor.classify(ticket.text) for ticket in payload.tickets]}
        except ModelNotReadyError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return app


app = create_app()

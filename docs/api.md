# API reference

Run after installing dependencies and training a model:

    uvicorn api.main:app --reload

OpenAPI documentation: http://localhost:8000/docs

## Health
GET /health

Returns service status and whether the model has been loaded.

## Single prediction
POST /api/v1/predict

    {"text": "My cash withdrawal was debited but no cash came out."}

Returns intent, confidence, recommended department, priority, sentiment status, human-review flag, and model version. Successful predictions are stored in local SQLite history. Returns 503 if the model artifact is missing.

## Batch prediction
POST /api/v1/predict/batch

    {"tickets": [{"text": "I cannot access my account"}, {"text": "My card was retained by an ATM"}]}

Returns one result per ticket and stores successful predictions. Request size is bounded by the configured row limit.

## History
GET /api/v1/history?limit=100

Returns the most recent locally stored predictions. The limit must be between 1 and 1,000. This local demonstration endpoint has no authentication; do not expose it to the public internet.

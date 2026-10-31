# API reference

Start the API after installing dependencies and training a local intent model:

    uvicorn api.main:app --reload

Interactive OpenAPI documentation: http://localhost:8000/docs

## Health

**GET /health**

Returns service status and whether the intent model has been loaded. A healthy process does not imply that a model artifact exists; prediction requests return 503 until a model is available.

## Single prediction

**POST /api/v1/predict**

Request:

    {"text": "My cash withdrawal was debited but no cash came out."}

The response includes:
- `intent`: predicted Banking77 intent label
- `confidence`: maximum class probability from the estimator; not necessarily calibrated
- `department`: deterministic routing suggestion
- `priority`: rules-based urgency recommendation
- `priority_reasons`: matched rule phrases explaining the recommendation
- `sentiment`: `Not configured` unless a separate sentiment model is selected
- `needs_human_review`: true when confidence is below the configured threshold
- `model_version`: local artifact identifier

Successful predictions are stored in local SQLite history. Returns 503 if the model artifact is missing.

## Batch prediction

**POST /api/v1/predict/batch**

Request:

    {"tickets": [{"text": "I cannot access my account"}, {"text": "My card was retained by an ATM"}]}

Returns one result per ticket and stores successful predictions. Request size is bounded by `SUPPORTIQ_MAX_BATCH_ROWS` (default 1,000).

## History

**GET /api/v1/history?limit=100**

Returns the most recent locally stored predictions. The limit must be between 1 and 1,000. This local demonstration endpoint has no authentication; do not expose it to the public internet.

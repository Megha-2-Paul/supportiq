# API reference

Run locally after installing the package and training the baseline:

    uvicorn api.main:app --reload

Interactive OpenAPI documentation is available at /docs.

## Health
GET /health

Returns application status and whether the model has been loaded into memory.

## Single prediction
POST /api/v1/predict

    {"text": "My cash withdrawal was debited but no cash came out."}

Returns intent, confidence, recommended department, priority, sentiment status, human-review flag, and model version. Returns 503 if no model artifact exists.

## Batch prediction
POST /api/v1/predict/batch

    {"tickets": [{"text": "I cannot access my account"}, {"text": "My card was retained by an ATM"}]}

The request is bounded by configured row limits. Invalid payloads are rejected by Pydantic.

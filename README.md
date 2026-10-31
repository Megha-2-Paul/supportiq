# SupportIQ

**Intelligent Banking Customer Support Classification & Analytics**

SupportIQ is a portfolio-grade demonstration of an end-to-end NLP application for banking support messages. It combines intent classification, transparent routing and urgency recommendations, a FastAPI service, a Streamlit interface, batch analysis, local SQLite history, tests, and Docker configuration.

> **Responsible-use notice:** SupportIQ is a learning and portfolio prototype, not a production banking system. Use synthetic examples only. Never submit credentials, payment-card data, authentication codes, account identifiers, or private customer records.

## Features

- 77-class banking intent classification using the public Banking77 benchmark.
- TF-IDF + Logistic Regression baseline training and held-out evaluation.
- Confidence-aware predictions and a human-review flag.
- Deterministic department-routing recommendations.
- Explainable rules-based priority recommendations.
- Single-ticket analysis and CSV/XLSX batch UI.
- FastAPI single and batch endpoints with OpenAPI docs.
- SQLite prediction-history module.
- Streamlit interface, pytest suite, GitHub Actions, Docker, and developer documentation.

## Modeling transparency

Banking77 supplies intent labels; it does **not** contain sentiment or priority annotations. SupportIQ therefore does not pretend to train either task from Banking77. Sentiment currently reports **Not configured** until a separate model and source are selected and evaluated. Priority is a configurable keyword heuristic, not a trained classifier or fraud detector. Classifier confidence may be uncalibrated and must not be treated as certainty.

The baseline training script uses the official Banking77 train and test splits. It reports accuracy, macro-F1, weighted-F1, and per-class metrics. Model performance is not claimed until the script has been run and the resulting report reviewed.

## Quick start

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    pip install datasets
    python ml/train_baseline.py

Start the API:

    uvicorn api.main:app --reload

Start the dashboard in another terminal:

    streamlit run app/streamlit_app.py

Open http://localhost:8501 for the dashboard and http://localhost:8000/docs for API documentation.

## Tests

    pytest

## Docker

After training a model locally:

    docker compose up --build

The API is exposed on port 8000 and Streamlit on port 8501. The model artifact is mounted from the local artifacts directory.

## Repository map

- src/supportiq — application logic, schemas, model inference, rules, storage
- ml — training and evaluation
- api — FastAPI entry point
- app — Streamlit user interface
- tests — automated tests
- docs — architecture, API, development, data governance
- data/samples — synthetic demonstration data

## Dataset

Upstream source: [PolyAI Banking77 on Hugging Face](https://huggingface.co/datasets/PolyAI/banking77). Review the current dataset card, license, and terms before redistribution or publishing trained artifacts. Raw data is not stored in this repository.

## Limitations and responsible use

This prototype has no production authentication, authorization, encryption, retention controls, regulated-data safeguards, audit trail, monitoring, or institution-specific compliance review. Routing and priority are suggestions only and require human review. Do not use this software for automated account restrictions, fraud determinations, credit decisions, or other high-impact decisions.

See docs/ for architecture, API usage, development, and data governance.

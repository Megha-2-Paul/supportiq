# Development guide

## Environment

Use Python 3.10 or newer.

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev,training]"

On Windows PowerShell:

    .venv/Scripts/Activate.ps1

## Classical baseline

The `training` extra installs the Hugging Face dataset loader. Train the baseline:

    python ml/train_baseline.py

This downloads PolyAI Banking77 and creates `artifacts/intent_model.joblib` plus `reports/baseline_metrics.json`. Training may take several minutes depending on CPU and network.

## Optional DistilBERT experiment

Install the transformer extra:

    pip install -e ".[transformers]"

Then run:

    python ml/train_transformer.py --epochs 2 --batch-size 16

This experiment requires more compute, memory, disk space, and network access. See [the transformer experiment guide](transformer-experiment.md).

## Run

Terminal 1:

    uvicorn api.main:app --reload

Terminal 2:

    streamlit run app/streamlit_app.py

Dashboard: http://localhost:8501

API documentation: http://localhost:8000/docs

## Test and lint

    pytest
    ruff check .

Do not commit downloaded datasets, database files, credentials, or generated model artifacts.

# Development guide

## Environment
Use Python 3.10 or newer.

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

On Windows, activate with .venv\\Scripts\\activate.

## Classical baseline
Install the dataset loader and train:

    pip install datasets
    python ml/train_baseline.py

This downloads PolyAI Banking77 and creates artifacts/intent_model.joblib plus reports/baseline_metrics.json. Training may take several minutes depending on CPU and network.

## Optional DistilBERT experiment
Install the transformer extra:

    pip install -e ".[transformers]"
    python ml/train_transformer.py --epochs 2 --batch-size 16

This experiment requires more compute, memory, disk space, and network access. See docs/transformer-experiment.md.

## Run
Terminal 1:

    uvicorn api.main:app --reload

Terminal 2:

    streamlit run app/streamlit_app.py

## Test and lint

    pytest
    ruff check .

Do not commit downloaded datasets, database files, credentials, or generated model artifacts.

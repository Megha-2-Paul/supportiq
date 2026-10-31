# Development guide

## Environment
Use Python 3.10 or newer. Create and activate a virtual environment, then install development dependencies:

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

On Windows, activate with .venv\\Scripts\\activate.

## Train
Install the datasets dependency and run:

    pip install datasets
    python ml/train_baseline.py

The script downloads Banking77 from Hugging Face and creates artifacts/intent_model.joblib and reports/baseline_metrics.json. Training may take several minutes depending on CPU and network.

## Run
Terminal 1:

    uvicorn api.main:app --reload

Terminal 2:

    streamlit run app/streamlit_app.py

## Test and lint

    pytest
    ruff check .

Do not commit the downloaded dataset, database, or generated model artifacts.

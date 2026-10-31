# SupportIQ

**Banking customer-support ticket classification and analytics**

SupportIQ is an end-to-end Python portfolio prototype that demonstrates how natural-language customer support messages can be classified, triaged, and explored through an interactive dashboard. It combines a scikit-learn NLP pipeline, FastAPI REST service, Streamlit UI, batch processing, local SQLite history, automated tests, and Docker configuration.

> **Responsible-use notice:** SupportIQ is a learning and portfolio prototype, not a production banking system. Use synthetic examples only. Never submit credentials, payment-card data, authentication codes, account identifiers, or private customer records.

## Product capabilities

| Capability | Implementation |
|---|---|
| Intent classification | 77 Banking77 intents; TF-IDF word n-grams + Logistic Regression baseline |
| Confidence handling | Maximum class probability and configurable human-review threshold |
| Ticket triage | Deterministic department routing and explainable keyword-based priority |
| Sentiment | Optional separately configured model; unconfigured by default |
| Interactive experience | Streamlit dashboard for single tickets, batch files, history, and metrics |
| API | FastAPI single and batch prediction endpoints, health check, and OpenAPI docs |
| Local persistence | SQLite prediction history |
| Engineering | Pytest, GitHub Actions, Docker, developer and model documentation |

## Architecture

```text
CSV / Excel / Streamlit
          |
          v
      FastAPI API
          |
          v
   SupportIQ service
      |      |       |
     NLP   Routing Priority
    model   rules    rules
          |
          v
    SQLite history
```

## Model and evaluation transparency

The baseline trains on the official train split of [PolyAI Banking77](https://huggingface.co/datasets/PolyAI/banking77) and evaluates on its official test split. It reports accuracy, macro-F1, weighted-F1, and per-class metrics.

**Verified reference run (GitHub Actions, 2026-10-31 UTC):**

| Metric | Official test split |
|---|---:|
| Accuracy | 87.37% |
| Macro-F1 | 87.40% |
| Weighted-F1 | 87.40% |

The run used 10,003 training examples and 3,080 official test examples. The CI workflow also verified that the saved model artifact loads and produces a prediction. Run `python ml/train_baseline.py` locally to regenerate the model and detailed report; results may vary with dataset revisions or dependency versions. These benchmark metrics do not represent expected performance on any bank's private customer messages.

Banking77 provides intent labels, not sentiment or priority labels. Accordingly:
- Priority is a transparent configurable keyword heuristic, not a trained classifier or fraud detector.
- Sentiment is **Not configured** until a separate model and source are selected and evaluated.
- Maximum class probability may be uncalibrated and must not be treated as certainty.
- Routing, priority, and intent outputs are decision-support suggestions requiring human review.

## Quick start

Python 3.10+ is required. From the repository root:

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1

pip install -e ".[dev,training]"
python ml/train_baseline.py
```

Start the API in one terminal:

```bash
uvicorn api.main:app --reload
```

Start the dashboard in a second terminal:

```bash
streamlit run app/streamlit_app.py
```

- Dashboard: http://localhost:8501
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Tests

```bash
pytest
ruff check .
```

## Docker

Train the baseline model first so that `artifacts/intent_model.joblib` exists, then run:

```bash
docker compose up --build
```

The API is exposed on port 8000 and the dashboard on port 8501. Docker Compose waits for the API health check before starting the dashboard.

## Repository guide

- `src/supportiq/` — application logic, schemas, inference, routing, priority, storage
- `ml/` — baseline training and optional DistilBERT experiment
- `api/` — FastAPI entry point
- `app/` — Streamlit dashboard
- `tests/` — automated tests
- `docs/` — architecture, API, development, governance, model card, portfolio walkthrough
- `data/samples/` — synthetic sample tickets

## Portfolio materials

See [the Fiverr portfolio showcase guide](docs/fiverr-portfolio-showcase.md) for the project description, skills, gallery plan, cover prompt, and demo-video storyboard.

## Dataset and licensing

The training script downloads the public Banking77 dataset from Hugging Face at runtime; raw dataset files are not stored in this repository. Review the upstream dataset card, license, version, and terms before redistribution or publication of derived artifacts. This repository is licensed under MIT; that license does not override third-party dataset terms.

## Limitations and responsible use

This prototype has no production authentication, authorization, encryption, retention controls, regulated-data safeguards, audit trail, monitoring, or institution-specific compliance review. Do not use it for automated account restrictions, fraud determinations, credit decisions, or other high-impact decisions. Human review is required.

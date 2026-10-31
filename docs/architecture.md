# Architecture

SupportIQ accepts a ticket from the Streamlit UI, CSV/XLSX batch flow, or FastAPI. Input is validated before an intent model is invoked. The prediction layer returns an intent label and an available confidence estimate, then separate decision modules recommend a department and rules-based priority. Sentiment is explicitly marked not configured until a separately sourced and evaluated sentiment model is selected.

The application separates model code, business rules, storage, API contracts, and UI. SQLite stores prediction history for local demonstration. Training and evaluation are kept separate from serving code.

## Model evaluation

The baseline training script uses the official Banking77 train/test split. Report accuracy, macro-F1, weighted-F1, and per-class precision/recall/F1. The test split must not be used for hyperparameter selection. Any transformer candidate must use a validation split derived only from training data, then be evaluated once on the official test split. Compare runtime and model size as well as predictive metrics.

## Limitations

- Banking77 represents banking queries and intents, not a production bank's private ticket stream.
- Dataset labels contain no priority or sentiment targets.
- Confidence from a classifier is not inherently calibrated; low or missing confidence must trigger human review.
- Routing and priority rules are illustrative and require institution-specific governance before any operational use.

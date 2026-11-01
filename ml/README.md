# Model training

Install the baseline training extra:

    pip install -e ".[training]"

Then run:

    python ml/train_baseline.py

The script downloads the upstream PolyAI Banking77 dataset, trains TF-IDF + Logistic Regression on its official train split, evaluates once on its official test split, and writes a Joblib artifact plus a JSON report. Do not tune against the test split. Record the dataset revision, license, package versions, and metrics when publishing a trained artifact.

For the optional transformer experiment, install:

    pip install -e ".[transformers]"

See [the transformer experiment guide](../docs/transformer-experiment.md).

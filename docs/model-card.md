# SupportIQ intent model card

## Model purpose
Classify short banking-support messages into one of the intent labels in the Banking77 benchmark. The output is a routing aid for a human support operator.

## Training data
- Source: PolyAI Banking77, loaded from Hugging Face datasets.
- Intended labels: 77 banking-query intent categories.
- The dataset is a public benchmark, not a representative sample of any particular bank's customers.
- Verify the current dataset card, revision, and license before reuse or redistribution.

## Training procedure
The classical baseline uses word-level TF-IDF (unigrams and bigrams) and Logistic Regression with class weighting. The optional DistilBERT experiment creates a validation split from the training partition and reserves the official test split for final evaluation.

## Evaluation

The baseline training script writes accuracy, macro-F1, weighted-F1, and class-level metrics to `reports/baseline_metrics.json`.

**Verified reference run (GitHub Actions, 2026-10-31 UTC):**

| Metric | Result |
|---|---:|
| Training examples | 10,003 |
| Official test examples | 3,080 |
| Accuracy | 87.37% |
| Macro-F1 | 87.40% |
| Weighted-F1 | 87.40% |

The run used Python 3.11.17, Hugging Face `datasets` 3.6.0, and scikit-learn 1.9.1. CI also confirmed that the saved artifact loads and returns an inference result. Re-run the training script to regenerate the detailed report; results can vary with dataset revisions and dependency versions. These benchmark scores must not be interpreted as performance on real bank customer data.

## Limitations
- Domain and language coverage are limited by the benchmark.
- User messages may differ in spelling, context, language, and vocabulary.
- Maximum class probability is not necessarily calibrated confidence.
- The model does not detect fraud, determine eligibility, or make account decisions.
- Human review is required, especially for low-confidence or consequential cases.

## Out-of-scope uses
Do not use this model to automatically freeze accounts, reject transactions, determine creditworthiness, make fraud findings, or replace trained banking support staff.

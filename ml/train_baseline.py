"""Train a reproducible TF-IDF + Logistic Regression baseline on Banking77."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import joblib
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/intent_model.joblib")
    parser.add_argument("--report", default="reports/baseline_metrics.json")
    parser.add_argument("--max-features", type=int, default=100000)
    args = parser.parse_args()
    dataset = load_dataset("PolyAI/banking77")
    train, test = dataset["train"], dataset["test"]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=args.max_features,
                                  strip_accents="unicode", sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced", n_jobs=None)),
    ])
    model.fit(train["text"], train["label"])
    predictions = model.predict(test["text"])
    metrics = {
        "dataset": "PolyAI/banking77",
        "split": "official test split",
        "accuracy": accuracy_score(test["label"], predictions),
        "macro_f1": f1_score(test["label"], predictions, average="macro"),
        "weighted_f1": f1_score(test["label"], predictions, average="weighted"),
        "classification_report": classification_report(test["label"], predictions, output_dict=True),
    }
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    report = Path(args.report); report.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output)
    report.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in metrics.items() if k != "classification_report"}, indent=2))


if __name__ == "__main__":
    main()

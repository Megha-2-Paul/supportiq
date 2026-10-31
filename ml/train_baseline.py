"""Train TF-IDF + Logistic Regression on the official Banking77 split."""
import argparse, json
from pathlib import Path
import joblib
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/intent_model.joblib")
    parser.add_argument("--report", default="reports/baseline_metrics.json")
    args = parser.parse_args()
    dataset = load_dataset("PolyAI/banking77")
    train, test = dataset["train"], dataset["test"]
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=100000,
                                  strip_accents="unicode", sublinear_tf=True)),
        ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])
    model.fit(train["text"], train["label"])
    predicted = model.predict(test["text"])
    metrics = {"dataset": "PolyAI/banking77", "split": "official test split",
        "accuracy": float(accuracy_score(test["label"], predicted)),
        "macro_f1": float(f1_score(test["label"], predicted, average="macro")),
        "weighted_f1": float(f1_score(test["label"], predicted, average="weighted")),
        "classification_report": classification_report(test["label"], predicted, output_dict=True)}
    out, report = Path(args.output), Path(args.report)
    out.parent.mkdir(parents=True, exist_ok=True); report.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out); report.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in metrics.items() if k != "classification_report"}, indent=2))
if __name__ == "__main__":
    main()

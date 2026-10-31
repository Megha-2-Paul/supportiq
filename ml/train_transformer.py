"""Optional DistilBERT fine-tuning experiment for Banking77.

Install with: pip install -e ".[transformers]"
Validation data is split from the official training set. The official test set is
used only for the final evaluation at the end of training.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from datasets import load_dataset
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    Trainer,
    TrainingArguments,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="distilbert-base-uncased")
    parser.add_argument("--output", default="artifacts/distilbert-banking77")
    parser.add_argument("--epochs", type=float, default=2)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()
    raw = load_dataset("PolyAI/banking77")
    label_names = raw["train"].features["label"].names
    train_valid = raw["train"].train_test_split(test_size=0.1, seed=42, stratify_by_column="label")
    tokenizer = AutoTokenizer.from_pretrained(args.model)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, max_length=160)

    train_ds = train_valid["train"].map(tokenize, batched=True)
    valid_ds = train_valid["test"].map(tokenize, batched=True)
    test_ds = raw["test"].map(tokenize, batched=True)
    columns = ["input_ids", "attention_mask", "label"]
    train_ds.set_format(type="torch", columns=columns)
    valid_ds.set_format(type="torch", columns=columns)
    test_ds.set_format(type="torch", columns=columns)
    model = AutoModelForSequenceClassification.from_pretrained(
        args.model, num_labels=len(label_names),
        id2label={i: name for i, name in enumerate(label_names)},
        label2id={name: i for i, name in enumerate(label_names)})
    def metrics(pred):
        logits, labels = pred
        predictions = np.argmax(logits, axis=-1)
        return {"accuracy": accuracy_score(labels, predictions),
                "macro_f1": f1_score(labels, predictions, average="macro"),
                "weighted_f1": f1_score(labels, predictions, average="weighted")}
    training_args = TrainingArguments(
        output_dir=args.output, learning_rate=2e-5, per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size, num_train_epochs=args.epochs,
        weight_decay=0.01, evaluation_strategy="epoch", save_strategy="epoch",
        load_best_model_at_end=True, metric_for_best_model="macro_f1",
        greater_is_better=True, logging_steps=100, report_to="none", seed=42)
    trainer = Trainer(model=model, args=training_args, train_dataset=train_ds,
                      eval_dataset=valid_ds, tokenizer=tokenizer,
                      data_collator=DataCollatorWithPadding(tokenizer), compute_metrics=metrics)
    trainer.train()
    final_metrics = trainer.evaluate(test_ds, metric_key_prefix="test")
    Path(args.output).mkdir(parents=True, exist_ok=True)
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    Path("reports").mkdir(exist_ok=True)
    Path("reports/distilbert_metrics.json").write_text(
        json.dumps({"dataset":"PolyAI/banking77","validation_split":"10% of training set",
                    "test_split":"official test split","metrics":final_metrics}, indent=2),
        encoding="utf-8")
    print(json.dumps(final_metrics, indent=2))


if __name__ == "__main__":
    main()

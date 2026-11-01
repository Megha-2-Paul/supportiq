# Optional DistilBERT experiment

The optional transformer script fine-tunes DistilBERT on Banking77. It reserves 10% of the official training split for validation, selects the best checkpoint using validation macro-F1, and evaluates once on the official test split after training.

Install the optional dependencies:

    pip install -e ".[transformers]"

Run:

    python ml/train_transformer.py --epochs 2 --batch-size 16

The experiment can require substantial RAM, disk space, and compute. Reduce batch size or use a supported accelerator if necessary. Compare the transformer against the classical baseline on the same official test split, and report model size and inference latency as well as macro-F1. Do not claim the transformer is superior unless the measured results support that conclusion.

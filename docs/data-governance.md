# Data governance and safe demonstration

- Banking77 is a public benchmark for banking intent classification, not a production bank's customer database.
- Confirm the current upstream dataset license, version, and terms before redistribution or publication of derived artifacts.
- The dataset has intent labels only. It has no sentiment or priority ground truth.
- Use synthetic examples in the UI and portfolio screenshots.
- Never commit credentials, one-time codes, card numbers, bank account identifiers, personal customer records, or private bank exports.
- Keep raw and processed data out of version control.
- Model outputs are decision support only and must be reviewed by a person.
- Priority rules are illustrative keyword heuristics, not fraud detection, regulatory risk scoring, or a trained classifier.
- Model confidence can be poorly calibrated; a high score is not a guarantee of correctness.
- Before any real-world deployment, add authentication, authorization, encryption, audit controls, retention/deletion policies, monitoring, model governance, and institution-specific legal/compliance review.

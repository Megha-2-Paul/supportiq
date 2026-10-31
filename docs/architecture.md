# Architecture and design

## Request lifecycle
1. A message enters through Streamlit or the FastAPI contract.
2. Pydantic validates type and length; the service rejects blank or too-short messages.
3. A persisted scikit-learn pipeline predicts a Banking77 intent.
4. The application returns the predicted intent and the model's maximum class probability when supported. This score is not automatically calibrated.
5. Separate decision modules recommend a support department and rules-based urgency.
6. Sentiment remains explicitly unavailable unless a separate sentiment model is configured.
7. SQLite records the result for local demo history.

## Model development
The baseline uses TF-IDF word unigrams/bigrams and Logistic Regression. Training uses the upstream Banking77 train split; evaluation uses its official test split. Report accuracy, macro-F1, weighted-F1, and per-class precision/recall/F1. Do not use the test split for tuning. A future DistilBERT experiment must split validation data from the training split and only evaluate the final candidate once on the official test set.

## Design choices
- Keep training code separate from inference code.
- Keep routing and priority logic deterministic, inspectable, and independently tested.
- Use a human-review flag for low confidence or unavailable confidence.
- Store only local demo history; this is not a production retention or access-control design.
- Do not silently replace a missing model with fabricated predictions.

# Portfolio demonstration guide

## 90-second walkthrough
1. Open the SupportIQ dashboard and explain the problem: support teams receive many free-text requests and need consistent triage.
2. Show a synthetic ticket in the single-ticket analysis page.
3. Explain the predicted intent, confidence score, recommended department, and priority rationale.
4. Upload the sample CSV and demonstrate batch classification plus CSV export.
5. Open ticket history and the analytics overview.
6. Explain the ML evaluation report and how macro-F1 is used for a multi-class, potentially imbalanced problem.
7. Close with limitations: public benchmark data, separate sentiment model, rules-based priority, and human review.

## Suggested synthetic demo messages
- "My cash withdrawal was debited but no cash came out."
- "I cannot log in to my mobile banking app."
- "I do not recognize a card payment on my statement."
- "How long does an international transfer usually take?"

Never record real customer information. Avoid showing environment files, credentials, private datasets, or local database contents.

## Portfolio screenshots
Capture the overview after synthetic demo predictions, a single-ticket result, batch CSV results, history, and the model-performance page after running training. Do not invent metric values or claim results before the evaluation script has been run.

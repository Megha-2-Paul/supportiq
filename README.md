# SupportIQ

Intelligent Banking Customer Support Classification & Analytics.

A portfolio-grade demonstration combining banking intent classification, human-reviewed routing and priority recommendations, sentiment analysis, analytics, FastAPI, Streamlit, SQLite, tests, and Docker.

> **Responsible use:** This is a demonstration and decision-support tool, not a production banking system. Do not submit real credentials, payment-card data, account identifiers, or other sensitive customer information.

## Modeling notes

The intended intent dataset is [Banking77](https://huggingface.co/datasets/PolyAI/banking77). It contains intent labels only; it does not provide sentiment or priority targets. Sentiment will use a separately documented model/data source, and priority will remain transparent configurable rules rather than a fabricated supervised classifier. Model selection will use held-out evaluation, including macro-F1 and per-class metrics.

The repository is being initialized on `feature/supportiq`; `main` is intentionally left unchanged.

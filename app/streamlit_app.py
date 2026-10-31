"""SupportIQ Streamlit dashboard."""
import json
import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="SupportIQ | Banking Intelligence",
    page_icon="◈",
    layout="wide",
)
API = os.getenv("SUPPORTIQ_API_URL", "http://localhost:8000")
CONFIDENCE_THRESHOLD = float(os.getenv("SUPPORTIQ_CONFIDENCE_THRESHOLD", "0.55"))
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.8rem; max-width: 1280px}
    [data-testid="stMetric"] {
        background: #111c2d; border: 1px solid #26364b;
        padding: 16px; border-radius: 12px;
    }
    .hero {
        padding: 22px 26px; border-radius: 16px;
        background: linear-gradient(110deg,#10243a,#183b52);
        border: 1px solid #2b5065;
    }
    .small-muted {color: #9eb0c2; font-size: .9rem}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero"><h1>◈ SupportIQ</h1><p class="small-muted">'
    "Banking support intelligence · ticket classification and operational insights"
    "</p></div>",
    unsafe_allow_html=True,
)
st.warning(
    "Portfolio demonstration only. Use synthetic examples. Never enter real credentials, "
    "account numbers, payment data, or authentication codes."
)
page = st.sidebar.radio(
    "Workspace",
    [
        "Overview",
        "Classify a ticket",
        "Batch analysis",
        "Ticket history",
        "Model performance",
        "About & limitations",
    ],
)


def call_api(text):
    response = requests.post(
        f"{API}/api/v1/predict", json={"text": text}, timeout=45
    )
    response.raise_for_status()
    return response.json()


def load_history():
    response = requests.get(
        f"{API}/api/v1/history", params={"limit": 1000}, timeout=20
    )
    response.raise_for_status()
    return pd.DataFrame(response.json().get("items", []))


if page == "Overview":
    st.subheader("Support operations at a glance")
    try:
        history = load_history()
        if history.empty:
            st.info(
                "No predictions recorded yet. Start with a sample ticket to populate "
                "the dashboard."
            )
        else:
            col1, col2, col3 = st.columns(3)
            col1.metric("Tickets analyzed", len(history))
            col2.metric("Most common intent", str(history["intent"].mode().iloc[0]))
            col3.metric(
                "Human review flagged",
                int((history["confidence"] < CONFIDENCE_THRESHOLD).sum()),
            )
            left, right = st.columns(2)
            with left:
                st.markdown("#### Intent distribution")
                st.bar_chart(history["intent"].value_counts().head(12))
            with right:
                st.markdown("#### Priority recommendations")
                st.bar_chart(history["priority"].value_counts())
    except requests.RequestException:
        st.info("Connect the API and begin classifying tickets to populate live analytics.")
    st.caption("Analytics reflect only locally recorded demo predictions.")

elif page == "Classify a ticket":
    st.subheader("Single-ticket analysis")
    message = st.text_area(
        "Customer message",
        height=150,
        placeholder="Example: My cash withdrawal was debited but no cash came out.",
    )
    if st.button("Analyze ticket", type="primary", disabled=len(message.strip()) < 3):
        try:
            result = call_api(message)
            col1, col2, col3 = st.columns(3)
            col1.metric("Predicted intent", result["intent"])
            col2.metric("Model confidence", f'{result["confidence"]:.1%}')
            col3.metric("Suggested priority", result["priority"])
            st.write("**Recommended team:**", result["department"])
            st.write("**Sentiment:**", result["sentiment"])
            st.write("**Priority rationale:**", ", ".join(result.get("priority_reasons", [])))
            if result["needs_human_review"]:
                st.warning(
                    "Human review recommended: confidence is below the configured "
                    "threshold or unavailable."
                )
            st.caption(
                "Priority is a rules-based suggestion. Sentiment is not configured "
                "unless a separately evaluated model is installed."
            )
        except requests.RequestException as exc:
            st.error(f"Could not reach API at {API}: {exc}")

elif page == "Batch analysis":
    st.subheader("Batch CSV / Excel analysis")
    sample_path = Path("data/samples/sample_tickets.csv")
    if sample_path.exists():
        st.download_button(
            "Download sample CSV",
            sample_path.read_bytes(),
            file_name="supportiq_sample_tickets.csv",
            mime="text/csv",
        )
    file = st.file_uploader("Upload a file with a message column", type=["csv", "xlsx"])
    if file:
        try:
            frame = (
                pd.read_csv(file)
                if file.name.lower().endswith(".csv")
                else pd.read_excel(file)
            )
            st.dataframe(frame.head(10), use_container_width=True)
            if "message" not in frame.columns:
                st.error("Your file must contain a message column.")
            elif len(frame) > 1000:
                st.error("Maximum 1,000 rows per batch.")
            else:
                messages = frame["message"].fillna("").astype(str).str.strip()
                valid = messages[messages.str.len() >= 3]
                skipped = len(frame) - len(valid)
                st.caption(f"{len(valid)} valid messages · {skipped} blank or too-short rows will be skipped")
                if st.button("Classify batch", disabled=valid.empty):
                    payload = {
                        "tickets": [{"text": value} for value in valid.tolist()]
                    }
                    response = requests.post(
                        f"{API}/api/v1/predict/batch",
                        json=payload,
                        timeout=120,
                    )
                    response.raise_for_status()
                    results = pd.DataFrame(response.json()["results"])
                    output = results.copy()
                    output.insert(0, "source_row", valid.index + 2)
                    st.success(f"Classified {len(results)} tickets.")
                    st.dataframe(output, use_container_width=True, hide_index=True)
                    st.download_button(
                        "Download predictions CSV",
                        output.to_csv(index=False).encode("utf-8"),
                        "supportiq_predictions.csv",
                        "text/csv",
                    )
        except (requests.RequestException, ValueError, OSError) as exc:
            st.error(f"Batch processing failed: {exc}")

elif page == "Ticket history":
    st.subheader("Recent ticket predictions")
    try:
        history = load_history()
        if history.empty:
            st.info("No ticket history yet.")
        else:
            st.dataframe(history, use_container_width=True, hide_index=True)
            st.download_button(
                "Export history CSV",
                history.to_csv(index=False).encode("utf-8"),
                "supportiq_history.csv",
                "text/csv",
            )
    except requests.RequestException as exc:
        st.error(f"Could not load history: {exc}")

elif page == "Model performance":
    st.subheader("Model evaluation")
    report_path = Path("reports/baseline_metrics.json")
    if report_path.exists():
        metrics = json.loads(report_path.read_text(encoding="utf-8"))
        col1, col2, col3 = st.columns(3)
        col1.metric("Accuracy", f'{metrics["accuracy"]:.3f}')
        col2.metric("Macro-F1", f'{metrics["macro_f1"]:.3f}')
        col3.metric("Weighted-F1", f'{metrics["weighted_f1"]:.3f}')
        st.caption(f'Dataset: {metrics.get("dataset")} · Split: {metrics.get("split")}')
        report = metrics.get("classification_report", {})
        rows = [
            {"class": key, **value}
            for key, value in report.items()
            if isinstance(value, dict) and "f1-score" in value
        ]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info(
            "No evaluation report found. Train the baseline model using the command "
            "in docs/development.md. No performance figures are fabricated."
        )

else:
    st.subheader("About SupportIQ")
    st.markdown(
        """
        - **Intent model:** intended to be trained on the public Banking77 benchmark;
          it is not trained on private bank tickets.
        - **Priority:** transparent keyword rules, not a supervised ML model or fraud detector.
        - **Sentiment:** not configured until a separately sourced and evaluated model is selected.
        - **Confidence:** scores may be uncalibrated; uncertain predictions should be reviewed.
        - **Privacy:** this prototype does not provide production-grade banking security,
          retention controls, or compliance guarantees.
        """
    )

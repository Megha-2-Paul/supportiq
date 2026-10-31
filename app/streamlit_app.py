"""SupportIQ Streamlit dashboard."""
import json
import os
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="SupportIQ | Banking Intelligence", page_icon="◈", layout="wide")
API = os.getenv("SUPPORTIQ_API_URL", "http://localhost:8000")
st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1280px}
[data-testid="stMetric"]{background:#111c2d;border:1px solid #26364b;padding:16px;border-radius:12px}
.hero{padding:22px 26px;border-radius:16px;background:linear-gradient(110deg,#10243a,#183b52);border:1px solid #2b5065}
.small-muted{color:#9eb0c2;font-size:.9rem}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>◈ SupportIQ</h1><p class="small-muted">Banking support intelligence · ticket classification and operational insights</p></div>', unsafe_allow_html=True)
st.warning("Portfolio demonstration only. Use synthetic examples. Never enter real credentials, account numbers, payment data, or authentication codes.")
page = st.sidebar.radio("Workspace", ["Overview", "Classify a ticket", "Batch analysis", "Ticket history", "Model performance", "About & limitations"])

def call_api(text):
    response = requests.post(f"{API}/api/v1/predict", json={"text": text}, timeout=45)
    response.raise_for_status()
    return response.json()

def load_history():
    response = requests.get(f"{API}/api/v1/history", params={"limit": 1000}, timeout=20)
    response.raise_for_status()
    return pd.DataFrame(response.json().get("items", []))

if page == "Overview":
    st.subheader("Support operations at a glance")
    try:
        history = load_history()
        if history.empty:
            st.info("No predictions recorded yet. Start with a sample ticket to populate the dashboard.")
        else:
            a,b,c = st.columns(3)
            a.metric("Tickets analyzed", len(history))
            b.metric("Most common intent", str(history["intent"].mode().iloc[0]))
            c.metric("Human review flagged", int((history["confidence"] < 0.55).sum()))
            left,right = st.columns(2)
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
    text = st.text_area("Customer message", height=150, placeholder="Example: My cash withdrawal was debited but no cash came out.")
    if st.button("Analyze ticket", type="primary", disabled=len(text.strip()) < 3):
        try:
            result = call_api(text)
            a,b,c = st.columns(3)
            a.metric("Predicted intent", result["intent"])
            b.metric("Model confidence", f'{result["confidence"]:.1%}')
            c.metric("Suggested priority", result["priority"])
            st.write("**Recommended team:**", result["department"])
            st.write("**Sentiment:**", result["sentiment"])
            if result["needs_human_review"]:
                st.warning("Human review recommended: confidence is below threshold or unavailable.")
            st.caption("Priority is a rules-based suggestion; sentiment is not configured unless a separately evaluated model is installed.")
        except requests.RequestException as exc:
            st.error(f"Could not reach API at {API}: {exc}")
elif page == "Batch analysis":
    st.subheader("Batch CSV / Excel analysis")
    file = st.file_uploader("Upload a file with a message column", type=["csv","xlsx"])
    if file:
        try:
            frame = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
            st.dataframe(frame.head(10), use_container_width=True)
            if "message" not in frame.columns:
                st.error("Your file must contain a message column.")
            elif len(frame) > 1000:
                st.error("Maximum 1,000 rows per batch.")
            elif st.button("Classify batch"):
                valid = frame["message"].fillna("").astype(str)
                payload = {"tickets":[{"text":m.strip()} for m in valid if len(m.strip()) >= 3]}
                response = requests.post(f"{API}/api/v1/predict/batch", json=payload, timeout=120)
                response.raise_for_status()
                results = response.json()["results"]
                result_frame = pd.DataFrame(results)
                st.dataframe(result_frame, use_container_width=True)
                st.download_button("Download predictions CSV", result_frame.to_csv(index=False).encode(), "supportiq_predictions.csv", "text/csv")
        except Exception as exc:
            st.error(f"Batch processing failed: {exc}")
elif page == "Ticket history":
    st.subheader("Recent ticket predictions")
    try:
        history = load_history()
        if history.empty:
            st.info("No ticket history yet.")
        else:
            st.dataframe(history, use_container_width=True, hide_index=True)
            st.download_button("Export history CSV", history.to_csv(index=False).encode(), "supportiq_history.csv", "text/csv")
    except requests.RequestException as exc:
        st.error(f"Could not load history: {exc}")
elif page == "Model performance":
    st.subheader("Model evaluation")
    report_path = Path("reports/baseline_metrics.json")
    if report_path.exists():
        metrics = json.loads(report_path.read_text(encoding="utf-8"))
        a,b,c = st.columns(3)
        a.metric("Accuracy", f'{metrics["accuracy"]:.3f}')
        b.metric("Macro-F1", f'{metrics["macro_f1"]:.3f}')
        c.metric("Weighted-F1", f'{metrics["weighted_f1"]:.3f}')
        st.caption(f'Dataset: {metrics.get("dataset")} · Split: {metrics.get("split")}')
        report = metrics.get("classification_report", {})
        rows = [{"class":k,**v} for k,v in report.items() if isinstance(v,dict) and "f1-score" in v]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No evaluation report found. Train the baseline model using the command in docs/development.md.")
else:
    st.subheader("About SupportIQ")
    st.markdown("""
- **Intent model:** trained on the public Banking77 benchmark; not trained on private bank tickets.
- **Priority:** transparent keyword rules, not a supervised ML model or fraud detector.
- **Sentiment:** Not configured until a separately sourced and evaluated model is selected.
- **Confidence:** scores may be uncalibrated; uncertain predictions should be reviewed by a person.
- **Privacy:** this prototype does not provide production-grade banking security, retention controls, or compliance guarantees.
""")

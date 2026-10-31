"""SupportIQ — polished Streamlit banking-support intelligence workspace."""
import json
import os
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="SupportIQ | Support intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

API = os.getenv("SUPPORTIQ_API_URL", "http://localhost:8000")
CONFIDENCE_THRESHOLD = float(os.getenv("SUPPORTIQ_CONFIDENCE_THRESHOLD", "0.55"))
REPORT_PATH = Path("reports/baseline_metrics.json")
SAMPLE_PATH = Path("data/samples/sample_tickets.csv")

# A warm, restrained palette: forest, sage, ivory and copper.
st.markdown(
    """
    <style>
    :root {
      --forest: #173b36;
      --forest-2: #285b50;
      --sage: #a9c2b3;
      --sage-pale: #e8efe9;
      --ivory: #f5f3ec;
      --paper: #fffefa;
      --ink: #202d2a;
      --muted: #71817a;
      --copper: #b77d4d;
      --line: #e2e7df;
    }
    .stApp { background: var(--ivory); color: var(--ink); }
    [data-testid="stHeader"] { background: rgba(245,243,236,.92); }
    .block-container { max-width: 1440px; padding-top: 1.35rem; padding-bottom: 3rem; }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #173b36 0%, #102d29 100%);
      border-right: 1px solid #294c44;
    }
    [data-testid="stSidebar"] * { color: #f3f5ef !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
      padding: .42rem .55rem; border-radius: 9px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
      background: rgba(255,255,255,.09);
    }
    [data-testid="stMetric"] {
      background: var(--paper); border: 1px solid var(--line);
      border-radius: 15px; padding: 17px 18px;
      box-shadow: 0 3px 12px rgba(23,59,54,.035);
    }
    [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: .83rem; }
    [data-testid="stMetricValue"] { color: var(--forest) !important; font-weight: 700; }
    [data-testid="stMetricDelta"] { font-size: .78rem; }
    h1, h2, h3 { color: var(--forest) !important; letter-spacing: -.025em; }
    h1 { font-weight: 750 !important; }
    h2, h3 { font-weight: 680 !important; }
    p, li, label { color: var(--ink); }
    [data-testid="stVerticalBlockBorderWrapper"] {
      background: var(--paper); border-color: var(--line) !important;
      border-radius: 15px;
    }
    .brand-lockup { padding: 8px 4px 22px; }
    .brand-mark {
      display: inline-flex; width: 38px; height: 38px; align-items: center;
      justify-content: center; border-radius: 12px; background: #dce9df;
      color: var(--forest); font-size: 22px; font-weight: 800; margin-right: 9px;
    }
    .brand-name { color: #fff; font-size: 1.28rem; font-weight: 750; vertical-align: middle; }
    .brand-caption { color: #b7cbc1; font-size: .76rem; margin: 7px 0 0 2px; }
    .eyebrow {
      color: var(--forest-2); text-transform: uppercase; letter-spacing: .13em;
      font-size: .69rem; font-weight: 800; margin-bottom: 5px;
    }
    .page-intro {
      background: linear-gradient(112deg, #fffefa 0%, #edf2eb 100%);
      border: 1px solid var(--line); border-radius: 18px;
      padding: 23px 26px; margin: 2px 0 20px;
    }
    .page-intro p { color: var(--muted); margin: 5px 0 0; font-size: .93rem; }
    .status-pill {
      display: inline-block; padding: 6px 10px; border-radius: 30px;
      background: #e5eee7; color: #285b50; font-size: .73rem; font-weight: 700;
      border: 1px solid #d2e1d5;
    }
    .section-kicker {
      color: var(--muted); text-transform: uppercase; letter-spacing: .1em;
      font-size: .68rem; font-weight: 800; margin: 17px 0 8px;
    }
    .note-card {
      background: #edf2eb; border-left: 3px solid var(--copper);
      padding: 12px 15px; border-radius: 8px; color: #44534c; font-size: .84rem;
    }
    div.stButton > button[kind="primary"] {
      background: var(--forest-2); border: 1px solid var(--forest-2);
      border-radius: 9px; color: white; font-weight: 650;
    }
    div.stButton > button[kind="primary"]:hover {
      background: var(--forest); border-color: var(--forest);
    }
    div.stButton > button, [data-testid="stDownloadButton"] button {
      border-radius: 9px; border-color: #d4ded5;
    }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 10px; }
    [data-testid="stAlert"] { border-radius: 10px; }
    hr { border-color: var(--line); }
    /* Subtle motion: polished feedback without distracting from data. */
    @keyframes riseIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes softPulse {
      0%, 100% { box-shadow: 0 3px 12px rgba(23,59,54,.04); }
      50% { box-shadow: 0 7px 22px rgba(20,184,140,.12); }
    }
    @keyframes statusGlow {
      0%, 100% { opacity: .72; }
      50% { opacity: 1; }
    }
    .page-intro { animation: riseIn .48s ease-out both; }
    [data-testid="stMetric"] {
      animation: riseIn .55s ease-out both;
      transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
    }
    [data-testid="stMetric"]:hover {
      transform: translateY(-3px);
      border-color: #9bbdaf;
      animation: softPulse 2.4s ease-in-out infinite;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
      transition: border-color .2s ease, box-shadow .2s ease, transform .2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
      border-color: #b6cec0 !important;
      box-shadow: 0 7px 20px rgba(23,59,54,.055);
    }
    div.stButton > button, [data-testid="stDownloadButton"] button {
      transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
    }
    div.stButton > button:hover, [data-testid="stDownloadButton"] button:hover {
      transform: translateY(-1px);
      box-shadow: 0 5px 13px rgba(23,59,54,.12);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
      transition: background .18s ease, transform .18s ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
      transform: translateX(3px);
    }
    [data-testid="stDataFrame"] { animation: riseIn .4s ease-out both; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .01ms !important;
      }
    }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="brand-lockup">
      <span class="brand-mark">◈</span><span class="brand-name">SupportIQ</span>
      <div class="brand-caption">BANKING SUPPORT INTELLIGENCE</div>
    </div>
    """,
    unsafe_allow_html=True,
)
page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Overview",
        "Classify a ticket",
        "Batch analysis",
        "Ticket history",
        "Model performance",
        "About & limitations",
    ],
    label_visibility="visible",
)
st.sidebar.markdown("---")
st.sidebar.markdown(
    '<div style="font-size:.72rem;color:#b7cbc1 !important">'
    "PORTFOLIO EDITION · v1.0<br/>Public Banking77 benchmark</div>",
    unsafe_allow_html=True,
)


def page_header(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f'<div class="page-intro"><div class="eyebrow">{kicker}</div>'
        f'<h1 style="margin:0;font-size:1.85rem">{title}</h1>'
        f"<p>{description}</p></div>",
        unsafe_allow_html=True,
    )


def call_api(text: str) -> dict:
    response = requests.post(
        f"{API}/api/v1/predict", json={"text": text}, timeout=45
    )
    response.raise_for_status()
    return response.json()


def load_history() -> pd.DataFrame:
    response = requests.get(
        f"{API}/api/v1/history", params={"limit": 1000}, timeout=20
    )
    response.raise_for_status()
    return pd.DataFrame(response.json().get("items", []))


def show_privacy_notice() -> None:
    st.markdown(
        '<div class="note-card"><strong>Demo data only.</strong> Use synthetic '
        "examples. Never enter real credentials, account numbers, payment data, "
        "authentication codes or private customer records.</div>",
        unsafe_allow_html=True,
    )


if page == "Overview":
    page_header(
        "WORKSPACE OVERVIEW",
        "Support operations",
        "A live view of locally recorded ticket predictions and model insights.",
    )
    show_privacy_notice()
    try:
        history = load_history()
        if history.empty:
            st.markdown("### Your workspace is ready")
            st.info(
                "No predictions have been recorded yet. Start by classifying a "
                "sample ticket or uploading a small demo CSV. Your dashboard "
                "metrics will populate from actual local prediction history."
            )
        else:
            total = len(history)
            review_count = int(
                (pd.to_numeric(history["confidence"], errors="coerce")
                 < CONFIDENCE_THRESHOLD).sum()
            )
            most_common = str(history["intent"].mode().iloc[0])
            average_confidence = pd.to_numeric(
                history["confidence"], errors="coerce"
            ).mean()
            st.markdown('<div class="section-kicker">LIVE ACTIVITY</div>', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Tickets analyzed", f"{total:,}")
            c2.metric("Most frequent intent", most_common.replace("_", " ").title())
            c3.metric("Review recommended", f"{review_count:,}")
            c4.metric(
                "Average confidence",
                f"{average_confidence:.1%}" if pd.notna(average_confidence) else "—",
            )
            left, right = st.columns([1.35, 1])
            with left:
                st.markdown("### Intent landscape")
                st.caption("Most frequent predicted intents in local history")
                intent_counts = history["intent"].value_counts().head(10)
                st.bar_chart(intent_counts, color="#527d6d")
            with right:
                st.markdown("### Priority mix")
                st.caption("Rule-based priority recommendations")
                priority_counts = history["priority"].value_counts()
                st.bar_chart(priority_counts, color="#b77d4d")
            st.markdown("### Latest predictions")
            display_cols = [
                col for col in ["created_at", "text", "intent", "priority", "confidence"]
                if col in history.columns
            ]
            st.dataframe(
                history[display_cols].head(8),
                use_container_width=True,
                hide_index=True,
            )
    except requests.RequestException:
        st.error(
            f"The API is unavailable at {API}. Start the FastAPI service, then "
            "refresh this page."
        )
    st.caption("Dashboard analytics are based only on locally recorded demo predictions.")

elif page == "Classify a ticket":
    page_header(
        "TICKET WORKBENCH",
        "Classify a customer message",
        "Run an intent prediction and inspect the suggested routing and review signals.",
    )
    show_privacy_notice()
    with st.container(border=True):
        message = st.text_area(
            "Customer message",
            height=155,
            placeholder="Example: My cash withdrawal was debited but no cash came out.",
            help="Use a fictional or synthetic support message for this demonstration.",
        )
        analyze = st.button(
            "Analyze ticket",
            type="primary",
            disabled=len(message.strip()) < 3,
        )
    if analyze:
        try:
            result = call_api(message.strip())
            st.markdown("### Prediction result")
            c1, c2, c3 = st.columns(3)
            c1.metric("Predicted intent", result["intent"].replace("_", " ").title())
            c2.metric("Model confidence", f'{result["confidence"]:.1%}')
            c3.metric("Suggested priority", result["priority"].title())
            with st.container(border=True):
                st.markdown("**Recommended team**")
                st.write(result["department"])
                st.markdown("**Priority rationale**")
                reasons = result.get("priority_reasons", [])
                st.write(", ".join(reasons) if reasons else "No priority keywords matched.")
                st.markdown("**Sentiment**")
                st.write(result["sentiment"])
            if result["needs_human_review"]:
                st.warning(
                    "Human review recommended: confidence is below the configured "
                    "threshold or unavailable."
                )
            st.caption(
                "Priority is a rules-based suggestion. Sentiment is not configured "
                "unless a separately evaluated model is installed. Confidence may "
                "be uncalibrated and is not a measure of certainty."
            )
        except requests.RequestException as exc:
            st.error(f"Could not reach API at {API}: {exc}")

elif page == "Batch analysis":
    page_header(
        "BATCH WORKBENCH",
        "Analyze tickets in batches",
        "Upload a CSV or Excel file, classify valid messages and export the results.",
    )
    show_privacy_notice()
    if SAMPLE_PATH.exists():
        st.download_button(
            "Download sample CSV",
            SAMPLE_PATH.read_bytes(),
            file_name="supportiq_sample_tickets.csv",
            mime="text/csv",
        )
    file = st.file_uploader(
        "Choose a CSV or Excel file with a message column",
        type=["csv", "xlsx"],
    )
    if file:
        try:
            frame = (
                pd.read_csv(file)
                if file.name.lower().endswith(".csv")
                else pd.read_excel(file)
            )
            st.markdown("### File preview")
            st.dataframe(frame.head(10), use_container_width=True, hide_index=True)
            if "message" not in frame.columns:
                st.error("Your file must contain a column named message.")
            elif len(frame) > 1000:
                st.error("Maximum 1,000 rows per batch.")
            else:
                messages = frame["message"].fillna("").astype(str).str.strip()
                valid = messages[messages.str.len() >= 3]
                skipped = len(frame) - len(valid)
                a, b = st.columns(2)
                a.metric("Valid messages", f"{len(valid):,}")
                b.metric("Rows skipped", f"{skipped:,}")
                if st.button("Classify batch", type="primary", disabled=valid.empty):
                    payload = {"tickets": [{"text": value} for value in valid.tolist()]}
                    response = requests.post(
                        f"{API}/api/v1/predict/batch",
                        json=payload,
                        timeout=120,
                    )
                    response.raise_for_status()
                    results = pd.DataFrame(response.json()["results"])
                    output = results.copy()
                    output.insert(0, "source_row", valid.index + 2)
                    st.success(f"Successfully classified {len(results)} tickets.")
                    st.dataframe(
                        output, use_container_width=True, hide_index=True
                    )
                    st.download_button(
                        "Download predictions CSV",
                        output.to_csv(index=False).encode("utf-8"),
                        "supportiq_predictions.csv",
                        "text/csv",
                    )
        except (requests.RequestException, ValueError, OSError) as exc:
            st.error(f"Batch processing failed: {exc}")

elif page == "Ticket history":
    page_header(
        "LOCAL RECORDS",
        "Ticket history",
        "Review and export predictions recorded by this local demo instance.",
    )
    try:
        history = load_history()
        if history.empty:
            st.info("No ticket history yet. Analyze a sample ticket to create the first record.")
        else:
            st.metric("Recorded predictions", f"{len(history):,}")
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
    page_header(
        "MODEL CARD",
        "Model performance",
        "Evaluation results from the public Banking77 benchmark test split.",
    )
    if REPORT_PATH.exists():
        try:
            metrics = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
            c1, c2, c3 = st.columns(3)
            c1.metric("Accuracy", f'{metrics["accuracy"]:.2%}')
            c2.metric("Macro-F1", f'{metrics["macro_f1"]:.2%}')
            c3.metric("Weighted-F1", f'{metrics["weighted_f1"]:.2%}')
            st.caption(
                f'Dataset: {metrics.get("dataset", "Banking77")} · '
                f'Split: {metrics.get("split", "official test")}'
            )
            report = metrics.get("classification_report", {})
            rows = [
                {"Intent": key.replace("_", " ").title(), **value}
                for key, value in report.items()
                if isinstance(value, dict) and "f1-score" in value
            ]
            if rows:
                st.markdown("### Per-intent evaluation")
                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True,
                )
        except (OSError, ValueError, KeyError, TypeError) as exc:
            st.error(f"Could not read the model evaluation report: {exc}")
    else:
        st.info(
            "No evaluation report found. Train the baseline model using the "
            "instructions in docs/development.md. No performance figures are fabricated."
        )
    st.markdown(
        '<div class="note-card">Benchmark results describe performance on the '
        "public Banking77 dataset only. They are not a guarantee of performance "
        "on private customer messages or in a live banking environment.</div>",
        unsafe_allow_html=True,
    )

else:
    page_header(
        "PROJECT NOTES",
        "About SupportIQ",
        "A transparent portfolio prototype for support-ticket classification and triage.",
    )
    with st.container(border=True):
        st.markdown("### What the prototype demonstrates")
        st.markdown(
            "- **Intent model:** TF-IDF features and Logistic Regression trained "
            "against the public Banking77 benchmark (77 intent classes).\n"
            "- **Priority:** explainable keyword rules, not a supervised priority "
            "classifier or fraud detector.\n"
            "- **Sentiment:** not configured unless a separately sourced and "
            "evaluated model is installed.\n"
            "- **Confidence:** maximum class probability may be uncalibrated; "
            "uncertain predictions require human review.\n"
            "- **Engineering:** Python, scikit-learn, FastAPI, Streamlit, SQLite "
            "and Docker."
        )
    with st.container(border=True):
        st.markdown("### Responsible-use limitations")
        st.markdown(
            "This is not production banking software. It does not include "
            "production authentication, authorization, encryption, retention "
            "controls, regulated-data safeguards, audit trails, monitoring or "
            "institution-specific compliance review. Do not use it for automated "
            "account restrictions, fraud determinations, credit decisions or "
            "other high-impact decisions. Human review is required."
        )

"""SupportIQ Streamlit user interface."""
import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="SupportIQ | Banking Intelligence", page_icon="◈", layout="wide")
API = os.getenv("SUPPORTIQ_API_URL", "http://localhost:8000")
st.markdown("""<style>
.block-container{padding-top:2rem;max-width:1250px}
[data-testid="stMetric"]{background:#111c2d;border:1px solid #26364b;padding:16px;border-radius:12px}
.hero{padding:22px 26px;border-radius:16px;background:linear-gradient(110deg,#10243a,#183b52);border:1px solid #2b5065}
.small-muted{color:#9eb0c2;font-size:0.9rem}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>◈ SupportIQ</h1><p class="small-muted">Banking support intelligence · ticket classification and operational insights</p></div>', unsafe_allow_html=True)
st.warning("Portfolio demonstration only. Use synthetic examples. Never enter real customer credentials, account numbers, payment-card data, or authentication codes.")
page = st.sidebar.radio("Workspace", ["Overview", "Classify a ticket", "Batch analysis", "About & limitations"])
def call_api(text):
    response = requests.post(f"{API}/api/v1/predict", json={"text": text}, timeout=45)
    response.raise_for_status()
    return response.json()

if page == "Overview":
    st.subheader("A clearer view of customer support demand")
    c1,c2,c3 = st.columns(3)
    c1.metric("Intent taxonomy", "Banking77", "77 intents")
    c2.metric("Inference modes", "Single + batch")
    c3.metric("Decision support", "Human reviewed")
    st.markdown("### Product capabilities")
    st.write("Intent classification · department recommendations · transparent priority rules · prediction confidence · API integration.")
    st.info("Train the baseline model using the documented ML command before running live classification.")
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
                st.warning("Human review recommended: confidence is below the configured threshold or unavailable.")
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
                results = []
                for message in frame["message"].fillna("").astype(str):
                    if len(message.strip()) < 3:
                        results.append({"intent":"Invalid / empty","confidence":0.0,"department":"Manual review","priority":"Unknown","sentiment":"Not configured","needs_human_review":True})
                    else:
                        results.append(call_api(message))
                output = pd.concat([frame.reset_index(drop=True),pd.DataFrame(results)],axis=1)
                st.dataframe(output,use_container_width=True)
                st.download_button("Download results CSV",output.to_csv(index=False).encode(), "supportiq_predictions.csv","text/csv")
        except Exception as exc:
            st.error(f"Batch processing failed: {exc}")
else:
    st.subheader("About SupportIQ")
    st.markdown("""
- **Intent model:** trained on the public Banking77 benchmark; not trained on a bank's private tickets.
- **Priority:** transparent keyword rules, not a supervised ML model or fraud detector.
- **Sentiment:** explicitly Not configured until a separately sourced and evaluated model is selected.
- **Confidence:** model scores may be uncalibrated; uncertain predictions should be reviewed by a person.
- **Privacy:** this prototype does not provide production-grade banking security, retention controls, or compliance guarantees.
""")

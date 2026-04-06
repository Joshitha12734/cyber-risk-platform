import streamlit as st
import pandas as pd
import json
import os

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Enterprise Cyber Risk Platform", layout="wide")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "Outputs")

# ==============================
# LOGIN SYSTEM
# ==============================
def login():
    st.title("🔐 CRQ Platform Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "test1234":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ==============================
# LOAD DATA (FIXED + LLM READY)
# ==============================
@st.cache_data
def load_data():
    file_path = os.path.join(OUTPUT_DIR, "final_risk.json")

    with open(file_path) as f:
        data = json.load(f)

    # ✅ Extract results correctly
    if "results" in data:
        df = pd.DataFrame(data["results"])
    else:
        st.error("Invalid data format: 'results' key missing")
        return pd.DataFrame()

    # ✅ Normalize column names (REAL-WORLD FIX)
    df = df.rename(columns={
        "asset_id": "asset",
        "business_risk": "risk_score",
        "llm_business_explanation": "llm_explanation"
    })

    return df

df = load_data()

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔎 Controls")

risk_levels = st.sidebar.multiselect(
    "Risk Level",
    options=df["risk_level"].unique(),
    default=df["risk_level"].unique()
)

assets = st.sidebar.multiselect(
    "Assets",
    options=df["asset"].unique(),
    default=df["asset"].unique()
)

# ==============================
# FILTER DATA
# ==============================
filtered_df = df[
    (df["risk_level"].isin(risk_levels)) &
    (df["asset"].isin(assets))
]

# ==============================
# TITLE
# ==============================
st.title("🔐 Enterprise Cyber Risk Quantification Platform")
st.markdown("### Translating Technical Vulnerabilities into Business Risk Decisions")

# ==============================
# EXECUTIVE METRICS
# ==============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Risks", len(filtered_df))
col2.metric("Critical Risks", len(filtered_df[filtered_df["risk_level"] == "Critical"]))
col3.metric("High Risks", len(filtered_df[filtered_df["risk_level"] == "High"]))

# ==============================
# TOP RISKS
# ==============================
st.subheader("🔥 Top Risks")

top_risks = filtered_df.sort_values(by="risk_score", ascending=False).head(5)

for _, row in top_risks.iterrows():
    st.error(f"{row['cve_id']} | {row['asset']} | Risk: {row['risk_score']}")

# ==============================
# FULL TABLE (NO ERRORS)
# ==============================
st.subheader("📋 Full Risk Table")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("### 📊 Risk Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Average Risk Score", round(filtered_df["risk_score"].mean(), 2))
    col2.metric("Max Risk Score", filtered_df["risk_score"].max())
    col3.metric("Min Risk Score", filtered_df["risk_score"].min())
else:
    st.info("No data available")

# ==============================
# CHART
# ==============================
st.subheader("📈 Risk Distribution")

risk_counts = filtered_df["risk_level"].value_counts()
st.bar_chart(risk_counts)

# ==============================
# LLM SECTION (KEY FEATURE)
# ==============================
st.subheader("🧠 AI Business Explanation")

selected_cve = st.selectbox("Select CVE", filtered_df["cve_id"].unique())

selected_row = filtered_df[filtered_df["cve_id"] == selected_cve].iloc[0]

if "llm_explanation" in selected_row and pd.notna(selected_row["llm_explanation"]):
    st.info(selected_row["llm_explanation"])
else:
    st.warning("No AI explanation available")

# ==============================
# INSIGHTS
# ==============================
st.subheader("🧠 Insights")

if len(filtered_df[filtered_df["risk_level"] == "Critical"]) > 5:
    st.warning("⚠️ High number of critical risks detected!")

if not filtered_df.empty:
    most_risky_asset = filtered_df.groupby("asset")["risk_score"].mean().idxmax()
    st.success(f"Most at-risk asset: {most_risky_asset}")

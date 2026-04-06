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
# LOGIN
# ==============================
def login():
    st.title("🔐 CRQ Platform Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "admin123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    file_path = os.path.join(OUTPUT_DIR, "final_risk.json")

    with open(file_path) as f:
        data = json.load(f)

    if "results" not in data:
        st.error("Invalid JSON format")
        return pd.DataFrame()

    df = pd.DataFrame(data["results"])

    # Rename columns (enterprise standard)
    df = df.rename(columns={
        "asset_id": "asset",
        "business_risk": "risk_score",
        "llm_business_explanation": "llm_explanation"
    })

    return df

df = load_data()

# ==============================
# SIDEBAR
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
# FILTER
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
# METRICS
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
# DASHBOARD CHARTS
# ==============================
st.subheader("📊 Risk Overview Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Risk Level Distribution")
    st.bar_chart(filtered_df["risk_level"].value_counts())

with col2:
    st.markdown("### Asset Risk Exposure")
    st.bar_chart(filtered_df.groupby("asset")["risk_score"].mean())

# ==============================
# TECH vs BUSINESS RISK
# ==============================
st.subheader("⚖️ Technical vs Business Risk")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Technical Risk")
    st.bar_chart(filtered_df.groupby("cve_id")["base_risk"].mean())

with col2:
    st.markdown("### Business Risk")
    st.bar_chart(filtered_df.groupby("cve_id")["risk_score"].mean())

# ==============================
# RISK AMPLIFICATION
# ==============================
st.subheader("📉 Risk Amplification")

filtered_df["risk_gap"] = filtered_df["risk_score"] - filtered_df["base_risk"]

st.bar_chart(filtered_df.groupby("asset")["risk_gap"].mean())

# ==============================
# FULL TABLE
# ==============================
st.subheader("📋 Full Risk Table")

st.dataframe(filtered_df, use_container_width=True)

# ==============================
# LLM SECTION
# ==============================
st.subheader("🧠 AI Business Explanation")

selected_cve = st.selectbox("Select CVE", filtered_df["cve_id"].unique())

selected_rows = filtered_df[filtered_df["cve_id"] == selected_cve]

for _, row in selected_rows.iterrows():
    st.markdown(f"### 🔹 Asset: {row['asset']}")
    st.write(f"**Risk Level:** {row['risk_level']}")
    st.write(f"**Decision:** {row['decision']}")
    st.info(row["llm_explanation"])

# ==============================
# EXECUTIVE INSIGHTS
# ==============================
st.subheader("🧠 Executive Insights")

critical_count = len(filtered_df[filtered_df["risk_level"] == "Critical"])
high_count = len(filtered_df[filtered_df["risk_level"] == "High"])

if critical_count > 5:
    st.error(f"🚨 {critical_count} critical risks require immediate action")

if high_count > 10:
    st.warning(f"⚠️ High risk exposure detected")

if not filtered_df.empty:
    asset_risk = filtered_df.groupby("asset")["risk_score"].mean()
    top_asset = asset_risk.idxmax()
    st.info(f"🔥 Most exposed asset: {top_asset}")

    top_cve = filtered_df.sort_values(by="risk_score", ascending=False).iloc[0]["cve_id"]
    st.info(f"🎯 Highest impact vulnerability: {top_cve}")

# Decision distribution
st.markdown("### 🏢 Decision Overview")
st.bar_chart(filtered_df["decision"].value_counts())

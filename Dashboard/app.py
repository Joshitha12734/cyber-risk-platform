import streamlit as st
import json
import os
import pandas as pd
import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Cyber Risk Intelligence Platform",
    page_icon="🔐",
    layout="wide"
)

# =========================
# STYLING (PRODUCT UI)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #00ffcc;
}
.stMetric {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIMPLE LOGIN
# =========================
def login():
    st.title("🔐 CRQ Platform Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "crq123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# =========================
# LOAD DATA
# =========================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Outputs")

with open(os.path.join(OUTPUT_DIR, "technical_risk.json")) as f:
    tech = json.load(f)

with open(os.path.join(OUTPUT_DIR, "contextual_risk.json")) as f:
    context = json.load(f)

tech_df = pd.DataFrame(tech["results"])
df = pd.DataFrame(context["results"])

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔍 Controls")

# Session Info
st.sidebar.write(f"🕒 Session: {datetime.datetime.now()}")

# Filters
risk_levels = st.sidebar.multiselect(
    "Risk Level",
    options=df["risk_level"].unique(),
    default=df["risk_level"].unique()
)

decisions = st.sidebar.multiselect(
    "Decision",
    options=df["decision"].unique(),
    default=df["decision"].unique()
)

assets = st.sidebar.multiselect(
    "Asset",
    options=df["asset_id"].unique(),
    default=df["asset_id"].unique()
)

search = st.sidebar.text_input("🔍 Search CVE")

# Mode Selection
mode = st.sidebar.radio("View Mode", [
    "Executive View",
    "Analyst View",
    "Deep Dive"
])

# Apply filters
filtered_df = df[
    (df["risk_level"].isin(risk_levels)) &
    (df["decision"].isin(decisions)) &
    (df["asset_id"].isin(assets))
]

if search:
    filtered_df = filtered_df[filtered_df["cve_id"].str.contains(search)]

# =========================
# TITLE
# =========================
st.title("🔐 Cyber Risk Intelligence Platform")

# =========================
# EXECUTIVE VIEW
# =========================
if mode == "Executive View":
    st.header("👑 Executive Risk Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Risks", len(filtered_df))
    col2.metric("Critical", len(filtered_df[filtered_df["risk_level"] == "Critical"]))
    col3.metric("High", len(filtered_df[filtered_df["risk_level"] == "High"]))
    col4.metric("Rejected", len(filtered_df[filtered_df["decision"] == "Reject"]))

    st.subheader("🚨 Top 5 Critical Risks")
    top5 = filtered_df.sort_values(by="business_risk", ascending=False).head(5)

    for _, row in top5.iterrows():
        st.error(
            f"{row['cve_id']} | Asset: {row['asset_id']} | Risk: {row['business_risk']} | Action: {row['recommended_action']}"
        )

    st.subheader("📊 Risk Distribution")
    st.bar_chart(filtered_df["risk_level"].value_counts())

    st.subheader("📊 Risk by Asset")
    st.bar_chart(filtered_df.groupby("asset_id")["business_risk"].sum())

# =========================
# ANALYST VIEW
# =========================
elif mode == "Analyst View":
    st.header("🧑‍💻 Security Analyst Workbench")

    st.subheader("🔥 Active Threat Queue")
    critical_df = filtered_df[filtered_df["risk_level"] == "Critical"]

    for _, row in critical_df.head(10).iterrows():
        st.error(
            f"{row['cve_id']} | Asset: {row['asset_id']} | Risk: {row['business_risk']}"
        )

    st.subheader("📋 Full Risk Table")

    def highlight(val):
        if val == "Critical":
            return "background-color: red"
        elif val == "High":
            return "background-color: orange"
        elif val == "Medium":
            return "background-color: yellow"
        return ""

    styled = filtered_df.style.applymap(highlight, subset=["risk_level"])
    st.dataframe(styled, use_container_width=True)

# =========================
# DEEP DIVE
# =========================
elif mode == "Deep Dive":
    st.header("🔍 Vulnerability Investigation")

    selected = st.selectbox("Select CVE", filtered_df["cve_id"])

    row = filtered_df[filtered_df["cve_id"] == selected].iloc[0]

    st.subheader("📌 Details")
    st.json(row)

    st.subheader("🧠 AI Explanation")
    st.info(row["llm_business_explanation"])

    st.subheader("🎯 Recommended Action")
    st.success(row["recommended_action"])

# =========================
# COMMON INSIGHTS (ALL MODES)
# =========================
st.subheader("🧠 Key Insights")

if len(filtered_df[filtered_df["risk_level"] == "Critical"]) > 10:
    st.warning("High number of critical vulnerabilities detected!")

if len(filtered_df[filtered_df["decision"] == "Reject"]) > 5:
    st.error("Multiple high-risk changes rejected!")

top_asset = filtered_df.groupby("asset_id")["business_risk"].sum().idxmax()
st.info(f"🎯 Most at-risk asset: {top_asset}")

# =========================
# HEATMAP
# =========================
st.subheader("🔥 Risk Heatmap")

heatmap = filtered_df.pivot_table(
    values="business_risk",
    index="asset_id",
    columns="risk_level",
    aggfunc="sum"
)

st.dataframe(heatmap)

# =========================
# RISK CORRELATION
# =========================
st.subheader("📈 Technical vs Business Risk")

merged = pd.merge(
    df,
    tech_df,
    on="cve_id",
    suffixes=("_business", "_technical")
)

st.scatter_chart(merged[["risk_score", "business_risk"]])

# =========================
# DOWNLOAD REPORT
# =========================
st.download_button(
    label="📥 Download Risk Report",
    data=filtered_df.to_json(indent=2),
    file_name="risk_report.json",
    mime="application/json"
)
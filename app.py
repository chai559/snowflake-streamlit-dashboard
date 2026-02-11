import streamlit as st
import pandas as pd
import snowflake.connector

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Fraud Analytics Dashboard", layout="wide")

st.title("🚨 Fraud Analytics Dashboard")

# -----------------------------
# Connect to Snowflake
# -----------------------------
conn = snowflake.connector.connect(
     user="chaithu59",
    password="tk.-e7NTRrv5ise",
    account="BSEXVIS-FO68852",
    warehouse="COMPUTE_WH",
    database="FRAUD_ANALYTICS_DB",
    schema="GOLD"
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM FACT_TRANSACTIONS"
    return pd.read_sql(query, conn)

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

# Risk Score Filter (if column exists)
if "RISK_SCORE" in df.columns:
    risk = st.sidebar.slider("Risk Score",
                             int(df["RISK_SCORE"].min()),
                             int(df["RISK_SCORE"].max()),
                             (0, int(df["RISK_SCORE"].max())))
    df = df[(df["RISK_SCORE"] >= risk[0]) & (df["RISK_SCORE"] <= risk[1])]

# Location Filter (if column exists)
if "LOCATION_ID" in df.columns:
    location = st.sidebar.selectbox("Select Location",
                                     ["All"] + list(df["LOCATION_ID"].unique()))
    if location != "All":
        df = df[df["LOCATION_ID"] == location]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", len(df))

if "AMOUNT" in df.columns:
    col2.metric("Total Amount", f"${df['AMOUNT'].sum():,.2f}")

if "IS_FRAUD" in df.columns:
    col3.metric("Fraud Transactions", df["IS_FRAUD"].sum())

# -----------------------------
# CHARTS SECTION
# -----------------------------
st.subheader("📈 Transaction Analysis")

if "AMOUNT" in df.columns:
    st.line_chart(df["AMOUNT"])

if "IS_FRAUD" in df.columns:
    fraud_count = df["IS_FRAUD"].value_counts()
    st.bar_chart(fraud_count)

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📄 Raw Data")
st.dataframe(df)

import streamlit as st
import snowflake.connector
import pandas as pd

st.title("Fraud Analytics Dashboard")

# Snowflake connection using secrets
conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

query = "SELECT * FROM TRANSACTIONS_RAW LIMIT 100"
df = pd.read_sql(query, conn)

st.subheader("Transactions Data")
st.dataframe(df)

st.bar_chart(df["AMOUNT"])

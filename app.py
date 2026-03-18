import streamlit as st

from utils.data_loader import load_lead_data, load_financial_data

st.set_page_config(page_title="Lead Validation Dashboard", layout="wide")

st.title("Lead Validation Dashboard")

st.write(
"""
This platform analyzes business leads and evaluates financial projections.
"""
)

st.header("Data Layer Test")

try:
    df_leads = load_lead_data()
    st.subheader("Lead Data Preview")
    st.dataframe(df_leads.head())

except Exception as e:
    st.error(f"Lead data error: {e}")

try:
    df_finance = load_financial_data()
    st.subheader("Financial Data Preview")
    st.dataframe(df_finance.head())

except Exception as e:
    st.error(f"Finance data error: {e}")
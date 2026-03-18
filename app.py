import streamlit as st

st.set_page_config(
    page_title="Lead Validation Intelligence Platform",
    layout="wide"
)

st.title("Lead Validation Intelligence Platform")

st.markdown(
"""
This platform evaluates partnership leads and simulates
their financial impact.

Use the sidebar to navigate:

• Lead Intelligence  
• Financial Model
"""
)

st.markdown("---")

st.header("Platform Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Lead Intelligence")
    st.write("Analyze lead quality, segmentation and scoring.")

with col2:
    st.subheader("Financial Model")
    st.write("Simulate ROI, payback and investment scenarios.")
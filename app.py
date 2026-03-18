import streamlit as st

st.set_page_config(
    page_title="Lead Validation Intelligence Platform",
    layout="wide"
)

st.title("Lead Validation Intelligence Platform")

with st.expander("🚀 Project Strategy & Business Context", expanded=True):
    st.header("Reducing Investment Uncertainty in B2B Soft-Landing")
    st.markdown(
        "This platform was designed to help partners mitigate financial risk and optimize B2B prospecting. "
        "By integrating financial simulations with a proprietary lead-scoring engine, we provide a clear roadmap for market entry."
    )
    
    st.markdown("---")
    
    colA, colB = st.columns(2)
    with colA:
        st.subheader("📊 The Financial Edge")
        st.markdown(
            "The **3-Tier Model (Basic, Lite, Premium)** allows partners to scale services depending on their target budgets. "
            "It maps the financial return of each tier, helping partners thoroughly choose the right investment level based on projected ROI and Break-Even viability."
        )
        
    with colB:
        st.subheader("🚦 The Semáforo System")
        st.markdown(
            "The qualification logic uses a **'Hot, Potential, and Cold'** scoring system (🟢🟡🔴). "
            "This structured approach prioritizes high-value sales targets efficiently, ensuring that sales teams execute outreach only on top-tier prospects."
        )

st.markdown("---")

st.header("📖 How to use this Dashboard")
st.markdown(
    """
    - **[Lead Intelligence] _(Sales Execution)_**: Use this tab to filter incoming leads, review the Priority Matrix, and identify *Tier 1 + Prospección* targets for immediate outreach.
    - **[Financial Model] _(Investment Strategy)_**: Use this tab to simulate market scenarios, analyze the 12-month accumulated payback, and build a risk-averse strategy with the partner before market entry.
    """
)
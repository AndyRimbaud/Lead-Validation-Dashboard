import streamlit as st
import plotly.express as px

from utils.data_loader import load_lead_data
from utils.lead_analysis import (
    funnel_metrics,
    semaforo_distribution,
    top_leads,
    leads_by_category,
    score_distribution,
    clean_semaforo
)

st.set_page_config(page_title="Lead Intelligence", layout="wide")

@st.cache_data(show_spinner="Loading lead data...")
def get_cached_lead_data():
    return load_lead_data()

st.title("Lead Intelligence Dashboard")

try:
    df = get_cached_lead_data()
except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.stop()

if df.empty:
    st.warning("Lead data is empty or could not be loaded. Please verify data sources.")
    st.stop()

# -----------------------
# 1) FUNNEL
# -----------------------

st.subheader("1. Lead Funnel")

funnel = funnel_metrics(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Leads", funnel["total"])
col2.metric("Leads No Descartados", funnel["valid"])
col3.metric("Leads con Score", funnel["with_score"])
col4.metric("Leads Tier 1 (Gold)", funnel["top_tier"])

st.markdown("---")

# -----------------------
# 2) MATRIZ DE PRIORIDAD
# -----------------------

st.subheader("2. Matriz de Prioridad")

df['Estado'] = clean_semaforo(df)

fig_scatter = px.scatter(
    df,
    x="score",
    y="tier_objetivo",
    color="Estado",
    hover_data=["company_name", "sector"] if "company_name" in df.columns else None,
    color_discrete_map={
        "🔴": "red",
        "🟡": "#FFBF00",
        "🟢": "green"
    },
    title="Score vs Tier"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# -----------------------
# 3) GESTIÓN DE LEADS
# -----------------------

st.subheader("3. Gestión de Leads")

tab1, tab2, tab3 = st.tabs([
    "Bandeja de Entrada (Todos)", 
    "Prioridad Inmediata (Prospección)", 
    "Archivo (Descartados)"
])

def style_semaforo(val):
    color = "transparent"
    if val == "🔴":
        color = "rgba(255, 0, 0, 0.4)"
    elif val == "🟡":
        color = "rgba(255, 191, 0, 0.4)"
    elif val == "🟢":
        color = "rgba(0, 128, 0, 0.4)"
    return f'background-color: {color}'

def render_styled_dataframe(data_to_render):
    if data_to_render.empty:
        st.info("No hay leads en esta selección.")
    else:
        cols_to_show = ["company_name", "sector", "score", "tier_objetivo", "Estado"]
        cols = [c for c in cols_to_show if c in data_to_render.columns]
        
        st.dataframe(
            data_to_render[cols].style.map(style_semaforo, subset=["Estado"]),
            use_container_width=True
        )

with tab1:
    render_styled_dataframe(df)

with tab2:
    render_styled_dataframe(df[df["Estado"] == "🟢"])

with tab3:
    render_styled_dataframe(df[df["Estado"] == "🔴"])
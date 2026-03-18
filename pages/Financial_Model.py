import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_financial_data
from utils.finance_analysis import get_scenario_metrics, generate_12_month_projection

st.set_page_config(page_title="Financial Model", layout="wide")

# -----------------------------------
# HEADER
# -----------------------------------

st.title("Financial Model Dashboard")

st.markdown(
"""
This dashboard simulates the financial viability of a Soft Landing program
based on client acquisition scenarios.
"""
)

# -----------------------------------
# LOAD DATA
# -----------------------------------

try:
    df_fin = load_financial_data()
except Exception as e:
    st.error(f"Error cargando los datos financieros: {e}")
    st.stop()

# -----------------------------------
# INPUTS (SIMULATION)
# -----------------------------------

st.sidebar.header("Scenario Simulation")
escenario_seleccionado = st.sidebar.selectbox(
    "Seleccione Escenario", 
    ["Conservador", "Realista", "Optimista"]
)

# -----------------------------------
# CALCULATIONS
# -----------------------------------

metrics = get_scenario_metrics(df_fin, escenario_seleccionado)

# -----------------------------------
# KPI SECTION
# -----------------------------------

st.subheader("Key Financial Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Precio Pond. Mensual", f"{metrics.get('precio_mensual', 0):,.0f} €")
col2.metric("Margen Bruto", f"{metrics.get('margen_bruto', 0) * 100:,.1f} %")
col3.metric("EBIT", f"{metrics.get('ebit', 0):,.0f} €")
col4.metric("Payback (meses)", f"{metrics.get('payback', 0):,.1f}")
col5.metric("ROI", f"{metrics.get('roi', 0):,.2f}")  # Si el excel trae 2.17, es 2.17x o 217%. Lo mostramos tal cual o en formato %.

st.markdown("---")

# -----------------------------------
# 12-MONTH PROJECTION (HEATMAP)
# -----------------------------------

st.subheader("Proyección a 12 Meses")

df_proj = generate_12_month_projection(metrics.get("precio_mensual", 0))

st.markdown("Visualización en Mapa de Calor de los Beneficios:")

# Función nativa de pandas para gradiente térmico sin requerir matplotlib
def custom_gradient(s):
    min_v, max_v = s.min(), s.max()
    rng = max_v - min_v
    if rng == 0: return ['' for _ in s]
    
    colors = []
    for val in s:
        if pd.isna(val):
            colors.append('')
            continue
            
        norm = (val - min_v) / rng
        if norm < 0.5:
            # Red to Yellow
            ratio = norm / 0.5
            r, g, b = 255, int(255 * ratio), 0
        else:
            # Yellow to Green
            ratio = (norm - 0.5) / 0.5
            r, g, b = int(255 * (1 - ratio)), int(255 - (255 - 160) * ratio), 0
            
        colors.append(f'background-color: rgba({r}, {g}, {b}, 0.5)')
        
    return colors

heatmap = df_proj.style.apply(
    custom_gradient,
    subset=["Beneficio (€)", "Beneficio Acumulado (€)"]
).format({
    "Ingresos (€)": "{:,.0f} €",
    "Costes Fijos (€)": "{:,.0f} €",
    "Beneficio (€)": "{:,.0f} €",
    "Beneficio Acumulado (€)": "{:,.0f} €"
})

st.dataframe(heatmap, use_container_width=True)

# -----------------------------------
# BUSINESS INSIGHT BLOCK
# -----------------------------------

st.markdown("---")

st.info(
"""
💡 **Insight**

Este modelo lee directamente los resultados calculados en la plestaña *Proyección por Escenarios* del Excel 
para mantener una única fuente de la verdad (SSOT). La evolución a 12 meses muestra el impacto de las cuotas.
"""
)
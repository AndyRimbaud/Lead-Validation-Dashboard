import pandas as pd
from typing import Dict, Any

# ---------------------------
# ESCENARIOS Y MÉTRICAS
# ---------------------------

def get_scenario_metrics(df: pd.DataFrame, scenario_name: str) -> Dict[str, Any]:
    """Extrae las métricas del escenario seleccionado desde el DataFrame cargado del Excel."""
    
    if df is None or df.empty:
        return {}
        
    # Buscar la fila del escenario. Los nombres en Excel suelen tener espacios o diferencias mínimas.
    match = df[df['Escenarios'].str.contains(scenario_name, case=False, na=False)]
    
    if match.empty:
        return {}
        
    row = match.iloc[0]
    
    # Extraer las columnas exactas que vimos en el print
    metrics = {
        "precio_mensual": row.get("Precio ponderdo mes por cliente", 0),
        "ingreso_anual": row.get("Ingreso Total Año", 0) if "Ingreso Total Año" in row else row.get("Ingreso Total Ao", 0),
        "cogs": row.get("COGS", 0),
        "margen_bruto": row.get("Margen Bruto", 0),
        "ebit": row.get("EBIT", 0),
        "resultado_neto": row.get("Resultado Neto", 0),
        "roi": row.get("ROI", 0),
        "payback": row.get("Payback Meses", 0)
    }
    
    # Manejar posibles errores de lectura (e.g. NaN)
    for k, v in metrics.items():
        if pd.isna(v):
            metrics[k] = 0
            
    return metrics

# ---------------------------
# PROYECCIÓN 12 MESES
# ---------------------------

def generate_12_month_projection(precio_mensual: float, costes_fijos_anuales: float = 40000, target_col: int = 8) -> pd.DataFrame:
    """Genera la proyección a 12 meses."""
    
    # Curva de adquisición simulada (empieza lenta, acelera y se estabiliza) matching closely what Excel had
    # Excel showed Month 1: 0, Month 2: 0, Month 3: 1, Month 4: 1, Month 5: 2 ...
    clientes_acumulados = [0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 8]
    
    df = pd.DataFrame({"Mes": range(1, 13)})
    df["Clientes Acumulativos"] = clientes_acumulados
    
    coste_mensual = costes_fijos_anuales / 12
    
    # Ingresos = Clientes activos en el mes * precio mensual de la cuota
    df["Ingresos (€)"] = df["Clientes Acumulativos"] * precio_mensual
    df["Costes Fijos (€)"] = coste_mensual
    df["Beneficio (€)"] = df["Ingresos (€)"] - df["Costes Fijos (€)"]
    df["Beneficio Acumulado (€)"] = df["Beneficio (€)"].cumsum()
    
    return df
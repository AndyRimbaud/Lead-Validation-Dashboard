import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# File paths
LEAD_SCORING_PATH = DATA_DIR / "lead_scoring.xlsx"
PLAN_FINANCIERO_PATH = DATA_DIR / "plan_financiero.xlsx"

# Expected columns for Data Validation
# Note: Ensure these match the actual headers in your .xlsx files (normalized)
EXPECTED_LEAD_COLUMNS = [
    "id",
    "nombre_tipo",
    "sector",
    "contacto_ideal",
    "score",
    "tier_objetivo"
]

EXPECTED_FINANCE_COLUMNS = [
    "mes",
    "clientes_acumulativos",
    "ingresos_cuota_mensual_cliente",
    "costes_fijos",
    "costes_variables",
    "beneficio",
    "beneficio_acumulado"
]

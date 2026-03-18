import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = BASE_DIR / "data"

# File paths
LEAD_SCORING_PATH = DATA_DIR / "lead_scoring.xlsx"
PLAN_FINANCIERO_PATH = DATA_DIR / "plan_financiero.xlsx"

# -------------------------------------------------------------------------
# DATA VALIDATION SCHEMA
# -------------------------------------------------------------------------

# Expected columns for Lead Data (After Merge & Normalization)
# Solo exigimos las columnas críticas para que el dashboard y el funnel funcionen.
EXPECTED_LEAD_COLUMNS = [
    "company_name",    # Renombrado desde "Nombre / Tipo" y "Lead"
    "sector",
    "score",
    "tier_objetivo",
    "semaforo"         # Integrado desde la pestaña 2
]

# Expected columns for Financial Data
# Dejamos un esquema mínimo temporal. En la FASE 3 actualizaremos esto 
# para que lea la matriz de Escenarios y Proyecciones correctamente.
EXPECTED_FINANCE_COLUMNS = []
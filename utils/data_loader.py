import pandas as pd
import os
import logging
import unicodedata
import re

from config.settings import (
    LEAD_SCORING_PATH,
    PLAN_FINANCIERO_PATH,
    EXPECTED_LEAD_COLUMNS,
    EXPECTED_FINANCE_COLUMNS
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# -----------------------
# NORMALIZE COLUMNS
# -----------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    new_cols = []

    for col in df.columns:
        col_str = str(col)

        # remove accents
        col_str = unicodedata.normalize('NFKD', col_str).encode('ASCII', 'ignore').decode('utf-8')

        col_str = col_str.lower().strip()

        # remove symbols
        col_str = re.sub(r'[^\w\s]', '', col_str)

        # replace spaces
        col_str = re.sub(r'\s+', '_', col_str)

        new_cols.append(col_str)

    df.columns = new_cols
    return df


# -----------------------
# VALIDATION
# -----------------------

def validate_columns(df: pd.DataFrame, expected_columns: list, dataset_name: str) -> pd.DataFrame:
    missing = [col for col in expected_columns if col not in df.columns]

    if missing:
        msg = f"En {dataset_name} faltan estas columnas obligatorias: {missing}"
        logging.error(msg)
        raise ValueError(msg)

    return df


# -----------------------
# LOAD LEAD DATA (FINAL)
# -----------------------

def load_lead_data() -> pd.DataFrame:

    if not os.path.exists(LEAD_SCORING_PATH):
        msg = f"File not found: {LEAD_SCORING_PATH}"
        logging.error(msg)
        raise FileNotFoundError(msg)

    try:
        # 🔥 STEP 1 — Read Sheet 1 (Lead Scoring)
        df_sheet1 = pd.read_excel(LEAD_SCORING_PATH, sheet_name=0, header=0)
        # Renombramos la PRIMERA columna dinámicamente, ignorando espacios ocultos
        df_sheet1.rename(columns={df_sheet1.columns[0]: 'company_name'}, inplace=True)

        # 🔥 STEP 2 — Read Sheet 2 (Semáforo)
        df_sheet2 = pd.read_excel(LEAD_SCORING_PATH, sheet_name=1, header=0)
        # Renombramos la PRIMERA columna
        df_sheet2.rename(columns={df_sheet2.columns[0]: 'company_name'}, inplace=True)

        # 🔥 STEP 3 — Limpiar espacios extra en los nombres de las empresas para que el merge no falle
        df_sheet1['company_name'] = df_sheet1['company_name'].astype(str).str.strip()
        df_sheet2['company_name'] = df_sheet2['company_name'].astype(str).str.strip()

        # 🔥 STEP 4 — Merge (Left Join usando Sheet 1 como base)
        df = pd.merge(df_sheet1, df_sheet2, on='company_name', how='left')

        # 🔥 STEP 5 — Clean empty rows
        df = df.dropna(how="all")

        # 🔥 STEP 6 — Renombrar columnas críticas antes de la normalización
        rename_map = {
            'Semáforo': 'semaforo',
            'Tier Objetivo': 'tier_objetivo',
            'Score': 'score',
            'Sector': 'sector'
        }
        df = df.rename(columns=rename_map)

        # 🔥 STEP 7 — Normalize (esto pasará todo a minúsculas y quitará acentos)
        df = normalize_columns(df)

        # Asegurarnos de que 'company_name' mantiene su nombre tras normalizar
        # (ya que no tiene acentos ni caracteres raros, debería quedarse igual, pero por seguridad)
        if 'company_name' not in df.columns and 'companyname' in df.columns:
            df = df.rename(columns={'companyname': 'company_name'})

        # 🔥 STEP 8 — Remove junk columns (Unnamed)
        df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False, na=False)]

        # 🔥 STEP 9 — Validate schema
        df = validate_columns(df, EXPECTED_LEAD_COLUMNS, "Lead Data")

        # 🔥 STEP 10 — Fill missing values
        numeric_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        df[numeric_cols] = df[numeric_cols].fillna(0)
        df[cat_cols] = df[cat_cols].fillna("Unknown")

        logging.info(f"Lead data loaded successfully. Shape: {df.shape}")

        return df

    except Exception as e:
        logging.error(f"Error loading lead data: {e}")
        # En lugar de devolver un DataFrame vacío, relanzamos el error para que Streamlit lo muestre y podamos depurar
        raise e


# -----------------------
# LOAD FINANCIAL DATA
# -----------------------

def load_financial_data() -> pd.DataFrame:

    if not os.path.exists(PLAN_FINANCIERO_PATH):
        raise FileNotFoundError(f"No se encontró el archivo: {PLAN_FINANCIERO_PATH}")

    try:
        xls = pd.ExcelFile(PLAN_FINANCIERO_PATH)
        # Buscar la hoja que contenga "Proyecci" y "Escenarios" para evitar fallos de codificación
        sheet_name = [sn for sn in xls.sheet_names if 'Proyecci' in sn and 'Escenario' in sn]
        if not sheet_name:
            raise ValueError("No se encontró la hoja de 'Proyección por Escenarios' en el Excel.")
        
        df = pd.read_excel(xls, sheet_name=sheet_name[0])
        
        # Las métricas dinámicas serán extraídas directamente de este DataFrame
        # Limpieza básica de nombres de columnas para que sea fácil consumirlas
        df.columns = df.columns.astype(str).str.strip()
        
        return df

    except Exception as e:
        logging.error(f"Error loading financial scenarios: {e}")
        raise e
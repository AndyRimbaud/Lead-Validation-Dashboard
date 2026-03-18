import pandas as pd
import streamlit as st
import os
import logging
from config.settings import (
    LEAD_SCORING_PATH,
    PLAN_FINANCIERO_PATH,
    EXPECTED_LEAD_COLUMNS,
    EXPECTED_FINANCE_COLUMNS
)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame column names (lowercase, replace special chars, strip, replace spaces with underscores)."""
    df.columns = (df.columns.astype(str)
                  .str.lower()
                  .str.replace(r'[^\w\s]', '', regex=True)
                  .str.strip()
                  .str.replace(r'\s+', '_', regex=True))
    return df

def validate_columns(df: pd.DataFrame, expected_columns: list, dataset_name: str) -> None:
    """Validate that all expected columns are present in the DataFrame."""
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        error_msg = f"Dataset '{dataset_name}' is missing required columns: {missing_columns}"
        logging.error(error_msg)
        raise ValueError(error_msg)

@st.cache_data(show_spinner="Loading lead data...")
def load_lead_data() -> pd.DataFrame:
    """Load, clean, and validate lead scoring data."""
    if not os.path.exists(LEAD_SCORING_PATH):
        raise FileNotFoundError(f"Lead scoring file not found at {LEAD_SCORING_PATH}")

    try:
        df = pd.read_excel(LEAD_SCORING_PATH, sheet_name='Lead Scoring', header=1)
        df = normalize_columns(df)
        
        # Drop unused/unnamed columns that Excel might append
        df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False, na=False)]
        
        # Validates columns exist
        validate_columns(df, EXPECTED_LEAD_COLUMNS, "Lead Scoring")
        
        # Handle missing values: 0 for numeric, 'Unknown' for objects
        numeric_cols = df.select_dtypes(include=['number']).columns
        cat_cols = df.select_dtypes(exclude=['number']).columns
        
        df[numeric_cols] = df[numeric_cols].fillna(0)
        df[cat_cols] = df[cat_cols].fillna('Unknown')
        
        logging.info("Lead Data loaded completely.")
        return df

    except Exception as e:
        logging.error(f"Error loading lead data: {e}")
        raise

@st.cache_data(show_spinner="Loading financial data...")
def load_financial_data() -> pd.DataFrame:
    """Load, clean, and validate financial plan data."""
    if not os.path.exists(PLAN_FINANCIERO_PATH):
        raise FileNotFoundError(f"Financial plan file not found at {PLAN_FINANCIERO_PATH}")

    try:
        df = pd.read_excel(PLAN_FINANCIERO_PATH, sheet_name='Proyeccion 12 meses', header=0)
        df = normalize_columns(df)
        
        # Drop unused/unnamed columns
        df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False, na=False)]
        
        # Validates columns exist
        validate_columns(df, EXPECTED_FINANCE_COLUMNS, "Financial Plan")
        
        # Handle missing values: 0 for financial data
        df = df.fillna(0)
        
        logging.info("Financial Data loaded completely.")
        return df

    except Exception as e:
        logging.error(f"Error loading financial data: {e}")
        raise

import pandas as pd
from typing import Dict


def total_investment(df: pd.DataFrame) -> float:
    """
    Calculate the total investment from the financial plan.

    Args:
        df (pd.DataFrame): Financial DataFrame containing a 'valor' column.

    Returns:
        float: Total investment value.
    """
    if "valor" not in df.columns:
        raise ValueError("Column 'valor' not found in financial DataFrame.")

    values = pd.to_numeric(df["valor"], errors="coerce").dropna()

    return float(values.sum())


def cost_breakdown(df: pd.DataFrame) -> pd.Series:
    """
    Group costs by concept.

    Args:
        df (pd.DataFrame): Financial DataFrame containing 'concepto' and 'valor'.

    Returns:
        pd.Series: Cost per concept.
    """
    if "concepto" not in df.columns or "valor" not in df.columns:
        raise ValueError("Columns 'concepto' and 'valor' are required.")

    df_calc = df.copy()
    df_calc["valor"] = pd.to_numeric(df_calc["valor"], errors="coerce")

    return df_calc.groupby("concepto")["valor"].sum().sort_values(ascending=False)


def monthly_projection(df: pd.DataFrame) -> pd.Series:
    """
    Return monthly financial projections.

    Args:
        df (pd.DataFrame): Financial DataFrame containing monthly columns.

    Returns:
        pd.Series: Total projected revenue per month.
    """
    monthly_cols = [
        col for col in df.columns
        if "mes" in col or "month" in col
    ]

    if not monthly_cols:
        raise ValueError("No monthly projection columns found.")

    df_calc = df[monthly_cols].apply(pd.to_numeric, errors="coerce")

    return df_calc.sum()


def total_projected_revenue(df: pd.DataFrame) -> float:
    """
    Calculate total projected revenue from monthly projections.

    Args:
        df (pd.DataFrame): Financial DataFrame.

    Returns:
        float: Total projected revenue.
    """
    monthly = monthly_projection(df)

    return float(monthly.sum())
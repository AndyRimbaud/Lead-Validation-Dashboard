import pandas as pd
from typing import Dict, Any

def tier_distribution(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the distribution of leads across tiers.
    
    Args:
        df (pd.DataFrame): Pandas DataFrame containing lead data with a 'tier_objetivo' column.
        
    Returns:
        pd.Series: Counts of leads per tier.
    """
    if "tier_objetivo" not in df.columns:
        raise ValueError("Column 'tier_objetivo' not found in DataFrame.")
    return df["tier_objetivo"].value_counts().sort_index()

def score_distribution(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate statistics for lead scores.
    
    Args:
        df (pd.DataFrame): Pandas DataFrame containing lead data with a 'score' column.
        
    Returns:
        dict: A dictionary containing mean_score, median_score, min_score, and max_score.
    """
    if "score" not in df.columns:
        raise ValueError("Column 'score' not found in DataFrame.")
        
    # Handling non-numeric safely
    scores = pd.to_numeric(df["score"], errors="coerce").dropna()
    
    if scores.empty:
        return {
            "mean_score": 0.0,
            "median_score": 0.0,
            "min_score": 0.0,
            "max_score": 0.0
        }
        
    return {
        "mean_score": float(scores.mean()),
        "median_score": float(scores.median()),
        "min_score": float(scores.min()),
        "max_score": float(scores.max())
    }

def top_leads(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return the top n leads sorted by score in descending order.
    
    Args:
        df (pd.DataFrame): Pandas DataFrame containing lead data with a 'score' column.
        n (int): Number of top leads to return (default: 10).
        
    Returns:
        pd.DataFrame: Top n leads sorted by score.
    """
    if "score" not in df.columns:
        raise ValueError("Column 'score' not found in DataFrame.")
        
    # Ensure scores are numeric for sorting
    df_sorted = df.copy()
    df_sorted["score"] = pd.to_numeric(df_sorted["score"], errors="coerce")
    df_sorted = df_sorted.dropna(subset=["score"])

    return df_sorted.sort_values(by="score", ascending=False).head(n)


def leads_by_category(df: pd.DataFrame) -> pd.Series:
    """
    Group leads by category/sector and return the count.
    
    Args:
        df (pd.DataFrame): Pandas DataFrame containing lead data with a 'sector' column.
        
    Returns:
        pd.Series: Counts of leads per category/sector.
    """
    if "sector" not in df.columns:
        raise ValueError("Column 'sector' not found in DataFrame.")
    return df["sector"].value_counts().sort_values(ascending=False)

def tier_score_summary(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the average score per tier.
    
    Args:
        df (pd.DataFrame): Pandas DataFrame containing lead data with 'tier_objetivo' and 'score' columns.
        
    Returns:
        pd.Series: Average score per tier.
    """
    if "tier_objetivo" not in df.columns or "score" not in df.columns:
        raise ValueError("Columns 'tier_objetivo' and 'score' are required in DataFrame.")
        
    df_calc = df.copy()
    df_calc["score"] = pd.to_numeric(df_calc["score"], errors="coerce")
    return df_calc.groupby("tier_objetivo")["score"].mean()

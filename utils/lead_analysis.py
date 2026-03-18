import pandas as pd
from typing import Dict, Any


def _safe_col(df: pd.DataFrame, col: str, default: Any = 0) -> pd.Series:
    """Safely get a column or return a default series."""
    if col in df.columns:
        return df[col]
    return pd.Series([default] * len(df))


# -----------------------
# FUNNEL
# -----------------------

def clean_semaforo(df: pd.DataFrame) -> pd.Series:
    """Clasifica el estado del Semáforo en 🔴, 🟡 o 🟢."""
    if df is None or df.empty or "semaforo" not in df.columns:
        return pd.Series(["🟡"] * len(df) if df is not None else [])
    
    def classify(val):
        val_str = str(val).upper()
        if "DESCARTAR" in val_str:
            return "🔴"
        elif "PROSPECCIÓN" in val_str or "PROSPECCION" in val_str:
            return "🟢"
        else:
            return "🟡"
            
    return df["semaforo"].apply(classify)

def funnel_metrics(df: pd.DataFrame) -> Dict[str, Any]:

    if df is None or df.empty:
        return {"total": 0, "valid": 0, "with_score": 0, "top_tier": 0}

    total = len(df)

    # STEP 1: Leads No Descartados
    status = clean_semaforo(df)
    valid_df = df[status != "🔴"]

    # STEP 2: Leads con Score (Objetivización)
    scores = pd.to_numeric(_safe_col(valid_df, "score", 0), errors="coerce").fillna(0)
    with_score_df = valid_df[scores > 0]

    # STEP 3: Leads Tier 1 (Gold)
    tiers = _safe_col(with_score_df, "tier_objetivo", "Unknown").astype(str)
    top_tier_df = with_score_df[tiers.str.contains(r"1", regex=True, na=False)]

    return {
        "total": total,
        "valid": len(valid_df),
        "with_score": len(with_score_df),
        "top_tier": len(top_tier_df)
    }


# -----------------------
# SEMÁFORO
# -----------------------

def semaforo_distribution(df: pd.DataFrame) -> pd.Series:

    if df is None or df.empty:
        return pd.Series({"🔴": 0, "🟡": 0, "🟢": 0})

    status = clean_semaforo(df)
    return status.value_counts()


# -----------------------
# TOP LEADS
# -----------------------

def top_leads(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:

    if df is None or df.empty:
        return pd.DataFrame()

    df_safe = df.copy()

    df_safe["score"] = pd.to_numeric(
        _safe_col(df_safe, "score", 0),
        errors="coerce"
    ).fillna(0)

    return df_safe.sort_values(by="score", ascending=False).head(top_n)


# -----------------------
# SECTOR
# -----------------------

def leads_by_category(df: pd.DataFrame) -> pd.Series:

    if df is None or df.empty:
        return pd.Series(dtype=int)

    sector = _safe_col(df, "sector", "Unknown").astype(str)

    return sector.value_counts()


# -----------------------
# SCORE
# -----------------------

def score_distribution(df: pd.DataFrame) -> pd.Series:

    if df is None or df.empty:
        return pd.Series(dtype=float)

    return pd.to_numeric(
        _safe_col(df, "score", 0),
        errors="coerce"
    ).fillna(0)


# -----------------------
# TIER
# -----------------------

def tier_distribution(df: pd.DataFrame) -> pd.Series:

    if df is None or df.empty:
        return pd.Series(dtype=int)

    tier = _safe_col(df, "tier_objetivo", "Unknown").astype(str)

    return tier.value_counts()


def tier_score_summary(df: pd.DataFrame) -> pd.DataFrame:

    if df is None or df.empty:
        return pd.DataFrame()

    df_safe = df.copy()

    df_safe["score"] = pd.to_numeric(
        _safe_col(df_safe, "score", 0),
        errors="coerce"
    ).fillna(0)

    df_safe["tier_objetivo"] = _safe_col(
        df_safe,
        "tier_objetivo",
        "Unknown"
    ).astype(str)

    return df_safe.groupby("tier_objetivo")["score"].mean().reset_index()
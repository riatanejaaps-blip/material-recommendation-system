"""
utils/scoring.py

The recommendation engine — a transparent weighted-scoring algorithm.
Deliberately NOT machine learning: with only 50 labeled materials and
no ground-truth "correct" recommendation to train against, a weighted
multi-criteria score is both more honest about its inputs and fully
explainable to an engineer deciding on a real component.

How it works
------------
1. Hard filters remove materials that flat-out cannot meet a stated
   requirement (e.g. too weak, wrong manufacturing process).
2. Surviving materials get a 0-100 score built from five weighted,
   min-max normalized criteria: strength, density, cost, corrosion
   resistance, and temperature capability.
3. Materials are ranked by score; the top 5 are returned.
"""

from __future__ import annotations

from typing import Optional
import pandas as pd

from models.material import CorrosionEnvironment, ManufacturingProcess, ENVIRONMENT_MIN_CORROSION_RATING

# Preset weight profiles for the "Priority" selector. Values are
# relative — they get normalized to sum to 100 regardless of what's
# passed in, so a user's custom sliders don't need to add up exactly.
PRIORITY_PRESETS = {
    "Balanced":            {"strength": 20, "density": 20, "cost": 20, "corrosion": 20, "temperature": 20},
    "Highest Strength":    {"strength": 50, "density": 10, "cost": 10, "corrosion": 15, "temperature": 15},
    "Lowest Weight":       {"strength": 15, "density": 50, "cost": 10, "corrosion": 10, "temperature": 15},
    "Lowest Cost":         {"strength": 15, "density": 15, "cost": 50, "corrosion": 10, "temperature": 10},
    "Corrosion Resistance": {"strength": 15, "density": 10, "cost": 10, "corrosion": 50, "temperature": 15},
}


def _normalize(series: pd.Series, higher_is_better: bool) -> pd.Series:
    """Min-max scale a column to 0-1. Flat columns (all equal) score
    1.0 across the board rather than dividing by zero."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([1.0] * len(series), index=series.index)
    scaled = (series - lo) / (hi - lo)
    return scaled if higher_is_better else (1 - scaled)


def calculate_scores(
    df: pd.DataFrame,
    min_yield_strength: float = 0,
    min_tensile_strength: float = 0,
    max_density: Optional[float] = None,
    max_cost: Optional[float] = None,
    operating_temp: Optional[float] = None,
    environment: Optional[CorrosionEnvironment] = None,
    process: Optional[ManufacturingProcess] = None,
    weights: Optional[dict] = None,
) -> tuple[pd.DataFrame, bool]:
    """
    Score and rank materials against the given requirements.

    Returns (ranked_dataframe, exact_match_found). If no material
    survives the hard filters, falls back to scoring the full
    database and flags exact_match_found=False so the UI can warn
    the user that these are the closest options, not exact matches.
    """
    weights = weights or PRIORITY_PRESETS["Balanced"]
    total_weight = sum(weights.values()) or 1
    w = {k: v / total_weight for k, v in weights.items()}

    candidates = df.copy()

    # ---- Hard filters ----
    candidates = candidates[candidates["Yield Strength (MPa)"] >= min_yield_strength]
    candidates = candidates[candidates["Ultimate Strength (MPa)"] >= min_tensile_strength]
    if max_density is not None:
        candidates = candidates[candidates["Density (g/cm3)"] <= max_density]
    if max_cost is not None:
        candidates = candidates[candidates["Relative Cost"] <= max_cost]
    if operating_temp is not None:
        candidates = candidates[candidates["Max Service Temp (C)"] >= operating_temp]
    if environment is not None:
        min_corr = ENVIRONMENT_MIN_CORROSION_RATING[environment]
        candidates = candidates[candidates["Corrosion Resistance"] >= min_corr]
    if process is not None:
        candidates = candidates[candidates["Manufacturing Compatibility"].apply(lambda lst: process.value in lst)]

    exact_match_found = len(candidates) > 0
    scored_df = candidates if exact_match_found else df.copy()

    if len(scored_df) == 0:
        return scored_df, exact_match_found

    # ---- Weighted, normalized scoring ----
    strength_component = (
        _normalize(scored_df["Yield Strength (MPa)"], True) * 0.5
        + _normalize(scored_df["Ultimate Strength (MPa)"], True) * 0.5
    )
    density_component = _normalize(scored_df["Density (g/cm3)"], False)
    cost_component = _normalize(scored_df["Relative Cost"], False)
    corrosion_component = _normalize(scored_df["Corrosion Resistance"], True)
    temperature_component = _normalize(scored_df["Max Service Temp (C)"], True)

    scored_df = scored_df.copy()
    scored_df["Score"] = (
        strength_component * w["strength"]
        + density_component * w["density"]
        + cost_component * w["cost"]
        + corrosion_component * w["corrosion"]
        + temperature_component * w["temperature"]
    ) * 100

    scored_df = scored_df.sort_values("Score", ascending=False).reset_index(drop=True)
    return scored_df, exact_match_found


def top_n(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Convenience slice — returns the top-N rows of an already-scored,
    already-sorted DataFrame."""
    return df.head(n)

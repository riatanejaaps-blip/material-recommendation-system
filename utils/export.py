"""
utils/export.py

Export helper for the recommendation results:
    export_to_excel(df, path) -> .xlsx via pandas/openpyxl

Takes an in-memory path (BytesIO works for Streamlit's download
buttons) or a plain file path string.
"""

from __future__ import annotations

from typing import Union, IO
import pandas as pd


def export_to_excel(df: pd.DataFrame, path: Union[str, IO]) -> None:
    """Write a DataFrame to an .xlsx file. Drops list-typed columns
    (Applications, Advantages, etc.) into comma-joined strings first —
    openpyxl can't write native Python lists into a cell."""
    export_df = df.copy()
    for col in export_df.columns:
        if export_df[col].apply(lambda v: isinstance(v, list)).any():
            export_df[col] = export_df[col].apply(
                lambda v: ", ".join(v) if isinstance(v, list) else v
            )
    export_df.to_excel(path, index=False, engine="openpyxl", sheet_name="Recommendations")

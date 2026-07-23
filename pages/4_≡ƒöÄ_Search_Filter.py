"""
pages/4_Search_Filter.py

Browse and filter the full 50-material database by family, cost,
density, temperature, corrosion resistance, and manufacturing process.
"""

import io
import streamlit as st
from data.materials_database import get_materials_dataframe
from utils.export import export_to_excel

st.set_page_config(page_title="Search & Filter | Material Recommender", page_icon="🔎", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

st.title("🔎 Search & Filter")

with st.sidebar:
    st.markdown("### Filters")
    families = st.multiselect("Family", sorted(df["Family"].unique()), default=list(df["Family"].unique()))
    cost_range = st.slider("Relative Cost", 1, 10, (1, 10))
    density_range = st.slider("Density (g/cm3)", float(df["Density (g/cm3)"].min()), float(df["Density (g/cm3)"].max()),
                               (float(df["Density (g/cm3)"].min()), float(df["Density (g/cm3)"].max())))
    temp_range = st.slider("Max Service Temp (C)", int(df["Max Service Temp (C)"].min()), int(df["Max Service Temp (C)"].max()),
                            (int(df["Max Service Temp (C)"].min()), int(df["Max Service Temp (C)"].max())))
    corrosion_range = st.slider("Corrosion Resistance", 1, 10, (1, 10))

    all_processes = sorted({p for lst in df["Manufacturing Compatibility"] for p in lst})
    processes = st.multiselect("Manufacturing Process", all_processes)

    search_text = st.text_input("Search by name")

# ---- Apply filters ----
filtered = df[
    df["Family"].isin(families)
    & df["Relative Cost"].between(*cost_range)
    & df["Density (g/cm3)"].between(*density_range)
    & df["Max Service Temp (C)"].between(*temp_range)
    & df["Corrosion Resistance"].between(*corrosion_range)
]
if processes:
    filtered = filtered[filtered["Manufacturing Compatibility"].apply(lambda lst: any(p in lst for p in processes))]
if search_text:
    filtered = filtered[filtered["Name"].str.contains(search_text, case=False)]

st.caption(f"{len(filtered)} of {len(df)} materials match your filters")

display_cols = ["Name", "Family", "Density (g/cm3)", "Yield Strength (MPa)", "Ultimate Strength (MPa)",
                 "Max Service Temp (C)", "Corrosion Resistance", "Relative Cost"]
st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

buf = io.BytesIO()
export_to_excel(filtered, buf)
st.download_button("⬇ Download filtered results as Excel", buf.getvalue(), "filtered_materials.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

"""
pages/5_Tools.py

Bonus features: unit converter, material cost estimator, and a raw
decision matrix table. (Dark mode is handled natively by Streamlit's
built-in theme switcher — Settings menu, top right — so it isn't
duplicated here with custom CSS.)
"""

import streamlit as st
from data.materials_database import get_materials_dataframe
from utils.unit_converter import CONVERSIONS

st.set_page_config(page_title="Tools | Material Recommender", page_icon="🛠️", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

st.title("🛠️ Tools")

tab1, tab2, tab3 = st.tabs(["Unit Converter", "Cost Estimator", "Decision Matrix"])

# ---- Unit converter ----
with tab1:
    st.subheader("Unit Converter")
    c1, c2 = st.columns(2)
    with c1:
        conversion = st.selectbox("Conversion", list(CONVERSIONS.keys()))
        value = st.number_input("Value", value=1.0)
    with c2:
        result = CONVERSIONS[conversion](value)
        st.metric("Result", f"{result:,.4f}")

# ---- Cost estimator ----
with tab2:
    st.subheader("Material Cost Estimator")
    st.caption("Rough estimate using the database's relative cost index as a multiplier on a baseline $/kg rate — for ballpark comparison only, not a quotation.")
    material_name = st.selectbox("Material", sorted(df["Name"].tolist()))
    mass_kg = st.number_input("Component mass (kg)", min_value=0.0, value=1.0, step=0.1)
    baseline_rate = st.number_input("Baseline rate ($ per kg, at cost index 1)", min_value=0.1, value=2.0, step=0.5)

    row = df[df["Name"] == material_name].iloc[0]
    estimated_rate = baseline_rate * row["Relative Cost"]
    estimated_total = estimated_rate * mass_kg

    e1, e2 = st.columns(2)
    e1.metric("Estimated $/kg", f"${estimated_rate:,.2f}")
    e2.metric("Estimated total cost", f"${estimated_total:,.2f}")

# ---- Decision matrix ----
with tab3:
    st.subheader("Decision Matrix")
    st.caption("Raw property table for any selected materials — useful for a manual weighted-decision matrix in a report.")
    names = st.multiselect("Materials", sorted(df["Name"].tolist()), default=sorted(df["Name"].tolist())[:5])
    if names:
        matrix = df[df["Name"].isin(names)].set_index("Name")[
            ["Yield Strength (MPa)", "Density (g/cm3)", "Relative Cost", "Corrosion Resistance", "Max Service Temp (C)"]
        ]
        st.dataframe(matrix.style.background_gradient(cmap="Greens", axis=0), use_container_width=True)
    else:
        st.info("Select at least one material.")

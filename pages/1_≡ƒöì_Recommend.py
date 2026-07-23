"""
pages/1_Recommend.py

The core feature: user enters requirements + priority, gets the top 5
recommended materials with a radar comparison chart and export options.
"""

import io
import streamlit as st
import plotly.graph_objects as go

from data.materials_database import get_materials_dataframe
from models.material import CorrosionEnvironment, ManufacturingProcess
from utils.scoring import calculate_scores, PRIORITY_PRESETS, top_n
from utils.export import export_to_excel, export_to_pdf

st.set_page_config(page_title="Recommend | Material Recommender", page_icon="🔍", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

st.title("🔍 Material Recommendation")
st.caption("Enter your requirements below. Weights determine how each requirement is traded off during scoring.")

# ---- Requirements form ----
with st.form("requirements_form"):
    st.markdown('<div class="section-label">Mechanical requirements</div>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        min_yield = st.number_input("Min. Yield Strength (MPa)", min_value=0, value=200, step=10)
    with r2:
        min_tensile = st.number_input("Min. Tensile Strength (MPa)", min_value=0, value=0, step=10)
    with r3:
        max_density = st.number_input("Max. Density (g/cm3)", min_value=0.0, value=9.0, step=0.1)
    with r4:
        max_cost = st.slider("Max. Relative Cost (1=cheapest, 10=priciest)", 1, 10, 10)

    st.markdown('<div class="section-label">Service conditions</div>', unsafe_allow_html=True)
    r5, r6, r7 = st.columns(3)
    with r5:
        operating_temp = st.number_input("Operating Temperature (C)", value=25, step=10)
    with r6:
        environment = st.selectbox("Corrosion Environment", [e.value for e in CorrosionEnvironment])
    with r7:
        process = st.selectbox("Manufacturing Process", ["Any"] + [p.value for p in ManufacturingProcess])

    st.markdown('<div class="section-label">Priority</div>', unsafe_allow_html=True)
    priority = st.radio(
        "What matters most?",
        list(PRIORITY_PRESETS.keys()),
        horizontal=True,
    )

    with st.expander("Customize weights (optional)"):
        preset = PRIORITY_PRESETS[priority]
        cw1, cw2, cw3, cw4, cw5 = st.columns(5)
        w_strength = cw1.slider("Strength", 0, 100, preset["strength"])
        w_density = cw2.slider("Weight", 0, 100, preset["density"])
        w_cost = cw3.slider("Cost", 0, 100, preset["cost"])
        w_corrosion = cw4.slider("Corrosion", 0, 100, preset["corrosion"])
        w_temp = cw5.slider("Temperature", 0, 100, preset["temperature"])

    submitted = st.form_submit_button("Find Materials", use_container_width=True)

if submitted:
    weights = {
        "strength": w_strength, "density": w_density, "cost": w_cost,
        "corrosion": w_corrosion, "temperature": w_temp,
    }
    env_enum = CorrosionEnvironment(environment)
    proc_enum = None if process == "Any" else ManufacturingProcess(process)

    scored, exact_match = calculate_scores(
        df,
        min_yield_strength=min_yield,
        min_tensile_strength=min_tensile,
        max_density=max_density,
        max_cost=max_cost,
        operating_temp=operating_temp,
        environment=env_enum,
        process=proc_enum,
        weights=weights,
    )
    results = top_n(scored, 5)
    st.session_state["last_results"] = results
    st.session_state["last_requirements"] = {
        "Min Yield Strength": f"{min_yield} MPa",
        "Min Tensile Strength": f"{min_tensile} MPa",
        "Max Density": f"{max_density} g/cm3",
        "Max Relative Cost": max_cost,
        "Operating Temperature": f"{operating_temp} C",
        "Environment": environment,
        "Process": process,
        "Priority": priority,
    }

    if not exact_match:
        st.warning(
            "No material satisfied every hard requirement — showing the closest-scoring "
            "options across the full database instead. Consider relaxing a constraint."
        )

# ---- Results ----
if "last_results" in st.session_state and len(st.session_state["last_results"]) > 0:
    results = st.session_state["last_results"]

    st.divider()
    st.subheader("Top 5 Recommended Materials")

    for i, row in results.reset_index(drop=True).iterrows():
        st.markdown(
            f"""<div class="material-card">
            <span class="rank-badge">{i+1}</span><b style="font-size:16px">{row['Name']}</b>
            &nbsp;·&nbsp; <span style="color:#5A5548">{row['Family']}</span>
            &nbsp;·&nbsp; <b style="color:#0F5C55">Score: {row['Score']:.1f}/100</b><br>
            <span style="font-size:13px;color:#5A5548">
            Yield {row['Yield Strength (MPa)']} MPa &nbsp;|&nbsp;
            Density {row['Density (g/cm3)']} g/cm3 &nbsp;|&nbsp;
            Cost index {row['Relative Cost']} &nbsp;|&nbsp;
            Corrosion rating {row['Corrosion Resistance']}/10 &nbsp;|&nbsp;
            Max temp {row['Max Service Temp (C)']} C
            </span></div>""",
            unsafe_allow_html=True,
        )

    # ---- Radar comparison of the top 5 ----
    st.subheader("Comparison — Top 5 (normalized)")
    metrics = ["Yield Strength (MPa)", "Density (g/cm3)", "Relative Cost", "Corrosion Resistance", "Max Service Temp (C)"]
    fig = go.Figure()
    for _, row in results.iterrows():
        norm_vals = []
        for m in metrics:
            col_min, col_max = df[m].min(), df[m].max()
            v = (row[m] - col_min) / (col_max - col_min) if col_max > col_min else 1
            # Invert density & cost so "outward" always means "better" on the chart
            if m in ["Density (g/cm3)", "Relative Cost"]:
                v = 1 - v
            norm_vals.append(v)
        fig.add_trace(go.Scatterpolar(r=norm_vals + [norm_vals[0]], theta=metrics + [metrics[0]], fill="toself", name=row["Name"]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=500)
    st.plotly_chart(fig, use_container_width=True)

    # ---- Export ----
    st.subheader("Export")
    e1, e2 = st.columns(2)
    with e1:
        buf = io.BytesIO()
        export_to_excel(results, buf)
        st.download_button("⬇ Download as Excel", buf.getvalue(), "material_recommendations.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with e2:
        pdf_buf = io.BytesIO()
        export_to_pdf(results, st.session_state["last_requirements"], pdf_buf)
        st.download_button("⬇ Download as PDF", pdf_buf.getvalue(), "material_recommendations.pdf", "application/pdf")

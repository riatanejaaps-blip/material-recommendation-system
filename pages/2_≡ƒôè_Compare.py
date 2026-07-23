"""
pages/2_Compare.py

Side-by-side comparison of any set of materials the user selects:
radar chart, grouped bar chart of key properties, and three scatter
plots (cost vs strength, density vs strength, temperature vs cost).
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from data.materials_database import get_materials_dataframe

st.set_page_config(page_title="Compare | Material Recommender", page_icon="📊", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

st.title("📊 Material Comparison")
st.caption("Select 2 or more materials to compare their properties side by side.")

selected_names = st.multiselect(
    "Materials to compare",
    options=sorted(df["Name"].tolist()),
    default=sorted(df["Name"].tolist())[:3],
)

if len(selected_names) < 2:
    st.info("Select at least 2 materials to see comparison charts.")
    st.stop()

subset = df[df["Name"].isin(selected_names)].reset_index(drop=True)

# ---- Radar chart ----
st.subheader("Radar comparison (normalized 0-1, outward = better)")
metrics = ["Yield Strength (MPa)", "Density (g/cm3)", "Relative Cost", "Corrosion Resistance", "Max Service Temp (C)"]
fig_radar = go.Figure()
for _, row in subset.iterrows():
    vals = []
    for m in metrics:
        lo, hi = df[m].min(), df[m].max()
        v = (row[m] - lo) / (hi - lo) if hi > lo else 1
        if m in ["Density (g/cm3)", "Relative Cost"]:
            v = 1 - v
        vals.append(v)
    fig_radar.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=metrics + [metrics[0]], fill="toself", name=row["Name"]))
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=480)
st.plotly_chart(fig_radar, use_container_width=True)

# ---- Bar chart ----
st.subheader("Property comparison (bar chart)")
bar_metric = st.selectbox("Property", metrics, index=0)
fig_bar = px.bar(subset, x="Name", y=bar_metric, color="Name", text=bar_metric)
fig_bar.update_layout(showlegend=False, height=420)
st.plotly_chart(fig_bar, use_container_width=True)

# ---- Scatter plots ----
st.subheader("Trade-off scatter plots")
s1, s2, s3 = st.columns(3)
with s1:
    fig = px.scatter(subset, x="Relative Cost", y="Yield Strength (MPa)", color="Name",
                      size="Density (g/cm3)", title="Cost vs Strength", height=380)
    st.plotly_chart(fig, use_container_width=True)
with s2:
    fig = px.scatter(subset, x="Density (g/cm3)", y="Yield Strength (MPa)", color="Name",
                      title="Density vs Strength", height=380)
    st.plotly_chart(fig, use_container_width=True)
with s3:
    fig = px.scatter(subset, x="Max Service Temp (C)", y="Relative Cost", color="Name",
                      title="Temperature vs Cost", height=380)
    st.plotly_chart(fig, use_container_width=True)

# ---- Corrosion rating bar ----
st.subheader("Corrosion resistance rating")
fig_corr = px.bar(subset.sort_values("Corrosion Resistance"), x="Corrosion Resistance", y="Name",
                   orientation="h", color="Corrosion Resistance", color_continuous_scale="Teal", height=max(300, 40 * len(subset)))
st.plotly_chart(fig_corr, use_container_width=True)

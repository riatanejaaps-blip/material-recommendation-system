"""
app.py

Home page and entry point of the Smart Material Recommendation System.
Run with:  streamlit run app.py

Streamlit auto-discovers every file under pages/ and adds it to the
sidebar navigation automatically — this file only needs to render the
landing page content.
"""

import streamlit as st
from data.materials_database import get_materials_dataframe

st.set_page_config(
    page_title="Smart Material Recommendation System",
    page_icon="🧪",
    layout="wide",
)

# ---- Load shared CSS ----
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

# ---- Hero ----
st.title("🧪 Smart Material Recommendation System")
st.markdown(
    "A decision-support tool for engineers: enter your load, weight, cost, "
    "temperature, and environment requirements, and get ranked material "
    "recommendations backed by a transparent, physics-grounded scoring model "
    "— **not a black-box ML prediction.**"
)

st.divider()

# ---- Quick metrics ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Materials in database", len(df))
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Material families", df["Family"].nunique())
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Manufacturing processes", 6)
    st.markdown("</div>", unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Scoring criteria", 5)
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ---- Feature overview ----
st.subheader("What you can do here")
c1, c2, c3, c4 = st.columns(4)

features = [
    ("🔍", "Recommend", "Enter requirements & priorities, get your top 5 ranked materials."),
    ("📊", "Compare", "Radar, bar, and scatter charts across any set of materials."),
    ("📄", "Material Detail", "Full property sheet, applications, advantages & limitations."),
    ("🔎", "Search & Filter", "Slice the full database by family, cost, density, temperature, and more."),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(
            f'<div class="feature-card"><div style="font-size:28px">{icon}</div>'
            f'<b>{title}</b><p style="font-size:13px;color:#5A5548">{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.divider()
st.markdown(
    "<span class='section-label'>Get started</span><br>"
    "Use the sidebar to jump to <b>Recommend</b> for a guided material search, "
    "or go straight to <b>Search &amp; Filter</b> to browse the full database.",
    unsafe_allow_html=True,
)

with st.expander("How the recommendation engine works"):
    st.markdown(
        """
    1. **Hard filters** remove materials that cannot physically satisfy your requirements
       (too weak, wrong manufacturing process, insufficient corrosion rating, etc.)
    2. **Five criteria** — strength, density, cost, corrosion resistance, and temperature
       capability — are each normalized to a 0–1 scale.
    3. Your **priority weighting** (or custom sliders) combines those into a single
       0–100 score.
    4. The **top 5** highest-scoring materials are returned, ranked.

    No machine learning model is involved — every score is traceable back to the
    material's actual properties and your stated weights, which is what makes this
    suitable for a real engineering decision, not just a demo.
    """
    )

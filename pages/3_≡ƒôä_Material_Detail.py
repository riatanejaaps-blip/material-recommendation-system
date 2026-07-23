"""
pages/3_Material_Detail.py

Full property sheet for a single material: mechanical & physical
properties, applications, advantages, limitations, industries, and
typical components — everything the spec's "Material Detail Page"
section asks for.
"""

import streamlit as st
from data.materials_database import get_materials_dataframe

st.set_page_config(page_title="Material Detail | Material Recommender", page_icon="📄", layout="wide")
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = get_materials_dataframe()

st.title("📄 Material Detail")

name = st.selectbox("Select a material", sorted(df["Name"].tolist()))
row = df[df["Name"] == name].iloc[0]

st.header(row["Name"])
st.caption(f"Family: {row['Family']}")

# ---- Favorites (session-only, keeps state simple without a database) ----
favorites = st.session_state.setdefault("favorites", [])
if name in favorites:
    if st.button("★ Remove from favorites"):
        favorites.remove(name)
        st.rerun()
else:
    if st.button("☆ Add to favorites"):
        favorites.append(name)
        st.rerun()

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="section-label">Mechanical Properties</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        - **Yield Strength:** {row['Yield Strength (MPa)']} MPa
        - **Ultimate Strength:** {row['Ultimate Strength (MPa)']} MPa
        - **Elastic Modulus:** {row['Elastic Modulus (GPa)']} GPa
        - **Hardness:** {row['Hardness (HB)']} HB
        - **Strength-to-Weight:** {row['Strength-to-Weight']}
        """
    )
with col2:
    st.markdown('<div class="section-label">Physical Properties</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        - **Density:** {row['Density (g/cm3)']} g/cm3
        - **Max Service Temperature:** {row['Max Service Temp (C)']} C
        - **Corrosion Resistance:** {row['Corrosion Resistance']}/10
        - **Relative Cost Index:** {row['Relative Cost']}/10
        - **Manufacturing Compatibility:** {', '.join(row['Manufacturing Compatibility'])}
        """
    )

st.divider()
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="section-label">Applications</div>', unsafe_allow_html=True)
    for a in row["Applications"]:
        st.markdown(f"- {a}")
with c2:
    st.markdown('<div class="section-label">Advantages</div>', unsafe_allow_html=True)
    for a in row["Advantages"]:
        st.markdown(f"- ✅ {a}")
with c3:
    st.markdown('<div class="section-label">Limitations</div>', unsafe_allow_html=True)
    for a in row["Limitations"]:
        st.markdown(f"- ⚠️ {a}")

st.divider()
c4, c5 = st.columns(2)
with c4:
    st.markdown('<div class="section-label">Recommended Industries</div>', unsafe_allow_html=True)
    st.write(", ".join(row["Recommended Industries"]) or "—")
with c5:
    st.markdown('<div class="section-label">Typical Components</div>', unsafe_allow_html=True)
    st.write(", ".join(row["Typical Components"]) or "—")

if favorites:
    with st.sidebar:
        st.markdown("### ★ Favorites")
        for f in favorites:
            st.write(f"- {f}")

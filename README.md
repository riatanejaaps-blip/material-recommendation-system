# Smart Material Recommendation System

A Streamlit web app that recommends engineering materials against
user-defined requirements — strength, weight, cost, temperature,
and corrosion environment — using a transparent **weighted scoring
algorithm**, not machine learning. Every recommendation is traceable
back to the material's actual properties and the weights you chose,
which is what makes it defensible for a real engineering decision.

## Features

- **Recommend** — enter mechanical/service requirements and a priority
  (or custom weights), get your top 5 ranked materials with a radar
  comparison chart, Excel export, and PDF report export.
- **Compare** — pick any materials and view radar, bar, and scatter
  (cost vs strength, density vs strength, temperature vs cost) charts.
- **Material Detail** — full property sheet: mechanical/physical
  properties, applications, advantages, limitations, industries,
  typical components. Includes session-based favorites.
- **Search & Filter** — filter the full 50-material database by
  family, cost, density, temperature, corrosion rating, and process.
- **Tools** — unit converter, a rough material cost estimator, and a
  raw decision-matrix table.
- **Database** — 50 materials across all 12 requested families
  (carbon steel, HSLA, tool steel, stainless, aluminium, titanium,
  nickel, copper, magnesium, engineering plastics, ceramics, composites).

## Project structure

```
material_recommender/
├── app.py                      # Home page (Streamlit entry point)
├── requirements.txt
├── models/
│   └── material.py             # Material dataclass, enums, validation
├── data/
│   └── materials_database.py   # 50 materials + DataFrame builder
├── utils/
│   ├── scoring.py               # weighted recommendation engine
│   ├── unit_converter.py
│   └── export.py                 # Excel + PDF export
├── pages/
│   ├── 1_🔍_Recommend.py
│   ├── 2_📊_Compare.py
│   ├── 3_📄_Material_Detail.py
│   ├── 4_🔎_Search_Filter.py
│   └── 5_🛠️_Tools.py
├── assets/
│   └── style.css
└── .streamlit/
    └── config.toml            # theme (colors)
```

## Setup

```bash
cd material_recommender
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).
Every file in `pages/` shows up in the sidebar automatically — no
manual routing code needed.

## How the recommendation engine works

1. **Hard filters** remove materials that cannot physically satisfy a
   stated requirement (too weak, wrong manufacturing process, etc.).
   If nothing survives, the app falls back to ranking the full
   database and flags this clearly rather than returning nothing.
2. Five criteria — **strength, density, cost, corrosion resistance,
   temperature capability** — are each min-max normalized to 0–1.
3. Your **priority weighting** (a preset like "Lowest Weight", or
   custom sliders) combines those into one 0–100 score.
4. The **top 5** highest-scoring materials are returned, ranked.

## Notes

- **Property values are representative engineering estimates**
  (typical handbook ranges), meant to demonstrate the recommendation
  logic — not certified datasheet values for real design use.
- **Dark mode**: use Streamlit's built-in theme switcher (☰ menu, top
  right → Settings → Theme) rather than a custom toggle — this keeps
  the app's own code simpler and gets the same result.
- No `scikit-learn` is used anywhere; the "no ML" requirement is
  reflected in the actual dependency list in `requirements.txt`.

## Talking points for an interview / resume writeup

- **Why weighted scoring instead of ML**: 50 labeled rows with no
  ground-truth "correct" recommendation isn't enough to train a model
  on, and a transparent scoring formula is something an engineer can
  audit and trust for a real material choice — a black-box prediction
  isn't.
- **Modular architecture**: the `Material` dataclass with
  `__post_init__` validation is the single source of truth; the
  scoring engine (`utils/scoring.py`) is pure functions with no
  Streamlit dependency, so it's independently testable.
- **Hard filters + soft scoring** is a standard two-stage decision
  pattern: eliminate the physically impossible first, then rank what
  remains — mirrors how you'd actually shortlist materials by hand.

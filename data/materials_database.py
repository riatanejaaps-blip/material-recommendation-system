"""
data/materials_database.py

The materials database for the Smart Material Recommendation System.

Contains 50 engineering materials across all 12 required families, each
built from the `Material` dataclass in models/material.py. Property
values are representative engineering estimates (typical handbook
ranges, midpoint/room-temperature values) intended for demonstrating
the recommendation logic — not certified datasheet values for design
use. See README.md for that disclaimer in context.

Exposes:
    MATERIALS_DB          -> List[Material]
    get_materials_dataframe() -> pd.DataFrame  (used by every page)
    get_material_by_name(name) -> Material
"""

from __future__ import annotations

from typing import List, Dict
import pandas as pd

from models.material import (
    Material,
    MaterialFamily as Fam,
    ManufacturingProcess as Proc,
)

# Short aliases to keep each entry on a readable line
C, F, R, W, MC, AM = (
    Proc.CASTING, Proc.FORGING, Proc.ROLLING,
    Proc.WELDING, Proc.MACHINING, Proc.ADDITIVE_MANUFACTURING,
)


def M(name, family, density, ys, uts, E, hb, temp, corr, cost,
      processes, applications, advantages, limitations,
      industries=None, components=None, desc="") -> Material:
    """Compact constructor so the 50-row table below stays readable."""
    return Material(
        name=name, family=family, density=density, yield_strength=ys,
        ultimate_strength=uts, elastic_modulus=E, hardness=hb,
        max_service_temp=temp, corrosion_resistance=corr, relative_cost=cost,
        manufacturing_compatibility=processes, applications=applications,
        advantages=advantages, limitations=limitations,
        recommended_industries=industries or [], typical_components=components or [],
        description=desc,
    )


MATERIALS_DB: List[Material] = [

    # ---------------- Carbon Steels ----------------
    M("AISI 1018", Fam.CARBON_STEEL, 7.87, 220, 400, 205, 126, 400, 2, 1,
      [R, W, MC, F], ["Shafts", "Brackets", "Pins"],
      ["Low cost", "Good weldability", "Easy to machine"],
      ["Low corrosion resistance", "Low strength vs alloy steels"],
      ["General fabrication", "Automotive"], ["Bolts", "Structural brackets"]),

    M("AISI 1045", Fam.CARBON_STEEL, 7.85, 310, 565, 200, 170, 400, 2, 2,
      [R, F, MC, W], ["Gears", "Axles", "Crankshafts"],
      ["Good strength-to-cost ratio", "Responds well to heat treatment"],
      ["Poor corrosion resistance", "Needs coating for outdoor use"],
      ["Automotive", "Machinery"], ["Gear shafts", "Spindles"]),

    M("AISI 1095", Fam.CARBON_STEEL, 7.85, 525, 685, 200, 197, 350, 2, 2,
      [R, F, MC], ["Springs", "Cutting tools", "Blades"],
      ["High hardness after heat treatment", "Good wear resistance"],
      ["Brittle if over-hardened", "Poor weldability"],
      ["Tooling", "Hand tools"], ["Leaf springs", "Knife blades"]),

    M("ASTM A36 Structural Steel", Fam.CARBON_STEEL, 7.85, 250, 400, 200, 119, 400, 2, 1,
      [R, W, MC, C], ["Structural beams", "Plates", "Bridges"],
      ["Very low cost", "Excellent weldability", "Widely available"],
      ["Rusts without coating", "Moderate strength"],
      ["Construction", "Infrastructure"], ["I-beams", "Baseplates"]),

    # ---------------- HSLA Steels ----------------
    M("ASTM A572 Grade 50", Fam.HSLA_STEEL, 7.85, 345, 450, 200, 150, 400, 3, 2,
      [R, W, MC], ["Structural steel", "Heavy equipment frames"],
      ["Higher strength than A36 at similar cost", "Good weldability"],
      ["Still needs corrosion protection outdoors"],
      ["Construction", "Heavy machinery"], ["Load-bearing frames"]),

    M("ASTM A588 Weathering Steel", Fam.HSLA_STEEL, 7.85, 345, 485, 200, 160, 400, 5, 3,
      [R, W], ["Bridges", "Outdoor structures"],
      ["Forms protective patina, reduces long-term maintenance"],
      ["Initial rust patina is unsightly", "Not for marine/chemical exposure"],
      ["Infrastructure", "Architecture"], ["Bridge girders", "Sculptures"]),

    M("API 5L X65 Pipeline Steel", Fam.HSLA_STEEL, 7.85, 448, 531, 200, 180, 400, 3, 3,
      [R, W], ["Oil & gas pipelines"],
      ["High strength allows thinner-walled pipe", "Good toughness"],
      ["Requires external coating for buried/subsea service"],
      ["Oil & gas", "Energy"], ["Transmission pipelines"]),

    # ---------------- Tool Steels ----------------
    M("D2 Tool Steel", Fam.TOOL_STEEL, 7.70, 1500, 1900, 210, 650, 425, 4, 6,
      [F, MC], ["Blanking dies", "Punches", "Cutting tools"],
      ["High wear resistance", "Holds a sharp edge"],
      ["Difficult to machine before hardening", "Moderate toughness"],
      ["Tooling", "Stamping"], ["Blanking dies", "Shear blades"]),

    M("H13 Tool Steel", Fam.TOOL_STEEL, 7.80, 1380, 1650, 210, 578, 550, 4, 6,
      [F, MC, C], ["Die casting dies", "Extrusion dies", "Forging dies"],
      ["Excellent hot hardness", "Good thermal shock resistance"],
      ["Expensive vs carbon tool steels"],
      ["Die casting", "Forging"], ["Die casting molds"]),

    M("O1 Tool Steel", Fam.TOOL_STEEL, 7.85, 1380, 1650, 200, 600, 350, 2, 4,
      [F, MC], ["Hand tools", "Gauges", "Knives"],
      ["Oil-hardening: less distortion than water-hardening steels"],
      ["Poor corrosion resistance", "Limited high-temp use"],
      ["Tooling"], ["Precision gauges", "Cutting blades"]),

    # ---------------- Stainless Steels ----------------
    M("SS 304", Fam.STAINLESS_STEEL, 8.00, 215, 505, 193, 155, 870, 7, 4,
      [R, W, MC, C, F], ["Kitchen equipment", "Piping", "Enclosures"],
      ["Good general corrosion resistance", "Widely available", "Good formability"],
      ["Susceptible to chloride pitting"],
      ["Food processing", "Architecture"], ["Sinks", "Handrails"]),

    M("SS 316", Fam.STAINLESS_STEEL, 8.00, 205, 515, 193, 149, 870, 9, 5,
      [R, W, MC, F, C], ["Marine hardware", "Chemical tanks", "Medical implants"],
      ["Molybdenum addition gives strong chloride/marine resistance"],
      ["More expensive than 304"],
      ["Marine", "Pharma", "Medical"], ["Boat fittings", "Surgical instruments"]),

    M("SS 410", Fam.STAINLESS_STEEL, 7.70, 275, 485, 200, 155, 700, 5, 3,
      [F, MC, R], ["Turbine blades", "Valve parts", "Cutlery"],
      ["Hardenable martensitic stainless, good strength"],
      ["Lower corrosion resistance than austenitic grades"],
      ["Power generation", "Cutlery"], ["Steam turbine blades"]),

    M("SS 430", Fam.STAINLESS_STEEL, 7.70, 310, 450, 200, 183, 815, 6, 3,
      [R, F, MC], ["Appliance trim", "Automotive exhaust trim"],
      ["Lower cost than austenitic grades, magnetic"],
      ["Poor weldability", "Lower toughness at low temp"],
      ["Appliances", "Automotive trim"], ["Trim panels", "Exhaust tips"]),

    M("SS 17-4 PH", Fam.STAINLESS_STEEL, 7.75, 1170, 1310, 196, 375, 315, 7, 6,
      [MC, C, F, AM], ["Aerospace fittings", "Pump shafts", "Valve components"],
      ["High strength combined with good corrosion resistance"],
      ["Strength drops above ~300 C"],
      ["Aerospace", "Oil & gas"], ["Landing gear parts", "Pump shafts"]),

    M("SS 2205 Duplex", Fam.STAINLESS_STEEL, 7.80, 450, 655, 200, 260, 300, 9, 6,
      [W, R, F], ["Offshore platforms", "Pressure vessels"],
      ["High strength plus excellent chloride stress-corrosion resistance"],
      ["Requires controlled welding heat input"],
      ["Offshore", "Chemical processing"], ["Pressure vessels", "Piping"]),

    # ---------------- Aluminium Alloys ----------------
    M("Al 6061-T6", Fam.ALUMINIUM_ALLOY, 2.70, 276, 310, 68.9, 95, 200, 6, 3,
      [MC, W, F, AM], ["Structural frames", "Bike frames", "Brackets"],
      ["Good strength-to-weight", "Weldable", "Widely available"],
      ["Lower strength than 7075"],
      ["Aerospace", "Automotive", "Sporting goods"], ["Structural extrusions"]),

    M("Al 7075-T6", Fam.ALUMINIUM_ALLOY, 2.81, 503, 572, 71.7, 150, 150, 4, 5,
      [MC, F], ["Aircraft structural parts", "High-stress fittings"],
      ["Very high strength-to-weight ratio among aluminium alloys"],
      ["Poor weldability", "Lower corrosion resistance than 6061"],
      ["Aerospace", "Motorsport"], ["Wing spars", "Gears"]),

    M("Al 2024-T3", Fam.ALUMINIUM_ALLOY, 2.78, 345, 483, 73.1, 120, 150, 4, 5,
      [MC, F], ["Aircraft fuselage skin"],
      ["Excellent fatigue resistance"],
      ["Poor corrosion resistance without cladding", "Poor weldability"],
      ["Aerospace"], ["Fuselage skins", "Wing ribs"]),

    M("Al 5052-H32", Fam.ALUMINIUM_ALLOY, 2.68, 193, 228, 70.3, 60, 150, 8, 3,
      [R, W, MC], ["Sheet metal enclosures", "Marine panels", "Fuel tanks"],
      ["Very good corrosion resistance, especially marine", "Good formability"],
      ["Lower strength than heat-treatable alloys"],
      ["Marine", "Sheet metal fabrication"], ["Boat hulls", "Fuel tanks"]),

    M("Al 3003-H14", Fam.ALUMINIUM_ALLOY, 2.73, 145, 150, 69.0, 40, 150, 8, 2,
      [R, W, MC], ["Cooking utensils", "Chemical tanks", "Roofing"],
      ["Low cost", "Excellent formability and corrosion resistance"],
      ["Low strength"],
      ["Consumer goods", "HVAC"], ["Heat exchanger fins", "Cookware"]),

    M("Al 356 Cast", Fam.ALUMINIUM_ALLOY, 2.68, 165, 228, 72.4, 70, 150, 6, 3,
      [C], ["Engine blocks", "Housings", "Wheels"],
      ["Excellent castability", "Good pressure tightness"],
      ["Lower strength than wrought alloys"],
      ["Automotive"], ["Engine blocks", "Transmission housings"]),

    # ---------------- Titanium Alloys ----------------
    M("Ti-6Al-4V (Grade 5)", Fam.TITANIUM_ALLOY, 4.43, 880, 950, 113.8, 334, 400, 9, 8,
      [F, MC, AM], ["Aerospace structures", "Medical implants"],
      ["Outstanding strength-to-weight", "Excellent corrosion resistance"],
      ["High material and machining cost"],
      ["Aerospace", "Medical"], ["Turbine discs", "Hip implants"]),

    M("CP Titanium Grade 2", Fam.TITANIUM_ALLOY, 4.51, 275, 345, 103.0, 200, 300, 9, 7,
      [F, MC, W], ["Chemical processing equipment", "Marine hardware"],
      ["Excellent corrosion resistance, good weldability"],
      ["Lower strength than alloyed grades"],
      ["Chemical processing", "Marine"], ["Heat exchangers", "Piping"]),

    M("Ti-6Al-4V ELI (Grade 23)", Fam.TITANIUM_ALLOY, 4.43, 795, 860, 114.0, 320, 400, 9, 9,
      [F, MC, AM], ["Surgical implants", "Aerospace fasteners"],
      ["Extra-low interstitial grade: better fracture toughness for implants"],
      ["Highest cost among common titanium grades"],
      ["Medical", "Aerospace"], ["Bone plates", "Spinal implants"]),

    # ---------------- Nickel Alloys ----------------
    M("Inconel 718", Fam.NICKEL_ALLOY, 8.19, 1035, 1240, 200.0, 350, 700, 9, 9,
      [F, MC, C, AM], ["Jet engine turbine discs", "Gas turbine components"],
      ["Retains strength at high temperature", "Excellent creep resistance"],
      ["Very difficult and costly to machine"],
      ["Aerospace", "Power generation"], ["Turbine discs", "Combustor parts"]),

    M("Inconel 625", Fam.NICKEL_ALLOY, 8.44, 460, 827, 207.5, 220, 980, 10, 9,
      [F, MC, W, AM], ["Marine risers", "Chemical processing", "Exhaust systems"],
      ["Exceptional corrosion and oxidation resistance at high temperature"],
      ["High cost", "Work hardens quickly during machining"],
      ["Oil & gas", "Marine", "Aerospace"], ["Flexible risers", "Reactor liners"]),

    M("Monel 400", Fam.NICKEL_ALLOY, 8.83, 240, 550, 179.0, 130, 480, 9, 8,
      [F, MC, W], ["Marine propeller shafts", "Chemical valves"],
      ["Excellent resistance to seawater and hydrofluoric acid"],
      ["Expensive", "Limited high-temp strength vs Inconel"],
      ["Marine", "Chemical processing"], ["Pump shafts", "Valve trim"]),

    M("Hastelloy C-276", Fam.NICKEL_ALLOY, 8.89, 355, 790, 205.0, 190, 650, 10, 10,
      [F, MC, W, C], ["Flue gas desulfurization", "Chemical reactors"],
      ["Resists nearly all aggressive chemical environments"],
      ["Very high cost", "Difficult to machine"],
      ["Chemical processing", "Pollution control"], ["Reactor vessels", "Scrubbers"]),

    # ---------------- Copper Alloys ----------------
    M("C11000 Copper (ETP)", Fam.COPPER_ALLOY, 8.94, 69, 220, 110.0, 40, 200, 8, 4,
      [R, MC, W], ["Electrical busbars", "Wiring", "Heat exchangers"],
      ["Excellent electrical and thermal conductivity"],
      ["Low mechanical strength"],
      ["Electrical", "HVAC"], ["Busbars", "Heat exchanger tubes"]),

    M("C36000 Brass (Free Cutting)", Fam.COPPER_ALLOY, 8.50, 124, 338, 97.0, 78, 200, 6, 3,
      [MC, C], ["Fittings", "Valve stems", "Fasteners"],
      ["Excellent machinability", "Good corrosion resistance"],
      ["Lower strength than bronzes"],
      ["Plumbing", "Fasteners"], ["Valve stems", "Precision fittings"]),

    M("C51000 Phosphor Bronze", Fam.COPPER_ALLOY, 8.86, 296, 517, 110.0, 160, 200, 7, 5,
      [R, F, MC], ["Springs", "Bearings", "Bellows"],
      ["Good fatigue strength and wear resistance"],
      ["More expensive than brass"],
      ["Electrical connectors", "Bearings"], ["Springs", "Bushings"]),

    M("C71500 Cupronickel", Fam.COPPER_ALLOY, 8.94, 138, 380, 150.0, 90, 300, 9, 6,
      [R, W, MC], ["Seawater piping", "Condenser tubes"],
      ["Outstanding resistance to seawater corrosion and biofouling"],
      ["Lower strength", "Higher cost than copper"],
      ["Marine", "Desalination"], ["Condenser tubes", "Seawater piping"]),

    # ---------------- Magnesium Alloys ----------------
    M("AZ31B Magnesium Alloy", Fam.MAGNESIUM_ALLOY, 1.77, 200, 260, 45.0, 73, 150, 3, 4,
      [R, F, MC], ["Laptop/electronics housings", "Aerospace brackets"],
      ["Lightest structural metal commonly used, good machinability"],
      ["Low corrosion resistance", "Flammable as fine chips/powder"],
      ["Electronics", "Aerospace"], ["Housings", "Brackets"]),

    M("AZ91D Magnesium Alloy", Fam.MAGNESIUM_ALLOY, 1.81, 160, 230, 45.0, 63, 120, 3, 4,
      [C, MC], ["Automotive housings", "Power tool housings"],
      ["Excellent castability, very lightweight"],
      ["Low corrosion resistance", "Low ductility"],
      ["Automotive", "Power tools"], ["Transmission housings"]),

    M("WE43 Magnesium Alloy", Fam.MAGNESIUM_ALLOY, 1.84, 170, 250, 44.0, 75, 300, 5, 8,
      [C, MC], ["Aerospace gearbox housings", "Biodegradable implants"],
      ["Best high-temperature strength among magnesium alloys"],
      ["Expensive due to rare-earth content"],
      ["Aerospace", "Medical"], ["Gearbox housings", "Bioresorbable implants"]),

    # ---------------- Engineering Plastics ----------------
    M("Nylon 6/6 (PA66)", Fam.ENGINEERING_PLASTIC, 1.14, 82, 90, 2.9, 15, 150, 8, 2,
      [MC, AM], ["Gears", "Bushings", "Cable ties"],
      ["Good wear resistance", "Self-lubricating", "Low cost"],
      ["Absorbs moisture, dimensions can shift"],
      ["General industrial", "Automotive"], ["Gears", "Bushings"]),

    M("Polycarbonate (PC)", Fam.ENGINEERING_PLASTIC, 1.20, 62, 65, 2.3, 10, 135, 8, 3,
      [MC, AM], ["Safety glazing", "Machine guards", "Enclosures"],
      ["Very high impact resistance", "Optically clear"],
      ["Scratches easily", "Attacked by some solvents"],
      ["Electronics", "Safety equipment"], ["Machine guards", "Lenses"]),

    M("ABS", Fam.ENGINEERING_PLASTIC, 1.05, 40, 45, 2.3, 8, 100, 7, 1,
      [AM, MC], ["Enclosures", "Automotive interior trim", "Prototypes"],
      ["Low cost", "Easy to mold and 3D print", "Good impact resistance"],
      ["Poor UV resistance", "Lower temperature capability"],
      ["Consumer products", "Prototyping"], ["Enclosures", "Interior trim"]),

    M("PEEK", Fam.ENGINEERING_PLASTIC, 1.32, 100, 110, 3.6, 20, 250, 9, 9,
      [MC, AM], ["Aerospace brackets", "Medical implants", "Semiconductor parts"],
      ["High-temperature capability for a plastic", "Chemically inert"],
      ["Very expensive relative to other plastics"],
      ["Aerospace", "Medical", "Semiconductor"], ["Spinal cages", "Wafer handling parts"]),

    M("UHMWPE", Fam.ENGINEERING_PLASTIC, 0.94, 21, 40, 0.8, 5, 80, 9, 3,
      [MC], ["Conveyor liners", "Bearing pads", "Joint implants"],
      ["Extremely low friction and wear", "Chemically inert"],
      ["Low stiffness, deforms under sustained load"],
      ["Material handling", "Medical"], ["Chute liners", "Knee implant inserts"]),

    M("Acetal (POM)", Fam.ENGINEERING_PLASTIC, 1.41, 65, 70, 3.1, 12, 100, 7, 2,
      [MC], ["Precision gears", "Snap-fit fasteners", "Zipper teeth"],
      ["High stiffness and dimensional stability for a plastic"],
      ["Poor UV resistance", "Flammable"],
      ["Consumer products", "Precision mechanisms"], ["Gears", "Fasteners"]),

    # ---------------- Ceramics ----------------
    M("Alumina (Al2O3)", Fam.CERAMIC, 3.95, 300, 300, 370.0, 1500, 1700, 10, 6,
      [MC], ["Cutting tool inserts", "Electrical insulators", "Wear plates"],
      ["Very high hardness and wear resistance", "Excellent electrical insulation"],
      ["Brittle, poor tensile/impact strength"],
      ["Electronics", "Tooling"], ["Insulators", "Wear-resistant liners"]),

    M("Silicon Carbide (SiC)", Fam.CERAMIC, 3.10, 300, 300, 410.0, 2800, 1650, 10, 7,
      [MC], ["Abrasives", "Kiln furniture", "Armor plating"],
      ["Extreme hardness", "Retains strength at very high temperature"],
      ["Very brittle", "Difficult and costly to machine"],
      ["Aerospace", "Defense", "High-temp processing"], ["Body armor", "Furnace components"]),

    M("Zirconia (ZrO2)", Fam.CERAMIC, 6.00, 500, 500, 200.0, 1200, 1200, 10, 8,
      [MC], ["Dental crowns", "Cutting blades", "Oxygen sensors"],
      ["Higher fracture toughness than most ceramics"],
      ["Expensive", "Still brittle relative to metals"],
      ["Medical/dental", "Sensors"], ["Dental crowns", "Cutting inserts"]),

    M("Silicon Nitride (Si3N4)", Fam.CERAMIC, 3.20, 600, 600, 310.0, 1600, 1400, 10, 8,
      [MC], ["Bearing balls", "Turbocharger rotors"],
      ["Good thermal shock resistance for a ceramic", "Low density, high stiffness"],
      ["Brittle", "High processing cost"],
      ["Automotive", "Aerospace bearings"], ["Bearing balls", "Turbine rotors"]),

    # ---------------- Composites ----------------
    M("Carbon Fiber Reinforced Polymer (CFRP)", Fam.COMPOSITE, 1.60, 600, 600, 135.0, 50, 150, 9, 8,
      [MC], ["Aircraft structures", "Racing car monocoques", "Bike frames"],
      ["Outstanding strength-to-weight ratio", "High stiffness"],
      ["Expensive", "Anisotropic — properties vary by fiber direction"],
      ["Aerospace", "Motorsport"], ["Wing skins", "Chassis panels"]),

    M("Glass Fiber Reinforced Polymer (GFRP)", Fam.COMPOSITE, 1.80, 300, 300, 25.0, 40, 120, 9, 4,
      [MC], ["Boat hulls", "Storage tanks", "Wind turbine blades"],
      ["Good strength at lower cost than carbon fiber", "Corrosion resistant"],
      ["Lower stiffness than CFRP"],
      ["Marine", "Renewable energy"], ["Boat hulls", "Turbine blades"]),

    M("Kevlar Composite", Fam.COMPOSITE, 1.44, 550, 550, 70.0, 30, 150, 9, 7,
      [MC], ["Body armor", "Impact-resistant panels"],
      ["Excellent impact and tear resistance for its weight"],
      ["Weak in compression relative to tension", "UV degradation"],
      ["Defense", "Protective equipment"], ["Body armor panels"]),

    M("Aluminium Metal Matrix Composite (Al-MMC)", Fam.COMPOSITE, 2.90, 400, 450, 100.0, 120, 300, 6, 7,
      [C, MC], ["Brake rotors", "Drive shafts", "Structural aerospace parts"],
      ["Higher stiffness and wear resistance than plain aluminium"],
      ["Reinforcement particles accelerate cutting-tool wear"],
      ["Automotive", "Aerospace"], ["Brake rotors", "Drive shafts"]),
]


def get_materials_dataframe() -> pd.DataFrame:
    """Build the pandas DataFrame every page filters/scores/charts from."""
    return pd.DataFrame([m.to_dict() for m in MATERIALS_DB])


def get_material_by_name(name: str) -> Material:
    """Look up a single Material object by exact name (for detail pages)."""
    matches: Dict[str, Material] = {m.name: m for m in MATERIALS_DB}
    if name not in matches:
        raise KeyError(f"No material named '{name}' in the database.")
    return matches[name]

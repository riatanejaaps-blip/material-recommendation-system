"""
utils/unit_converter.py

Small, self-contained unit conversion helpers used by the Tools page.
Kept as plain functions (not a class) since each conversion is a
stateless, one-line calculation.
"""

from __future__ import annotations

# ---- Stress / pressure ----
def mpa_to_psi(mpa: float) -> float:
    return mpa * 145.038

def psi_to_mpa(psi: float) -> float:
    return psi / 145.038

def mpa_to_ksi(mpa: float) -> float:
    return mpa * 0.145038

# ---- Modulus (large stress values, reported in GPa <-> Msi) ----
def gpa_to_msi(gpa: float) -> float:
    return gpa * 0.145038

def msi_to_gpa(msi: float) -> float:
    return msi / 0.145038

# ---- Density ----
def gcm3_to_lbin3(gcm3: float) -> float:
    return gcm3 * 0.0361273

def lbin3_to_gcm3(lbin3: float) -> float:
    return lbin3 / 0.0361273

def gcm3_to_kgm3(gcm3: float) -> float:
    return gcm3 * 1000.0

# ---- Temperature ----
def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9

def celsius_to_kelvin(c: float) -> float:
    return c + 273.15

# ---- Mass ----
def kg_to_lb(kg: float) -> float:
    return kg * 2.20462

def lb_to_kg(lb: float) -> float:
    return lb / 2.20462


# Registry used to drive the Tools page dropdown without a long if/elif chain.
CONVERSIONS = {
    "MPa -> psi": mpa_to_psi,
    "psi -> MPa": psi_to_mpa,
    "MPa -> ksi": mpa_to_ksi,
    "GPa -> Msi": gpa_to_msi,
    "Msi -> GPa": msi_to_gpa,
    "g/cm3 -> lb/in3": gcm3_to_lbin3,
    "lb/in3 -> g/cm3": lbin3_to_gcm3,
    "g/cm3 -> kg/m3": gcm3_to_kgm3,
    "Celsius -> Fahrenheit": celsius_to_fahrenheit,
    "Fahrenheit -> Celsius": fahrenheit_to_celsius,
    "Celsius -> Kelvin": celsius_to_kelvin,
    "kg -> lb": kg_to_lb,
    "lb -> kg": lb_to_kg,
}

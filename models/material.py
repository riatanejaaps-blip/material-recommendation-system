"""
models/material.py

Core data model for the Smart Material Recommendation System.

Defines the `Material` dataclass — the single source of truth for what
an engineering material "is" in this application — along with the
controlled-vocabulary enums (family, manufacturing process, corrosion
environment) used across the database, scoring engine, and UI pages.

Using enums instead of raw strings for these fields means a typo like
"Marine " (trailing space) or "marine" can't silently break filtering
downstream — invalid values fail fast at construction time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class MaterialFamily(str, Enum):
    """Broad material classification used for grouping and filtering."""
    CARBON_STEEL = "Carbon Steel"
    HSLA_STEEL = "HSLA Steel"
    TOOL_STEEL = "Tool Steel"
    STAINLESS_STEEL = "Stainless Steel"
    ALUMINIUM_ALLOY = "Aluminium Alloy"
    TITANIUM_ALLOY = "Titanium Alloy"
    NICKEL_ALLOY = "Nickel Alloy"
    COPPER_ALLOY = "Copper Alloy"
    MAGNESIUM_ALLOY = "Magnesium Alloy"
    ENGINEERING_PLASTIC = "Engineering Plastic"
    CERAMIC = "Ceramic"
    COMPOSITE = "Composite"


class ManufacturingProcess(str, Enum):
    """Manufacturing routes a material can be compatible with."""
    CASTING = "Casting"
    FORGING = "Forging"
    ROLLING = "Rolling"
    WELDING = "Welding"
    MACHINING = "Machining"
    ADDITIVE_MANUFACTURING = "Additive Manufacturing"


class CorrosionEnvironment(str, Enum):
    """Service environments used to filter by corrosion demand."""
    INDOOR = "Indoor"
    OUTDOOR = "Outdoor"
    MARINE = "Marine"
    CHEMICAL = "Chemical"
    HIGH_HUMIDITY = "High Humidity"


# Minimum corrosion-resistance rating (1-10 scale) a material needs to be
# considered viable in a given environment. Marine and Chemical are the
# most demanding; Indoor is the most forgiving.
ENVIRONMENT_MIN_CORROSION_RATING: Dict[CorrosionEnvironment, int] = {
    CorrosionEnvironment.INDOOR: 2,
    CorrosionEnvironment.OUTDOOR: 5,
    CorrosionEnvironment.HIGH_HUMIDITY: 6,
    CorrosionEnvironment.CHEMICAL: 8,
    CorrosionEnvironment.MARINE: 9,
}


@dataclass
class Material:
    """
    Represents a single engineering material and its properties.

    Units (fixed across the whole database for consistent comparison):
        density               g/cm^3
        yield_strength        MPa
        ultimate_strength     MPa
        elastic_modulus       GPa
        hardness              HB (Brinell equivalent)
        max_service_temp      degrees Celsius
        corrosion_resistance  1-10 rating (10 = best, e.g. Marine-grade)
        relative_cost         1-10 relative index (10 = most expensive)
    """

    name: str
    family: MaterialFamily
    density: float
    yield_strength: float
    ultimate_strength: float
    elastic_modulus: float
    hardness: float
    max_service_temp: float
    corrosion_resistance: int
    relative_cost: float
    manufacturing_compatibility: List[ManufacturingProcess]
    applications: List[str]
    advantages: List[str]
    limitations: List[str]
    recommended_industries: List[str] = field(default_factory=list)
    typical_components: List[str] = field(default_factory=list)
    description: str = ""

    def __post_init__(self) -> None:
        """Basic sanity checks so bad database entries fail loudly,
        not silently, at load time rather than deep inside the UI."""
        if self.density <= 0:
            raise ValueError(f"{self.name}: density must be positive, got {self.density}")
        if self.yield_strength < 0 or self.ultimate_strength < 0:
            raise ValueError(f"{self.name}: strength values cannot be negative")
        if self.ultimate_strength < self.yield_strength:
            raise ValueError(
                f"{self.name}: ultimate_strength ({self.ultimate_strength}) "
                f"cannot be less than yield_strength ({self.yield_strength})"
            )
        if not (1 <= self.corrosion_resistance <= 10):
            raise ValueError(f"{self.name}: corrosion_resistance must be between 1 and 10")
        if not (1 <= self.relative_cost <= 10):
            raise ValueError(f"{self.name}: relative_cost must be between 1 and 10")

    # ---- Derived engineering properties ----------------------------------

    def strength_to_weight_ratio(self) -> float:
        """Yield strength per unit density (MPa per g/cm^3) — higher is
        better for weight-sensitive applications like aerospace or EVs."""
        return self.yield_strength / self.density if self.density else 0.0

    def specific_stiffness(self) -> float:
        """Elastic modulus per unit density — a common aerospace metric."""
        return self.elastic_modulus / self.density if self.density else 0.0

    # ---- Compatibility checks ----------------------------------------------

    def supports_process(self, process: ManufacturingProcess) -> bool:
        """Whether this material can be manufactured via the given process."""
        return process in self.manufacturing_compatibility

    def suitable_for_environment(self, environment: CorrosionEnvironment) -> bool:
        """Whether this material's corrosion rating clears the minimum
        bar required for the given service environment."""
        required = ENVIRONMENT_MIN_CORROSION_RATING[environment]
        return self.corrosion_resistance >= required

    def suitable_for_temperature(self, operating_temp: float) -> bool:
        """Whether this material can handle the given operating temperature."""
        return self.max_service_temp >= operating_temp

    # ---- Serialization -------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Flatten to a plain dict — used to build the pandas DataFrame
        in data/materials_database.py and for JSON/Excel export."""
        return {
            "Name": self.name,
            "Family": self.family.value,
            "Density (g/cm3)": self.density,
            "Yield Strength (MPa)": self.yield_strength,
            "Ultimate Strength (MPa)": self.ultimate_strength,
            "Elastic Modulus (GPa)": self.elastic_modulus,
            "Hardness (HB)": self.hardness,
            "Max Service Temp (C)": self.max_service_temp,
            "Corrosion Resistance": self.corrosion_resistance,
            "Relative Cost": self.relative_cost,
            "Strength-to-Weight": round(self.strength_to_weight_ratio(), 2),
            "Manufacturing Compatibility": [p.value for p in self.manufacturing_compatibility],
            "Applications": self.applications,
            "Advantages": self.advantages,
            "Limitations": self.limitations,
            "Recommended Industries": self.recommended_industries,
            "Typical Components": self.typical_components,
            "Description": self.description,
        }

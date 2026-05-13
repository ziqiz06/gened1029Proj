"""
simulation.py
Physics and habitability logic for Cosmic Origins Adventure.
"""
import math
from dataclasses import dataclass

# ── Stellar constants ─────────────────────────────────────────────────────────

HABITABLE_ZONES = {        # (inner_AU, outer_AU)
    "M": (0.1,  0.4),
    "K": (0.4,  0.8),
    "G": (0.7,  1.5),
    "F": (1.2,  2.5),
}

LUMINOSITY = {"M": 0.04, "K": 0.20, "G": 1.00, "F": 3.00}

STAR_LABELS = {
    "M": "M Dwarf (Red Dwarf)",
    "K": "K Dwarf (Orange Dwarf)",
    "G": "G Dwarf (Sun-like)",
    "F": "F Dwarf (Yellow-White)",
}

# ── Scoring tables ────────────────────────────────────────────────────────────

# Atmospheric greenhouse offset (°C)
ATM_OFFSET  = {"none": -20, "thin": +5, "thick": +15, "greenhouse": +60}

WATER_SCORE = {"none": 0, "ice": 5,  "liquid": 20, "abundant": 25}
ATM_SCORE   = {"none": 0, "thin": 15, "thick": 20,  "greenhouse": 5}
MAG_SCORE   = {"absent": 0, "weak": 7, "strong": 15}
GEO_SCORE   = {"dead": 0, "moderate": 8, "active": 15}
IMPACT_MOD  = {"calm": +5, "moderate": 0, "heavy": -15}

# Albedo by surface type — affects how much stellar energy is absorbed
_ALBEDO = {
    "abundant":   0.25,   # dark ocean absorbs more
    "liquid":     0.28,
    "ice":        0.62,   # bright ice/snow is very reflective
    "none":       0.20,   # bare dark rock
}


# ── World dataclass ───────────────────────────────────────────────────────────

@dataclass
class World:
    journey: str = "earth_like"

    # Star
    star_type: str = "G"

    # Orbit
    distance_au: float = 1.0

    # Physical
    mass_earth:  float = 1.0
    planet_type: str   = "rocky"

    # Atmosphere
    atmosphere: str = "thick"       # none / thin / thick / greenhouse

    # Water
    water: str = "abundant"         # none / ice / liquid / abundant

    # Protection
    magnetic_field: str = "strong"  # absent / weak / strong

    # Geology
    geology: str = "active"         # dead / moderate / active

    # Impact history
    impact_history: str = "moderate"  # calm / moderate / heavy

    # Moon
    moon: str = "large"             # none / small / large

    # Icy-moon-specific
    tidal_heating:    str  = "moderate"   # none / moderate / strong
    subsurface_ocean: bool = True

    # Star-system-specific
    num_planets: int = 8

    # Computed
    surface_temp_c:    float = 0.0
    habitability_score: int  = 0
    in_habitable_zone:  bool = True

    def compute(self) -> "World":
        if self.journey == "icy_moon":
            self.surface_temp_c = _icy_moon_temp(self)
        else:
            self.surface_temp_c = calc_temp(
                self.star_type, self.distance_au,
                self.atmosphere, self.water
            )
        self.in_habitable_zone  = in_hz(self.star_type, self.distance_au)
        self.habitability_score = calc_habitability(self)
        return self

    # ── Display helpers ───────────────────────────────────────────────────────

    @property
    def display_name(self) -> str:
        return {
            "rocky":       "Lithos",
            "gas_giant":   "Jovaris",
            "icy_moon":    "Glaceon",
            "earth_like":  "Nova Terra",
            "star_system": "Helio System",
        }.get(self.journey, "Unknown World")

    @property
    def hab_label(self) -> str:
        s = self.habitability_score
        if self.journey == "star_system":
            if s >= 70: return "Excellent System"
            if s >= 50: return "Promising System"
            if s >= 30: return "Marginal System"
            return "Hostile System"
        if self.journey == "gas_giant":
            if s >= 50: return "Moon Habitability Possible"
            if s >= 25: return "Moon Habitability Marginal"
            return "No Moon Habitability"
        if self._is_earth:
            return "Life Confirmed"
        if s >= 80: return "Possible Life"
        if s >= 55: return "Potentially Habitable"
        if s >= 30: return "Marginal"
        return "Uninhabitable"

    @property
    def hab_color(self) -> str:
        return {
            "Life Confirmed":             "#00bb55",
            "Possible Life":              "#44aa44",
            "Potentially Habitable":      "#aaaa00",
            "Marginal":                   "#cc7700",
            "Uninhabitable":              "#bb2200",
            "Moon Habitability Possible": "#44aacc",
            "Moon Habitability Marginal": "#4477aa",
            "No Moon Habitability":       "#554455",
            "Excellent System":           "#44ccaa",
            "Promising System":           "#44aacc",
            "Marginal System":            "#aaaa00",
            "Hostile System":             "#bb2200",
        }.get(self.hab_label, "#555555")

    @property
    def color(self) -> str:
        if self.journey == "gas_giant":   return "#d4956a"
        if self.journey == "icy_moon":    return "#c8dce8"
        if self.water in ("liquid", "abundant"): return "#2a6db5"
        if self.surface_temp_c < -40 or self.water == "ice": return "#aabfcc"
        if self.surface_temp_c > 400:     return "#c82000"
        return "#b87844"

    @property
    def _is_earth(self) -> bool:
        return (
            self.journey == "earth_like"
            and self.star_type == "G"
            and abs(self.distance_au - 1.0) < 0.05
            and self.atmosphere == "thick"
            and self.water == "abundant"
            and self.magnetic_field == "strong"
            and self.geology == "active"
        )

    @property
    def _mass_class(self) -> str:
        m = self.mass_earth
        if self.journey == "gas_giant":
            if m < 50:  return "Mini-Neptune"
            if m < 150: return "Saturn-like"
            if m < 500: return "Jupiter-like"
            return "Super-Jupiter"
        if m < 0.5:  return "Small world"
        if m < 1.5:  return "Earth-sized"
        if m < 4:    return "Super-Earth"
        return "Mega-Earth"

    @property
    def summary_lines(self) -> list[str]:
        if self.journey == "gas_giant":
            return [
                f"Star type: {STAR_LABELS.get(self.star_type, self.star_type)}",
                f"Distance from star: {self.distance_au} AU",
                f"Mass: {self.mass_earth}× Earth ({self._mass_class})",
                f"Magnetic field: {self.magnetic_field}",
                f"Moon system: {self.moon}",
                f"In habitable zone: {'yes ✅' if self.in_habitable_zone else 'no ❌'}",
                f"Moon habitability potential: {self.hab_label}",
            ]
        if self.journey == "star_system":
            return [
                f"Star type: {STAR_LABELS.get(self.star_type, self.star_type)}",
                f"Number of planets: {self.num_planets}",
                f"Outer gas giant shield: {self.moon}",
                f"Impact history: {self.impact_history}",
                f"Habitable zone: {HABITABLE_ZONES.get(self.star_type, (0,0))[0]}–"
                f"{HABITABLE_ZONES.get(self.star_type, (0,0))[1]} AU",
                f"System rating: {self.hab_label}",
            ]
        if self.journey == "icy_moon":
            return [
                f"Star type: {STAR_LABELS.get(self.star_type, self.star_type)}",
                f"Parent planet distance: {self.distance_au} AU",
                f"Moon mass: {self.mass_earth}× Earth",
                f"Surface temperature: {self.surface_temp_c}°C",
                f"Tidal heating: {self.tidal_heating}",
                f"Subsurface ocean: {'yes' if self.subsurface_ocean else 'no'}",
                f"Magnetic shielding: {self.magnetic_field}",
                f"Geological activity: {self.geology}",
            ]
        return [
            f"Star type: {STAR_LABELS.get(self.star_type, self.star_type)}",
            f"Distance from star: {self.distance_au} AU",
            f"Mass: {self.mass_earth}× Earth ({self._mass_class})",
            f"Surface temperature: {self.surface_temp_c}°C",
            f"Atmosphere: {self.atmosphere}",
            f"Water: {self.water}",
            f"Magnetic field: {self.magnetic_field}",
            f"Geology: {self.geology}",
        ]

    @property
    def score_explanation(self) -> list[tuple[str, int, int]]:
        """Returns (factor, points_earned, max_points) for the result breakdown."""
        if self.journey == "gas_giant":
            moon_pts = {"large": 30, "small": 10, "none": 0}[self.moon]
            return [
                ("Large moon system", moon_pts, 30),
                ("Magnetic field (moon protection)", {"strong": 25, "weak": 12, "absent": 0}[self.magnetic_field], 25),
                ("Distance (near HZ)", 20 if self.in_habitable_zone else 0, 20),
                ("Mass (Jupiter-range optimal)", 15 if 30 <= self.mass_earth <= 318 else 0, 15),
            ]
        if self.journey == "star_system":
            star_pts = {"K": 35, "G": 30, "F": 20, "M": 15}[self.star_type]
            planet_pts = 25 if self.num_planets >= 8 else (18 if self.num_planets >= 4 else 8)
            shield_pts = {"large": 15, "small": 8, "none": 0}[self.moon]
            impact_pts = {"calm": 10, "moderate": 5, "heavy": 0}[self.impact_history]
            return [
                ("Star stability & lifespan", star_pts, 35),
                ("Number of planets", planet_pts, 25),
                ("Outer giant shield", shield_pts, 15),
                ("Impact history", impact_pts, 10),
            ]
        if self.journey == "icy_moon":
            heat_pts = {"none": 5, "moderate": 30, "strong": 15}[self.tidal_heating]
            return [
                ("Subsurface ocean", 35 if self.subsurface_ocean else 0, 35),
                ("Tidal heating (moderate = sweet spot)", heat_pts, 30),
                ("Magnetic shielding", MAG_SCORE.get(self.magnetic_field, 0) // 2, 7),
                ("Geological activity", GEO_SCORE.get(self.geology, 0), 15),
            ]
        temp_pts = 30 if -20 <= self.surface_temp_c <= 65 else (10 if -60 <= self.surface_temp_c <= 100 else 0)
        return [
            ("Temperature in liquid-water range", temp_pts, 30),
            ("Water presence", WATER_SCORE.get(self.water, 0), 25),
            ("Atmosphere", ATM_SCORE.get(self.atmosphere, 0), 20),
            ("Magnetic field", MAG_SCORE.get(self.magnetic_field, 0), 15),
            ("Geological activity", GEO_SCORE.get(self.geology, 0), 15),
            ("Impact history", IMPACT_MOD.get(self.impact_history, 0), 5),
            ("Large stabilising moon", 5 if self.moon == "large" else 0, 5),
        ]


# ── Physics ───────────────────────────────────────────────────────────────────

def calc_temp(star_type: str, distance_au: float,
              atmosphere: str, water: str = "none") -> float:
    """
    Simplified energy-balance temperature.
    T_eq = 278 × (L × (1−albedo))^0.25 / sqrt(d)  →  Celsius + atmospheric offset.
    Albedo varies with surface type: ice is reflective, ocean is dark.
    A greenhouse atmosphere adds a further +60°C.
    """
    lum    = LUMINOSITY.get(star_type, 1.0)
    albedo = _ALBEDO.get(water, 0.30)
    if atmosphere == "greenhouse":
        albedo = 0.72      # Venus-like thick cloud cover is very bright
    elif atmosphere == "thick" and water in ("liquid", "abundant"):
        albedo = 0.30      # Earth-like cloud feedback

    temp_k = 278.0 * (lum * (1.0 - albedo)) ** 0.25 / math.sqrt(max(distance_au, 0.01))
    return round(temp_k - 273.15 + ATM_OFFSET.get(atmosphere, 0), 1)


def _icy_moon_temp(w: World) -> float:
    """
    Icy moon surface temperature = stellar heating at distance + tidal heating offset.
    Ice is highly reflective (albedo ~0.65), so stellar input is low in the outer system.
    Tidal heating from the parent planet adds warmth independently of the star.
    """
    lum    = LUMINOSITY.get(w.star_type, 1.0)
    temp_k = 278.0 * (lum * (1.0 - 0.65)) ** 0.25 / math.sqrt(max(w.distance_au, 0.01))
    base   = temp_k - 273.15          # typically −150°C to −200°C in outer system
    tidal  = {"none": 0, "moderate": 30, "strong": 90}
    return round(base + tidal.get(w.tidal_heating, 0), 1)


def in_hz(star_type: str, distance_au: float) -> bool:
    inner, outer = HABITABLE_ZONES.get(star_type, (0.7, 1.5))
    return inner <= distance_au <= outer


def calc_habitability(w: World) -> int:
    """Return 0–100 habitability score."""
    if w.journey == "gas_giant":
        return _gas_giant_score(w)
    if w.journey == "star_system":
        return _star_system_score(w)
    if w.journey == "icy_moon":
        return _icy_moon_score(w)
    return _rocky_score(w)


def _rocky_score(w: World) -> int:
    s = 0
    if -20 <= w.surface_temp_c <= 65:
        s += 30
    elif -60 <= w.surface_temp_c <= 100:
        s += 10
    s += WATER_SCORE.get(w.water, 0)
    s += ATM_SCORE.get(w.atmosphere, 0)
    s += MAG_SCORE.get(w.magnetic_field, 0)
    s += GEO_SCORE.get(w.geology, 0)
    s += IMPACT_MOD.get(w.impact_history, 0)
    if w.moon == "large":
        s += 5    # large moon stabilises axial tilt (like Earth's Moon)
    return max(0, min(100, s))


def _icy_moon_score(w: World) -> int:
    s = 0
    if w.subsurface_ocean:
        s += 35
    # Moderate tidal heating is the sweet spot: enough for liquid water,
    # not so much that the moon becomes volcanic like Io.
    s += {"none": 5, "moderate": 30, "strong": 15}[w.tidal_heating]
    s += MAG_SCORE.get(w.magnetic_field, 0) // 2   # partial shielding from parent planet
    s += GEO_SCORE.get(w.geology, 0)
    return max(0, min(100, s))


def _gas_giant_score(w: World) -> int:
    """Score a gas giant by its potential to host habitable moons."""
    if w.moon == "none":
        return 0    # no moons → no moon habitability possible
    s = 0
    s += {"large": 30, "small": 10}[w.moon]
    # Strong magnetic field protects moons from radiation
    s += {"strong": 25, "weak": 12, "absent": 0}[w.magnetic_field]
    # Being near the star's HZ gives moons both tidal + solar heating
    if in_hz(w.star_type, w.distance_au):
        s += 20
    # Jupiter-mass range (30–318 Earth) is optimal — super-Jupiters
    # generate intense radiation belts that sterilise moons
    if 30 <= w.mass_earth <= 318:
        s += 15
    elif w.mass_earth > 318:
        s -= 10
    return max(0, min(70, s))


def _star_system_score(w: World) -> int:
    """Score the star system's overall potential to host habitable worlds."""
    s = 0
    # Star type stability and lifespan
    s += {"K": 35, "G": 30, "F": 20, "M": 15}[w.star_type]
    # More planets → more chances for one to land in the HZ
    if w.num_planets >= 8:
        s += 25
    elif w.num_planets >= 4:
        s += 18
    else:
        s += 8
    # Outer gas giant shields inner rocky worlds from bombardment
    s += {"large": 15, "small": 8, "none": 0}[w.moon]
    # Impact history
    s += {"calm": 10, "moderate": 5, "heavy": 0}[w.impact_history]
    return max(0, min(85, s))


# ── Build from choices dict ───────────────────────────────────────────────────

def build_world(journey: str, choices: dict) -> World:
    type_map = {
        "rocky": "rocky", "gas_giant": "gas_giant",
        "icy_moon": "icy_moon", "earth_like": "rocky", "star_system": "star",
    }
    w = World(journey=journey, planet_type=type_map.get(journey, "rocky"))
    for key, val in choices.items():
        if hasattr(w, key):
            setattr(w, key, val)
    return w.compute()


# ── Earth reference ───────────────────────────────────────────────────────────

EARTH = build_world("earth_like", {
    "star_type": "G", "distance_au": 1.0, "mass_earth": 1.0,
    "atmosphere": "thick", "water": "abundant",
    "magnetic_field": "strong", "geology": "active",
    "impact_history": "moderate", "moon": "large",
})
EARTH.surface_temp_c    = 15.0
EARTH.habitability_score = 95

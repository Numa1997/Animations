"""
Physical constants and unit conversions.

All values in SI units unless otherwise specified.
"""

import numpy as np

# Mathematical constants
PI = np.pi
E = np.e
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2

# Fundamental constants
SPEED_OF_LIGHT = 299792458.0  # m/s (exact)
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s (exact)
REDUCED_PLANCK = PLANCK_CONSTANT / (2 * PI)  # ℏ
GRAVITATIONAL_CONSTANT = 6.67430e-11  # m³/(kg⋅s²)
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K (exact)
AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹ (exact)
ELEMENTARY_CHARGE = 1.602176634e-19  # C (exact)
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m
VACUUM_PERMEABILITY = 1.25663706212e-6  # H/m

# Standard gravity
STANDARD_GRAVITY = 9.80665  # m/s² (exact)

# Astronomical constants
AU = 1.495978707e11  # m (astronomical unit)
PARSEC = 3.0857e16  # m
LIGHT_YEAR = 9.4607e15  # m
SOLAR_MASS = 1.98847e30  # kg
EARTH_MASS = 5.97217e24  # kg
EARTH_RADIUS = 6.371e6  # m

# Atomic constants
ELECTRON_MASS = 9.1093837015e-31  # kg
PROTON_MASS = 1.67262192369e-27  # kg
NEUTRON_MASS = 1.67492749804e-27  # kg
ATOMIC_MASS_UNIT = 1.66053906660e-27  # kg
BOHR_RADIUS = 5.29177210903e-11  # m
RYDBERG_CONSTANT = 1.0973731568160e7  # m⁻¹

# Common unit conversions
class Units:
    """Unit conversion factors."""

    # Length
    METER_TO_CM = 100
    METER_TO_MM = 1000
    METER_TO_KM = 1e-3
    METER_TO_INCH = 39.3701
    METER_TO_FOOT = 3.28084

    # Time
    SECOND_TO_MS = 1000
    SECOND_TO_MIN = 1/60
    SECOND_TO_HOUR = 1/3600
    SECOND_TO_DAY = 1/86400

    # Mass
    KG_TO_GRAM = 1000
    KG_TO_POUND = 2.20462

    # Energy
    JOULE_TO_ERG = 1e7
    JOULE_TO_EV = 6.242e18
    JOULE_TO_CAL = 0.239006
    JOULE_TO_KWH = 2.778e-7

    # Power
    WATT_TO_HP = 0.00134102

    # Angle
    RAD_TO_DEG = 180 / PI
    DEG_TO_RAD = PI / 180

    # Temperature
    @staticmethod
    def celsius_to_kelvin(T_C):
        """Convert Celsius to Kelvin."""
        return T_C + 273.15

    @staticmethod
    def kelvin_to_celsius(T_K):
        """Convert Kelvin to Celsius."""
        return T_K - 273.15

    @staticmethod
    def fahrenheit_to_celsius(T_F):
        """Convert Fahrenheit to Celsius."""
        return (T_F - 32) * 5/9

    @staticmethod
    def celsius_to_fahrenheit(T_C):
        """Convert Celsius to Fahrenheit."""
        return T_C * 9/5 + 32


# Common physical scenarios
class CommonValues:
    """Typical values for common scenarios."""

    # Earth
    g_earth = STANDARD_GRAVITY  # m/s²

    # Air (at STP)
    air_density = 1.225  # kg/m³
    air_viscosity = 1.81e-5  # Pa⋅s

    # Water
    water_density = 1000  # kg/m³
    water_viscosity = 8.9e-4  # Pa⋅s at 25°C

    # Room temperature
    room_temp_K = 293.15  # K (20°C)
    room_temp_C = 20.0  # °C


if __name__ == '__main__':
    # Sanity checks
    print(f"Speed of light: {SPEED_OF_LIGHT:.3e} m/s")
    print(f"Planck constant: {PLANCK_CONSTANT:.3e} J⋅s")
    print(f"Standard gravity: {STANDARD_GRAVITY} m/s²")
    print(f"π = {PI:.10f}")
    print(f"90° = {90 * Units.DEG_TO_RAD:.10f} rad")

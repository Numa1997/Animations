"""
Symbolic definitions for bouncing balls on parameterized parabola.

This module contains the mathematical equations in symbolic and numerical form.

The parabola is parameterized as y = a*x², where:
- a = 1.0: Standard parabola
- a < 1.0: Flatter curve (gentler slopes, smaller collision angles)
- a > 1.0: Steeper curve (sharper slopes, larger collision angles)
"""

import numpy as np
from typing import Tuple

# Parabola definition
def parabola(x: float, a: float = 1.0) -> float:
    """
    Parameterized parabola equation: y = a*x²

    Parameters
    ----------
    x : float
        Horizontal position
    a : float, optional
        Parabola steepness parameter (default 1.0)

    Returns
    -------
    float
        Vertical position y = a*x²
    """
    return a * x**2

def parabola_derivative(x: float, a: float = 1.0) -> float:
    """
    Derivative of parameterized parabola: dy/dx = 2*a*x

    Parameters
    ----------
    x : float
        Horizontal position
    a : float, optional
        Parabola steepness parameter (default 1.0)

    Returns
    -------
    float
        Slope at position x
    """
    return 2*a*x

# Free fall equations (between bounces)
def free_fall_derivatives(t: float, state: np.ndarray, g: float = 9.80665,
                         a: float = 1.0) -> np.ndarray:
    """
    Free fall equations of motion.

    Parameters
    ----------
    t : float
        Time (not used, but required for ODE interface)
    state : ndarray
        State vector [x, y, vx, vy]
    g : float
        Gravitational acceleration (m/s²)
    a : float
        Parabola parameter (not used in free fall, but kept for consistency)

    Returns
    -------
    ndarray
        Derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]
    """
    x, y, vx, vy = state
    return np.array([vx, vy, 0.0, -g])

# Collision detection
def collision_event(t: float, state: np.ndarray, g: float = 9.80665,
                   a: float = 1.0) -> float:
    """
    Event function for collision detection.
    Returns zero when ball touches parabola.

    Parameters
    ----------
    t : float
        Time
    state : ndarray
        State vector [x, y, vx, vy]
    g : float
        Gravitational acceleration
    a : float
        Parabola steepness parameter

    Returns
    -------
    float
        Event function h = y - a*x²
    """
    x, y, vx, vy = state
    return y - a*x**2  # No buffer - event detection handles re-triggers naturally

def is_approaching(state: np.ndarray, a: float = 1.0) -> bool:
    """
    Check if ball is approaching the parabola.

    Parameters
    ----------
    state : ndarray
        State vector [x, y, vx, vy]
    a : float
        Parabola steepness parameter

    Returns
    -------
    bool
        True if approaching (dh/dt < 0)
    """
    x, y, vx, vy = state
    dh_dt = vy - 2*a*x*vx
    return dh_dt < 0

# Elastic reflection
def normal_vector(x_c: float, a: float = 1.0) -> Tuple[float, float]:
    """
    Compute normalized normal vector at collision point on y = a*x².

    For parabola y = a*x², the tangent has slope dy/dx = 2*a*x_c.
    Tangent vector: (1, 2*a*x_c)
    Normal vector (perpendicular, pointing OUTWARD): (2*a*x_c, 1)

    The outward normal points away from the parabola interior (below the curve).
    At x > 0 (right side), it points RIGHT and UP.
    At x < 0 (left side), it points LEFT and UP.

    Parameters
    ----------
    x_c : float
        x-coordinate of collision point
    a : float
        Parabola steepness parameter

    Returns
    -------
    tuple
        (nx, ny) - normalized normal vector components pointing OUTWARD
    """
    norm = np.sqrt(1 + 4*a**2*x_c**2)
    return (2*a*x_c / norm, 1.0 / norm)  # FIXED: Positive sign for outward normal

def tangent_vector(x_c: float, a: float = 1.0) -> Tuple[float, float]:
    """
    Compute normalized tangent vector at collision point.

    Parameters
    ----------
    x_c : float
        x-coordinate of collision point
    a : float
        Parabola steepness parameter

    Returns
    -------
    tuple
        (tx, ty) - normalized tangent vector components
    """
    norm = np.sqrt(1 + 4*a**2*x_c**2)
    return (1.0 / norm, 2*a*x_c / norm)

def reflect_velocity(vx: float, vy: float, x_c: float, a: float = 1.0) -> Tuple[float, float]:
    """
    Compute reflected velocity after elastic collision with parabola.

    Uses the formula: v' = v - 2(v·n̂)n̂

    Parameters
    ----------
    vx, vy : float
        Velocity components before collision
    x_c : float
        x-coordinate of collision point
    a : float
        Parabola steepness parameter

    Returns
    -------
    tuple
        (vx', vy') - velocity components after collision
    """
    # Compute normal vector components
    nx, ny = normal_vector(x_c, a)

    # Compute dot product v · n̂
    v_dot_n = vx*nx + vy*ny

    # Reflect: v' = v - 2(v·n̂)n̂
    vx_new = vx - 2*v_dot_n*nx
    vy_new = vy - 2*v_dot_n*ny

    return vx_new, vy_new

def reflect_velocity_direct(vx: float, vy: float, x_c: float, a: float = 1.0) -> Tuple[float, float]:
    """
    Direct formula for reflected velocity (optimized).

    Derived formulae for y = a*x²:

    Normal: n̂ = (-2ax_c, 1) / √(1 + 4a²x_c²)

    v·n̂ = (-2ax_c·vx + vy) / √(1 + 4a²x_c²)

    Reflection v' = v - 2(v·n̂)n̂:

    vx' = [vx(1 - 4a²x_c²) + 4ax_c·vy] / (1 + 4a²x_c²)
    vy' = [4ax_c·vx + vy(4a²x_c² - 1)] / (1 + 4a²x_c²)

    When a=1, reduces to:
    vx' = [vx(1 - 4x_c²) + 4x_c·vy] / (1 + 4x_c²)
    vy' = [4x_c·vx + vy(4x_c² - 1)] / (1 + 4x_c²)

    Parameters
    ----------
    vx, vy : float
        Velocity components before collision
    x_c : float
        x-coordinate of collision point
    a : float
        Parabola steepness parameter

    Returns
    -------
    tuple
        (vx', vy') - velocity components after collision
    """
    denom = 1.0 + 4*a**2*x_c**2
    vx_new = (vx*(1 - 4*a**2*x_c**2) + 4*a*x_c*vy) / denom
    vy_new = (4*a*x_c*vx + vy*(4*a**2*x_c**2 - 1)) / denom
    return vx_new, vy_new

# Energy calculations
def kinetic_energy(vx: float, vy: float, m: float = 1.0) -> float:
    """Kinetic energy: T = (1/2)m(vx² + vy²)"""
    return 0.5 * m * (vx**2 + vy**2)

def potential_energy(y: float, m: float = 1.0, g: float = 9.80665) -> float:
    """Gravitational potential energy: V = mgy"""
    return m * g * y

def total_energy(x: float, y: float, vx: float, vy: float,
                 m: float = 1.0, g: float = 9.80665, a: float = 1.0) -> float:
    """
    Total mechanical energy: E = T + V

    Note: Parameter 'a' doesn't affect energy, only collision geometry.
    """
    return kinetic_energy(vx, vy, m) + potential_energy(y, m, g)

# Divergence metrics
def separation_distance(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Euclidean distance between two balls in configuration space.

    Parameters
    ----------
    state1, state2 : ndarray
        State vectors [x, y, vx, vy]

    Returns
    -------
    float
        Distance d = √[(x₁-x₂)² + (y₁-y₂)²]
    """
    x1, y1 = state1[0], state1[1]
    x2, y2 = state2[0], state2[1]
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def velocity_separation(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Velocity space separation.

    Parameters
    ----------
    state1, state2 : ndarray
        State vectors [x, y, vx, vy]

    Returns
    -------
    float
        Distance in velocity space
    """
    vx1, vy1 = state1[2], state1[3]
    vx2, vy2 = state2[2], state2[3]
    return np.sqrt((vx1 - vx2)**2 + (vy1 - vy2)**2)

def full_phase_space_separation(state1: np.ndarray, state2: np.ndarray) -> float:
    """
    Full 4D phase space separation.

    Parameters
    ----------
    state1, state2 : ndarray
        State vectors [x, y, vx, vy]

    Returns
    -------
    float
        Distance in 4D phase space
    """
    diff = state1 - state2
    return np.linalg.norm(diff)


if __name__ == '__main__':
    # Test reflection with different 'a' values
    print("Testing elastic reflection with parameterized parabola:")
    print("=" * 60)

    vx, vy = 1.0, -2.0
    x_c = 1.0

    for a in [0.3, 0.5, 1.0, 2.0]:
        print(f"\nParabola parameter a = {a:.1f}:")
        print(f"Before: vx={vx:.4f}, vy={vy:.4f}")

        vx_new, vy_new = reflect_velocity(vx, vy, x_c, a)
        print(f"After (general): vx'={vx_new:.4f}, vy'={vy_new:.4f}")

        vx_new2, vy_new2 = reflect_velocity_direct(vx, vy, x_c, a)
        print(f"After (direct):  vx'={vx_new2:.4f}, vy'={vy_new2:.4f}")

        # Check energy conservation
        E_before = vx**2 + vy**2
        E_after = vx_new**2 + vy_new**2
        print(f"Speed before: {np.sqrt(E_before):.6f}")
        print(f"Speed after:  {np.sqrt(E_after):.6f}")
        print(f"Energy conserved: {np.isclose(E_before, E_after)}")

        # Check agreement between methods
        print(f"Methods agree: {np.allclose([vx_new, vy_new], [vx_new2, vy_new2])}")

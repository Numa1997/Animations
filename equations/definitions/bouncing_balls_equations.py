"""
Symbolic definitions for bouncing balls on parabola.

This module contains the mathematical equations in symbolic and numerical form.
"""

import numpy as np
from typing import Tuple

# Parabola definition
def parabola(x: float) -> float:
    """Parabola equation: y = x²"""
    return x**2

def parabola_derivative(x: float) -> float:
    """Derivative of parabola: dy/dx = 2x"""
    return 2*x

# Free fall equations (between bounces)
def free_fall_derivatives(t: float, state: np.ndarray, g: float = 9.80665) -> np.ndarray:
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

    Returns
    -------
    ndarray
        Derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]
    """
    x, y, vx, vy = state
    return np.array([vx, vy, 0.0, -g])

# Collision detection
def collision_event(t: float, state: np.ndarray, g: float = 9.80665) -> float:
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

    Returns
    -------
    float
        Event function h = y - x²
    """
    x, y, vx, vy = state
    return y - x**2

def is_approaching(state: np.ndarray) -> bool:
    """
    Check if ball is approaching the parabola.

    Parameters
    ----------
    state : ndarray
        State vector [x, y, vx, vy]

    Returns
    -------
    bool
        True if approaching (dh/dt < 0)
    """
    x, y, vx, vy = state
    dh_dt = vy - 2*x*vx
    return dh_dt < 0

# Elastic reflection
def normal_vector(x_c: float) -> Tuple[float, float]:
    """
    Compute normalized normal vector at collision point.

    Parameters
    ----------
    x_c : float
        x-coordinate of collision point

    Returns
    -------
    tuple
        (nx, ny) - normalized normal vector components
    """
    norm = np.sqrt(1 + 4*x_c**2)
    return (-2*x_c / norm, 1.0 / norm)

def tangent_vector(x_c: float) -> Tuple[float, float]:
    """
    Compute normalized tangent vector at collision point.

    Parameters
    ----------
    x_c : float
        x-coordinate of collision point

    Returns
    -------
    tuple
        (tx, ty) - normalized tangent vector components
    """
    norm = np.sqrt(1 + 4*x_c**2)
    return (1.0 / norm, 2*x_c / norm)

def reflect_velocity(vx: float, vy: float, x_c: float) -> Tuple[float, float]:
    """
    Compute reflected velocity after elastic collision with parabola.

    Uses the formula: v' = v - 2(v·n̂)n̂

    Parameters
    ----------
    vx, vy : float
        Velocity components before collision
    x_c : float
        x-coordinate of collision point

    Returns
    -------
    tuple
        (vx', vy') - velocity components after collision
    """
    # Compute normal vector components
    nx, ny = normal_vector(x_c)

    # Compute dot product v · n̂
    v_dot_n = vx*nx + vy*ny

    # Reflect: v' = v - 2(v·n̂)n̂
    vx_new = vx - 2*v_dot_n*nx
    vy_new = vy - 2*v_dot_n*ny

    return vx_new, vy_new

def reflect_velocity_direct(vx: float, vy: float, x_c: float) -> Tuple[float, float]:
    """
    Direct formula for reflected velocity (optimized).

    Derived formulae:
    vx' = [vx(1 + 12xc²) - 4xc·vy] / (1 + 4xc²)
    vy' = [4xc·vx + vy(4xc² - 1)] / (1 + 4xc²)

    Parameters
    ----------
    vx, vy : float
        Velocity components before collision
    x_c : float
        x-coordinate of collision point

    Returns
    -------
    tuple
        (vx', vy') - velocity components after collision
    """
    denom = 1.0 + 4*x_c**2
    vx_new = (vx*(1 + 12*x_c**2) - 4*x_c*vy) / denom
    vy_new = (4*x_c*vx + vy*(4*x_c**2 - 1)) / denom
    return vx_new, vy_new

# Energy calculations
def kinetic_energy(vx: float, vy: float, m: float = 1.0) -> float:
    """Kinetic energy: T = (1/2)m(vx² + vy²)"""
    return 0.5 * m * (vx**2 + vy**2)

def potential_energy(y: float, m: float = 1.0, g: float = 9.80665) -> float:
    """Gravitational potential energy: V = mgy"""
    return m * g * y

def total_energy(x: float, y: float, vx: float, vy: float,
                 m: float = 1.0, g: float = 9.80665) -> float:
    """Total mechanical energy: E = T + V"""
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
    # Test reflection
    print("Testing elastic reflection:")
    vx, vy = 1.0, -2.0
    x_c = 1.0
    print(f"Before: vx={vx}, vy={vy}")

    vx_new, vy_new = reflect_velocity(vx, vy, x_c)
    print(f"After (general): vx'={vx_new:.6f}, vy'={vy_new:.6f}")

    vx_new2, vy_new2 = reflect_velocity_direct(vx, vy, x_c)
    print(f"After (direct):  vx'={vx_new2:.6f}, vy'={vy_new2:.6f}")

    # Check energy conservation
    E_before = vx**2 + vy**2
    E_after = vx_new**2 + vy_new**2
    print(f"Speed before: {np.sqrt(E_before):.6f}")
    print(f"Speed after:  {np.sqrt(E_after):.6f}")
    print(f"Energy conserved: {np.isclose(E_before, E_after)}")

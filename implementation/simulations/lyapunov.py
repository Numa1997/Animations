"""
Lyapunov Exponent Calculator for Chaos Quantification

Calculate finite-time Lyapunov exponents from diverging trajectories.
"""

import numpy as np
from typing import Dict


def calculate_lyapunov_exponent(traj1: Dict, traj2: Dict, delta_0: float) -> Dict:
    """
    Calculate finite-time Lyapunov exponent from two trajectories.

    The Lyapunov exponent λ characterizes the rate of exponential divergence:
        δ(t) ≈ δ₀ * e^(λt)

    Therefore: λ(t) ≈ (1/t) * ln(δ(t)/δ₀)

    Parameters
    ----------
    traj1, traj2 : dict
        Trajectory data with keys 't', 'x', 'y'
    delta_0 : float
        Initial separation between trajectories

    Returns
    -------
    dict
        - 't': time array
        - 'lambda': Lyapunov exponent as function of time
        - 'lambda_mean': mean Lyapunov exponent
        - 'lambda_final': final Lyapunov exponent value
        - 'separation': separation as function of time
        - 'exp_fit': exponential fit parameters (if applicable)
    """
    # Find common time grid
    t1, t2 = np.array(traj1['t']), np.array(traj2['t'])
    t_max_common = min(t1[-1], t2[-1])

    # Create common time grid
    n_points = min(len(t1), len(t2))
    t_common = np.linspace(0, t_max_common, n_points)

    # Interpolate trajectories to common grid
    x1 = np.interp(t_common, t1, traj1['x'])
    y1 = np.interp(t_common, t1, traj1['y'])
    x2 = np.interp(t_common, t2, traj2['x'])
    y2 = np.interp(t_common, t2, traj2['y'])

    # Calculate separation
    sep = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Avoid log(0) and division by zero
    valid_idx = (sep > 1e-10) & (t_common > 1e-10) & (sep > delta_0 * 0.1)
    t_valid = t_common[valid_idx]
    sep_valid = sep[valid_idx]

    if len(t_valid) == 0:
        return {
            't': t_common,
            'lambda': np.zeros_like(t_common),
            'lambda_mean': 0.0,
            'lambda_final': 0.0,
            'separation': sep,
            'exp_fit': None
        }

    # Calculate λ(t) = ln(sep(t)/delta_0) / t
    lambda_t = np.log(sep_valid / delta_0) / t_valid

    # For exponential fit: ln(sep) = ln(delta_0) + λ*t
    # So fit ln(sep) vs t to get λ
    try:
        from scipy.stats import linregress
        slope, intercept, r_value, p_value, std_err = linregress(t_valid, np.log(sep_valid))
        exp_fit = {
            'lambda': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'std_err': std_err
        }
    except:
        exp_fit = None

    return {
        't': t_valid,
        'lambda': lambda_t,
        'lambda_mean': np.mean(lambda_t),
        'lambda_final': lambda_t[-1] if len(lambda_t) > 0 else 0.0,
        'separation': sep,
        't_full': t_common,
        'exp_fit': exp_fit
    }


def estimate_divergence_time(traj1: Dict, traj2: Dict, delta_0: float,
                            threshold_factor: float = 10.0) -> Dict:
    """
    Estimate time for trajectories to diverge beyond threshold.

    Parameters
    ----------
    traj1, traj2 : dict
        Trajectory data
    delta_0 : float
        Initial separation
    threshold_factor : float
        Divergence threshold as multiple of initial separation

    Returns
    -------
    dict
        - 'divergence_time': time when threshold exceeded (or None)
        - 'diverged': bool, whether divergence occurred
        - 'threshold': threshold value used
        - 'max_separation': maximum separation achieved
    """
    t1, t2 = np.array(traj1['t']), np.array(traj2['t'])
    t_max_common = min(t1[-1], t2[-1])

    n_points = min(len(t1), len(t2))
    t_common = np.linspace(0, t_max_common, n_points)

    x1 = np.interp(t_common, t1, traj1['x'])
    y1 = np.interp(t_common, t1, traj1['y'])
    x2 = np.interp(t_common, t2, traj2['x'])
    y2 = np.interp(t_common, t2, traj2['y'])

    sep = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    threshold = threshold_factor * delta_0
    diverged_indices = np.where(sep > threshold)[0]

    if len(diverged_indices) > 0:
        divergence_time = t_common[diverged_indices[0]]
        diverged = True
    else:
        divergence_time = None
        diverged = False

    return {
        'divergence_time': divergence_time,
        'diverged': diverged,
        'threshold': threshold,
        'max_separation': np.max(sep),
        'final_separation': sep[-1]
    }


def classify_chaos(lambda_mean: float) -> str:
    """
    Classify system as chaotic based on Lyapunov exponent.

    Parameters
    ----------
    lambda_mean : float
        Mean Lyapunov exponent

    Returns
    -------
    str
        Classification: 'strongly_chaotic', 'chaotic', 'weakly_chaotic', 'regular'
    """
    if lambda_mean > 1.0:
        return 'strongly_chaotic'
    elif lambda_mean > 0.1:
        return 'chaotic'
    elif lambda_mean > 0.01:
        return 'weakly_chaotic'
    else:
        return 'regular'

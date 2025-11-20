"""
Solver for bouncing ball on parabola with collision detection.

This module implements the numerical integration with event-based collision detection.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import List, Tuple, Optional, Dict
import sys
import os

# Add equations directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../equations/definitions'))
from bouncing_balls_equations import (
    free_fall_derivatives,
    collision_event,
    is_approaching,
    reflect_velocity,
    total_energy
)


class BouncingBallSolver:
    """
    Solver for a single ball bouncing on parameterized parabola y = a*x².

    Handles:
    - Free fall integration between bounces
    - Collision detection using event-based methods
    - Elastic reflection at collisions
    - Energy conservation tracking

    Parameters
    ----------
    a : float
        Parabola steepness parameter (default 1.0)
        - a = 1.0: Standard parabola
        - a < 1.0: Flatter curve
        - a > 1.0: Steeper curve
    """

    def __init__(self, g: float = 9.80665, a: float = 1.0,
                 tolerance_abs: float = 1e-12,
                 tolerance_rel: float = 1e-10, max_step: float = 0.01):
        """
        Initialize solver.

        Parameters
        ----------
        g : float
            Gravitational acceleration (m/s²)
        a : float
            Parabola steepness parameter
        tolerance_abs : float
            Absolute tolerance for integration
        tolerance_rel : float
            Relative tolerance for integration
        max_step : float
            Maximum integration step size (s)
        """
        self.g = g
        self.a = a
        self.tolerance_abs = tolerance_abs
        self.tolerance_rel = tolerance_rel
        self.max_step = max_step

        # Storage for trajectory and bounce data
        self.reset_trajectory()

    def reset_trajectory(self):
        """Clear stored trajectory and bounce data."""
        self.t_history = []
        self.x_history = []
        self.y_history = []
        self.vx_history = []
        self.vy_history = []
        self.bounce_times = []
        self.bounce_positions = []
        self.bounce_energies = []

    def integrate_segment(self, state0: np.ndarray, t_start: float,
                          t_end: float) -> Tuple[np.ndarray, np.ndarray, Optional[float]]:
        """
        Integrate from t_start to t_end or until collision.

        Parameters
        ----------
        state0 : ndarray
            Initial state [x, y, vx, vy]
        t_start : float
            Start time
        t_end : float
            End time

        Returns
        -------
        t_array : ndarray
            Time points
        state_array : ndarray
            State at each time point (shape: [4, n_points])
        t_collision : float or None
            Time of collision if one occurred, None otherwise
        """
        # Define event function for collision
        def event_func(t, state):
            return collision_event(t, state, self.g, self.a)

        # Only trigger on approaching collisions
        event_func.direction = -1  # Negative crossing
        event_func.terminal = True  # Stop integration at event

        # Integrate
        sol = solve_ivp(
            fun=lambda t, state: free_fall_derivatives(t, state, self.g, self.a),
            t_span=(t_start, t_end),
            y0=state0,
            method='DOP853',  # High-order Runge-Kutta
            events=event_func,
            rtol=self.tolerance_rel,
            atol=self.tolerance_abs,
            max_step=self.max_step,
            dense_output=True
        )

        t_array = sol.t
        state_array = sol.y

        # Check if collision occurred
        t_collision = None
        if sol.t_events[0].size > 0:
            t_collision = sol.t_events[0][0]

        return t_array, state_array, t_collision

    def apply_collision(self, state: np.ndarray) -> np.ndarray:
        """
        Apply elastic reflection at collision.

        Parameters
        ----------
        state : ndarray
            State at collision [x, y, vx, vy]

        Returns
        -------
        new_state : ndarray
            State after reflection [x, y, vx', vy']
        """
        x, y, vx, vy = state

        # Compute reflected velocities
        vx_new, vy_new = reflect_velocity(vx, vy, x, self.a)

        # Position unchanged (stays on parabola)
        return np.array([x, y, vx_new, vy_new])

    def simulate(self, x0: float, y0: float, vx0: float, vy0: float,
                 t_end: float, max_bounces: int = 100) -> Dict:
        """
        Simulate ball trajectory including bounces.

        Parameters
        ----------
        x0, y0 : float
            Initial position
        vx0, vy0 : float
            Initial velocity
        t_end : float
            Maximum simulation time
        max_bounces : int
            Maximum number of bounces before stopping

        Returns
        -------
        dict
            Trajectory data with keys:
            - 't': time array
            - 'x', 'y', 'vx', 'vy': state arrays
            - 'bounces': list of bounce times and positions
            - 'energy': energy conservation check
        """
        # CRITICAL: Validate initial conditions
        parabola_height = self.a * x0**2
        if y0 <= parabola_height:
            raise ValueError(
                f"Ball starts below/on parabola: y0={y0:.6f} but a*x0²={parabola_height:.6f}. "
                f"Must have y0 > a*x0² to start above the curve."
            )

        if t_end <= 0:
            raise ValueError(f"t_end must be positive, got {t_end}")

        if self.a <= 0:
            raise ValueError(f"Parabola steepness 'a' must be positive, got {self.a}")

        if max_bounces < 1:
            raise ValueError(f"max_bounces must be at least 1, got {max_bounces}")

        self.reset_trajectory()

        state = np.array([x0, y0, vx0, vy0])
        t_current = 0.0
        bounce_count = 0

        # Record initial energy
        E0 = total_energy(x0, y0, vx0, vy0, g=self.g, a=self.a)

        while t_current < t_end and bounce_count < max_bounces:
            # Integrate until next collision or t_end
            t_array, state_array, t_collision = self.integrate_segment(
                state, t_current, t_end
            )

            # Store this segment
            self.t_history.extend(t_array)
            self.x_history.extend(state_array[0, :])
            self.y_history.extend(state_array[1, :])
            self.vx_history.extend(state_array[2, :])
            self.vy_history.extend(state_array[3, :])

            if t_collision is not None:
                # Collision occurred
                bounce_count += 1
                t_current = t_collision

                # Get state at collision
                state = state_array[:, -1]
                x_c, y_c, vx_c, vy_c = state

                # Check if actually approaching
                if not is_approaching(state, self.a):
                    # Spurious collision, continue
                    continue

                # Record bounce
                self.bounce_times.append(t_current)
                self.bounce_positions.append((x_c, y_c))

                # Check energy before bounce
                E = total_energy(x_c, y_c, vx_c, vy_c, g=self.g, a=self.a)
                self.bounce_energies.append(E)

                # Apply reflection
                state = self.apply_collision(state)

                # Verify energy conservation
                x_c, y_c, vx_new, vy_new = state
                E_after = total_energy(x_c, y_c, vx_new, vy_new, g=self.g, a=self.a)

                energy_error = abs(E_after - E) / E0
                if energy_error > 1e-6:
                    print(f"Warning: Energy error at bounce {bounce_count}: {energy_error:.2e}")

            else:
                # No collision, reached t_end
                break

        # Convert to numpy arrays
        result = {
            't': np.array(self.t_history),
            'x': np.array(self.x_history),
            'y': np.array(self.y_history),
            'vx': np.array(self.vx_history),
            'vy': np.array(self.vy_history),
            'bounces': {
                'times': self.bounce_times,
                'positions': self.bounce_positions,
                'count': bounce_count
            },
            'energy': {
                'initial': E0,
                'final': total_energy(
                    self.x_history[-1], self.y_history[-1],
                    self.vx_history[-1], self.vy_history[-1],
                    g=self.g, a=self.a
                ),
                'conservation_error': abs(
                    total_energy(
                        self.x_history[-1], self.y_history[-1],
                        self.vx_history[-1], self.vy_history[-1],
                        g=self.g, a=self.a
                    ) - E0
                ) / E0
            }
        }

        return result


if __name__ == '__main__':
    # Test the solver with different 'a' values
    print("Testing BouncingBallSolver with parameterized parabola")
    print("=" * 60)

    for a_val in [0.3, 1.0]:
        print(f"\n{'='*60}")
        print(f"Testing with a = {a_val} (parabola: y = {a_val}x²)")
        print(f"{'='*60}")

        solver = BouncingBallSolver(g=9.80665, a=a_val)

        # Drop ball from (-2, 5) at rest
        result = solver.simulate(
            x0=-2.0, y0=5.0,
            vx0=0.0, vy0=0.0,
            t_end=10.0,
            max_bounces=50
        )

        print(f"Simulated {len(result['t'])} time points")
        print(f"Number of bounces: {result['bounces']['count']}")
        print(f"Energy conservation error: {result['energy']['conservation_error']:.2e}")
        print(f"Initial energy: {result['energy']['initial']:.4f} J")
        print(f"Final energy: {result['energy']['final']:.4f} J")

        print("\nFirst 5 bounces:")
        for i in range(min(5, len(result['bounces']['times']))):
            t = result['bounces']['times'][i]
            x, y = result['bounces']['positions'][i]
            print(f"  Bounce {i+1}: t={t:.3f}s at (x={x:.3f}, y={y:.3f})")

"""
Divergence study for pairs of bouncing balls.

Simulates pairs of balls with different initial separations and measures
divergence time.
"""

import numpy as np
import sys
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '../solvers'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../equations/definitions'))

from bouncing_ball_solver import BouncingBallSolver
from bouncing_balls_equations import separation_distance, is_approaching


@dataclass
class DivergenceResult:
    """Results from a single divergence study."""
    delta_x: float  # Initial separation
    t_divergence: Optional[float]  # Time to divergence (None if didn't diverge)
    d_initial: float  # Initial separation distance
    d_final: float  # Final separation distance
    diverged: bool  # Whether divergence occurred
    max_time_reached: bool  # Whether we hit max_time without diverging
    bounce_count_1: int  # Number of bounces for ball 1
    bounce_count_2: int  # Number of bounces for ball 2
    trajectory_1: Dict  # Full trajectory data for ball 1
    trajectory_2: Dict  # Full trajectory data for ball 2
    separation_history: np.ndarray  # Separation distance vs time


class DivergenceStudy:
    """
    Study divergence dynamics for pairs of bouncing balls.
    """

    def __init__(self, g: float = 9.80665, threshold_factor: float = 100.0,
                 tolerance_abs: float = 1e-12, tolerance_rel: float = 1e-10):
        """
        Initialize divergence study.

        Parameters
        ----------
        g : float
            Gravitational acceleration
        threshold_factor : float
            Divergence threshold: d(t) > threshold_factor × d(0)
        tolerance_abs, tolerance_rel : float
            Integration tolerances
        """
        self.g = g
        self.threshold_factor = threshold_factor
        self.solver = BouncingBallSolver(
            g=g,
            tolerance_abs=tolerance_abs,
            tolerance_rel=tolerance_rel
        )

    def simulate_pair(self, x1_0: float, y1_0: float, vx1_0: float, vy1_0: float,
                      delta_x: float, delta_y: float = 0.0,
                      t_max: float = 30.0, max_bounces: int = 100,
                      dt_sample: float = 0.01) -> DivergenceResult:
        """
        Simulate a pair of balls and detect divergence.

        Parameters
        ----------
        x1_0, y1_0 : float
            Initial position of ball 1
        vx1_0, vy1_0 : float
            Initial velocity of ball 1
        delta_x, delta_y : float
            Initial separation (ball 2 starts at x1_0 + delta_x, y1_0 + delta_y)
        t_max : float
            Maximum simulation time
        max_bounces : int
            Maximum number of bounces
        dt_sample : float
            Time step for separation sampling

        Returns
        -------
        DivergenceResult
            Complete results including divergence time
        """
        # Initial conditions for ball 2
        x2_0 = x1_0 + delta_x
        y2_0 = y1_0 + delta_y
        vx2_0 = vx1_0
        vy2_0 = vy1_0

        # Initial separation
        state1_0 = np.array([x1_0, y1_0, vx1_0, vy1_0])
        state2_0 = np.array([x2_0, y2_0, vx2_0, vy2_0])
        d_initial = separation_distance(state1_0, state2_0)

        # Divergence threshold
        d_threshold = self.threshold_factor * d_initial

        # Simulate both balls simultaneously with time stepping
        t_current = 0.0
        dt = dt_sample

        # Current states
        state1 = state1_0.copy()
        state2 = state2_0.copy()

        # Storage
        t_history = [0.0]
        separation_history = [d_initial]
        diverged = False
        t_divergence = None

        # For tracking
        segments_1 = []
        segments_2 = []
        bounces_1 = []
        bounces_2 = []

        while t_current < t_max:
            # Integrate both balls for one time step
            t_next = min(t_current + dt, t_max)

            # Ball 1
            t1_array, state1_array, t1_collision = self.solver.integrate_segment(
                state1, t_current, t_next
            )
            segments_1.append((t1_array, state1_array))

            if t1_collision is not None:
                state1 = state1_array[:, -1]
                if is_approaching(state1):
                    bounces_1.append((t1_collision, state1[:2].copy()))
                    state1 = self.solver.apply_collision(state1)

            else:
                state1 = state1_array[:, -1]

            # Ball 2
            t2_array, state2_array, t2_collision = self.solver.integrate_segment(
                state2, t_current, t_next
            )
            segments_2.append((t2_array, state2_array))

            if t2_collision is not None:
                state2 = state2_array[:, -1]
                if is_approaching(state2):
                    bounces_2.append((t2_collision, state2[:2].copy()))
                    state2 = self.solver.apply_collision(state2)
            else:
                state2 = state2_array[:, -1]

            # Compute separation
            d_current = separation_distance(state1, state2)

            t_current = t_next
            t_history.append(t_current)
            separation_history.append(d_current)

            # Check divergence
            if d_current > d_threshold and not diverged:
                diverged = True
                t_divergence = t_current
                break  # Stop simulation

            # Safety check for bounces
            if len(bounces_1) >= max_bounces or len(bounces_2) >= max_bounces:
                break

        # Reconstruct full trajectories
        traj1 = self._reconstruct_trajectory(segments_1)
        traj2 = self._reconstruct_trajectory(segments_2)

        traj1['bounces'] = {
            'times': [b[0] for b in bounces_1],
            'positions': [b[1] for b in bounces_1],
            'count': len(bounces_1)
        }
        traj2['bounces'] = {
            'times': [b[0] for b in bounces_2],
            'positions': [b[1] for b in bounces_2],
            'count': len(bounces_2)
        }

        # Create result
        result = DivergenceResult(
            delta_x=delta_x,
            t_divergence=t_divergence,
            d_initial=d_initial,
            d_final=separation_history[-1],
            diverged=diverged,
            max_time_reached=(t_current >= t_max),
            bounce_count_1=len(bounces_1),
            bounce_count_2=len(bounces_2),
            trajectory_1=traj1,
            trajectory_2=traj2,
            separation_history=np.array(separation_history)
        )

        return result

    def _reconstruct_trajectory(self, segments: List[Tuple]) -> Dict:
        """Reconstruct full trajectory from segments."""
        t_full = []
        x_full = []
        y_full = []
        vx_full = []
        vy_full = []

        for t_array, state_array in segments:
            t_full.extend(t_array)
            x_full.extend(state_array[0, :])
            y_full.extend(state_array[1, :])
            vx_full.extend(state_array[2, :])
            vy_full.extend(state_array[3, :])

        return {
            't': np.array(t_full),
            'x': np.array(x_full),
            'y': np.array(y_full),
            'vx': np.array(vx_full),
            'vy': np.array(vy_full)
        }

    def parameter_sweep(self, x1_0: float, y1_0: float, vx1_0: float, vy1_0: float,
                        delta_x_range: Tuple[float, float], num_points: int = 20,
                        spacing: str = 'logarithmic', **kwargs) -> List[DivergenceResult]:
        """
        Perform parameter sweep over initial separations.

        Parameters
        ----------
        x1_0, y1_0, vx1_0, vy1_0 : float
            Initial conditions for ball 1
        delta_x_range : tuple
            (min, max) range for delta_x
        num_points : int
            Number of different separations to test
        spacing : str
            'linear' or 'logarithmic'
        **kwargs
            Additional arguments passed to simulate_pair

        Returns
        -------
        list of DivergenceResult
            Results for each separation value
        """
        # Generate delta_x values
        if spacing == 'logarithmic':
            delta_x_values = np.logspace(
                np.log10(delta_x_range[0]),
                np.log10(delta_x_range[1]),
                num_points
            )
        else:  # linear
            delta_x_values = np.linspace(
                delta_x_range[0],
                delta_x_range[1],
                num_points
            )

        results = []
        for i, delta_x in enumerate(delta_x_values):
            print(f"Running {i+1}/{num_points}: δx = {delta_x:.2e} m")

            result = self.simulate_pair(
                x1_0, y1_0, vx1_0, vy1_0,
                delta_x=delta_x,
                **kwargs
            )

            results.append(result)

            if result.diverged:
                print(f"  → Diverged at t = {result.t_divergence:.3f} s")
            else:
                print(f"  → Did not diverge (d_final/d_initial = {result.d_final/result.d_initial:.1f})")

        return results


if __name__ == '__main__':
    print("Testing DivergenceStudy")
    print("-" * 50)

    study = DivergenceStudy(threshold_factor=100.0)

    # Test a single pair
    print("\nSingle pair test:")
    result = study.simulate_pair(
        x1_0=-2.0, y1_0=5.0,
        vx1_0=0.0, vy1_0=0.0,
        delta_x=1e-3,
        t_max=20.0
    )

    print(f"Initial separation: {result.d_initial:.2e} m")
    print(f"Final separation: {result.d_final:.2e} m")
    print(f"Diverged: {result.diverged}")
    if result.diverged:
        print(f"Divergence time: {result.t_divergence:.3f} s")
    print(f"Bounces (ball 1): {result.bounce_count_1}")
    print(f"Bounces (ball 2): {result.bounce_count_2}")

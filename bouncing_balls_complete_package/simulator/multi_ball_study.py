"""
Multi-Ball Chaos Study

Simulates multiple bouncing balls simultaneously to study:
- Collective divergence behavior
- Ensemble statistics
- Advanced chaos metrics
- Color-coded visualization
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../solvers'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../equations/definitions'))

from bouncing_ball_solver import BouncingBallSolver


@dataclass
class MultiBallResult:
    """Results from multi-ball simulation."""
    n_balls: int
    delta_x: float
    a: float
    t_max: float

    # Trajectories for all balls
    trajectories: List[Dict[str, np.ndarray]]  # List of trajectory dicts

    # Divergence metrics
    pairwise_divergences: Dict[Tuple[int, int], Dict]  # (i,j) -> divergence info
    max_divergence_time: float
    min_divergence_time: float
    avg_divergence_time: float

    # Ensemble statistics
    ensemble_spread: np.ndarray  # Spread of ensemble over time
    centroid_trajectory: Dict[str, np.ndarray]  # Mean position/velocity

    # Bounce statistics
    bounce_counts: List[int]
    total_bounces: int

    # Chaos metrics
    lyapunov_estimate: float
    spreading_rate: float


class MultiBallStudy:
    """
    Multi-ball bouncing simulation for ensemble chaos studies.

    Simulates N balls with slight initial perturbations to study:
    - Collective divergence
    - Statistical spreading
    - Advanced chaos characterization
    """

    def __init__(self, g: float = 9.80665, a: float = 1.0,
                 threshold_factor: float = 100.0,
                 tolerance_abs: float = 1e-12,
                 tolerance_rel: float = 1e-9):
        """
        Initialize multi-ball study.

        Parameters
        ----------
        g : float
            Gravitational acceleration (m/s²)
        a : float
            Parabola steepness parameter (y = a*x²)
        threshold_factor : float
            Divergence threshold multiplier
        tolerance_abs : float
            Absolute tolerance for ODE solver
        tolerance_rel : float
            Relative tolerance for ODE solver
        """
        self.g = g
        self.a = a
        self.threshold_factor = threshold_factor
        self.tolerance_abs = tolerance_abs
        self.tolerance_rel = tolerance_rel

    def create_symmetric_arrangement(self, n_balls: int, center_x: float = -2.0,
                                    center_y: float = 5.0,
                                    radius: float = 1e-3) -> List[Tuple[float, float]]:
        """
        Create symmetric circular arrangement of initial positions.

        Parameters
        ----------
        n_balls : int
            Number of balls
        center_x : float
            Center x position
        center_y : float
            Center y position
        radius : float
            Radius of circular arrangement

        Returns
        -------
        List of (x, y) positions
        """
        positions = []
        for i in range(n_balls):
            angle = 2 * np.pi * i / n_balls
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            positions.append((x, y))
        return positions

    def create_linear_arrangement(self, n_balls: int, x_start: float = -2.0,
                                 y: float = 5.0, spacing: float = 1e-3) -> List[Tuple[float, float]]:
        """
        Create linear arrangement of initial positions.

        Parameters
        ----------
        n_balls : int
            Number of balls
        x_start : float
            Starting x position
        y : float
            Y position (same for all)
        spacing : float
            Spacing between balls

        Returns
        -------
        List of (x, y) positions
        """
        positions = []
        for i in range(n_balls):
            x = x_start + i * spacing
            positions.append((x, y))
        return positions

    def simulate_ensemble(self, n_balls: int = 4,
                         arrangement: str = 'circular',
                         x_center: float = -2.0,
                         y_center: float = 5.0,
                         vx_0: float = 0.0,
                         vy_0: float = 0.0,
                         perturbation: float = 1e-3,
                         t_max: float = 20.0,
                         max_bounces: int = 100,
                         dt_sample: float = 0.01) -> MultiBallResult:
        """
        Simulate ensemble of balls with symmetric initial arrangement.

        Parameters
        ----------
        n_balls : int
            Number of balls to simulate
        arrangement : str
            'circular' or 'linear' arrangement
        x_center, y_center : float
            Center of initial arrangement
        vx_0, vy_0 : float
            Initial velocities (same for all balls)
        perturbation : float
            Size of initial position perturbation
        t_max : float
            Maximum simulation time
        max_bounces : int
            Maximum number of bounces per ball
        dt_sample : float
            Sampling time step

        Returns
        -------
        MultiBallResult with all trajectories and metrics
        """
        # Create initial positions
        if arrangement == 'circular':
            positions = self.create_symmetric_arrangement(
                n_balls, x_center, y_center, perturbation
            )
        else:  # linear
            positions = self.create_linear_arrangement(
                n_balls, x_center, y_center, perturbation
            )

        # Run simulation for each ball
        trajectories = []
        bounce_counts = []

        for i, (x0, y0) in enumerate(positions):
            solver = BouncingBallSolver(
                g=self.g,
                a=self.a,
                tolerance_abs=self.tolerance_abs,
                tolerance_rel=self.tolerance_rel
            )

            result = solver.simulate(
                x0=x0,
                y0=y0,
                vx0=vx_0,
                vy0=vy_0,
                t_end=t_max,
                max_bounces=max_bounces
            )

            # Add bounce_times for compatibility
            result['bounce_times'] = result['bounces']['times']

            trajectories.append(result)
            bounce_counts.append(result['bounces']['count'])

        # Compute pairwise divergences
        pairwise_divergences = {}
        divergence_times = []

        for i in range(n_balls):
            for j in range(i+1, n_balls):
                div_info = self._compute_pairwise_divergence(
                    trajectories[i], trajectories[j],
                    positions[i], positions[j]
                )
                pairwise_divergences[(i, j)] = div_info
                if div_info['diverged']:
                    divergence_times.append(div_info['t_divergence'])

        # Divergence statistics
        if divergence_times:
            max_div_time = max(divergence_times)
            min_div_time = min(divergence_times)
            avg_div_time = np.mean(divergence_times)
        else:
            max_div_time = min_div_time = avg_div_time = t_max

        # Compute ensemble statistics
        ensemble_spread = self._compute_ensemble_spread(trajectories)
        centroid = self._compute_centroid_trajectory(trajectories)

        # Chaos metrics
        lyapunov_est = self._estimate_lyapunov(
            pairwise_divergences, perturbation, avg_div_time
        )
        spreading_rate = self._compute_spreading_rate(ensemble_spread)

        return MultiBallResult(
            n_balls=n_balls,
            delta_x=perturbation,
            a=self.a,
            t_max=t_max,
            trajectories=trajectories,
            pairwise_divergences=pairwise_divergences,
            max_divergence_time=max_div_time,
            min_divergence_time=min_div_time,
            avg_divergence_time=avg_div_time,
            ensemble_spread=ensemble_spread,
            centroid_trajectory=centroid,
            bounce_counts=bounce_counts,
            total_bounces=sum(bounce_counts),
            lyapunov_estimate=lyapunov_est,
            spreading_rate=spreading_rate
        )

    def _compute_pairwise_divergence(self, traj1: Dict, traj2: Dict,
                                    pos1: Tuple[float, float],
                                    pos2: Tuple[float, float]) -> Dict:
        """Compute divergence between two trajectories."""
        # Initial separation
        d_initial = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        threshold = self.threshold_factor * d_initial

        # Find common time points
        t1 = traj1['t']
        t2 = traj2['t']

        # Use shorter trajectory
        n_points = min(len(t1), len(t2))

        # Compute separation over time
        separations = []
        times = []

        for i in range(n_points):
            if abs(t1[i] - t2[i]) < 1e-6:  # Times match
                dx = traj1['x'][i] - traj2['x'][i]
                dy = traj1['y'][i] - traj2['y'][i]
                sep = np.sqrt(dx**2 + dy**2)
                separations.append(sep)
                times.append(t1[i])

        separations = np.array(separations)
        times = np.array(times)

        # Check for divergence
        diverged_idx = np.where(separations > threshold)[0]

        if len(diverged_idx) > 0:
            diverged = True
            t_divergence = times[diverged_idx[0]]
        else:
            diverged = False
            t_divergence = None

        return {
            'diverged': diverged,
            't_divergence': t_divergence,
            'd_initial': d_initial,
            'd_final': separations[-1] if len(separations) > 0 else 0,
            'separations': separations,
            'times': times
        }

    def _compute_ensemble_spread(self, trajectories: List[Dict]) -> np.ndarray:
        """
        Compute ensemble spread (standard deviation of positions) over time.

        Returns
        -------
        Array of spreads at each time point
        """
        # Find common time points (use first trajectory as reference)
        n_points = len(trajectories[0]['t'])
        spreads = []

        for i in range(n_points):
            positions = []
            for traj in trajectories:
                if i < len(traj['x']):
                    positions.append([traj['x'][i], traj['y'][i]])

            if len(positions) > 1:
                positions = np.array(positions)
                # Compute spread as average distance from centroid
                centroid = np.mean(positions, axis=0)
                distances = np.sqrt(np.sum((positions - centroid)**2, axis=1))
                spread = np.mean(distances)
                spreads.append(spread)
            else:
                spreads.append(0)

        return np.array(spreads)

    def _compute_centroid_trajectory(self, trajectories: List[Dict]) -> Dict:
        """Compute centroid (mean) trajectory of ensemble."""
        n_points = len(trajectories[0]['t'])

        t_centroid = []
        x_centroid = []
        y_centroid = []
        vx_centroid = []
        vy_centroid = []

        for i in range(n_points):
            x_vals = []
            y_vals = []
            vx_vals = []
            vy_vals = []

            for traj in trajectories:
                if i < len(traj['x']):
                    x_vals.append(traj['x'][i])
                    y_vals.append(traj['y'][i])
                    vx_vals.append(traj['vx'][i])
                    vy_vals.append(traj['vy'][i])

            if len(x_vals) > 0:
                t_centroid.append(trajectories[0]['t'][i])
                x_centroid.append(np.mean(x_vals))
                y_centroid.append(np.mean(y_vals))
                vx_centroid.append(np.mean(vx_vals))
                vy_centroid.append(np.mean(vy_vals))

        return {
            't': np.array(t_centroid),
            'x': np.array(x_centroid),
            'y': np.array(y_centroid),
            'vx': np.array(vx_centroid),
            'vy': np.array(vy_centroid)
        }

    def _estimate_lyapunov(self, pairwise_div: Dict, d_initial: float,
                          avg_div_time: float) -> float:
        """
        Estimate largest Lyapunov exponent from divergence data.

        λ ≈ log(d_final / d_initial) / t_divergence
        """
        if avg_div_time == 0 or avg_div_time == float('inf'):
            return 0.0

        # Use average of all pairwise estimates
        estimates = []
        for (i, j), div_info in pairwise_div.items():
            if div_info['diverged']:
                growth = div_info['d_final'] / div_info['d_initial']
                if growth > 1:
                    lambda_est = np.log(growth) / div_info['t_divergence']
                    estimates.append(lambda_est)

        if estimates:
            return np.mean(estimates)
        else:
            return 0.0

    def _compute_spreading_rate(self, ensemble_spread: np.ndarray) -> float:
        """
        Compute rate of ensemble spreading.

        Returns average rate of spread increase (m/s).
        """
        if len(ensemble_spread) < 2:
            return 0.0

        # Compute derivative (finite differences)
        # Assuming dt_sample used in simulation
        dt = 0.01  # Should match dt_sample

        spread_rate = np.diff(ensemble_spread) / dt

        # Return average positive rate
        positive_rates = spread_rate[spread_rate > 0]
        if len(positive_rates) > 0:
            return np.mean(positive_rates)
        else:
            return 0.0


if __name__ == '__main__':
    # Example usage
    print("Multi-Ball Chaos Study")
    print("=" * 50)

    study = MultiBallStudy(a=0.3, threshold_factor=100.0)

    # Simulate 4 balls in circular arrangement
    result = study.simulate_ensemble(
        n_balls=4,
        arrangement='circular',
        x_center=-2.0,
        y_center=5.0,
        perturbation=1e-3,
        t_max=20.0
    )

    print(f"\nSimulation Results:")
    print(f"Number of balls: {result.n_balls}")
    print(f"Total bounces: {result.total_bounces}")
    print(f"Bounce counts: {result.bounce_counts}")
    print(f"\nDivergence Statistics:")
    print(f"Min divergence time: {result.min_divergence_time:.3f} s")
    print(f"Avg divergence time: {result.avg_divergence_time:.3f} s")
    print(f"Max divergence time: {result.max_divergence_time:.3f} s")
    print(f"\nChaos Metrics:")
    print(f"Lyapunov exponent estimate: {result.lyapunov_estimate:.4f} s⁻¹")
    print(f"Ensemble spreading rate: {result.spreading_rate:.6f} m/s")
    print(f"Final ensemble spread: {result.ensemble_spread[-1]:.6f} m")

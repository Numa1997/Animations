"""
Matplotlib-based visualization for bouncing balls.

Creates static plots and animations.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from typing import Dict, List, Optional
import sys
import os

# Add implementation path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../implementation/simulations'))


class BouncingBallsVisualizer:
    """Visualize bouncing ball trajectories and divergence."""

    def __init__(self, figsize=(12, 8), dpi=100):
        """Initialize visualizer."""
        self.figsize = figsize
        self.dpi = dpi

    def plot_parabola(self, ax, x_range=(-3, 3), a=1.0, **kwargs):
        """
        Plot the parabolic boundary.

        Parameters
        ----------
        a : float
            Parabola steepness (y = a*x²)
        """
        x = np.linspace(x_range[0], x_range[1], 500)
        y = a * x**2
        ax.plot(x, y, color='green', linewidth=2,
               label=f'Parabola: y={a}x²' if a != 1.0 else 'Parabola: y=x²', **kwargs)
        ax.fill_between(x, 0, y, alpha=0.1, color='green')

    def plot_trajectory(self, ax, trajectory: Dict, label: str = '',
                       color: str = 'blue', show_bounces: bool = True):
        """Plot a single trajectory."""
        # Plot path
        ax.plot(trajectory['x'], trajectory['y'], '-', color=color,
                linewidth=1.5, alpha=0.7, label=label)

        # Plot start point
        ax.plot(trajectory['x'][0], trajectory['y'][0], 'o',
                color=color, markersize=8, label=f'{label} start')

        # Plot bounces
        if show_bounces and 'bounces' in trajectory:
            bounce_x = [pos[0] for pos in trajectory['bounces']['positions']]
            bounce_y = [pos[1] for pos in trajectory['bounces']['positions']]
            ax.scatter(bounce_x, bounce_y, color=color, marker='x',
                      s=50, zorder=5, alpha=0.8)

    def plot_pair_comparison(self, result, save_path: Optional[str] = None):
        """
        Plot trajectories of both balls overlaid.

        Parameters
        ----------
        result : DivergenceResult
            Results from divergence study
        save_path : str, optional
            Path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        # Plot parabola
        self.plot_parabola(ax)

        # Plot trajectories
        self.plot_trajectory(ax, result.trajectory_1, label='Ball 1',
                           color='#1f77b4', show_bounces=True)
        self.plot_trajectory(ax, result.trajectory_2, label='Ball 2',
                           color='#ff7f0e', show_bounces=True)

        ax.set_xlabel('x (m)', fontsize=12)
        ax.set_ylabel('y (m)', fontsize=12)
        ax.set_title(f'Bouncing Balls Trajectories (δx = {result.delta_x:.2e} m)', fontsize=14)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal', adjustable='box')

        # Add divergence info
        info_text = f"Diverged: {result.diverged}\n"
        if result.diverged:
            info_text += f"t_div = {result.t_divergence:.3f} s\n"
        info_text += f"Bounces: {result.bounce_count_1}, {result.bounce_count_2}"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
                verticalalignment='top', fontsize=10,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved trajectory plot to {save_path}")

        return fig

    def plot_separation_vs_time(self, t_history: List[float],
                                separation_history: np.ndarray,
                                d_initial: float, threshold_factor: float,
                                save_path: Optional[str] = None):
        """Plot separation distance vs time."""
        fig, ax = plt.subplots(figsize=(10, 6), dpi=self.dpi)

        ax.plot(t_history, separation_history, 'b-', linewidth=2, label='Separation d(t)')
        ax.axhline(d_initial, color='green', linestyle='--',
                  label=f'd₀ = {d_initial:.2e} m')
        ax.axhline(threshold_factor * d_initial, color='red', linestyle='--',
                  label=f'Threshold = {threshold_factor}×d₀')

        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Separation (m)', fontsize=12)
        ax.set_title('Separation Distance vs Time', fontsize=14)
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, alpha=0.3, which='both')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')

        return fig

    def plot_divergence_analysis(self, results: List, save_path: Optional[str] = None):
        """
        Plot divergence time vs initial separation.

        Parameters
        ----------
        results : list of DivergenceResult
            Results from parameter sweep
        save_path : str, optional
            Path to save figure
        """
        # Extract data
        delta_x_values = []
        t_div_values = []

        for res in results:
            if res.diverged:
                delta_x_values.append(res.delta_x)
                t_div_values.append(res.t_divergence)

        if len(delta_x_values) == 0:
            print("No divergence data to plot!")
            return None

        delta_x_values = np.array(delta_x_values)
        t_div_values = np.array(t_div_values)

        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi)

        # Left: regular plot
        ax1.plot(delta_x_values, t_div_values, 'o-', markersize=8, linewidth=2)
        ax1.set_xlabel('Initial Separation δx (m)', fontsize=12)
        ax1.set_ylabel('Divergence Time (s)', fontsize=12)
        ax1.set_title('Divergence Time vs Initial Separation', fontsize=14)
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')

        # Right: log-log plot
        ax2.loglog(delta_x_values, t_div_values, 'o-', markersize=8, linewidth=2)
        ax2.set_xlabel('Initial Separation δx (m)', fontsize=12)
        ax2.set_ylabel('Divergence Time (s)', fontsize=12)
        ax2.set_title('Log-Log Plot', fontsize=14)
        ax2.grid(True, alpha=0.3, which='both')

        # Try to fit power law: t_div = A * (delta_x)^alpha
        # log(t_div) = log(A) + alpha * log(delta_x)
        if len(delta_x_values) > 2:
            coeffs = np.polyfit(np.log(delta_x_values), np.log(t_div_values), 1)
            alpha = coeffs[0]
            log_A = coeffs[1]
            A = np.exp(log_A)

            # Plot fit
            delta_x_fit = np.logspace(np.log10(delta_x_values.min()),
                                     np.log10(delta_x_values.max()), 100)
            t_div_fit = A * delta_x_fit**alpha

            ax2.plot(delta_x_fit, t_div_fit, 'r--', linewidth=2,
                    label=f'Fit: t ∝ δx^{alpha:.2f}')
            ax2.legend()

            # Add text annotation
            fit_text = f"Power law fit:\nt_div = {A:.2e} × (δx)^{alpha:.2f}"
            ax1.text(0.05, 0.95, fit_text, transform=ax1.transAxes,
                    verticalalignment='top', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved divergence analysis to {save_path}")

        return fig

    def create_animation(self, result, fps: int = 60, duration: float = 10.0,
                        save_path: Optional[str] = None, format: str = 'mp4'):
        """
        Create animation of both balls bouncing.

        Parameters
        ----------
        result : DivergenceResult
            Results containing trajectories
        fps : int
            Frames per second (default 60 for smooth video)
        duration : float
            Target animation duration (s)
        save_path : str, optional
            Path to save animation
        format : str
            Output format: 'mp4', 'gif', or 'both'
        """
        traj1 = result.trajectory_1
        traj2 = result.trajectory_2

        # Downsample for animation
        n_frames = int(fps * duration)
        idx1 = np.linspace(0, len(traj1['t']) - 1, n_frames, dtype=int)
        idx2 = np.linspace(0, len(traj2['t']) - 1, n_frames, dtype=int)

        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize, dpi=100)
        self.plot_parabola(ax, x_range=(-3, 3))

        # Initialize elements
        ball1, = ax.plot([], [], 'o', color='#1f77b4', markersize=12, label='Ball 1')
        ball2, = ax.plot([], [], 'o', color='#ff7f0e', markersize=12, label='Ball 2')
        trail1, = ax.plot([], [], '-', color='#1f77b4', alpha=0.5, linewidth=1)
        trail2, = ax.plot([], [], '-', color='#ff7f0e', alpha=0.5, linewidth=1)
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)

        ax.set_xlim(-3, 3)
        ax.set_ylim(0, 6)
        ax.set_xlabel('x (m)')
        ax.set_ylabel('y (m)')
        ax.set_title(f'Bouncing Balls (δx = {result.delta_x:.2e} m)')
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')

        trail_length = 100

        def init():
            ball1.set_data([], [])
            ball2.set_data([], [])
            trail1.set_data([], [])
            trail2.set_data([], [])
            time_text.set_text('')
            return ball1, ball2, trail1, trail2, time_text

        def animate(frame):
            i1 = idx1[frame]
            i2 = idx2[frame]

            # Update ball positions
            ball1.set_data([traj1['x'][i1]], [traj1['y'][i1]])
            ball2.set_data([traj2['x'][i2]], [traj2['y'][i2]])

            # Update trails
            start1 = max(0, i1 - trail_length)
            start2 = max(0, i2 - trail_length)
            trail1.set_data(traj1['x'][start1:i1+1], traj1['y'][start1:i1+1])
            trail2.set_data(traj2['x'][start2:i2+1], traj2['y'][start2:i2+1])

            # Update time
            t = traj1['t'][i1]
            time_text.set_text(f't = {t:.2f} s')

            return ball1, ball2, trail1, trail2, time_text

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=n_frames, interval=1000/fps,
                                      blit=True)

        if save_path:
            import os
            base_path = os.path.splitext(save_path)[0]

            if format in ['mp4', 'both']:
                mp4_path = base_path + '.mp4'
                print(f"Saving MP4 video to {mp4_path}...")
                try:
                    anim.save(mp4_path, writer='ffmpeg', fps=fps,
                             extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'],
                             dpi=150)
                    print(f"MP4 video saved! ({fps} fps)")
                except Exception as e:
                    print(f"MP4 save failed (ffmpeg not available?): {e}")
                    print("Falling back to GIF...")
                    format = 'gif'

            if format in ['gif', 'both']:
                gif_path = base_path + '.gif'
                print(f"Saving GIF animation to {gif_path}...")
                anim.save(gif_path, writer='pillow', fps=min(fps, 30))
                print(f"GIF animation saved!")

        return anim, fig


if __name__ == '__main__':
    print("Visualizer module loaded successfully!")

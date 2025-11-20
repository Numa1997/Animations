"""
Multi-Ball Visualization with Color Coding

Creates advanced visualizations for multi-ball chaos studies:
- Color-coded trajectories
- Divergence heat maps
- Ensemble spread visualization
- Advanced chaos metrics plots
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
from matplotlib.colors import Normalize
import matplotlib.patches as patches
from typing import List, Dict, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../implementation/simulations'))


class MultiBallVisualizer:
    """Visualizer for multi-ball bouncing simulations."""

    def __init__(self, figsize=(14, 10), dpi=120):
        """
        Initialize visualizer.

        Parameters
        ----------
        figsize : tuple
            Figure size (width, height) in inches
        dpi : int
            Dots per inch for figure resolution
        """
        self.figsize = figsize
        self.dpi = dpi

    def create_static_plot(self, result, save_path: Optional[str] = None):
        """
        Create comprehensive static plot showing all aspects.

        Parameters
        ----------
        result : MultiBallResult
            Results from multi-ball simulation
        save_path : str, optional
            Path to save figure
        """
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)

        # Create 2x2 grid
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # 1. Trajectories (top left)
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_trajectories(ax1, result)

        # 2. Pairwise divergence (top right)
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_pairwise_divergence(ax2, result)

        # 3. Ensemble spread (bottom left)
        ax3 = fig.add_subplot(gs[1, 0])
        self._plot_ensemble_spread(ax3, result)

        # 4. Chaos metrics (bottom right)
        ax4 = fig.add_subplot(gs[1, 1])
        self._plot_chaos_metrics(ax4, result)

        # Main title
        fig.suptitle(
            f'Multi-Ball Chaos Study: {result.n_balls} Balls (a={result.a})',
            fontsize=16, fontweight='bold'
        )

        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved plot to {save_path}")

        return fig

    def _plot_trajectories(self, ax, result):
        """Plot color-coded trajectories."""
        # Parabola
        x_para = np.linspace(-3, 3, 500)
        y_para = result.a * x_para**2
        ax.plot(x_para, y_para, 'g-', linewidth=2, alpha=0.5,
               label=f'y={result.a}x²')
        ax.fill_between(x_para, 0, y_para, alpha=0.1, color='green')

        # Color map for balls
        colors = cm.rainbow(np.linspace(0, 1, result.n_balls))

        # Plot each trajectory
        for i, (traj, color) in enumerate(zip(result.trajectories, colors)):
            ax.plot(traj['x'], traj['y'],
                   color=color, linewidth=1.5, alpha=0.7,
                   label=f'Ball {i+1}')

            # Mark start position
            ax.plot(traj['x'][0], traj['y'][0],
                   'o', color=color, markersize=8,
                   markeredgecolor='black', markeredgewidth=1)

        # Centroid
        cent = result.centroid_trajectory
        ax.plot(cent['x'], cent['y'],
               'k--', linewidth=2, alpha=0.5, label='Centroid')

        ax.set_xlabel('x (m)', fontsize=11)
        ax.set_ylabel('y (m)', fontsize=11)
        ax.set_title('Color-Coded Trajectories', fontsize=12, fontweight='bold')
        ax.set_xlim(-3, 3)
        ax.set_ylim(0, 6)
        ax.legend(fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')

    def _plot_pairwise_divergence(self, ax, result):
        """Plot pairwise divergence times as heat map."""
        n = result.n_balls

        # Create divergence time matrix
        div_matrix = np.full((n, n), np.nan)

        for (i, j), div_info in result.pairwise_divergences.items():
            if div_info['diverged']:
                div_matrix[i, j] = div_info['t_divergence']
                div_matrix[j, i] = div_info['t_divergence']
            else:
                div_matrix[i, j] = result.t_max
                div_matrix[j, i] = result.t_max

        # Plot heat map
        im = ax.imshow(div_matrix, cmap='RdYlGn_r', aspect='auto',
                      vmin=0, vmax=result.t_max)

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Divergence Time (s)', fontsize=10)

        # Add text annotations
        for i in range(n):
            for j in range(n):
                if not np.isnan(div_matrix[i, j]):
                    text = ax.text(j, i, f'{div_matrix[i, j]:.1f}',
                                 ha="center", va="center",
                                 color="black", fontsize=9)

        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels([f'B{i+1}' for i in range(n)])
        ax.set_yticklabels([f'B{i+1}' for i in range(n)])
        ax.set_title('Pairwise Divergence Times', fontsize=12, fontweight='bold')

    def _plot_ensemble_spread(self, ax, result):
        """Plot ensemble spread over time."""
        t = result.trajectories[0]['t'][:len(result.ensemble_spread)]

        ax.semilogy(t, result.ensemble_spread, 'b-', linewidth=2, label='Spread')

        # Mark initial spread
        ax.axhline(result.ensemble_spread[0], color='green',
                  linestyle='--', alpha=0.5, label=f'Initial')

        # Mark divergence times
        div_times = []
        for (i, j), div_info in result.pairwise_divergences.items():
            if div_info['diverged']:
                div_times.append(div_info['t_divergence'])

        if div_times:
            ax.axvline(min(div_times), color='red',
                      linestyle=':', alpha=0.7, label='First divergence')

        ax.set_xlabel('Time (s)', fontsize=11)
        ax.set_ylabel('Ensemble Spread (m, log)', fontsize=11)
        ax.set_title('Ensemble Spreading', fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which='both')

    def _plot_chaos_metrics(self, ax, result):
        """Display chaos metrics and statistics."""
        ax.axis('off')

        # Prepare text
        metrics_text = f"""
CHAOS METRICS
{'=' * 40}

Divergence Statistics:
  Min divergence time: {result.min_divergence_time:.3f} s
  Avg divergence time: {result.avg_divergence_time:.3f} s
  Max divergence time: {result.max_divergence_time:.3f} s

Ensemble Statistics:
  Number of balls: {result.n_balls}
  Total bounces: {result.total_bounces}
  Avg bounces/ball: {result.total_bounces/result.n_balls:.1f}
  Initial perturbation: {result.delta_x:.2e} m
  Final spread: {result.ensemble_spread[-1]:.6f} m
  Spread growth: {result.ensemble_spread[-1]/result.delta_x:.1f}×

Chaos Characterization:
  Lyapunov exponent: {result.lyapunov_estimate:.4f} s⁻¹
  Spreading rate: {result.spreading_rate:.6f} m/s
  Parabola steepness: {result.a}

Bounce Distribution:
"""
        for i, count in enumerate(result.bounce_counts):
            metrics_text += f"  Ball {i+1}: {count} bounces\n"

        ax.text(0.05, 0.95, metrics_text,
               transform=ax.transAxes,
               fontsize=9,
               verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

        ax.set_title('Statistics & Metrics', fontsize=12, fontweight='bold')

    def create_animation(self, result, fps: int = 30,
                        duration: float = 15.0,
                        save_path: Optional[str] = None,
                        format: str = 'gif'):
        """
        Create animated visualization of multi-ball system.

        Parameters
        ----------
        result : MultiBallResult
            Simulation results
        fps : int
            Frames per second
        duration : float
            Video duration
        save_path : str, optional
            Path to save animation
        format : str
            'gif' or 'mp4'
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=self.dpi)

        # Setup parabola
        x_para = np.linspace(-3, 3, 500)
        y_para = result.a * x_para**2
        ax1.plot(x_para, y_para, 'g-', linewidth=2, alpha=0.5)
        ax1.fill_between(x_para, 0, y_para, alpha=0.1, color='green')

        # Color map
        colors = cm.rainbow(np.linspace(0, 1, result.n_balls))

        # Create ball markers and trails
        balls = []
        trails = []
        for color in colors:
            ball, = ax1.plot([], [], 'o', color=color, markersize=10,
                           markeredgecolor='black', markeredgewidth=1)
            trail, = ax1.plot([], [], '-', color=color, linewidth=1, alpha=0.5)
            balls.append(ball)
            trails.append(trail)

        # Centroid
        centroid_ball, = ax1.plot([], [], 'k*', markersize=15,
                                 markeredgecolor='yellow', markeredgewidth=1.5)
        centroid_trail, = ax1.plot([], [], 'k--', linewidth=1.5, alpha=0.7)

        ax1.set_xlim(-3, 3)
        ax1.set_ylim(0, 6)
        ax1.set_xlabel('x (m)', fontsize=11)
        ax1.set_ylabel('y (m)', fontsize=11)
        ax1.set_title(f'{result.n_balls}-Ball System', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_aspect('equal')

        # Setup spread plot
        t_data = result.trajectories[0]['t'][:len(result.ensemble_spread)]
        ax2.semilogy(t_data, result.ensemble_spread, 'b-',
                    linewidth=1, alpha=0.3, label='Full')
        spread_line, = ax2.semilogy([], [], 'b-', linewidth=2, label='Current')
        spread_point, = ax2.semilogy([], [], 'ro', markersize=8)

        ax2.set_xlabel('Time (s)', fontsize=11)
        ax2.set_ylabel('Ensemble Spread (m, log)', fontsize=11)
        ax2.set_title('Ensemble Spreading', fontsize=12, fontweight='bold')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, which='both')

        # Time text
        time_text = fig.text(0.5, 0.95, '', fontsize=14, fontweight='bold',
                           ha='center', va='top')

        # Animation parameters
        n_frames = int(fps * duration)
        n_points = len(result.trajectories[0]['t'])
        idx = np.linspace(0, n_points - 1, n_frames, dtype=int)
        trail_length = 100

        def init():
            for ball, trail in zip(balls, trails):
                ball.set_data([], [])
                trail.set_data([], [])
            centroid_ball.set_data([], [])
            centroid_trail.set_data([], [])
            spread_line.set_data([], [])
            spread_point.set_data([], [])
            time_text.set_text('')
            return balls + trails + [centroid_ball, centroid_trail,
                                    spread_line, spread_point, time_text]

        def animate(frame):
            i = idx[frame]

            # Update balls and trails
            for ball_idx, (ball, trail, traj) in enumerate(zip(balls, trails, result.trajectories)):
                if i < len(traj['x']):
                    ball.set_data([traj['x'][i]], [traj['y'][i]])

                    start = max(0, i - trail_length)
                    trail.set_data(traj['x'][start:i+1], traj['y'][start:i+1])

            # Update centroid
            cent = result.centroid_trajectory
            if i < len(cent['x']):
                centroid_ball.set_data([cent['x'][i]], [cent['y'][i]])
                start = max(0, i - trail_length)
                centroid_trail.set_data(cent['x'][start:i+1], cent['y'][start:i+1])

            # Update spread plot
            if i < len(t_data):
                spread_line.set_data(t_data[:i+1], result.ensemble_spread[:i+1])
                spread_point.set_data([t_data[i]], [result.ensemble_spread[i]])

            # Update time
            if i < len(result.trajectories[0]['t']):
                t = result.trajectories[0]['t'][i]
                time_text.set_text(f't = {t:.3f} s')

            return balls + trails + [centroid_ball, centroid_trail,
                                    spread_line, spread_point, time_text]

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=n_frames, interval=1000/fps,
                                      blit=True)

        if save_path:
            if format == 'gif':
                gif_path = save_path if save_path.endswith('.gif') else save_path + '.gif'
                print(f"Saving GIF animation to {gif_path}...")
                anim.save(gif_path, writer='pillow', fps=min(fps, 30), dpi=self.dpi)
                print(f"✓ GIF saved ({min(fps, 30)} fps)")
            elif format == 'mp4':
                mp4_path = save_path if save_path.endswith('.mp4') else save_path + '.mp4'
                print(f"Saving MP4 video to {mp4_path}...")
                try:
                    anim.save(mp4_path, writer='ffmpeg', fps=fps,
                             extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'],
                             dpi=self.dpi)
                    print(f"✓ MP4 saved ({fps} fps)")
                except Exception as e:
                    print(f"✗ MP4 failed: {e}, falling back to GIF")
                    gif_path = save_path.replace('.mp4', '.gif')
                    anim.save(gif_path, writer='pillow', fps=min(fps, 30), dpi=self.dpi)

        return anim, fig


if __name__ == '__main__':
    print("Multi-Ball Visualizer loaded!")

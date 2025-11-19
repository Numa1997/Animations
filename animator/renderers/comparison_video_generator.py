"""
Advanced video generation for bouncing balls.

Creates multi-panel comparison videos showing both balls and analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
from typing import Dict, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../implementation/simulations'))


class ComparisonVideoGenerator:
    """Generate advanced comparison videos with multiple panels."""

    def __init__(self, figsize=(16, 9), dpi=120):
        """Initialize video generator."""
        self.figsize = figsize
        self.dpi = dpi

    def create_side_by_side_video(self, result, fps: int = 60,
                                  duration: float = 15.0,
                                  save_path: Optional[str] = None,
                                  format: str = 'mp4',
                                  a: float = 1.0):
        """
        Create side-by-side comparison video with analysis panels.

        Layout:
        - Left: Trajectory animation
        - Top right: Separation vs time
        - Bottom right: Phase space

        Parameters
        ----------
        result : DivergenceResult
            Results containing trajectories
        fps : int
            Frames per second
        duration : float
            Target video duration
        save_path : str, optional
            Path to save video
        format : str
            'mp4', 'gif', or 'html5'
        a : float
            Parabola steepness parameter (y = a*x²)
        """
        traj1 = result.trajectory_1
        traj2 = result.trajectory_2

        # Setup figure with GridSpec
        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        gs = GridSpec(2, 2, figure=fig, width_ratios=[2, 1], height_ratios=[1, 1],
                     hspace=0.3, wspace=0.3)

        # Main trajectory plot (left, spans both rows)
        ax_main = fig.add_subplot(gs[:, 0])
        ax_sep = fig.add_subplot(gs[0, 1])   # Separation plot (top right)
        ax_phase = fig.add_subplot(gs[1, 1])  # Phase space (bottom right)

        # Downsample for animation
        n_frames = int(fps * duration)
        n_points = min(len(traj1['t']), len(traj2['t']))
        idx = np.linspace(0, n_points - 1, n_frames, dtype=int)

        # Setup main trajectory plot
        x_para = np.linspace(-3, 3, 500)
        y_para = a * x_para**2
        parabola_label = f'Parabola: y={a}x²' if a != 1.0 else 'Parabola: y=x²'
        ax_main.plot(x_para, y_para, 'g-', linewidth=2, alpha=0.5, label=parabola_label)
        ax_main.fill_between(x_para, 0, y_para, alpha=0.1, color='green')

        ball1_main, = ax_main.plot([], [], 'o', color='#1f77b4', markersize=14,
                                   label='Ball 1', zorder=5)
        ball2_main, = ax_main.plot([], [], 'o', color='#ff7f0e', markersize=14,
                                   label='Ball 2', zorder=5)
        trail1_main, = ax_main.plot([], [], '-', color='#1f77b4', alpha=0.4, linewidth=1.5)
        trail2_main, = ax_main.plot([], [], '-', color='#ff7f0e', alpha=0.4, linewidth=1.5)

        ax_main.set_xlim(-3, 3)
        ax_main.set_ylim(0, 6)
        ax_main.set_xlabel('x (m)', fontsize=12)
        ax_main.set_ylabel('y (m)', fontsize=12)
        ax_main.set_title(f'Bouncing Balls (δx = {result.delta_x:.2e} m)', fontsize=14, fontweight='bold')
        ax_main.legend(loc='upper right')
        ax_main.grid(True, alpha=0.3)
        ax_main.set_aspect('equal')

        # Setup separation plot
        t_full = traj1['t']
        sep_full = np.array([np.sqrt((traj1['x'][i] - traj2['x'][i])**2 +
                                     (traj1['y'][i] - traj2['y'][i])**2)
                            for i in range(len(t_full))])

        ax_sep.plot(t_full, sep_full, 'k-', alpha=0.2, linewidth=1, label='Full')
        sep_line, = ax_sep.plot([], [], 'b-', linewidth=2, label='Current')
        sep_point, = ax_sep.plot([], [], 'ro', markersize=8, zorder=5)

        ax_sep.axhline(result.d_initial, color='green', linestyle='--',
                      linewidth=1, alpha=0.5, label=f'd₀')
        ax_sep.axhline(100 * result.d_initial, color='red', linestyle='--',
                      linewidth=1, alpha=0.5, label='Threshold')

        ax_sep.set_xlabel('Time (s)', fontsize=10)
        ax_sep.set_ylabel('Separation (m)', fontsize=10)
        ax_sep.set_title('Separation Distance', fontsize=11, fontweight='bold')
        ax_sep.set_yscale('log')
        ax_sep.legend(fontsize=8, loc='upper left')
        ax_sep.grid(True, alpha=0.3, which='both')

        # Setup phase space plot
        ax_phase.plot(traj1['x'], traj1['vx'], '-', color='#1f77b4', alpha=0.2,
                     linewidth=1, label='Ball 1 (full)')
        ax_phase.plot(traj2['x'], traj2['vx'], '-', color='#ff7f0e', alpha=0.2,
                     linewidth=1, label='Ball 2 (full)')

        phase1_line, = ax_phase.plot([], [], '-', color='#1f77b4', linewidth=2)
        phase2_line, = ax_phase.plot([], [], '-', color='#ff7f0e', linewidth=2)
        phase1_point, = ax_phase.plot([], [], 'o', color='#1f77b4', markersize=8, zorder=5)
        phase2_point, = ax_phase.plot([], [], 'o', color='#ff7f0e', markersize=8, zorder=5)

        ax_phase.set_xlabel('Position x (m)', fontsize=10)
        ax_phase.set_ylabel('Velocity vₓ (m/s)', fontsize=10)
        ax_phase.set_title('Phase Space (x vs vₓ)', fontsize=11, fontweight='bold')
        ax_phase.legend(fontsize=8, loc='upper right')
        ax_phase.grid(True, alpha=0.3)

        # Time text
        time_text = fig.text(0.02, 0.98, '', fontsize=14, fontweight='bold',
                           verticalalignment='top')

        trail_length = 150

        def init():
            ball1_main.set_data([], [])
            ball2_main.set_data([], [])
            trail1_main.set_data([], [])
            trail2_main.set_data([], [])
            sep_line.set_data([], [])
            sep_point.set_data([], [])
            phase1_line.set_data([], [])
            phase2_line.set_data([], [])
            phase1_point.set_data([], [])
            phase2_point.set_data([], [])
            time_text.set_text('')
            return (ball1_main, ball2_main, trail1_main, trail2_main,
                   sep_line, sep_point, phase1_line, phase2_line,
                   phase1_point, phase2_point, time_text)

        def animate(frame):
            i = idx[frame]

            # Update main trajectory
            ball1_main.set_data([traj1['x'][i]], [traj1['y'][i]])
            ball2_main.set_data([traj2['x'][i]], [traj2['y'][i]])

            start = max(0, i - trail_length)
            trail1_main.set_data(traj1['x'][start:i+1], traj1['y'][start:i+1])
            trail2_main.set_data(traj2['x'][start:i+1], traj2['y'][start:i+1])

            # Update separation plot
            sep_line.set_data(t_full[:i+1], sep_full[:i+1])
            sep_point.set_data([t_full[i]], [sep_full[i]])

            # Update phase space
            phase_start = max(0, i - trail_length)
            phase1_line.set_data(traj1['x'][phase_start:i+1], traj1['vx'][phase_start:i+1])
            phase2_line.set_data(traj2['x'][phase_start:i+1], traj2['vx'][phase_start:i+1])
            phase1_point.set_data([traj1['x'][i]], [traj1['vx'][i]])
            phase2_point.set_data([traj2['x'][i]], [traj2['vx'][i]])

            # Update time
            t = traj1['t'][i]
            time_text.set_text(f't = {t:.3f} s')

            return (ball1_main, ball2_main, trail1_main, trail2_main,
                   sep_line, sep_point, phase1_line, phase2_line,
                   phase1_point, phase2_point, time_text)

        anim = animation.FuncAnimation(fig, animate, init_func=init,
                                      frames=n_frames, interval=1000/fps,
                                      blit=True)

        if save_path:
            base_path = os.path.splitext(save_path)[0] if save_path else None

            if format == 'mp4':
                mp4_path = base_path + '.mp4' if base_path else 'comparison.mp4'
                print(f"Saving MP4 video to {mp4_path}...")
                try:
                    anim.save(mp4_path, writer='ffmpeg', fps=fps,
                             extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'],
                             dpi=self.dpi)
                    print(f"✓ MP4 saved ({fps} fps, {duration:.1f}s)")
                except Exception as e:
                    print(f"✗ MP4 failed: {e}")
                    print("  Switching to GIF...")
                    format = 'gif'

            if format == 'gif':
                gif_path = base_path + '.gif' if base_path else 'comparison.gif'
                print(f"Saving GIF to {gif_path}...")
                anim.save(gif_path, writer='pillow', fps=min(fps, 30), dpi=self.dpi)
                print(f"✓ GIF saved ({min(fps, 30)} fps)")

            elif format == 'html5':
                from IPython.display import HTML
                html_path = base_path + '.html' if base_path else 'comparison.html'
                print(f"Saving HTML5 video to {html_path}...")
                with open(html_path, 'w') as f:
                    f.write(anim.to_html5_video())
                print(f"✓ HTML5 video saved")

        return anim, fig


if __name__ == '__main__':
    print("Comparison video generator loaded!")

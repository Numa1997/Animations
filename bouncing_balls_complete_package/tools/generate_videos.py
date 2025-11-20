#!/usr/bin/env python3
"""
Extended video generator for bouncing balls study.

Supports:
- Extended simulations (60+ seconds)
- High-quality MP4 videos (60 FPS)
- Configurable parameters via command line

Usage:
    python3 generate_videos.py [delta_x] [a] [options]

Examples:
    python3 generate_videos.py                    # Use defaults
    python3 generate_videos.py 1e-3 0.3          # Specific separation and parabola
    python3 generate_videos.py 1e-3 0.3 --extended  # Extended 60s video
    python3 generate_videos.py 1e-3 0.3 --duration 90 --fps 60 --format mp4
"""

import sys
import numpy as np
from pathlib import Path
import argparse

# Add paths
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')

from divergence_study import DivergenceStudy
from comparison_video_generator import ComparisonVideoGenerator
from matplotlib_bouncing_balls import BouncingBallsVisualizer


def generate_videos(delta_x=1e-4, a=0.3, output_dir='outputs/videos',
                    t_max=20.0, video_duration=None, fps=30,
                    video_format='gif', extended=False):
    """
    Generate all video formats for a given separation.

    Parameters
    ----------
    delta_x : float
        Initial separation between balls
    a : float
        Parabola steepness parameter (y = a*x²)
    output_dir : str
        Output directory path
    t_max : float
        Maximum simulation time (seconds)
    video_duration : float, optional
        Video duration (if None, uses min of t_max and divergence time)
    fps : int
        Frames per second for video
    video_format : str
        Output format: 'gif', 'mp4', or 'both'
    extended : bool
        If True, use extended settings (60s simulation, MP4, 60 FPS)
    """

    # Apply extended presets
    if extended:
        t_max = max(t_max, 60.0)
        fps = 60
        video_format = 'mp4' if video_format == 'gif' else video_format

    print("=" * 70)
    print("🎬 VIDEO GENERATOR - Bouncing Balls Divergence Study")
    print("=" * 70)
    print()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Initial separation: δx = {delta_x:.2e} m")
    print(f"🎯 Parabola parameter: a = {a} (y = {a}x²)")
    print(f"🎯 Simulation duration: t_max = {t_max:.1f} s")
    print(f"🎥 Video settings: {fps} FPS, format={video_format}")
    if extended:
        print(f"⚡ Extended mode: Enabled (60+ second videos)")
    print()

    # Run simulation
    print("🔄 Running simulation...")
    study = DivergenceStudy(a=a, threshold_factor=100.0, tolerance_abs=1e-12)

    result = study.simulate_pair(
        x1_0=-2.0,
        y1_0=5.0,
        vx1_0=0.0,
        vy1_0=0.0,
        delta_x=delta_x,
        t_max=t_max,
        max_bounces=200 if extended else 100,
        dt_sample=0.01
    )

    if result.diverged:
        print(f"   ✓ Diverged at t = {result.t_divergence:.3f} s")
    else:
        print(f"   ⚠ Did not diverge (separation grew {result.d_final/result.d_initial:.1f}×)")

    print(f"   Bounces: {result.bounce_count_1} / {result.bounce_count_2}")
    print()

    # Determine video duration
    if video_duration is None:
        # Auto-determine based on simulation results
        if result.diverged:
            auto_duration = min(result.t_divergence, t_max)
        else:
            auto_duration = min(t_max, 15.0)
        video_duration = auto_duration

    print(f"📹 Video duration: {video_duration:.1f} s")
    print()

    # Generate videos
    base_name = f"bouncing_balls_dx{delta_x:.0e}"

    # 1. Simple animation
    print("📹 Generating simple animation...")
    viz = BouncingBallsVisualizer()

    save_path = output_path / f"{base_name}_simple"
    viz.create_animation(
        result,
        fps=fps,
        duration=video_duration,
        save_path=str(save_path),
        format=video_format
    )
    print()

    # 2. Advanced comparison video
    print("📹 Generating comparison video (3-panel)...")
    comp_gen = ComparisonVideoGenerator()

    save_path = output_path / f"{base_name}_comparison"
    comp_gen.create_side_by_side_video(
        result,
        fps=fps,
        duration=video_duration,
        save_path=str(save_path),
        format=video_format,
        a=a
    )
    print()

    # Summary
    print("=" * 70)
    print("✅ VIDEO GENERATION COMPLETE!")
    print("=" * 70)
    print()
    print(f"📂 Generated files in: {output_dir}/")

    import os
    for f in sorted(output_path.glob(f"{base_name}*")):
        size_mb = os.path.getsize(f) / (1024*1024)
        print(f"   • {f.name} ({size_mb:.2f} MB)")
    print()

    print("🎥 Video Types:")
    print("   1. Simple: Just the bouncing balls on parabola")
    print("   2. Comparison: 3-panel view with separation & phase space")
    print()

    return result


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Generate extended bouncing balls videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 generate_videos.py                         # Use all defaults
  python3 generate_videos.py 1e-3 0.3               # Set separation and parabola
  python3 generate_videos.py 1e-3 0.3 --extended    # Extended 60s MP4 video
  python3 generate_videos.py 1e-4 1.0 --duration 90 --fps 60 --format mp4
  python3 generate_videos.py 5e-4 0.3 --t-max 120 --duration 120
        '''
    )

    parser.add_argument('delta_x', nargs='?', type=float, default=1e-4,
                       help='Initial separation between balls (default: 1e-4)')
    parser.add_argument('a', nargs='?', type=float, default=0.3,
                       help='Parabola steepness parameter (default: 0.3)')
    parser.add_argument('--t-max', type=float, default=20.0,
                       help='Maximum simulation time in seconds (default: 20.0)')
    parser.add_argument('--duration', type=float, default=None,
                       help='Video duration in seconds (default: auto-detect)')
    parser.add_argument('--fps', type=int, default=30,
                       help='Frames per second (default: 30)')
    parser.add_argument('--format', choices=['gif', 'mp4', 'both'], default='gif',
                       help='Video output format (default: gif)')
    parser.add_argument('--extended', action='store_true',
                       help='Extended mode: 60s simulation, MP4, 60 FPS')
    parser.add_argument('--output-dir', default='outputs/videos',
                       help='Output directory (default: outputs/videos)')

    args = parser.parse_args()

    try:
        result = generate_videos(
            delta_x=args.delta_x,
            a=args.a,
            output_dir=args.output_dir,
            t_max=args.t_max,
            video_duration=args.duration,
            fps=args.fps,
            video_format=args.format,
            extended=args.extended
        )
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

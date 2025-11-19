#!/usr/bin/env python3
"""
Quick video generator for bouncing balls study.

Usage:
    python3 generate_videos.py [delta_x]

Examples:
    python3 generate_videos.py           # Use default (1e-4)
    python3 generate_videos.py 1e-3      # Specific separation
"""

import sys
import numpy as np
from pathlib import Path

# Add paths
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')

from divergence_study import DivergenceStudy
from comparison_video_generator import ComparisonVideoGenerator
from matplotlib_bouncing_balls import BouncingBallsVisualizer


def generate_videos(delta_x=1e-4, output_dir='outputs/videos'):
    """Generate all video formats for a given separation."""

    print("=" * 70)
    print("🎬 VIDEO GENERATOR - Bouncing Balls Divergence Study")
    print("=" * 70)
    print()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Initial separation: δx = {delta_x:.2e} m")
    print()

    # Run simulation
    print("🔄 Running simulation...")
    study = DivergenceStudy(threshold_factor=100.0, tolerance_abs=1e-12)

    result = study.simulate_pair(
        x1_0=-2.0,
        y1_0=5.0,
        vx1_0=0.0,
        vy1_0=0.0,
        delta_x=delta_x,
        t_max=20.0,
        max_bounces=100,
        dt_sample=0.01
    )

    if result.diverged:
        print(f"   ✓ Diverged at t = {result.t_divergence:.3f} s")
    else:
        print(f"   ⚠ Did not diverge (separation grew {result.d_final/result.d_initial:.1f}×)")

    print(f"   Bounces: {result.bounce_count_1} / {result.bounce_count_2}")
    print()

    # Generate videos
    base_name = f"bouncing_balls_dx{delta_x:.0e}"

    # 1. Simple animation
    print("📹 Generating simple animation...")
    viz = BouncingBallsVisualizer()

    save_path = output_path / f"{base_name}_simple"
    viz.create_animation(
        result,
        fps=30,
        duration=min(12, result.t_divergence if result.diverged else 10),
        save_path=str(save_path),
        format='gif'
    )
    print()

    # 2. Advanced comparison video
    print("📹 Generating comparison video (3-panel)...")
    comp_gen = ComparisonVideoGenerator()

    save_path = output_path / f"{base_name}_comparison"
    comp_gen.create_side_by_side_video(
        result,
        fps=30,
        duration=min(12, result.t_divergence if result.diverged else 10),
        save_path=str(save_path),
        format='gif'
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
    # Parse command line argument
    if len(sys.argv) > 1:
        try:
            delta_x = float(sys.argv[1])
        except ValueError:
            print(f"Error: Invalid delta_x value: {sys.argv[1]}")
            print("Usage: python3 generate_videos.py [delta_x]")
            print("Example: python3 generate_videos.py 1e-3")
            sys.exit(1)
    else:
        delta_x = 1e-4  # Default

    try:
        result = generate_videos(delta_x)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

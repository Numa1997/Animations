#!/usr/bin/env python3
"""
Multi-Ball Chaos Study Generator

Generate comprehensive studies of multi-ball bouncing systems with:
- Symmetric initial arrangements
- Color-coded visualizations
- Advanced chaos metrics
- Ensemble statistics
"""

import sys
import numpy as np
from pathlib import Path
import argparse

# Add paths
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')

from multi_ball_study import MultiBallStudy
from multi_ball_visualizer import MultiBallVisualizer


def generate_multi_ball_study(
    n_balls: int = 4,
    arrangement: str = 'circular',
    a: float = 0.3,
    perturbation: float = 1e-3,
    t_max: float = 20.0,
    output_dir: str = 'outputs/multi_ball',
    create_animation: bool = True,
    fps: int = 30,
    video_format: str = 'gif'
):
    """
    Generate complete multi-ball chaos study.

    Parameters
    ----------
    n_balls : int
        Number of balls (2-8 recommended)
    arrangement : str
        'circular' or 'linear' initial arrangement
    a : float
        Parabola steepness
    perturbation : float
        Initial position perturbation size
    t_max : float
        Simulation time
    output_dir : str
        Output directory
    create_animation : bool
        Whether to create animation
    fps : int
        Animation frames per second
    video_format : str
        'gif' or 'mp4'
    """

    print("=" * 70)
    print(f"🎬 MULTI-BALL CHAOS STUDY GENERATOR")
    print("=" * 70)
    print()

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"📁 Output directory: {output_dir}")
    print(f"⚽ Number of balls: {n_balls}")
    print(f"📐 Arrangement: {arrangement}")
    print(f"🎯 Parabola parameter: a = {a}")
    print(f"🔀 Perturbation: {perturbation:.2e} m")
    print(f"⏱️  Max time: {t_max} s")
    print()

    # Run simulation
    print("🔄 Running multi-ball simulation...")
    study = MultiBallStudy(a=a, threshold_factor=100.0)

    result = study.simulate_ensemble(
        n_balls=n_balls,
        arrangement=arrangement,
        x_center=-2.0,
        y_center=5.0,
        perturbation=perturbation,
        t_max=t_max,
        max_bounces=200,
        dt_sample=0.01
    )

    print(f"   ✓ Simulation complete")
    print(f"   Total bounces: {result.total_bounces}")
    print(f"   Bounce counts: {result.bounce_counts}")
    print()

    # Display metrics
    print("📊 CHAOS METRICS:")
    print(f"   Divergence times (s):")
    print(f"      Min: {result.min_divergence_time:.3f}")
    print(f"      Avg: {result.avg_divergence_time:.3f}")
    print(f"      Max: {result.max_divergence_time:.3f}")
    print()
    print(f"   Ensemble statistics:")
    print(f"      Initial spread: {result.ensemble_spread[0]:.6e} m")
    print(f"      Final spread: {result.ensemble_spread[-1]:.6e} m")
    print(f"      Spread growth: {result.ensemble_spread[-1]/result.ensemble_spread[0]:.1f}×")
    print()
    print(f"   Chaos characterization:")
    print(f"      Lyapunov exponent: {result.lyapunov_estimate:.4f} s⁻¹")
    print(f"      Spreading rate: {result.spreading_rate:.6e} m/s")
    print()

    # Create visualizer
    viz = MultiBallVisualizer(figsize=(14, 10), dpi=120)

    # Generate static plot
    print("📈 Generating comprehensive static plot...")
    base_name = f"multi_ball_n{n_balls}_{arrangement}_a{a}_pert{perturbation:.0e}"
    static_path = output_path / f"{base_name}_analysis.png"

    viz.create_static_plot(result, save_path=str(static_path))
    print(f"   ✓ Saved to {static_path}")
    print()

    # Generate animation if requested
    if create_animation:
        print("🎥 Generating animation...")
        anim_path = output_path / f"{base_name}_animation"

        viz.create_animation(
            result,
            fps=fps,
            duration=min(15, t_max),
            save_path=str(anim_path),
            format=video_format
        )
        print()

    # Summary
    print("=" * 70)
    print("✅ MULTI-BALL STUDY COMPLETE!")
    print("=" * 70)
    print()
    print(f"📂 Generated files in: {output_dir}/")

    import os
    for f in sorted(output_path.glob(f"{base_name}*")):
        size_mb = os.path.getsize(f) / (1024*1024)
        print(f"   • {f.name} ({size_mb:.2f} MB)")
    print()

    return result


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Generate multi-ball chaos study',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # 4 balls, circular arrangement
  python3 generate_multi_ball_study.py

  # 6 balls, linear arrangement
  python3 generate_multi_ball_study.py --n-balls 6 --arrangement linear

  # 8 balls, steep parabola, extended time
  python3 generate_multi_ball_study.py --n-balls 8 --a 1.0 --t-max 30

  # High-quality MP4 animation
  python3 generate_multi_ball_study.py --n-balls 4 --fps 60 --format mp4
        '''
    )

    parser.add_argument('--n-balls', type=int, default=4,
                       help='Number of balls (default: 4)')
    parser.add_argument('--arrangement', choices=['circular', 'linear'],
                       default='circular',
                       help='Initial arrangement (default: circular)')
    parser.add_argument('--a', type=float, default=0.3,
                       help='Parabola steepness (default: 0.3)')
    parser.add_argument('--perturbation', type=float, default=1e-3,
                       help='Initial perturbation size (default: 1e-3)')
    parser.add_argument('--t-max', type=float, default=20.0,
                       help='Max simulation time (default: 20.0)')
    parser.add_argument('--output-dir', default='outputs/multi_ball',
                       help='Output directory (default: outputs/multi_ball)')
    parser.add_argument('--no-animation', action='store_true',
                       help='Skip animation generation')
    parser.add_argument('--fps', type=int, default=30,
                       help='Animation FPS (default: 30)')
    parser.add_argument('--format', choices=['gif', 'mp4'], default='gif',
                       help='Animation format (default: gif)')

    args = parser.parse_args()

    try:
        result = generate_multi_ball_study(
            n_balls=args.n_balls,
            arrangement=args.arrangement,
            a=args.a,
            perturbation=args.perturbation,
            t_max=args.t_max,
            output_dir=args.output_dir,
            create_animation=not args.no_animation,
            fps=args.fps,
            video_format=args.format
        )
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Batch video generator for bouncing balls study.

Generates videos for multiple parameter combinations in parallel.

Usage:
    python3 batch_generate_videos.py [options]

Examples:
    python3 batch_generate_videos.py                           # Use defaults
    python3 batch_generate_videos.py --separations 1e-3,5e-4,1e-4  # Specific separations
    python3 batch_generate_videos.py --extended --workers 4    # Extended videos, parallel
"""

import sys
import numpy as np
from pathlib import Path
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing as mp

# Add paths
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')

from generate_videos import generate_videos


def generate_single_video(params):
    """
    Generate a single video with given parameters.

    Parameters
    ----------
    params : dict
        Parameters for video generation

    Returns
    -------
    tuple
        (delta_x, a, success, message)
    """
    try:
        delta_x = params['delta_x']
        a = params['a']

        print(f"[Worker {mp.current_process().name}] Generating: δx={delta_x:.2e}, a={a}")

        result = generate_videos(
            delta_x=delta_x,
            a=a,
            output_dir=params['output_dir'],
            t_max=params['t_max'],
            video_duration=params['video_duration'],
            fps=params['fps'],
            video_format=params['video_format'],
            extended=params['extended']
        )

        return (delta_x, a, True, "Success")
    except Exception as e:
        return (delta_x, a, False, str(e))


def batch_generate_videos(
    separations=None,
    parabola_values=None,
    output_dir='outputs/videos/batch',
    t_max=20.0,
    video_duration=None,
    fps=30,
    video_format='gif',
    extended=False,
    workers=1
):
    """
    Generate videos for multiple parameter combinations.

    Parameters
    ----------
    separations : list of float
        List of delta_x values to test
    parabola_values : list of float
        List of parabola steepness values
    output_dir : str
        Base output directory
    t_max : float
        Maximum simulation time
    video_duration : float, optional
        Video duration
    fps : int
        Frames per second
    video_format : str
        Output format: 'gif', 'mp4', or 'both'
    extended : bool
        Use extended settings
    workers : int
        Number of parallel workers (1 = sequential)
    """

    # Default separations
    if separations is None:
        separations = [1e-3, 5e-4, 1e-4]

    # Default parabola values
    if parabola_values is None:
        parabola_values = [0.3]  # Just flatter parabola by default

    print("=" * 70)
    print("🎬 BATCH VIDEO GENERATOR - Bouncing Balls Study")
    print("=" * 70)
    print()
    print(f"📊 Separations: {len(separations)} values")
    print(f"📊 Parabola values: {len(parabola_values)} values")
    print(f"📊 Total videos: {len(separations) * len(parabola_values) * 2}")  # 2 per combination
    print(f"⚙️  Workers: {workers}")
    print(f"🎥 Settings: {fps} FPS, {video_format}")
    if extended:
        print(f"⚡ Extended mode: Enabled")
    print()

    # Create parameter combinations
    param_list = []
    for delta_x in separations:
        for a in parabola_values:
            params = {
                'delta_x': delta_x,
                'a': a,
                'output_dir': output_dir,
                't_max': t_max,
                'video_duration': video_duration,
                'fps': fps,
                'video_format': video_format,
                'extended': extended
            }
            param_list.append(params)

    # Generate videos
    results = []

    if workers == 1:
        # Sequential execution
        print("Running sequentially...")
        for i, params in enumerate(param_list, 1):
            print(f"\n[{i}/{len(param_list)}] Processing δx={params['delta_x']:.2e}, a={params['a']}")
            result = generate_single_video(params)
            results.append(result)
    else:
        # Parallel execution
        print(f"Running with {workers} parallel workers...")
        print()

        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Submit all jobs
            futures = {executor.submit(generate_single_video, params): params
                      for params in param_list}

            # Collect results as they complete
            for i, future in enumerate(as_completed(futures), 1):
                params = futures[future]
                try:
                    result = future.result()
                    results.append(result)

                    delta_x, a, success, msg = result
                    status = "✓" if success else "✗"
                    print(f"[{i}/{len(param_list)}] {status} δx={delta_x:.2e}, a={a}: {msg}")
                except Exception as e:
                    print(f"[{i}/{len(param_list)}] ✗ Job failed with exception: {e}")

    # Summary
    print()
    print("=" * 70)
    print("📊 BATCH GENERATION SUMMARY")
    print("=" * 70)

    successful = sum(1 for r in results if r[2])
    failed = len(results) - successful

    print(f"Total jobs: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print()

    if failed > 0:
        print("Failed jobs:")
        for delta_x, a, success, msg in results:
            if not success:
                print(f"  ✗ δx={delta_x:.2e}, a={a}: {msg}")
        print()

    print(f"📂 Output directory: {output_dir}")
    print()

    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Batch generate bouncing balls videos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 batch_generate_videos.py                                    # Default set
  python3 batch_generate_videos.py --separations 1e-3,5e-4,1e-4      # Custom separations
  python3 batch_generate_videos.py --extended --workers 4            # Extended, parallel
  python3 batch_generate_videos.py --parabolas 0.3,1.0 --workers 2  # Multiple parabolas
        '''
    )

    parser.add_argument('--separations', type=str, default=None,
                       help='Comma-separated list of delta_x values (e.g., "1e-3,5e-4,1e-4")')
    parser.add_argument('--parabolas', type=str, default=None,
                       help='Comma-separated list of parabola values (e.g., "0.3,1.0")')
    parser.add_argument('--t-max', type=float, default=20.0,
                       help='Maximum simulation time (default: 20.0)')
    parser.add_argument('--duration', type=float, default=None,
                       help='Video duration (default: auto)')
    parser.add_argument('--fps', type=int, default=30,
                       help='Frames per second (default: 30)')
    parser.add_argument('--format', choices=['gif', 'mp4', 'both'], default='gif',
                       help='Video format (default: gif)')
    parser.add_argument('--extended', action='store_true',
                       help='Extended mode: 60s, MP4, 60 FPS')
    parser.add_argument('--output-dir', default='outputs/videos/batch',
                       help='Output directory (default: outputs/videos/batch)')
    parser.add_argument('--workers', type=int, default=1,
                       help='Number of parallel workers (default: 1, sequential)')

    args = parser.parse_args()

    # Parse separations
    separations = None
    if args.separations:
        try:
            separations = [float(x.strip()) for x in args.separations.split(',')]
        except ValueError as e:
            print(f"Error parsing separations: {e}")
            sys.exit(1)

    # Parse parabola values
    parabola_values = None
    if args.parabolas:
        try:
            parabola_values = [float(x.strip()) for x in args.parabolas.split(',')]
        except ValueError as e:
            print(f"Error parsing parabola values: {e}")
            sys.exit(1)

    try:
        results = batch_generate_videos(
            separations=separations,
            parabola_values=parabola_values,
            output_dir=args.output_dir,
            t_max=args.t_max,
            video_duration=args.duration,
            fps=args.fps,
            video_format=args.format,
            extended=args.extended,
            workers=args.workers
        )

        # Exit with error if any failed
        failed = sum(1 for r in results if not r[2])
        sys.exit(1 if failed > 0 else 0)

    except Exception as e:
        print(f"\n❌ Batch generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

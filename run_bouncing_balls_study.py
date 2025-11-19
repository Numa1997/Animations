#!/usr/bin/env python3
"""
Main runner for bouncing balls divergence study.

This script orchestrates the entire study:
1. Load parameters
2. Run divergence simulations for multiple separations
3. Generate visualizations
4. Create report
5. Save all outputs
"""

import numpy as np
import yaml
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add module paths
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')

from divergence_study import DivergenceStudy
from matplotlib_bouncing_balls import BouncingBallsVisualizer


class BouncingBallsStudyRunner:
    """Main orchestrator for the complete study."""

    def __init__(self, param_file: str = 'input/parameters/bouncing_balls_params.yaml'):
        """Initialize study runner."""
        print("=" * 70)
        print("BOUNCING BALLS DIVERGENCE STUDY")
        print("=" * 70)
        print()

        # Load parameters
        with open(param_file, 'r') as f:
            self.params = yaml.safe_load(f)

        print(f"Loaded parameters from: {param_file}")
        print()

        # Create output directories
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_base = Path('outputs')
        self.output_dirs = {
            'visuals': self.output_base / 'visuals' / self.timestamp,
            'simulations': self.output_base / 'simulations' / self.timestamp,
            'reports': self.output_base / 'reports' / self.timestamp,
        }

        for dir_path in self.output_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        print(f"Output directory: {self.output_dirs['visuals'].parent.parent}")
        print()

        # Initialize study
        self.study = DivergenceStudy(
            g=self.params['physics']['g'],
            threshold_factor=self.params['divergence']['threshold_factor'],
            tolerance_abs=self.params['simulation']['tolerance_abs'],
            tolerance_rel=self.params['simulation']['tolerance_rel']
        )

        # Initialize visualizer
        self.viz = BouncingBallsVisualizer(figsize=(12, 8), dpi=150)

    def run_complete_study(self):
        """Execute the complete divergence study."""
        print("STARTING PARAMETER SWEEP")
        print("-" * 70)

        # Get initial conditions
        ic = self.params['initial_conditions']
        x1_0 = ic['x1_0']
        y1_0 = ic['y1_0']
        vx1_0 = ic['vx1_0']
        vy1_0 = ic['vy1_0']

        print(f"Initial conditions (Ball 1):")
        print(f"  Position: ({x1_0}, {y1_0}) m")
        print(f"  Velocity: ({vx1_0}, {vy1_0}) m/s")
        print()

        # Get separation range
        sep_params = self.params['separation_study']
        delta_x_range = (sep_params['delta_x_min'], sep_params['delta_x_max'])

        print(f"Separation range: {delta_x_range[0]:.2e} to {delta_x_range[1]:.2e} m")
        print(f"Number of samples: {sep_params['num_separations']}")
        print(f"Spacing: {sep_params['spacing']}")
        print()

        # Run parameter sweep
        self.results = self.study.parameter_sweep(
            x1_0=x1_0,
            y1_0=y1_0,
            vx1_0=vx1_0,
            vy1_0=vy1_0,
            delta_x_range=delta_x_range,
            num_points=sep_params['num_separations'],
            spacing=sep_params['spacing'],
            t_max=self.params['divergence']['max_time_if_no_divergence'],
            max_bounces=self.params['divergence']['max_bounces'],
            dt_sample=self.params['simulation']['dt_output']
        )

        print()
        print("PARAMETER SWEEP COMPLETE")
        print("=" * 70)
        print()

        return self.results

    def generate_visualizations(self):
        """Generate all visualizations."""
        print("GENERATING VISUALIZATIONS")
        print("-" * 70)

        viz_params = self.params['visualization']

        # 1. Plot a few example trajectories
        print("Creating trajectory plots...")
        n_examples = min(5, len(self.results))
        example_indices = np.linspace(0, len(self.results)-1, n_examples, dtype=int)

        for i, idx in enumerate(example_indices):
            result = self.results[idx]
            save_path = self.output_dirs['visuals'] / f'trajectory_dx{result.delta_x:.2e}.png'
            self.viz.plot_pair_comparison(result, save_path=save_path)
            print(f"  [{i+1}/{n_examples}] Saved: {save_path.name}")

        # 2. Separation vs time for a few cases
        print("\nCreating separation vs time plots...")
        for i, idx in enumerate(example_indices[:3]):  # Just a few
            result = self.results[idx]
            # Reconstruct time history
            t_history = np.linspace(0, len(result.separation_history)-1,
                                   len(result.separation_history)) * self.params['simulation']['dt_output']
            save_path = self.output_dirs['visuals'] / f'separation_vs_time_dx{result.delta_x:.2e}.png'
            self.viz.plot_separation_vs_time(
                t_history,
                result.separation_history,
                result.d_initial,
                self.params['divergence']['threshold_factor'],
                save_path=save_path
            )
            print(f"  [{i+1}/3] Saved: {save_path.name}")

        # 3. Main divergence analysis plot
        print("\nCreating divergence analysis plot...")
        save_path = self.output_dirs['visuals'] / 'divergence_time_vs_separation.png'
        self.viz.plot_divergence_analysis(self.results, save_path=save_path)

        # 4. Create animation for one case
        if viz_params.get('animate_trajectories', False):
            print("\nCreating animation (this may take a while)...")
            # Pick a middle case
            idx_mid = len(self.results) // 2
            result = self.results[idx_mid]
            save_path = self.output_dirs['visuals'] / f'animation_dx{result.delta_x:.2e}.gif'
            try:
                self.viz.create_animation(
                    result,
                    fps=30,
                    duration=min(10, result.t_divergence if result.diverged else 10),
                    save_path=save_path
                )
            except Exception as e:
                print(f"  Animation failed: {e}")

        print("\nVISUALIZATIONS COMPLETE")
        print("=" * 70)
        print()

    def save_data(self):
        """Save simulation data."""
        print("SAVING DATA")
        print("-" * 70)

        # Save summary data
        summary = {
            'timestamp': self.timestamp,
            'parameters': self.params,
            'num_simulations': len(self.results),
            'results': []
        }

        for res in self.results:
            summary['results'].append({
                'delta_x': float(res.delta_x),
                'd_initial': float(res.d_initial),
                'd_final': float(res.d_final),
                'diverged': bool(res.diverged),
                't_divergence': float(res.t_divergence) if res.diverged else None,
                'bounce_count_1': int(res.bounce_count_1),
                'bounce_count_2': int(res.bounce_count_2),
            })

        summary_path = self.output_dirs['simulations'] / 'study_summary.json'
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Saved summary: {summary_path}")

        # Save detailed data for each simulation
        for i, res in enumerate(self.results):
            data_path = self.output_dirs['simulations'] / f'simulation_{i:03d}_dx{res.delta_x:.2e}.npz'
            np.savez(
                data_path,
                delta_x=res.delta_x,
                t1=res.trajectory_1['t'],
                x1=res.trajectory_1['x'],
                y1=res.trajectory_1['y'],
                vx1=res.trajectory_1['vx'],
                vy1=res.trajectory_1['vy'],
                t2=res.trajectory_2['t'],
                x2=res.trajectory_2['x'],
                y2=res.trajectory_2['y'],
                vx2=res.trajectory_2['vx'],
                vy2=res.trajectory_2['vy'],
                separation=res.separation_history
            )

        print(f"Saved {len(self.results)} detailed simulation files")
        print()

    def generate_report(self):
        """Generate final study report."""
        print("GENERATING REPORT")
        print("-" * 70)

        report_lines = []

        # Header
        report_lines.append("# Bouncing Balls Divergence Study - Results")
        report_lines.append("")
        report_lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Study overview
        report_lines.append("## Study Overview")
        report_lines.append("")
        report_lines.append("Two balls falling under gravity, bouncing elastically off a parabolic")
        report_lines.append("boundary y = x². Initial conditions differ by a small separation δx.")
        report_lines.append("")
        report_lines.append("**Objective**: Measure divergence time as a function of initial separation")
        report_lines.append("")

        # Parameters
        report_lines.append("## Parameters")
        report_lines.append("")
        report_lines.append(f"- **Gravity**: g = {self.params['physics']['g']} m/s²")
        report_lines.append(f"- **Initial position**: ({self.params['initial_conditions']['x1_0']}, {self.params['initial_conditions']['y1_0']}) m")
        report_lines.append(f"- **Initial velocity**: ({self.params['initial_conditions']['vx1_0']}, {self.params['initial_conditions']['vy1_0']}) m/s")
        report_lines.append(f"- **Divergence threshold**: {self.params['divergence']['threshold_factor']}× initial separation")
        report_lines.append(f"- **Separation range**: {self.params['separation_study']['delta_x_min']:.2e} to {self.params['separation_study']['delta_x_max']:.2e} m")
        report_lines.append(f"- **Number of samples**: {self.params['separation_study']['num_separations']}")
        report_lines.append("")

        # Results summary
        report_lines.append("## Results Summary")
        report_lines.append("")

        num_diverged = sum(1 for r in self.results if r.diverged)
        report_lines.append(f"- **Total simulations**: {len(self.results)}")
        report_lines.append(f"- **Diverged cases**: {num_diverged}/{len(self.results)}")
        report_lines.append("")

        # Create table
        report_lines.append("### Detailed Results")
        report_lines.append("")
        report_lines.append("| δx (m) | d₀ (m) | Diverged | t_div (s) | Bounces (1/2) |")
        report_lines.append("|--------|--------|----------|-----------|---------------|")

        for res in self.results:
            t_div_str = f"{res.t_divergence:.3f}" if res.diverged else "—"
            diverged_str = "✓" if res.diverged else "✗"
            report_lines.append(
                f"| {res.delta_x:.2e} | {res.d_initial:.2e} | {diverged_str} | "
                f"{t_div_str} | {res.bounce_count_1}/{res.bounce_count_2} |"
            )

        report_lines.append("")

        # Analysis
        report_lines.append("## Analysis")
        report_lines.append("")

        diverged_results = [r for r in self.results if r.diverged]
        if len(diverged_results) > 2:
            delta_x_vals = np.array([r.delta_x for r in diverged_results])
            t_div_vals = np.array([r.t_divergence for r in diverged_results])

            # Fit power law
            coeffs = np.polyfit(np.log(delta_x_vals), np.log(t_div_vals), 1)
            alpha = coeffs[0]
            A = np.exp(coeffs[1])

            report_lines.append("### Power Law Fit")
            report_lines.append("")
            report_lines.append(f"The divergence time follows approximately:")
            report_lines.append("")
            report_lines.append(f"**t_div ≈ {A:.2e} × (δx)^{alpha:.3f}**")
            report_lines.append("")

            if alpha < -0.5:
                report_lines.append(f"The exponent α = {alpha:.3f} indicates **strong sensitivity**.")
                report_lines.append("Smaller separations lead to much longer divergence times.")
            else:
                report_lines.append(f"The exponent α = {alpha:.3f} suggests moderate sensitivity.")

            report_lines.append("")

        # Visualizations
        report_lines.append("## Visualizations")
        report_lines.append("")
        report_lines.append("See the `outputs/visuals` directory for:")
        report_lines.append("- Trajectory comparison plots")
        report_lines.append("- Separation vs time plots")
        report_lines.append("- Divergence time analysis (main result)")
        report_lines.append("- Animation of bouncing dynamics")
        report_lines.append("")

        # Conclusions
        report_lines.append("## Conclusions")
        report_lines.append("")
        report_lines.append("This study demonstrates **sensitivity to initial conditions** in a simple")
        report_lines.append("mechanical system. Even though the dynamics are deterministic (Newton's laws +")
        report_lines.append("elastic collisions), tiny differences in starting positions lead to completely")
        report_lines.append("different trajectories after sufficient time.")
        report_lines.append("")
        report_lines.append("The parabolic boundary acts as a **nonlinear amplifier**: each bounce magnifies")
        report_lines.append("small differences due to position-dependent reflection angles.")
        report_lines.append("")
        report_lines.append("This is a hallmark of **deterministic chaos** - long-term unpredictability")
        report_lines.append("arising from fundamental mathematical properties, not randomness or noise.")
        report_lines.append("")

        # Write report
        report_path = self.output_dirs['reports'] / 'STUDY_REPORT.md'
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))

        print(f"Report saved: {report_path}")
        print()

        # Also print summary to console
        print("\n" + "=" * 70)
        print("STUDY COMPLETE!")
        print("=" * 70)
        print(f"\nSimulations: {len(self.results)}")
        print(f"Diverged: {num_diverged}/{len(self.results)}")
        if len(diverged_results) > 2:
            print(f"\nPower law fit: t_div ≈ {A:.2e} × (δx)^{alpha:.3f}")
        print(f"\nOutputs saved to: {self.output_base}")
        print(f"  - Visuals: {self.output_dirs['visuals']}")
        print(f"  - Data: {self.output_dirs['simulations']}")
        print(f"  - Report: {self.output_dirs['reports']}")
        print()

    def run(self):
        """Run the complete study workflow."""
        try:
            # Run simulations
            self.run_complete_study()

            # Generate visualizations
            self.generate_visualizations()

            # Save data
            self.save_data()

            # Generate report
            self.generate_report()

            return True

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    runner = BouncingBallsStudyRunner()
    success = runner.run()

    if success:
        print("\n✅ Study completed successfully!")
    else:
        print("\n❌ Study failed!")
        sys.exit(1)

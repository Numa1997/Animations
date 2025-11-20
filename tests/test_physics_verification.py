"""
Physics Verification Tests for Bouncing Balls Simulation

These tests verify that the critical physics bugs are fixed and the
simulation behaves correctly.
"""

import numpy as np
import sys
import os

# Add paths
sys.path.append(os.path.join(os.path.dirname(__file__), '../equations/definitions'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../implementation/solvers'))

from bouncing_balls_equations import normal_vector, reflect_velocity, total_energy
from bouncing_ball_solver import BouncingBallSolver


def test_normal_vector_direction():
    """
    CRITICAL TEST: Verify normal points outward and reflection works correctly.

    This test ensures the sign bug in normal_vector() is fixed.
    """
    print("\n" + "="*70)
    print("TEST 1: Normal Vector Direction")
    print("="*70)

    # Test at x=1, a=1 (right side of parabola)
    n = normal_vector(1.0, 1.0)
    print(f"Normal at x=1, a=1: n = ({n[0]:.4f}, {n[1]:.4f})")

    assert n[0] > 0, f"❌ FAIL: Normal should point RIGHT at x > 0, got nx={n[0]}"
    assert n[1] > 0, f"❌ FAIL: Normal should point UP, got ny={n[1]}"
    print("✅ Normal points RIGHT and UP at x > 0")

    # Test at x=-1, a=1 (left side of parabola)
    n_left = normal_vector(-1.0, 1.0)
    print(f"Normal at x=-1, a=1: n = ({n_left[0]:.4f}, {n_left[1]:.4f})")

    assert n_left[0] < 0, f"❌ FAIL: Normal should point LEFT at x < 0, got nx={n_left[0]}"
    assert n_left[1] > 0, f"❌ FAIL: Normal should point UP, got ny={n_left[1]}"
    print("✅ Normal points LEFT and UP at x < 0")

    # Test at x=0, a=1 (vertex)
    n_vertex = normal_vector(0.0, 1.0)
    print(f"Normal at x=0, a=1: n = ({n_vertex[0]:.4f}, {n_vertex[1]:.4f})")

    assert abs(n_vertex[0]) < 1e-10, f"❌ FAIL: Normal should be vertical at vertex, got nx={n_vertex[0]}"
    assert n_vertex[1] > 0, f"❌ FAIL: Normal should point UP at vertex, got ny={n_vertex[1]}"
    print("✅ Normal points straight UP at vertex")

    # Test reflection: ball falling straight down should bounce to the right
    print("\nTesting elastic reflection:")
    v_in = np.array([0.0, -5.0])
    v_out = reflect_velocity(v_in[0], v_in[1], 1.0, 1.0)  # At x=1, a=1
    print(f"Velocity before: v_in = ({v_in[0]:.2f}, {v_in[1]:.2f})")
    print(f"Velocity after:  v_out = ({v_out[0]:.2f}, {v_out[1]:.2f})")

    assert v_out[0] > 0, f"❌ FAIL: Ball hitting right side should bounce right, got vx={v_out[0]}"
    assert v_out[1] > v_in[1], f"❌ FAIL: Vertical velocity should increase after bounce"
    print("✅ Ball bounces to the RIGHT at x > 0")

    # Verify energy is conserved in reflection
    speed_in = np.sqrt(v_in[0]**2 + v_in[1]**2)
    speed_out = np.sqrt(v_out[0]**2 + v_out[1]**2)
    speed_ratio = speed_out / speed_in
    print(f"\nSpeed before: {speed_in:.4f} m/s")
    print(f"Speed after:  {speed_out:.4f} m/s")
    print(f"Ratio: {speed_ratio:.6f} (should be 1.0 for elastic collision)")

    assert abs(speed_ratio - 1.0) < 1e-10, f"❌ FAIL: Speed not conserved in reflection!"
    print("✅ Speed conserved in elastic reflection")

    print("\n" + "="*70)
    print("✅ TEST 1 PASSED: Normal vector direction is correct!")
    print("="*70)


def test_reflection_directions():
    """
    CRITICAL TEST: Balls should bounce in physically correct directions.

    This ensures balls bounce AWAY from the impact point, not toward it.
    """
    print("\n" + "="*70)
    print("TEST 2: Reflection Directions")
    print("="*70)

    solver = BouncingBallSolver(a=1.0, g=9.80665)

    # Test ball at x=1 (right side)
    print("\nTest A: Ball at x=1 (right side of parabola)")
    traj_right = solver.simulate(x0=1.0, y0=3.0, vx0=0.0, vy0=0.0, t_end=2.0)

    if traj_right['bounces']['count'] == 0:
        print("❌ FAIL: No bounces detected!")
        raise AssertionError("No bounces detected for ball at x=1")

    bounce_time = traj_right['bounces']['times'][0]
    print(f"First bounce at t={bounce_time:.4f}s, total: {traj_right['bounces']['count']}")

    # Find velocity shortly after first bounce
    idx_after = np.where(np.array(traj_right['t']) > bounce_time + 0.01)[0]
    if len(idx_after) == 0:
        print("❌ FAIL: Not enough data after bounce")
        raise AssertionError("Not enough trajectory data after bounce")

    vx_after = traj_right['vx'][idx_after[0]]
    vy_after = traj_right['vy'][idx_after[0]]
    print(f"Velocity after bounce: vx={vx_after:.4f}, vy={vy_after:.4f}")

    assert vx_after > 0, f"❌ FAIL: Ball at x>0 should bounce RIGHT, got vx={vx_after}"
    print("✅ Ball bounces to the RIGHT at x > 0")

    # Test ball at x=-1 (left side)
    print("\nTest B: Ball at x=-1 (left side of parabola)")
    traj_left = solver.simulate(x0=-1.0, y0=3.0, vx0=0.0, vy0=0.0, t_end=2.0)

    if traj_left['bounces']['count'] == 0:
        print("❌ FAIL: No bounces detected!")
        raise AssertionError("No bounces detected for ball at x=-1")

    bounce_time = traj_left['bounces']['times'][0]
    print(f"First bounce at t={bounce_time:.4f}s, total: {traj_left['bounces']['count']}")

    idx_after = np.where(np.array(traj_left['t']) > bounce_time + 0.01)[0]
    vx_after = traj_left['vx'][idx_after[0]]
    vy_after = traj_left['vy'][idx_after[0]]
    print(f"Velocity after bounce: vx={vx_after:.4f}, vy={vy_after:.4f}")

    assert vx_after < 0, f"❌ FAIL: Ball at x<0 should bounce LEFT, got vx={vx_after}"
    print("✅ Ball bounces to the LEFT at x < 0")

    print("\n" + "="*70)
    print("✅ TEST 2 PASSED: Reflection directions are correct!")
    print("="*70)


def test_energy_conservation(tolerance=1e-3):
    """
    CRITICAL TEST: Total energy should be constant throughout trajectory.

    This verifies that the collision buffer and reflection preserve energy.
    """
    print("\n" + "="*70)
    print("TEST 3: Energy Conservation")
    print("="*70)
    print(f"Tolerance: {tolerance:.2e} (0.1%)")

    solver = BouncingBallSolver(a=1.0, g=9.80665)
    traj = solver.simulate(x0=-2.0, y0=5.0, vx0=0.0, vy0=0.0, t_end=10.0)

    print(f"\nSimulation completed:")
    print(f"  Duration: {traj['t'][-1]:.2f} s")
    print(f"  Bounces: {len(traj['bounces'])}")
    print(f"  Total points: {len(traj['t'])}")

    # Calculate energy at each point
    energies = []
    for i in range(len(traj['t'])):
        x, y, vx, vy = traj['x'][i], traj['y'][i], traj['vx'][i], traj['vy'][i]
        E = total_energy(x, y, vx, vy, g=solver.g, a=solver.a)
        energies.append(E)

    energies = np.array(energies)
    E_initial = energies[0]

    # Calculate relative energy drift
    drift = np.abs((energies - E_initial) / E_initial)
    max_drift = np.max(drift)
    mean_drift = np.mean(drift)

    print(f"\nEnergy analysis:")
    print(f"  Initial energy: {E_initial:.6f} J")
    print(f"  Final energy: {energies[-1]:.6f} J")
    print(f"  Max drift: {max_drift:.2e} ({max_drift*100:.4f}%)")
    print(f"  Mean drift: {mean_drift:.2e} ({mean_drift*100:.4f}%)")

    # Find worst drift point
    worst_idx = np.argmax(drift)
    print(f"  Worst at t={traj['t'][worst_idx]:.3f}s, E={energies[worst_idx]:.6f}J")

    assert max_drift < tolerance, f"❌ FAIL: Energy not conserved! Drift = {max_drift:.2e} > {tolerance:.2e}"
    print(f"✅ Energy conserved within tolerance!")

    print("\n" + "="*70)
    print("✅ TEST 3 PASSED: Energy conservation verified!")
    print("="*70)


def test_input_validation():
    """
    TEST 4: Input validation should catch invalid parameters.
    """
    print("\n" + "="*70)
    print("TEST 4: Input Validation")
    print("="*70)

    solver = BouncingBallSolver(a=1.0, g=9.80665)

    # Test 1: Ball starts below parabola
    print("\nTest A: Ball below parabola should raise ValueError")
    try:
        solver.simulate(x0=1.0, y0=0.5, vx0=0.0, vy0=0.0, t_end=1.0)  # y=0.5 < ax²=1.0
        print("❌ FAIL: Should have raised ValueError!")
        raise AssertionError("Should have raised ValueError for ball below parabola")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {str(e)[:60]}...")

    # Test 2: Negative time
    print("\nTest B: Negative t_end should raise ValueError")
    try:
        solver.simulate(x0=0.0, y0=5.0, vx0=0.0, vy0=0.0, t_end=-1.0)
        print("❌ FAIL: Should have raised ValueError!")
        raise AssertionError("Should have raised ValueError for negative t_end")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {str(e)[:60]}...")

    # Test 3: Invalid max_bounces
    print("\nTest C: Zero max_bounces should raise ValueError")
    try:
        solver.simulate(x0=0.0, y0=5.0, vx0=0.0, vy0=0.0, t_end=1.0, max_bounces=0)
        print("❌ FAIL: Should have raised ValueError!")
        raise AssertionError("Should have raised ValueError for max_bounces=0")
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {str(e)[:60]}...")

    print("\n" + "="*70)
    print("✅ TEST 4 PASSED: Input validation working!")
    print("="*70)


def run_all_tests():
    """
    Run all physics verification tests.
    """
    print("\n" + "#"*70)
    print("# CRITICAL PHYSICS VERIFICATION TESTS")
    print("# Testing fixes for normal vector sign bug and other issues")
    print("#"*70)

    tests_passed = 0
    tests_total = 4

    try:
        test_normal_vector_direction()
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ TEST 1 FAILED: {e}")

    try:
        test_reflection_directions()
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ TEST 2 FAILED: {e}")

    try:
        test_energy_conservation()
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")

    try:
        test_input_validation()
        tests_passed += 1
    except Exception as e:
        print(f"\n❌ TEST 4 FAILED: {e}")

    # Summary
    print("\n" + "#"*70)
    print(f"# TEST SUMMARY: {tests_passed}/{tests_total} PASSED")
    print("#"*70)

    if tests_passed == tests_total:
        print("\n🎉 ALL TESTS PASSED! Physics is verified correct!")
        print("\nCritical bugs fixed:")
        print("  ✅ Normal vector now points outward (sign fixed)")
        print("  ✅ Reflection directions are physically correct")
        print("  ✅ Energy is conserved (< 0.1% drift)")
        print("  ✅ Input validation catches invalid parameters")
        return True
    else:
        print(f"\n⚠️  WARNING: {tests_total - tests_passed} test(s) failed!")
        print("Physics bugs may still exist. Review failures above.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

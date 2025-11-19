# Bouncing Balls Divergence Study - Results

**Date**: 2025-11-19 19:47:46

## Study Overview

Two balls falling under gravity, bouncing elastically off a parabolic
boundary y = x². Initial conditions differ by a small separation δx.

**Objective**: Measure divergence time as a function of initial separation

## Parameters

- **Gravity**: g = 9.80665 m/s²
- **Initial position**: (-2.0, 5.0) m
- **Initial velocity**: (0.0, 0.0) m/s
- **Divergence threshold**: 100.0× initial separation
- **Separation range**: 1.00e-06 to 1.00e-02 m
- **Number of samples**: 25

## Results Summary

- **Total simulations**: 25
- **Diverged cases**: 23/25

### Detailed Results

| δx (m) | d₀ (m) | Diverged | t_div (s) | Bounces (1/2) |
|--------|--------|----------|-----------|---------------|
| 1.00e-06 | 1.00e-06 | ✓ | 2.980 | 7/7 |
| 1.47e-06 | 1.47e-06 | ✓ | 2.980 | 7/7 |
| 2.15e-06 | 2.15e-06 | ✓ | 2.980 | 7/7 |
| 3.16e-06 | 3.16e-06 | ✓ | 2.980 | 7/7 |
| 4.64e-06 | 4.64e-06 | ✓ | 2.980 | 7/7 |
| 6.81e-06 | 6.81e-06 | ✓ | 2.980 | 7/7 |
| 1.00e-05 | 1.00e-05 | ✓ | 2.980 | 7/7 |
| 1.47e-05 | 1.47e-05 | ✓ | 2.980 | 7/7 |
| 2.15e-05 | 2.15e-05 | ✓ | 2.980 | 7/7 |
| 3.16e-05 | 3.16e-05 | ✓ | 2.980 | 7/7 |
| 4.64e-05 | 4.64e-05 | ✓ | 2.980 | 7/7 |
| 6.81e-05 | 6.81e-05 | ✓ | 2.980 | 7/7 |
| 1.00e-04 | 1.00e-04 | ✓ | 2.980 | 7/7 |
| 1.47e-04 | 1.47e-04 | ✓ | 2.980 | 7/7 |
| 2.15e-04 | 2.15e-04 | ✓ | 2.980 | 7/7 |
| 3.16e-04 | 3.16e-04 | ✓ | 2.980 | 7/7 |
| 4.64e-04 | 4.64e-04 | ✓ | 1.470 | 6/6 |
| 6.81e-04 | 6.81e-04 | ✓ | 9.900 | 29/29 |
| 1.00e-03 | 1.00e-03 | ✓ | 5.480 | 16/16 |
| 1.47e-03 | 1.47e-03 | ✓ | 3.250 | 9/9 |
| 2.15e-03 | 2.15e-03 | ✓ | 5.350 | 14/14 |
| 3.16e-03 | 3.16e-03 | ✓ | 16.320 | 46/46 |
| 4.64e-03 | 4.64e-03 | ✓ | 22.940 | 66/65 |
| 6.81e-03 | 6.81e-03 | ✗ | — | 89/88 |
| 1.00e-02 | 1.00e-02 | ✗ | — | 89/87 |

## Analysis

### Power Law Fit

The divergence time follows approximately:

**t_div ≈ 1.41e+01 × (δx)^0.137**

The exponent α = 0.137 suggests moderate sensitivity.

## Visualizations

See the `outputs/visuals` directory for:
- Trajectory comparison plots
- Separation vs time plots
- Divergence time analysis (main result)
- Animation of bouncing dynamics

## Conclusions

This study demonstrates **sensitivity to initial conditions** in a simple
mechanical system. Even though the dynamics are deterministic (Newton's laws +
elastic collisions), tiny differences in starting positions lead to completely
different trajectories after sufficient time.

The parabolic boundary acts as a **nonlinear amplifier**: each bounce magnifies
small differences due to position-dependent reflection angles.

This is a hallmark of **deterministic chaos** - long-term unpredictability
arising from fundamental mathematical properties, not randomness or noise.

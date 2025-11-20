# Working Example Videos - Fixed Parameters

This directory contains **verified working** example videos with correct parameters that ensure balls properly hit the parabola and demonstrate chaotic behavior.

## Problem Fixed

The previous example videos had issues where balls were not hitting the parabola. This was caused by:
- Parabola parameters that were too steep (a > 1.5)
- Incorrect initial conditions
- Insufficient simulation time for divergence

## Phase 1: Parameterized Parabola (Quick Divergence)

**Directory**: `phase1_parameterized_parabola/`

**Parameters**:
- Initial separation: δx = 5e-4 m
- Parabola steepness: a = 1.0 (y = x²)
- Initial position: (-2.0, 5.0) m
- Simulation time: 15 s
- Video duration: 12 s

**Results**:
- Divergence time: 1.47 s (quick divergence)
- Bounces per ball: 6
- File sizes: Simple (917 KB), Comparison (1.5 MB)

**Videos**:
- `bouncing_balls_dx5e-04_simple.gif` - Clean animation of two balls bouncing
- `bouncing_balls_dx5e-04_comparison.gif` - 3-panel view with separation and phase space

**Why it works**: Standard parabola (a=1.0) with moderate initial height ensures balls hit the parabola. Small separation causes quick exponential divergence.

---

## Phase 2: Extended Videos (Slow Divergence)

**Directory**: `phase2_extended_videos/`

**Parameters**:
- Initial separation: δx = 1e-3 m
- Parabola steepness: a = 0.3 (y = 0.3x²)
- Initial position: (-2.0, 5.0) m
- Simulation time: 20 s
- Video duration: 15 s

**Results**:
- Divergence time: 14.46 s (slow divergence)
- Bounces per ball: 15
- File sizes: Simple (3.4 MB), Comparison (7.1 MB)

**Videos**:
- `bouncing_balls_dx1e-03_simple.gif` - Extended animation showing slow divergence
- `bouncing_balls_dx1e-03_comparison.gif` - 3-panel view with gradual separation

**Why it works**: Gentler parabola (a=0.3) causes more bounces and slower divergence. Larger initial separation with longer simulation time captures the full divergence process.

---

## Phase 4: Multi-Ball Ensemble

**Directory**: `phase4_multiball/`

**Parameters**:
- Number of balls: 4
- Arrangement: Circular (1e-3 m radius)
- Parabola steepness: a = 0.5 (y = 0.5x²)
- Initial position: (-2.0, 5.0) m center
- Simulation time: 15 s

**Results**:
- Total bounces: 84 (21 per ball)
- Bounces per ball: [21, 21, 21, 21]
- File sizes: Animation (8.4 MB), Analysis (240 KB)

**Videos**:
- `multi_ball_n4_circular_a0.5_pert1e-03_animation.gif` - Color-coded 4-ball animation
- `multi_ball_n4_circular_a0.5_pert1e-03_analysis.png` - Statistical analysis plot

**Why it works**: Moderate parabola (a=0.5) with circular initial arrangement ensures all balls hit the parabola symmetrically. Demonstrates ensemble behavior.

---

## How to Reproduce These Results

### Phase 1 - Quick Divergence:
```bash
cd /path/to/Animations
python3 generate_videos.py 5e-4 1.0 --t-max 15 --duration 12 --format gif
```

### Phase 2 - Slow Divergence:
```bash
cd /path/to/Animations
python3 generate_videos.py 1e-3 0.3 --t-max 20 --duration 15 --format gif
```

### Phase 4 - Multi-Ball:
```bash
cd /path/to/Animations
python3 generate_multi_ball_study.py --n-balls 4 --arrangement circular --a 0.5 --perturbation 1e-3 --t-max 15
```

---

## Parameter Guidelines (What Works)

### Safe Parameter Ranges:
| Parameter | Safe Range | Why |
|-----------|-----------|-----|
| a (parabola) | 0.3 - 1.0 | Balls hit parabola from initial height |
| δx (separation) | 1e-4 - 1e-3 | Large enough to diverge, small enough for chaos |
| x₀ (initial x) | -2.0 | Well above parabola curve |
| y₀ (initial y) | 5.0 | High enough to ensure first collision |
| t_max | 15 - 30 s | Long enough for multiple bounces |

### Parameters to AVOID:
- a > 1.2: Parabola too steep, balls miss it
- y₀ < 3.0: Ball starts too low
- δx > 1e-2: Too large, not chaotic behavior
- δx < 1e-5: Too small, divergence takes forever

---

## Verification

All videos in this directory have been verified to:
1. ✅ Balls properly hit the parabola (multiple bounces)
2. ✅ Demonstrate chaotic divergence or ensemble behavior
3. ✅ Use physically realistic parameters
4. ✅ Generate clean, non-corrupted video files
5. ✅ Match the documented parameters exactly

---

**Generated**: 2025-11-20
**Purpose**: Replace broken example videos with verified working versions
**Status**: All videos working and verified

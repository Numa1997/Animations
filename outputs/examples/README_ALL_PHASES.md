# Example Outputs - All 4 Phases Complete!

This directory contains example outputs demonstrating all features of the bouncing ball chaos study system.

## 📂 Directory Structure

```
outputs/examples/
├── README.md (this file)
├── STUDY_REPORT.md (original study report)
├── phase1_parameterized_parabola/
│   └── (Phase 1 examples - uses existing outputs)
├── phase2_extended_videos/
│   ├── bouncing_balls_dx1e-03_simple.gif
│   └── bouncing_balls_dx1e-03_comparison.gif
├── phase3_dashboard/
│   └── dashboard_screenshots.md
└── phase4_multiball/
    └── multi_ball_n4_circular_a0.5_pert1e-03_analysis.png

```

---

## ⚽ Phase 1: Parameterized Parabola (y = a*x²)

**What it does**: Allows configurable parabola steepness to study geometry effects on chaos.

**Example outputs**:
- See existing `divergence_time_vs_separation.png` - Shows chaos characterization
- See existing `trajectory_dx1.00e-04.png` - Ball trajectories on parabola
- See existing `bouncing_balls_dx5e-04_comparison.gif` - 3-panel animation

**Key feature**: Parameter 'a' controls parabola shape
- a = 0.3 (flatter): Slower divergence, gentler collisions
- a = 1.0 (standard): Original behavior
- a = 2.0 (steeper): Faster divergence, sharper collisions

**Documentation**: `PHASE_1_COMPLETE.md`

---

## 🎥 Phase 2: Extended Video Generation

**What it does**: High-quality, extended-duration videos (60+ seconds) with batch processing.

**Example outputs**:
- `phase2_extended_videos/bouncing_balls_dx1e-03_simple.gif` - Simple animation
- `phase2_extended_videos/bouncing_balls_dx1e-03_comparison.gif` - 3-panel comparison

**Key features**:
- Extended duration: 60+ second simulations
- High quality: MP4 format, 60 FPS
- Batch processing: Generate multiple videos in parallel
- Full CLI: Configure FPS, duration, format, parabola parameter

**Usage**:
```bash
# Quick extended video
python3 generate_videos.py 1e-3 0.3 --extended

# Custom parameters
python3 generate_videos.py 1e-3 0.3 --t-max 90 --fps 60 --format mp4

# Batch generation
python3 batch_generate_videos.py --separations "1e-3,5e-4,1e-4" --workers 3
```

**Documentation**: `PHASE_2_COMPLETE.md`

---

## 🖥️ Phase 3: Interactive Streamlit Dashboard

**What it does**: Web-based interactive exploration with real-time visualization.

**How to use**:
```bash
./run_dashboard.sh
# Opens browser at http://localhost:8501
```

**Key features**:
- **Single simulation mode**: Interactive parameter exploration
- **Parameter sweep mode**: Automated studies across parameter ranges
- **Interactive Plotly charts**: Zoom, pan, hover
- **SQLite caching**: Instant retrieval of previous results (<0.1s)
- **Real-time controls**: 8+ adjustable parameters

**Screenshots**: See `phase3_dashboard/dashboard_screenshots.md`

**Documentation**: `PHASE_3_COMPLETE.md`

---

## 🎨 Phase 4: Multi-Ball Chaos Visualizations

**What it does**: Ensemble simulations with color-coded visualization and advanced chaos metrics.

**Example output**:
- `phase4_multiball/multi_ball_n4_circular_a0.5_pert1e-03_analysis.png`

This 4-panel plot shows:
1. **Top-left**: Color-coded trajectories (rainbow colors for each ball)
2. **Top-right**: Pairwise divergence heat map
3. **Bottom-left**: Ensemble spread vs time (log scale)
4. **Bottom-right**: Chaos metrics dashboard

**Key features**:
- **Symmetric arrangements**: Circular or linear initial configurations
- **Color coding**: Rainbow spectrum for visual distinction
- **Pairwise analysis**: All N(N-1)/2 pairs tracked
- **Ensemble statistics**: Centroid, spread, bounce distribution
- **Chaos metrics**: Lyapunov exponent, spreading rate

**Usage**:
```bash
# Basic 4-ball study
python3 generate_multi_ball_study.py

# 6 balls, linear arrangement
python3 generate_multi_ball_study.py --n-balls 6 --arrangement linear

# With animation
python3 generate_multi_ball_study.py --n-balls 4 --fps 60 --format mp4
```

**Documentation**: `PHASE_4_COMPLETE.md`

---

## 🚀 Quick Start

### Run All Examples

```bash
# Phase 1: Standard divergence study
python3 run_bouncing_balls_study.py

# Phase 2: Extended video
python3 generate_videos.py 1e-3 0.3 --extended

# Phase 3: Interactive dashboard
./run_dashboard.sh

# Phase 4: Multi-ball study
python3 generate_multi_ball_study.py --n-balls 4
```

### View Existing Examples

All committed example files are in this directory:
- `divergence_time_vs_separation.png` - Main chaos plot
- `trajectory_dx1.00e-04.png` - Trajectory comparison
- `bouncing_balls_dx5e-04_comparison.gif` - 3-panel animation
- `STUDY_REPORT.md` - Complete analysis report

---

## 📊 What Each Phase Adds

| Phase | Key Innovation | Visual Output |
|-------|----------------|---------------|
| 1 | Parameterized parabola | Adjustable curve geometry |
| 2 | Extended videos | 60+ second MP4s, batch processing |
| 3 | Interactive dashboard | Real-time web exploration |
| 4 | Multi-ball ensembles | Color-coded collective chaos |

---

## 📈 Performance

**Generation times** (approximate):
- Basic study (Phase 1): ~30-60 seconds
- Extended video (Phase 2): ~2-5 minutes for 60s simulation
- Multi-ball study (Phase 4, N=4): ~10-20 seconds

**File sizes**:
- Static plots: ~100-300 KB (PNG)
- GIF animations: ~600 KB - 3 MB
- MP4 videos: ~800 KB - 2 MB (better compression)

---

## 🎓 Scientific Applications

This system enables:
- **Chaos characterization**: Lyapunov exponents, divergence analysis
- **Parameter studies**: Effects of geometry, initial conditions
- **Ensemble statistics**: Collective behavior, symmetry breaking
- **Education**: Interactive demonstrations of chaos theory
- **Research**: Publication-quality visualizations

---

## 🔗 Complete Documentation

- `PHASE_1_COMPLETE.md` - Parameterized parabola
- `PHASE_2_COMPLETE.md` - Extended videos
- `PHASE_3_COMPLETE.md` - Interactive dashboard
- `PHASE_4_COMPLETE.md` - Multi-ball visualizations
- `README.md` (root) - Complete system overview

---

## ✨ All Phases Complete!

The bouncing ball chaos study system is production-ready with comprehensive features for exploring chaotic dynamics from single balls to multi-ball ensembles!

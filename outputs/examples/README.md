# Example Outputs

This folder contains example outputs from the bouncing balls divergence study to demonstrate what the physics study generator produces.

## Files in This Directory

### 📊 `divergence_time_vs_separation.png`
**The main result plot!** Shows how divergence time varies with initial separation.
- Left panel: Regular scale
- Right panel: Log-log scale with power-law fit
- **Finding**: t_div ≈ 14.1 × (δx)^0.137

### 🎯 `trajectory_dx1.00e-04.png`
Example trajectory comparison showing:
- Both balls' paths overlaid on the parabola
- Bounce points marked
- Divergence information
- Initial separation: 100 micrometers

### 🎬 `bouncing_balls_dx5e-04_comparison.gif`
**Advanced 3-panel comparison video!** (590 KB)
- Left panel: Animated bouncing balls on parabola
- Top right: Real-time separation distance plot
- Bottom right: Phase space trajectory (position vs velocity)
- Shows complete divergence dynamics
- Initial separation: 500 micrometers

### 📄 `STUDY_REPORT.md`
Complete study report with:
- Results table for all 25 simulations
- Statistical analysis
- Power law fit
- Conclusions about chaotic dynamics

## Full Outputs Location

When you run a study, **all outputs** are generated in timestamped directories:

```
outputs/
├── visuals/YYYYMMDD_HHMMSS/       # All plots and animations
│   ├── trajectory_*.png           # 5 trajectory comparison plots
│   ├── separation_vs_time_*.png   # Separation growth plots
│   ├── divergence_time_vs_separation.png  # Main result
│   └── animation_*.gif            # Animated bouncing balls
│
├── simulations/YYYYMMDD_HHMMSS/   # Raw data
│   ├── study_summary.json         # All results in JSON
│   └── simulation_*.npz           # Individual simulation data
│
└── reports/YYYYMMDD_HHMMSS/       # Study report
    └── STUDY_REPORT.md
```

**Note**: Full outputs are gitignored to keep the repository size manageable. After running a study, you'll find everything in the timestamped folders above.

## How to Access Full Outputs

After running `python3 run_bouncing_balls_study.py`, look for:
- Latest timestamp folder in `outputs/visuals/`
- All visualizations (10+ files including animations)
- Complete simulation data (25 .npz files)

## Running Your Own Study

### Full Study (25 simulations)
```bash
pip install -r requirements.txt
python3 run_bouncing_balls_study.py
```
Generates: 12+ plots, 25 data files, report (~2-3 MB total)

### Quick Video Generation
```bash
# Generate videos for specific separation
python3 generate_videos.py 1e-4

# Or run with different separations
python3 generate_videos.py 1e-3
python3 generate_videos.py 5e-5
```

Generates:
- Simple animation: Just bouncing balls
- Comparison video: 3-panel view with analysis
- Both as high-quality GIF animations (~600 KB each)

### Video Types Available

1. **Simple Animation**: Clean view of both balls bouncing
2. **Comparison Video**: Advanced 3-panel layout
   - Main trajectory with trails
   - Real-time separation plot
   - Phase space evolution

Total output: ~1 MB per video pair, 30 fps, smooth motion

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

```bash
# Install dependencies
pip install -r requirements.txt

# Run the study
python3 run_bouncing_balls_study.py

# Check outputs
ls -lh outputs/visuals/$(ls -t outputs/visuals/ | head -1)/
```

This will generate:
- 📊 12+ visualization files (~1.5 MB)
- 💾 25 simulation data files
- 📄 Complete study report
- 🎬 Animated GIF of bouncing dynamics

Total output size: ~2-3 MB per study run.

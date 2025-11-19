# Outputs

Generated outputs from the physics study pipeline.

## Structure

### `reports/`
Complete study reports:
- Full analysis documents (PDF, HTML, Markdown)
- Executive summaries
- Technical appendices
- Combined text, equations, figures

**Naming**: `{phenomenon_name}_{date}_report.pdf`

### `visuals/`
Generated visualizations and animations:
- Static plots (PNG, PDF, SVG)
- Animated GIFs
- Video files (MP4, WebM)
- Interactive plots (HTML)

**Naming**: `{phenomenon_name}_{visualization_type}_{timestamp}.{ext}`

### `simulations/`
Raw simulation results and processed data:
- Time series data (CSV, HDF5, NumPy)
- State trajectories
- Observable quantities
- Statistics and derived quantities

**Naming**: `{phenomenon_name}_{parameters_hash}_data.{ext}`

### `parameter_space/`
Parameter space exploration results:
- Parameter sweep data
- Phase diagrams
- Bifurcation analyses
- Sensitivity analyses
- Stability maps

**Naming**: `{phenomenon_name}_param_sweep_{param_names}.{ext}`

## Organization

```
outputs/
├── reports/
│   └── pendulum_2024_study.pdf
├── visuals/
│   ├── pendulum_phase_space.png
│   ├── pendulum_animation.mp4
│   └── pendulum_energy.png
├── simulations/
│   ├── pendulum_data_run001.csv
│   └── pendulum_ensemble_results.h5
└── parameter_space/
    ├── pendulum_length_sweep.png
    └── pendulum_stability_map.png
```

## File Formats

- **Images**: PNG (web/screen), PDF/SVG (publications)
- **Videos**: MP4 (H.264) for compatibility
- **Data**: CSV (small), HDF5 (large), NPY (arrays)
- **Reports**: PDF (final), HTML (interactive), MD (source)

## Metadata

Include metadata files alongside outputs:
- Generation parameters
- Software versions
- Timestamps
- Descriptions

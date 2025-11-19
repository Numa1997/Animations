# Physics Study Generator

A comprehensive system for generating complete physics studies from phenomenon descriptions, including mathematical analysis, simulations, visualizations, and reports.

## System Overview

**Input**: Physical phenomenon description
**Output**: Complete study with equations, explanations, simulations, visuals, and reports

## Directory Structure

### 📥 `input/`
Definitions and parameters for physical phenomena to be studied
- `phenomena/` - Phenomenon definitions and descriptions
- `parameters/` - Parameter configurations for studies

### 📐 `equations/`
Mathematical equations and formulas
- `definitions/` - Equation definitions in symbolic form
- `derivations/` - Step-by-step mathematical derivations

### 📖 `explanations/`
Conceptual and theoretical explanations
- `theory/` - Rigorous theoretical background
- `intuition/` - Intuitive explanations and analogies

### 💻 `implementation/`
Computational implementations
- `solvers/` - Numerical solvers (ODE, PDE, etc.)
- `simulations/` - Simulation engines and runners
- `utils/` - Utility functions and helpers

### 🎬 `animator/`
Animation and visualization system
- `renderers/` - Rendering engines (matplotlib, manim, etc.)
- `scenes/` - Scene definitions and compositions
- `styles/` - Visual styles and themes

### 📊 `outputs/`
Generated study outputs
- `reports/` - Complete study reports
- `visuals/` - Generated visualizations and animations
- `simulations/` - Simulation results and data
- `parameter_space/` - Parameter space explorations

### 📋 `templates/`
Reusable templates
- `study_templates/` - Study report templates
- `visualization_templates/` - Visualization templates

### ⚙️ `config/`
Configuration files and settings

## Workflow

1. **Define** phenomenon in `input/phenomena/`
2. **Specify** parameters in `input/parameters/`
3. **Generate** equations in `equations/`
4. **Implement** solvers in `implementation/`
5. **Create** explanations in `explanations/`
6. **Produce** animations in `animator/`
7. **Output** complete study in `outputs/`

## Getting Started

### Quick Start - Run Example Study

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bouncing balls divergence study
python3 run_bouncing_balls_study.py

# View results
ls outputs/visuals/$(ls -t outputs/visuals/ | head -1)/
```

### Example Outputs

See **`outputs/examples/`** for example results from a complete study run:
- `divergence_time_vs_separation.png` - Main result plot showing chaos
- `trajectory_dx1.00e-04.png` - Trajectory comparison for both balls
- `STUDY_REPORT.md` - Complete analysis with results table

All outputs (plots, animations, data, reports) are generated in timestamped directories under `outputs/`.

### Extended Video Generation (Phase 2)

Generate high-quality, extended-duration videos with full parameter control:

```bash
# Quick extended video (60s, MP4, 60 FPS)
python3 generate_videos.py 1e-3 0.3 --extended

# Custom parameters
python3 generate_videos.py 1e-3 0.3 --t-max 90 --duration 80 --fps 60 --format mp4

# Batch generation (parallel)
python3 batch_generate_videos.py --separations "1e-3,5e-4,1e-4" --extended --workers 3

# Help and options
python3 generate_videos.py --help
python3 batch_generate_videos.py --help
```

**Features**:
- **Extended duration**: 60+ second simulations and videos
- **High quality**: MP4 format with 60 FPS
- **Batch processing**: Generate multiple videos in parallel
- **Full control**: Configure FPS, duration, format, parabola steepness

See `PHASE_2_COMPLETE.md` for complete documentation.

### Interactive Dashboard (Phase 3)

Explore chaos interactively with the Streamlit web dashboard:

```bash
# Launch the interactive dashboard
./run_dashboard.sh
# or
streamlit run streamlit_app.py

# Opens in browser at http://localhost:8501
```

**Features**:
- **Single simulation mode**: Interactive parameter exploration with real-time visualization
- **Parameter sweep mode**: Automated studies across parameter ranges
- **Interactive Plotly charts**: Zoom, pan, hover for detailed analysis
- **SQLite caching**: Intelligent results caching for instant retrieval
- **Two sweep modes**: Initial separation or parabola steepness
- **Export results**: Download data tables and plots

**Visualizations**:
- Trajectory plots with animated parabola
- Log-scale separation vs time
- Phase space portraits (x vs vₓ)
- Parameter sweep analysis

See `PHASE_3_COMPLETE.md` for complete documentation.

### Documentation

- `PHASE_1_COMPLETE.md` - Parameterized parabola implementation
- `PHASE_2_COMPLETE.md` - Extended video generation capabilities
- `PHASE_3_COMPLETE.md` - Interactive Streamlit dashboard
- See individual folder READMEs for detailed component information

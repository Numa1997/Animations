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

### Documentation

See individual folder READMEs for detailed information about each component.

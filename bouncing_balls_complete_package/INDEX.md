# Complete File Index - Bouncing Balls Chaos Study

## 📋 **Every File in This Package**

Total Files: 19 code files + 5 documentation files = **24 files**

---

## 🔬 **Core Physics (2 files)**

### 1. `core_physics/bouncing_balls_equations.py` (8.7 KB)
- **Source**: `equations/definitions/bouncing_balls_equations.py`
- **Purpose**: Pure mathematics - all physics formulas
- **Functions**: parabola(), normal_vector(), reflect_velocity(), total_energy(), free_fall_derivatives(), collision_event()
- **Dependencies**: numpy only
- **Run directly**: No (library only)

### 2. `core_physics/bouncing_ball_solver.py` (9.6 KB)
- **Source**: `implementation/solvers/bouncing_ball_solver.py`
- **Purpose**: Numerical ODE solver with collision detection
- **Class**: BouncingBallSolver
- **Dependencies**: numpy, scipy, bouncing_balls_equations.py
- **Run directly**: No (library only)

---

## 🎮 **Simulator (2 files)**

### 3. `simulator/divergence_study.py` (10.2 KB)
- **Source**: `implementation/simulations/divergence_study.py`
- **Purpose**: Two-ball divergence studies
- **Class**: DivergenceStudy, DivergenceResult (dataclass)
- **Dependencies**: numpy, dataclasses, bouncing_ball_solver.py
- **Run directly**: No (library only)

### 4. `simulator/multi_ball_study.py` (14.9 KB)
- **Source**: `implementation/simulations/multi_ball_study.py`
- **Purpose**: Multi-ball ensemble simulations
- **Class**: MultiBallStudy, MultiBallResult (dataclass)
- **Dependencies**: numpy, dataclasses, bouncing_ball_solver.py
- **Run directly**: No (library only)

---

## 🎨 **Visualization (3 files)**

### 5. `visualization/matplotlib_bouncing_balls.py` (11.7 KB)
- **Source**: `animator/renderers/matplotlib_bouncing_balls.py`
- **Purpose**: Static plots and simple animations
- **Class**: BouncingBallsVisualizer
- **Dependencies**: matplotlib, numpy, matplotlib.animation
- **Run directly**: No (library only)

### 6. `visualization/comparison_video_generator.py` (9.5 KB)
- **Source**: `animator/renderers/comparison_video_generator.py`
- **Purpose**: 3-panel comparison videos
- **Class**: ComparisonVideoGenerator
- **Dependencies**: matplotlib, numpy, matplotlib.animation, GridSpec
- **Run directly**: No (library only)

### 7. `visualization/multi_ball_visualizer.py` (13.7 KB)
- **Source**: `animator/renderers/multi_ball_visualizer.py`
- **Purpose**: Multi-ball color-coded visualizations
- **Class**: MultiBallVisualizer
- **Dependencies**: matplotlib, numpy, matplotlib.cm
- **Run directly**: No (library only)

---

## 🛠️ **User Tools (6 files)** ⭐ RUN THESE!

### 8. `tools/run_bouncing_balls_study.py` (16.9 KB)
- **Source**: Repository root
- **Purpose**: Complete automated chaos study
- **Run**: `python3 run_bouncing_balls_study.py`
- **Requires**: bouncing_balls_params.yaml in ../examples/
- **Produces**: outputs/visuals/TIMESTAMP/ with plots, animations, report
- **Time**: ~2-3 minutes

### 9. `tools/generate_videos.py` (7.2 KB)
- **Source**: Repository root
- **Purpose**: Generate high-quality videos
- **Run**: `python3 generate_videos.py 5e-4 1.0 [options]`
- **Arguments**: delta_x, a, --t-max, --duration, --fps, --format, --extended
- **Produces**: outputs/videos/ with GIF/MP4 files
- **Time**: ~30-60 seconds

### 10. `tools/batch_generate_videos.py` (8.8 KB)
- **Source**: Repository root
- **Purpose**: Batch video generation with parallel workers
- **Run**: `python3 batch_generate_videos.py --separations "1e-3,5e-4" --workers 2`
- **Arguments**: --separations, --parabolas, --workers, --extended
- **Produces**: Multiple videos in outputs/videos/batch/
- **Time**: Depends on workers and count

### 11. `tools/generate_multi_ball_study.py` (6.9 KB)
- **Source**: Repository root
- **Purpose**: Multi-ball chaos studies
- **Run**: `python3 generate_multi_ball_study.py --n-balls 4`
- **Arguments**: --n-balls, --arrangement, --a, --t-max, --fps, --format
- **Produces**: outputs/multi_ball/ with analysis plot + animation
- **Time**: ~20-40 seconds for 4 balls

### 12. `tools/streamlit_app.py` (20.3 KB)
- **Source**: Repository root
- **Purpose**: Interactive web dashboard
- **Run**: `streamlit run streamlit_app.py` or `./run_dashboard.sh`
- **Opens**: Browser at http://localhost:8501
- **Produces**: outputs/streamlit_cache.db (SQLite database)
- **Features**: Real-time exploration, caching, parameter sweeps

### 13. `tools/run_dashboard.sh` (287 bytes)
- **Source**: Repository root
- **Purpose**: Simple launcher for Streamlit dashboard
- **Run**: `./run_dashboard.sh`
- **Does**: Executes `streamlit run streamlit_app.py`

---

## 📚 **Examples (1 file)**

### 14. `examples/bouncing_balls_params.yaml` (4.0 KB)
- **Source**: `input/parameters/bouncing_balls_params.yaml`
- **Purpose**: Configuration file for run_bouncing_balls_study.py
- **Contains**: Physics parameters, initial conditions, simulation settings
- **Format**: YAML
- **Used by**: run_bouncing_balls_study.py

---

## 📖 **Documentation (5 files)** ⭐ READ THESE!

### 15. `README.md` (7.8 KB) ⭐ START HERE
- **Purpose**: Main package documentation
- **Sections**: Quick start, directory structure, tool descriptions, troubleshooting
- **Audience**: First-time users
- **Action**: Read first!

### 16. `INDEX.md` (this file) (6.0 KB)
- **Purpose**: Complete file listing with descriptions
- **Use**: Quick reference for what each file does

### 17. `documentation/ARCHITECTURE.md` (14.6 KB) ⭐ DETAILED CODE EXPLANATION
- **Purpose**: File-by-file code documentation
- **Sections**: Every file explained, dependencies, data flow, import tree
- **Audience**: Developers, anyone wanting to understand the code
- **Use**: Learn how everything fits together

### 18. `documentation/EXECUTION_FLOW.md` (12.4 KB) ⭐ STEP-BY-STEP EXECUTION
- **Purpose**: What happens when you run each command
- **Sections**: Command-by-command execution traces, low-level bounce physics
- **Audience**: Users wanting to understand what's happening
- **Use**: Debug issues, understand performance

### 19. `documentation/USAGE_GUIDE.md` (9.4 KB) ⭐ GUARANTEED WORKING EXAMPLES
- **Purpose**: Practical usage examples with guaranteed-to-work parameters
- **Sections**: Working examples, parameter tables, troubleshooting, verification
- **Audience**: Users getting started, troubleshooting problems
- **Use**: Get working examples quickly

---

## 📦 **Dependencies (1 file)**

### 20. `requirements.txt` (442 bytes)
- **Source**: Repository root
- **Purpose**: Python package dependencies
- **Install**: `pip install -r requirements.txt`
- **Packages**: numpy, scipy, matplotlib, pandas, pyyaml, plotly, streamlit

---

## 📊 **File Statistics**

| Category | Files | Total Size |
|----------|-------|------------|
| Core Physics | 2 | 18.4 KB |
| Simulator | 2 | 25.1 KB |
| Visualization | 3 | 34.9 KB |
| Tools | 6 | 60.4 KB |
| Examples | 1 | 4.0 KB |
| Documentation | 5 | 50.2 KB |
| Dependencies | 1 | 0.4 KB |
| **TOTAL** | **20** | **193.4 KB** |

---

## 🎯 **Quick Reference: Which File to Look At**

### **I want to understand...**
| What | File to Read |
|------|--------------|
| How physics works | `core_physics/bouncing_balls_equations.py` |
| How ODE solving works | `core_physics/bouncing_ball_solver.py` |
| How divergence is computed | `simulator/divergence_study.py` |
| How multi-ball works | `simulator/multi_ball_study.py` |
| How to generate videos | `tools/generate_videos.py` |
| How to use the system | `documentation/USAGE_GUIDE.md` |
| How everything fits together | `documentation/ARCHITECTURE.md` |
| What happens when I run X | `documentation/EXECUTION_FLOW.md` |

### **I want to run...**
| What | File to Run | From Directory |
|------|------------|----------------|
| Quick video | `generate_videos.py 5e-4 1.0` | `tools/` |
| Multi-ball study | `generate_multi_ball_study.py --n-balls 4` | `tools/` |
| Full study | `run_bouncing_balls_study.py` | `tools/` |
| Interactive dashboard | `./run_dashboard.sh` | `tools/` |
| Batch videos | `batch_generate_videos.py --separations "1e-3,5e-4"` | `tools/` |

### **I'm having issues with...**
| Problem | Check File |
|---------|------------|
| Import errors | `documentation/USAGE_GUIDE.md` (Path Setup section) |
| Wrong output | `documentation/USAGE_GUIDE.md` (Parameters tables) |
| Understanding what happened | `documentation/EXECUTION_FLOW.md` |
| Module not found | README.md (Troubleshooting section) |

---

## 🔗 **File Dependencies (Import Tree)**

```
USER TOOLS (tools/*.py)
    ↓
SIMULATOR (simulator/*.py)
    ↓
CORE PHYSICS (core_physics/*.py)
    ↓
STANDARD LIBRARY (numpy, scipy)
```

**Circular dependencies**: NONE (clean architecture!)

---

## ✅ **Verification Checklist**

After extracting this package, verify you have:
- [ ] 2 files in `core_physics/`
- [ ] 2 files in `simulator/`
- [ ] 3 files in `visualization/`
- [ ] 6 files in `tools/`
- [ ] 1 file in `examples/`
- [ ] 5 files in `documentation/`
- [ ] 1 `requirements.txt` file
- [ ] 1 `README.md` file
- [ ] 1 `INDEX.md` file (this file)

**Total: 20 files** (not counting documentation directory structure)

---

**This index provides a complete reference to every file in the package!**

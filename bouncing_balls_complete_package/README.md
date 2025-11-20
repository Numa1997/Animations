# Bouncing Balls Chaos Study - Complete Package

**A comprehensive physics simulation system for studying chaotic dynamics in bouncing ball systems**

---

## 📦 **What's in This Package**

This is a **standalone, complete package** containing all code needed to simulate and visualize chaotic behavior in bouncing ball systems. Everything you need is in this folder.

---

## 📂 **Directory Structure**

```
bouncing_balls_complete_package/
├── README.md (this file)
├── requirements.txt (Python dependencies)
│
├── core_physics/          ⭐ CORE PHYSICS ENGINE
│   ├── bouncing_balls_equations.py
│   └── bouncing_ball_solver.py
│
├── simulator/             ⭐ SIMULATION ORCHESTRATION
│   ├── divergence_study.py
│   └── multi_ball_study.py
│
├── visualization/         ⭐ VISUALIZATION ENGINES
│   ├── matplotlib_bouncing_balls.py
│   ├── comparison_video_generator.py
│   └── multi_ball_visualizer.py
│
├── tools/                 ⭐ USER-FACING SCRIPTS
│   ├── run_bouncing_balls_study.py
│   ├── generate_videos.py
│   ├── batch_generate_videos.py
│   ├── generate_multi_ball_study.py
│   ├── streamlit_app.py
│   └── run_dashboard.sh
│
├── examples/              ⭐ CONFIGURATION EXAMPLES
│   └── bouncing_balls_params.yaml
│
└── documentation/         ⭐ DETAILED GUIDES
    ├── ARCHITECTURE.md
    ├── EXECUTION_FLOW.md
    └── USAGE_GUIDE.md
```

---

## ⚡ **Quick Start** (3 Simple Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Your First Simulation
```bash
cd tools
python3 run_bouncing_balls_study.py
```

### 3. View Results
Results appear in `../outputs/visuals/<timestamp>/`

---

## 🎯 **What Each Tool Does**

### **Core Physics (Don't Run Directly)**
- `core_physics/bouncing_balls_equations.py` - Mathematical formulas
- `core_physics/bouncing_ball_solver.py` - Numerical integration engine

### **Simulators (Don't Run Directly)**
- `simulator/divergence_study.py` - Orchestrates divergence studies
- `simulator/multi_ball_study.py` - Multi-ball ensemble simulations

### **Visualizers (Don't Run Directly)**
- `visualization/*.py` - Create plots and animations

### **Tools (RUN THESE!)**

#### 1. **Basic Study** (`run_bouncing_balls_study.py`)
**What it does**: Complete chaos study with plots and analysis
**Run**: `python3 run_bouncing_balls_study.py`
**Produces**:
- Divergence time vs separation plot
- Trajectory comparisons
- Animation GIF
- Study report

#### 2. **Video Generator** (`generate_videos.py`)
**What it does**: Generate high-quality videos of bouncing balls
**Run**: `python3 generate_videos.py 1e-3 0.3 --extended`
**Produces**:
- Simple animation GIF/MP4
- 3-panel comparison video
- Up to 60+ second duration

#### 3. **Batch Videos** (`batch_generate_videos.py`)
**What it does**: Generate multiple videos in parallel
**Run**: `python3 batch_generate_videos.py --separations "1e-3,5e-4" --workers 2`
**Produces**: Multiple video sets simultaneously

#### 4. **Multi-Ball Study** (`generate_multi_ball_study.py`)
**What it does**: Simulate multiple balls with color-coded visualization
**Run**: `python3 generate_multi_ball_study.py --n-balls 4`
**Produces**:
- 4-panel analysis plot
- Color-coded animation
- Ensemble statistics

#### 5. **Interactive Dashboard** (`streamlit_app.py`)
**What it does**: Web-based interactive exploration
**Run**: `./run_dashboard.sh` or `streamlit run streamlit_app.py`
**Opens**: Browser at http://localhost:8501

---

## 🔄 **Complete Execution Flow**

```
USER RUNS A TOOL
       ↓
Tool imports SIMULATOR
       ↓
Simulator imports CORE PHYSICS
       ↓
Core physics computes trajectories
       ↓
Simulator processes results
       ↓
Tool calls VISUALIZATION
       ↓
Visualizer creates plots/animations
       ↓
OUTPUT FILES SAVED
```

---

## 📊 **What Gets Produced**

### From `run_bouncing_balls_study.py`:
```
outputs/visuals/YYYYMMDD_HHMMSS/
├── divergence_time_vs_separation.png
├── trajectory_dx*.png (multiple)
├── separation_vs_time_dx*.png (multiple)
├── animation_dx*.gif
└── STUDY_REPORT.md
```

### From `generate_videos.py`:
```
outputs/videos/
├── bouncing_balls_dx*_simple.gif
└── bouncing_balls_dx*_comparison.gif
```

### From `generate_multi_ball_study.py`:
```
outputs/multi_ball/
├── multi_ball_n*_*_analysis.png
└── multi_ball_n*_*_animation.gif
```

---

## 🔬 **Physics Background**

This system simulates balls bouncing on a parabolic curve **y = a·x²** where:
- **a** controls the steepness (smaller = flatter, larger = steeper)
- Balls undergo elastic collisions with the parabola
- Tiny differences in initial position lead to exponentially diverging trajectories (chaos!)

**Key Metrics**:
- **Divergence time**: When separation grows 100× initial value
- **Lyapunov exponent**: Rate of exponential separation
- **Energy conservation**: Verified to machine precision

---

## 💡 **Common Use Cases**

### 1. Generate a Quick Video
```bash
cd tools
python3 generate_videos.py 1e-3 0.3
```

### 2. Study Different Parabola Shapes
```bash
# Flatter parabola
python3 generate_videos.py 1e-3 0.3

# Standard parabola
python3 generate_videos.py 1e-3 1.0

# Steeper parabola
python3 generate_videos.py 1e-3 2.0
```

### 3. Multi-Ball Chaos Visualization
```bash
python3 generate_multi_ball_study.py --n-balls 6 --arrangement linear
```

### 4. Interactive Exploration
```bash
./run_dashboard.sh
# Then adjust parameters in browser
```

---

## 🐛 **Troubleshooting**

### "ModuleNotFoundError"
**Problem**: Python can't find modules
**Solution**: Make sure you're in the `tools/` directory when running scripts

### "No such file or directory"
**Problem**: Running from wrong location
**Solution**: Always run tools from `bouncing_balls_complete_package/tools/` directory

### Videos look wrong
**Problem**: Initial conditions may not show collisions
**Solution**: Try different parameters:
```bash
# This WILL show collisions
python3 generate_videos.py 5e-4 1.0 --t-max 20
```

### Balls don't hit parabola
**Problem**: Initial position too high or parabola too steep
**Solution**: Use recommended parameters:
- δx between 1e-4 and 1e-3
- a between 0.3 and 1.0
- Initial height around 5.0

---

## 📈 **Recommended First Runs**

### Best for seeing chaos quickly:
```bash
cd tools
python3 generate_videos.py 5e-4 1.0 --t-max 15 --duration 12
```

### Best multi-ball visualization:
```bash
python3 generate_multi_ball_study.py --n-balls 4 --a 1.0 --t-max 20
```

### Best for exploration:
```bash
./run_dashboard.sh
# Use: δx=5e-4, a=1.0, (x,y)=(-2,5), t_max=20
```

---

## 📚 **Further Documentation**

See `documentation/` folder for:
- `ARCHITECTURE.md` - Detailed system design
- `EXECUTION_FLOW.md` - Step-by-step code flow
- `USAGE_GUIDE.md` - Advanced usage examples

---

## ✅ **Verification**

To verify everything works:
```bash
cd tools
python3 -c "import sys; sys.path.append('../core_physics'); from bouncing_balls_equations import parabola; print(f'Parabola at x=2, a=1: y={parabola(2, 1)}')"
# Should print: Parabola at x=2, a=1: y=4.0
```

---

## 🎓 **Key Takeaways**

1. **Always run from `tools/` directory**
2. **Start with recommended parameters** (see above)
3. **Check outputs** in `../outputs/` after running
4. **For interactive use**, run the Streamlit dashboard
5. **For batch processing**, use `batch_generate_videos.py`

---

**This is a complete, self-contained package. Everything needed is here!**

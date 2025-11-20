# System Architecture - Complete Code Explanation

## 📋 **File-by-File Documentation**

---

## 🔬 **CORE PHYSICS** (Bottom Layer)

### `core_physics/bouncing_balls_equations.py`

**Source**: `equations/definitions/bouncing_balls_equations.py` (original repo)

**Purpose**: Contains all mathematical formulas for the physics simulation

**Key Functions**:
```python
def parabola(x, a=1.0):
    """Compute y = a*x²"""

def normal_vector(x_c, a=1.0):
    """Compute normal vector at collision point"""

def reflect_velocity(vx, vy, x_c, a=1.0):
    """Compute reflected velocity after elastic collision"""

def total_energy(x, y, vx, vy, g, a):
    """Compute total mechanical energy"""

def free_fall_derivatives(t, state, g, a):
    """ODE system for free fall: dx/dt, dy/dt, dvx/dt, dvy/dt"""

def collision_event(t, state, g, a):
    """Event function for collision detection"""
```

**Dependencies**: numpy

**Used By**: `bouncing_ball_solver.py`

**Physics Implemented**:
- Parabola equation: y = a·x²
- Normal vector: n = (-2ax, 1) / |....|
- Elastic reflection: v' = v - 2(v·n)n
- Gravitational acceleration: g = 9.80665 m/s²
- Energy: E = ½m(vx² + vy²) + mgy + U(parabola)

---

### `core_physics/bouncing_ball_solver.py`

**Source**: `implementation/solvers/bouncing_ball_solver.py` (original repo)

**Purpose**: Numerical integration engine that solves the bouncing ball ODE system

**Key Class**:
```python
class BouncingBallSolver:
    def __init__(self, g=9.80665, a=1.0, tolerance_abs=1e-12, ...):
        """Initialize solver with physics parameters"""

    def integrate_segment(self, state0, t_start, t_end):
        """Integrate from t_start to t_end or until collision"""
        # Uses scipy.integrate.solve_ivp with DOP853

    def apply_collision(self, state):
        """Apply elastic reflection at collision point"""

    def simulate(self, x0, y0, vx0, vy0, t_end, max_bounces):
        """Main simulation loop - integrates with bounces"""
        # Returns: {t, x, y, vx, vy, bounces, energy}
```

**Dependencies**:
- numpy
- scipy (solve_ivp from scipy.integrate)
- bouncing_balls_equations.py

**Used By**: `divergence_study.py`, `multi_ball_study.py`

**Algorithm**:
1. Start with initial conditions (x0, y0, vx0, vy0)
2. Integrate ODEs using scipy solve_ivp with DOP853 (high-precision)
3. Detect collisions using event-based detection
4. When collision detected:
   - Compute exact collision point
   - Apply elastic reflection formula
   - Continue integration
5. Repeat until t_end or max_bounces reached

**Key Parameters**:
- `tolerance_abs`: 1e-12 (very precise for chaos studies)
- `tolerance_rel`: 1e-9
- `max_step`: 0.01 seconds

---

## 🎮 **SIMULATOR LAYER** (Middle Layer)

### `simulator/divergence_study.py`

**Source**: `implementation/simulations/divergence_study.py` (original repo)

**Purpose**: Orchestrates studies of how nearby trajectories diverge (chaos)

**Key Class**:
```python
class DivergenceStudy:
    def __init__(self, g=9.80665, a=1.0, threshold_factor=100.0, ...):
        """Initialize study with BouncingBallSolver"""
        self.solver = BouncingBallSolver(g, a, ...)

    def simulate_pair(self, x1_0, y1_0, vx1_0, vy1_0, delta_x, t_max, ...):
        """Simulate TWO balls with initial separation delta_x"""
        # Ball 1: (x1_0, y1_0)
        # Ball 2: (x1_0 + delta_x, y1_0)
        # Returns: DivergenceResult with divergence info
```

**Dependencies**:
- numpy
- dataclasses
- bouncing_ball_solver.py

**Used By**: `run_bouncing_balls_study.py`, `generate_videos.py`, `streamlit_app.py`

**What It Does**:
1. Simulates two balls starting very close together (separated by delta_x)
2. Tracks separation distance over time: d(t) = |r₁(t) - r₂(t)|
3. Detects when d(t) > threshold × d(0) (divergence!)
4. Records divergence time, bounce counts, trajectories

**Dataclass Output**:
```python
@dataclass
class DivergenceResult:
    diverged: bool                    # Did they diverge?
    t_divergence: float              # When did divergence occur?
    d_initial: float                 # Initial separation
    d_final: float                   # Final separation
    trajectory_1: Dict               # Full trajectory of ball 1
    trajectory_2: Dict               # Full trajectory of ball 2
    bounce_count_1: int              # Number of bounces (ball 1)
    bounce_count_2: int              # Number of bounces (ball 2)
```

---

### `simulator/multi_ball_study.py`

**Source**: `implementation/simulations/multi_ball_study.py` (original repo)

**Purpose**: Simulates MULTIPLE balls (ensemble) to study collective chaos

**Key Class**:
```python
class MultiBallStudy:
    def simulate_ensemble(self, n_balls=4, arrangement='circular', ...):
        """Simulate N balls in symmetric arrangement"""
        # Creates N BouncingBallSolvers
        # Returns: MultiBallResult with all trajectories
```

**Dependencies**:
- numpy
- dataclasses
- bouncing_ball_solver.py

**Used By**: `generate_multi_ball_study.py`

**What It Does**:
1. Creates N initial positions in symmetric arrangement
   - Circular: balls arranged in circle
   - Linear: balls arranged in line
2. Simulates each ball independently
3. Computes pairwise divergences (all N(N-1)/2 pairs)
4. Calculates ensemble statistics:
   - Centroid (mean position)
   - Ensemble spread (how far apart they are)
   - Lyapunov exponent estimate
5. Returns complete multi-ball results

**Dataclass Output**:
```python
@dataclass
class MultiBallResult:
    n_balls: int
    trajectories: List[Dict]              # One per ball
    pairwise_divergences: Dict            # (i,j) -> divergence info
    ensemble_spread: np.ndarray          # Spread over time
    centroid_trajectory: Dict             # Mean trajectory
    lyapunov_estimate: float             # Chaos metric
    # ... more fields
```

---

## 🎨 **VISUALIZATION LAYER** (Top Layer - Graphics)

### `visualization/matplotlib_bouncing_balls.py`

**Source**: `animator/renderers/matplotlib_bouncing_balls.py` (original repo)

**Purpose**: Creates static plots and simple animations using matplotlib

**Key Class**:
```python
class BouncingBallsVisualizer:
    def plot_divergence_time_vs_separation(self, results_df):
        """Main chaos characterization plot"""

    def plot_trajectories(self, result):
        """Plot ball trajectories on parabola"""

    def plot_separation_vs_time(self, result):
        """Plot separation d(t) on log scale"""

    def create_animation(self, result, fps=30, duration=10, ...):
        """Create animated GIF"""
```

**Dependencies**: matplotlib, numpy, matplotlib.animation

**Used By**: `run_bouncing_balls_study.py`, `generate_videos.py`

**Produces**: PNG plots, GIF animations

---

### `visualization/comparison_video_generator.py`

**Source**: `animator/renderers/comparison_video_generator.py` (original repo)

**Purpose**: Creates multi-panel comparison videos (3-panel layout)

**Key Method**:
```python
def create_side_by_side_video(result, fps=60, duration=15, format='mp4', a=1.0):
    """Create 3-panel video:
    - Left: Trajectory animation
    - Top-right: Separation vs time
    - Bottom-right: Phase space (x vs vx)
    """
```

**Dependencies**: matplotlib, numpy, matplotlib.animation, matplotlib.gridspec

**Used By**: `generate_videos.py`

**Produces**: MP4 or GIF videos with 3-panel layout

---

### `visualization/multi_ball_visualizer.py`

**Source**: `animator/renderers/multi_ball_visualizer.py` (original repo)

**Purpose**: Creates multi-ball visualizations with color coding

**Key Methods**:
```python
def create_static_plot(result):
    """Create 4-panel analysis:
    - Top-left: Color-coded trajectories
    - Top-right: Pairwise divergence heat map
    - Bottom-left: Ensemble spread
    - Bottom-right: Chaos metrics
    """

def create_animation(result, fps=30, ...):
    """Animated multi-ball visualization with colors"""
```

**Dependencies**: matplotlib, numpy, matplotlib.cm (for color maps)

**Used By**: `generate_multi_ball_study.py`

**Produces**: PNG plots with 4 panels, GIF/MP4 animations with color-coded balls

---

## 🛠️ **TOOLS LAYER** (User Interface)

### `tools/run_bouncing_balls_study.py`

**Source**: `run_bouncing_balls_study.py` (original repo root)

**Purpose**: Complete automated chaos study with default parameters

**Execution Flow**:
```
1. Load parameters from YAML file
2. Create DivergenceStudy instance
3. Run simulations for multiple delta_x values
4. Create BouncingBallsVisualizer
5. Generate all plots
6. Create animation
7. Generate study report (markdown)
8. Save everything to timestamped output directory
```

**Dependencies**: ALL previous layers

**Produces**:
- `outputs/visuals/TIMESTAMP/`
  - divergence_time_vs_separation.png
  - trajectory_dx*.png (one per delta_x)
  - separation_vs_time_dx*.png
  - animation_dx*.gif
  - STUDY_REPORT.md

**Run**: `python3 run_bouncing_balls_study.py`

---

### `tools/generate_videos.py`

**Source**: `generate_videos.py` (original repo root)

**Purpose**: Generate high-quality videos with custom parameters

**CLI Arguments**:
```
python3 generate_videos.py [delta_x] [a] [options]

Positional:
  delta_x         Initial separation (default: 1e-4)
  a               Parabola steepness (default: 0.3)

Options:
  --t-max         Simulation duration (default: 20s)
  --duration      Video duration (default: auto)
  --fps           Frames per second (default: 30)
  --format        gif, mp4, or both (default: gif)
  --extended      Preset: 60s sim, MP4, 60 FPS
```

**Execution Flow**:
```
1. Parse command-line arguments
2. Create DivergenceStudy
3. Run simulate_pair()
4. Create BouncingBallsVisualizer
5. Create ComparisonVideoGenerator
6. Generate simple animation
7. Generate 3-panel comparison video
8. Save to outputs/videos/
```

**Produces**:
- `outputs/videos/`
  - bouncing_balls_dx*_simple.gif/mp4
  - bouncing_balls_dx*_comparison.gif/mp4

---

### `tools/batch_generate_videos.py`

**Source**: `batch_generate_videos.py` (original repo root)

**Purpose**: Generate multiple videos in parallel

**CLI Arguments**:
```
--separations    "1e-3,5e-4,1e-4" (comma-separated)
--parabolas      "0.3,1.0,2.0" (comma-separated)
--workers        Number of parallel workers (default: 1)
--extended       Use extended mode for all
```

**Execution Flow**:
```
1. Parse parameters
2. Create parameter combinations (cartesian product)
3. Launch parallel workers (using multiprocessing)
4. Each worker runs generate_videos() independently
5. Collect results and report summary
```

**Produces**: Multiple video sets in parallel

---

### `tools/generate_multi_ball_study.py`

**Source**: `generate_multi_ball_study.py` (original repo root)

**Purpose**: Create multi-ball ensemble studies

**CLI Arguments**:
```
--n-balls       Number of balls (default: 4)
--arrangement   circular or linear (default: circular)
--a             Parabola steepness (default: 0.3)
--perturbation  Initial spread (default: 1e-3)
--t-max         Simulation time (default: 20s)
--fps           Animation FPS (default: 30)
--format        gif or mp4 (default: gif)
--no-animation  Skip animation (static plot only)
```

**Execution Flow**:
```
1. Parse arguments
2. Create MultiBallStudy
3. Run simulate_ensemble()
4. Create MultiBallVisualizer
5. Generate 4-panel static plot
6. Generate color-coded animation (if requested)
7. Display metrics
8. Save to outputs/multi_ball/
```

**Produces**:
- `outputs/multi_ball/`
  - multi_ball_n*_*_analysis.png (4-panel plot)
  - multi_ball_n*_*_animation.gif/mp4

---

### `tools/streamlit_app.py`

**Source**: `streamlit_app.py` (original repo root)

**Purpose**: Interactive web dashboard for parameter exploration

**Features**:
- Two modes: Single simulation, Parameter sweep
- Interactive controls (sliders, inputs)
- Real-time Plotly visualizations
- SQLite caching for fast retrieval
- Export data tables

**Run**: `streamlit run streamlit_app.py` or `./run_dashboard.sh`

**Dependencies**: streamlit, plotly, sqlite3, DivergenceStudy

**Opens**: Browser at http://localhost:8501

---

## 🔄 **Complete Data Flow**

```
USER INPUT (parameters: δx, a, x0, y0, vx0, vy0, t_max)
      ↓
TOOL LAYER (generate_videos.py, run_bouncing_balls_study.py, etc.)
      ↓
SIMULATOR LAYER (DivergenceStudy or MultiBallStudy)
      ↓
CORE PHYSICS (BouncingBallSolver)
      ↓
EQUATIONS (bouncing_balls_equations.py)
      ↓
SCIPY INTEGRATION (solve_ivp with DOP853)
      ↓
RAW TRAJECTORIES (t, x, y, vx, vy arrays)
      ↓
SIMULATOR LAYER (processes results, computes divergence)
      ↓
VISUALIZATION LAYER (creates plots/animations)
      ↓
OUTPUT FILES (PNG, GIF, MP4, MD reports)
```

---

## 📊 **Import Dependencies (Bottom-Up)**

**Level 1** (No dependencies except numpy/scipy):
- `bouncing_balls_equations.py`

**Level 2** (Depends on Level 1):
- `bouncing_ball_solver.py` → imports bouncing_balls_equations

**Level 3** (Depends on Levels 1-2):
- `divergence_study.py` → imports bouncing_ball_solver
- `multi_ball_study.py` → imports bouncing_ball_solver

**Level 4** (Depends on Levels 1-3):
- `matplotlib_bouncing_balls.py` → uses DivergenceResult
- `comparison_video_generator.py` → uses DivergenceResult
- `multi_ball_visualizer.py` → uses MultiBallResult

**Level 5** (Top - Depends on all previous):
- All tools/*.py scripts → import everything needed

---

## 🎯 **Key Insight: Layered Architecture**

```
┌─────────────────────────────────────┐
│  TOOLS (user-facing scripts)        │
├─────────────────────────────────────┤
│  VISUALIZATION (matplotlib/plotly)  │
├─────────────────────────────────────┤
│  SIMULATOR (orchestration)          │
├─────────────────────────────────────┤
│  SOLVER (numerical integration)     │
├─────────────────────────────────────┤
│  EQUATIONS (pure mathematics)       │
└─────────────────────────────────────┘
```

Each layer only imports from layers below it. This ensures clean separation of concerns.

---

**This architecture document explains exactly where each file came from and what role it plays in the system!**

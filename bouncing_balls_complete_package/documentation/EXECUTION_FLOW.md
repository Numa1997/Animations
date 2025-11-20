# Execution Flow - What Happens When You Run Each Command

This document shows **exactly** what happens, step-by-step, when you run each tool.

---

## 🎬 **Command 1: `python3 generate_videos.py 5e-4 1.0`**

### **Step-by-Step Execution**:

```
1. SCRIPT STARTS
   File: tools/generate_videos.py
   Line: if __name__ == '__main__':

2. PARSE ARGUMENTS
   delta_x = 5e-4 (from command line)
   a = 1.0 (from command line)
   Other args use defaults (t_max=20, fps=30, format='gif')

3. CALL generate_videos() FUNCTION
   Parameters: delta_x=5e-4, a=1.0, t_max=20.0, ...

4. CREATE OUTPUT DIRECTORY
   Path: outputs/videos/
   Creates if doesn't exist

5. CREATE DIVERGENCE STUDY
   Code: study = DivergenceStudy(a=1.0, threshold_factor=100.0, ...)
   This creates: study.solver = BouncingBallSolver(a=1.0, ...)

6. RUN SIMULATION
   Code: result = study.simulate_pair(
           x1_0=-2.0, y1_0=5.0, vx1_0=0.0, vy1_0=0.0,
           delta_x=5e-4, t_max=20.0, max_bounces=100, dt_sample=0.01
         )

   Inside simulate_pair():
   a. Create two initial states:
      - Ball 1: (-2.0, 5.0, 0.0, 0.0)
      - Ball 2: (-2.0 + 5e-4, 5.0, 0.0, 0.0)  [slightly offset]

   b. Simulate Ball 1:
      - solver.integrate_segment() from t=0 to collision
      - Detect collision using collision_event()
      - Apply reflection using apply_collision()
      - Repeat until t=20.0 or 100 bounces

   c. Simulate Ball 2 (same process)

   d. Compute separation d(t) = |r1(t) - r2(t)| at each time

   e. Check if d(t) > 100 * d(0) (divergence threshold)

   f. Return DivergenceResult with:
      - diverged: True/False
      - t_divergence: time when divergence occurred
      - trajectory_1, trajectory_2: full trajectories
      - bounce_count_1, bounce_count_2

7. CREATE VISUALIZERS
   viz = BouncingBallsVisualizer()
   comp_gen = ComparisonVideoGenerator()

8. GENERATE SIMPLE ANIMATION
   Code: viz.create_animation(result, fps=30, duration=auto, format='gif')

   Process:
   - Creates matplotlib figure
   - Plots parabola y = 1.0 * x²
   - Animates balls moving along trajectories
   - Saves as: outputs/videos/bouncing_balls_dx5e-04_simple.gif

9. GENERATE COMPARISON VIDEO
   Code: comp_gen.create_side_by_side_video(result, fps=30, ...)

   Process:
   - Creates 3-panel figure:
     * Left: Trajectories
     * Top-right: Separation vs time
     * Bottom-right: Phase space
   - Animates all panels synchronously
   - Saves as: outputs/videos/bouncing_balls_dx5e-04_comparison.gif

10. PRINT SUMMARY
    Shows:
    - File sizes
    - Divergence status
    - Bounce counts

11. DONE
    Exit code 0
```

### **What You Get**:
```
outputs/videos/
├── bouncing_balls_dx5e-04_simple.gif (~ 900 KB)
└── bouncing_balls_dx5e-04_comparison.gif (~ 1.5 MB)
```

---

## 🎨 **Command 2: `python3 generate_multi_ball_study.py --n-balls 4`**

### **Step-by-Step Execution**:

```
1. SCRIPT STARTS
   File: tools/generate_multi_ball_study.py

2. PARSE ARGUMENTS
   n_balls = 4
   arrangement = 'circular' (default)
   a = 0.3 (default)
   perturbation = 1e-3
   t_max = 20.0

3. CREATE OUTPUT DIRECTORY
   Path: outputs/multi_ball/

4. CREATE MULTI-BALL STUDY
   study = MultiBallStudy(a=0.3, threshold_factor=100.0, ...)

5. RUN ENSEMBLE SIMULATION
   result = study.simulate_ensemble(
       n_balls=4,
       arrangement='circular',
       x_center=-2.0,
       y_center=5.0,
       perturbation=1e-3,
       t_max=20.0
   )

   Inside simulate_ensemble():

   a. CREATE SYMMETRIC POSITIONS
      Circular arrangement: 4 balls in circle
      - Ball 0: (-2.001, 5.000) [angle 0°]
      - Ball 1: (-2.000, 5.001) [angle 90°]
      - Ball 2: (-1.999, 5.000) [angle 180°]
      - Ball 3: (-2.000, 4.999) [angle 270°]

   b. SIMULATE EACH BALL INDEPENDENTLY
      For each ball i:
      - Create solver_i = BouncingBallSolver(a=0.3, ...)
      - Run solver_i.simulate(x0, y0, vx0=0, vy0=0, t_end=20.0)
      - Store result in trajectories[i]

   c. COMPUTE PAIRWISE DIVERGENCES
      For all pairs (i, j) where i < j:
      - Compute separation d_ij(t) = |r_i(t) - r_j(t)|
      - Check if d_ij(t) > 100 * d_ij(0)
      - Record divergence time
      Total: 4 balls → 6 pairs (0-1, 0-2, 0-3, 1-2, 1-3, 2-3)

   d. COMPUTE ENSEMBLE STATISTICS
      - Centroid: mean position at each time
      - Spread: average distance from centroid
      - Lyapunov estimate: from divergence data

   e. RETURN MultiBallResult

6. CREATE VISUALIZER
   viz = MultiBallVisualizer()

7. GENERATE 4-PANEL STATIC PLOT
   Code: viz.create_static_plot(result, save_path=...)

   Creates 4 subplots:
   - Top-left: Color-coded trajectories (rainbow colors)
   - Top-right: Pairwise divergence heat map
   - Bottom-left: Ensemble spread vs time
   - Bottom-right: Text metrics

   Saves as: multi_ball_n4_circular_a0.3_pert1e-03_analysis.png

8. GENERATE ANIMATION (if not --no-animation)
   Code: viz.create_animation(result, fps=30, format='gif')

   Creates dual-panel:
   - Left: Balls bouncing (color-coded)
   - Right: Ensemble spread plot

   Saves as: multi_ball_n4_circular_a0.3_pert1e-03_animation.gif

9. PRINT METRICS
   Shows:
   - Total bounces
   - Divergence times (min/avg/max)
   - Lyapunov exponent
   - Ensemble spread

10. DONE
```

### **What You Get**:
```
outputs/multi_ball/
├── multi_ball_n4_circular_a0.3_pert1e-03_analysis.png (~ 230 KB)
└── multi_ball_n4_circular_a0.3_pert1e-03_animation.gif (~ 10 MB)
```

---

## 📊 **Command 3: `python3 run_bouncing_balls_study.py`**

### **Step-by-Step Execution**:

```
1. SCRIPT STARTS
   File: tools/run_bouncing_balls_study.py

2. LOAD PARAMETERS FROM YAML
   File: ../examples/bouncing_balls_params.yaml

   Reads:
   - physics.g = 9.80665
   - physics.a = 0.3
   - initial_conditions.x1_0 = -2.0
   - initial_conditions.y1_0 = 5.0
   - divergence.separations = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
   - simulation.t_max = 10.0
   - simulation.max_bounces = 100

3. CREATE DIVERGENCE STUDY
   study = DivergenceStudy(g=9.80665, a=0.3, ...)

4. RUN SIMULATIONS FOR EACH SEPARATION
   For delta_x in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]:

   a. Run simulate_pair(delta_x=delta_x, ...)
   b. Store result in results list
   c. Print progress (e.g., "Running δx=1.00e-04...")

5. CREATE RESULTS DATAFRAME
   Convert results list to pandas DataFrame with columns:
   - delta_x
   - diverged
   - t_divergence
   - d_final
   - bounce_count_1, bounce_count_2

6. CREATE OUTPUT DIRECTORY
   Path: outputs/visuals/YYYYMMDD_HHMMSS/

7. CREATE VISUALIZER
   viz = BouncingBallsVisualizer()

8. GENERATE DIVERGENCE TIME PLOT
   viz.plot_divergence_time_vs_separation(results_df)
   Saves: divergence_time_vs_separation.png

9. FOR EACH RESULT, CREATE:
   a. Trajectory plot
      viz.plot_trajectories(result)
      Saves: trajectory_dx*.png

   b. Separation vs time plot
      viz.plot_separation_vs_time(result)
      Saves: separation_vs_time_dx*.png

10. CREATE ANIMATION
    Pick one result (e.g., dx=1e-4)
    viz.create_animation(result)
    Saves: animation_dx1e-04.gif

11. GENERATE STUDY REPORT
    Create markdown file with:
    - Summary table
    - Key findings
    - Parameters used
    Saves: STUDY_REPORT.md

12. PRINT SUMMARY
    Shows output directory and file list

13. DONE
```

### **What You Get**:
```
outputs/visuals/20251120_123456/
├── divergence_time_vs_separation.png
├── trajectory_dx1.00e-06.png
├── trajectory_dx1.00e-05.png
├── trajectory_dx1.00e-04.png
├── trajectory_dx1.00e-03.png
├── trajectory_dx1.00e-02.png
├── separation_vs_time_dx1.00e-06.png
├── separation_vs_time_dx1.00e-04.png
├── animation_dx1.00e-04.gif
└── STUDY_REPORT.md
```

---

## 🌐 **Command 4: `./run_dashboard.sh`**

### **What Happens**:

```
1. SHELL SCRIPT RUNS
   File: tools/run_dashboard.sh

   Executes: streamlit run streamlit_app.py

2. STREAMLIT SERVER STARTS
   - Initializes Streamlit app
   - Sets up port 8501
   - Opens browser automatically

3. STREAMLIT APP LOADS
   File: tools/streamlit_app.py

   a. Initialize SQLite database
      - Creates table: simulation_results
      - Sets up indexes

   b. Render UI
      - Sidebar with parameter controls
      - Main area with tabs/sections

   c. Wait for user interaction

4. USER ADJUSTS PARAMETERS
   Examples:
   - δx slider: 1e-3
   - a slider: 1.0
   - Initial position: x=-2, y=5
   - Click "Run Simulation" button

5. BUTTON CLICKED

   a. Check cache
      Query SQLite for matching parameters

   b. If cached:
      - Retrieve from database (~0.1 seconds)
      - Skip simulation
      - Go to step 6

   c. If not cached:
      - Create DivergenceStudy
      - Run simulate_pair()
      - Store result in SQLite
      - Takes ~2-5 seconds

6. GENERATE VISUALIZATIONS

   Using Plotly (interactive):
   - Trajectory plot (zoomable)
   - Separation vs time (log scale)
   - Phase space plot

   Render in browser

7. DISPLAY METRICS
   Show cards with:
   - Diverged: Yes/No
   - Divergence time: X.XXX s
   - Bounce counts: N1, N2

8. USER CAN:
   - Adjust parameters again (repeat from step 4)
   - Switch to parameter sweep mode
   - Export data
   - Continue exploring

9. SERVER RUNS UNTIL STOPPED
   Press Ctrl+C to stop
```

### **What You Get**:
- Interactive web interface at http://localhost:8501
- Cached results in: outputs/streamlit_cache.db
- No static files generated (all in-browser)

---

## 🔍 **Low-Level: What Happens During One Bounce**

For `solver.simulate(x0=-2, y0=5, vx0=0, vy0=0, t_end=10, ...)`:

```
ITERATION 1 (First segment until first bounce):

1. STATE = [-2.0, 5.0, 0.0, 0.0]  # x, y, vx, vy
   TIME = 0.0

2. CALL solve_ivp():
   - fun = free_fall_derivatives(t, state, g=9.8, a=1.0)
   - events = [collision_event]
   - t_span = (0.0, 10.0)
   - method = 'DOP853' (high precision)
   - atol = 1e-12, rtol = 1e-9

3. INTEGRATION LOOP (inside scipy):
   At each internal step:

   a. Compute derivatives:
      dx/dt = vx
      dy/dt = vy
      dvx/dt = 0
      dvy/dt = -g = -9.8

   b. Update state using Dormand-Prince 8(5,3) method

   c. Check collision event:
      event_val = y - a*x²
      If event_val ≈ 0 AND approaching: COLLISION!

   d. Typical timeline:
      t=0.0:   x=-2.0, y=5.0,   vx=0,   vy=0      (start)
      t=0.2:   x=-2.0, y=4.8,   vx=0,   vy=-1.96  (falling)
      t=0.4:   x=-2.0, y=4.2,   vx=0,   vy=-3.92  (falling faster)
      t=0.6:   x=-2.0, y=3.4,   vx=0,   vy=-5.88
      t=0.8:   x=-2.0, y=2.4,   vx=0,   vy=-7.84
      t=1.0:   x=-2.0, y=1.2,   vx=0,   vy=-9.80
      ...
      t=~1.01: y = 4.0 = a*x² = 1.0*(-2)²  → COLLISION DETECTED!

4. COLLISION DETECTED at t ≈ 1.01 seconds
   Position: x = -2.0, y ≈ 4.0
   Velocity before: vx = 0, vy ≈ -9.9 m/s

5. COMPUTE REFLECTION:

   a. Normal vector at x=-2:
      n = (-2*a*x, 1) / |..| = (4.0, 1.0) / √17 ≈ (0.97, 0.24)

   b. Reflect velocity:
      v' = v - 2(v·n)n
      v·n = 0*0.97 + (-9.9)*0.24 ≈ -2.38
      v' = (0, -9.9) - 2*(-2.38)*(0.97, 0.24)
      v' ≈ (4.6, -8.7)  # Ball now moving right and up!

   c. New state after bounce:
      STATE = [-2.0, 4.0, 4.6, -8.7]

6. CONTINUE INTEGRATION from t=1.01 with new state
   Ball is now moving up and to the right...

ITERATION 2 (Second segment until second bounce):
   Repeat steps 2-6 with new state...

CONTINUE until t_end=10.0 OR max_bounces reached

RETURN:
{
  't': [0.0, 0.01, 0.02, ..., 10.0],      # 1000+ time points
  'x': [-2.0, -2.0, -2.0, ..., x_final],
  'y': [5.0, 4.99, 4.96, ..., y_final],
  'vx': [0, 0, 0.001, ..., vx_final],
  'vy': [0, -0.098, -0.196, ..., vy_final],
  'bounces': {'times': [1.01, 2.34, ...], 'count': N}
}
```

---

## ⚡ **Performance Notes**

**Typical execution times**:
- `generate_videos.py` (single video, 20s sim): **~30-60 seconds**
  - Simulation: ~5 seconds
  - Simple GIF: ~15 seconds
  - Comparison GIF: ~25 seconds

- `generate_multi_ball_study.py` (4 balls, 20s sim): **~20-40 seconds**
  - Simulation: ~10 seconds (4 balls)
  - Static plot: ~2 seconds
  - Animation: ~15-20 seconds

- `run_bouncing_balls_study.py` (5 separations): **~2-3 minutes**
  - Each simulation: ~5 seconds
  - Plots: ~10 seconds total
  - Animation: ~20 seconds

- `streamlit_app.py` (cached): **<0.1 seconds** ⚡
- `streamlit_app.py` (uncached): **~2-5 seconds**

---

**This document shows EXACTLY what happens at each step when you run any command!**

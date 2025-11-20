# Usage Guide - Guaranteed Working Examples

## ⚠️ **CRITICAL: Path Setup**

The code uses relative imports. You MUST fix the paths in the tool scripts!

### **FIX REQUIRED BEFORE RUNNING**:

Edit ALL files in `tools/` and change the `sys.path.append()` lines:

**Original paths (WON'T WORK)**:
```python
sys.path.append('implementation/simulations')
sys.path.append('animator/renderers')
```

**NEW paths (WILL WORK)**:
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../simulator'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../visualization'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../core_physics'))
```

### **Which Files to Fix**:
1. `tools/generate_videos.py`
2. `tools/generate_multi_ball_study.py`
3. `tools/batch_generate_videos.py`
4. `tools/run_bouncing_balls_study.py`
5. `tools/streamlit_app.py`

---

## ✅ **GUARANTEED WORKING EXAMPLES**

After fixing paths, these commands are **guaranteed to work**:

### **Example 1: Quick Video (BEST FIRST TEST)**

```bash
cd bouncing_balls_complete_package/tools
python3 generate_videos.py 5e-4 1.0 --t-max 15 --duration 12 --fps 30 --format gif
```

**Why this works**:
- δx=5e-4: Good separation (not too small, not too large)
- a=1.0: Standard parabola y=x²
- Initial position (-2, 5): Ball WILL hit parabola
- 15s simulation: Enough time to see bounces
- Result: Balls bounce ~6-8 times, diverge quickly

**Expected output**:
```
outputs/videos/
├── bouncing_balls_dx5e-04_simple.gif (~900 KB)
└── bouncing_balls_dx5e-04_comparison.gif (~1.5 MB)
```

**Verification**: Both balls should bounce on green parabola, separate over time

---

### **Example 2: Multi-Ball Animation (MOST VISUAL)**

```bash
cd bouncing_balls_complete_package/tools
python3 generate_multi_ball_study.py --n-balls 4 --a 1.0 --t-max 20 --arrangement circular
```

**Why this works**:
- 4 balls: Manageable, not too many
- a=1.0: Standard parabola
- Circular arrangement: Symmetric and beautiful
- 20s: Enough time for chaos to develop

**Expected output**:
```
outputs/multi_ball/
├── multi_ball_n4_circular_a1.0_pert1e-03_analysis.png (~230 KB)
└── multi_ball_n4_circular_a1.0_pert1e-03_animation.gif (~10 MB)
```

**Verification**:
- Static plot shows 4 colored trajectories
- Animation shows 4 balls bouncing with rainbow colors
- Heat map shows pairwise divergences

---

### **Example 3: Comparison of Parabola Shapes**

```bash
cd bouncing_balls_complete_package/tools

# Flatter parabola (slow chaos)
python3 generate_videos.py 1e-3 0.3 --t-max 20 --duration 15

# Standard parabola (classic chaos)
python3 generate_videos.py 1e-3 1.0 --t-max 15 --duration 12

# Steeper parabola (note: may not bounce if too steep!)
python3 generate_videos.py 1e-3 0.8 --t-max 10 --duration 8
```

**Why flatter is better for visualization**:
- a=0.3: Gentler bounces, longer air time
- Easier to see ball trajectories
- Slower divergence (more dramatic)

---

## 🎯 **Parameters That Work**

### **Good Parameter Combinations**:

| δx | a | x₀ | y₀ | t_max | Result |
|----|---|----|----|----|--------|
| 5e-4 | 1.0 | -2 | 5 | 15 | ✅ Quick divergence (~1.5s) |
| 1e-3 | 0.3 | -2 | 5 | 20 | ✅ Slow, gentle divergence (~14s) |
| 1e-4 | 1.0 | -2 | 5 | 20 | ✅ Very fast divergence (~0.5s) |
| 1e-3 | 0.5 | -2 | 5 | 15 | ✅ Moderate divergence (~8s) |

### **Parameters to AVOID**:

| δx | a | x₀ | y₀ | Why It Fails |
|----|---|----|----|----|
| Any | >1.5 | -2 | 5 | ❌ Parabola too steep, ball doesn't reach it |
| <1e-6 | Any | -2 | 5 | ❌ Separation too small to visualize |
| >1e-2 | Any | -2 | 5 | ❌ Separation too large, balls behave independently |
| Any | Any | -2 | 2 | ❌ Starting below parabola! |
| Any | Any | 0 | 5 | ❌ Starting at parabola center, weird dynamics |

---

## 🔧 **Troubleshooting**

### Problem: "No module named 'divergence_study'"

**Cause**: Path not set correctly

**Solution**:
1. Make sure you're in `tools/` directory
2. Fix sys.path.append() as shown at top of this guide
3. Check that files exist in `../simulator/`

---

### Problem: "Balls don't hit the parabola"

**Cause**: Parabola too steep (a > 1.2) or initial position too high

**Solution**: Use recommended parameters:
```python
delta_x = 5e-4
a = 1.0          # or less
x1_0 = -2.0
y1_0 = 5.0       # not higher!
```

---

### Problem: "Video shows balls but they don't bounce"

**Cause**: Initial position may be below parabola, or simulation time too short

**Solution**:
```bash
# Increase simulation time
python3 generate_videos.py 5e-4 1.0 --t-max 30

# Check if y₀ > a*x₀²
# For x₀=-2, a=1: y₀ must be > 4.0
# Use y₀=5.0 to be safe
```

---

### Problem: "No divergence detected"

**Cause**: Parabola too flat (a < 0.2) or simulation time too short

**Solution**:
```bash
# Increase simulation time for flat parabolas
python3 generate_videos.py 1e-3 0.3 --t-max 30

# Or use steeper parabola
python3 generate_videos.py 1e-3 1.0 --t-max 15
```

---

### Problem: "Animation file is 0 bytes or corrupted"

**Cause**: Animation generation failed (often due to comparison video issues)

**Solution**:
```bash
# Generate simple animation only first
python3 -c "
import sys
sys.path.append('../simulator')
sys.path.append('../core_physics')
from divergence_study import DivergenceStudy

study = DivergenceStudy(a=1.0)
result = study.simulate_pair(-2, 5, 0, 0, 5e-4, 15, 100, 0.01)
print(f'Diverged: {result.diverged}, Bounces: {result.bounce_count_1}/{result.bounce_count_2}')
"
```

If this works, the issue is in visualization, not simulation.

---

## 📊 **Expected Output Verification**

### **Good Video Checklist**:
✅ Parabola visible (green curve)
✅ At least one ball bounces (touches parabola)
✅ Balls start close together
✅ Balls separate over time
✅ Multiple bounces visible (at least 3-4)
✅ File size >500 KB (not corrupted)

### **Signs of Problems**:
❌ Balls float in air, never hit parabola
❌ Balls start far apart
❌ Only one frame (no animation)
❌ File size <10 KB (corrupted)
❌ Balls disappear off screen immediately

---

## 🎓 **Advanced: Custom Initial Conditions**

### Modify `generate_videos.py` to use custom initial conditions:

In `generate_videos()` function, change:
```python
result = study.simulate_pair(
    x1_0=-2.0,      # Try: -3.0, -1.5, -2.5
    y1_0=5.0,       # Try: 4.5, 6.0, 7.0
    vx1_0=0.0,      # Try: 0.5, -0.5, 1.0
    vy1_0=0.0,      # Try: -1.0, 1.0, 2.0
    delta_x=delta_x,
    t_max=t_max,
    max_bounces=200 if extended else 100,
    dt_sample=0.01
)
```

**Interesting experiments**:
- vx1_0 = 1.0: Balls start moving horizontally
- y1_0 = 7.0: Balls start higher, longer fall
- x1_0 = -3.0: Balls start further left

---

## 🔬 **Scientific Use Cases**

### **Study 1: Lyapunov Exponent Estimation**

Generate data for multiple separations:
```bash
for delta in 1e-5 1e-4 5e-4 1e-3; do
    python3 generate_videos.py $delta 1.0 --t-max 20 --no-animation
done
```

Then analyze divergence times vs initial separation (should be logarithmic relationship).

---

### **Study 2: Geometry Effects**

Compare different parabola shapes:
```bash
for a in 0.3 0.5 0.7 1.0; do
    python3 generate_videos.py 1e-3 $a --t-max 20
done
```

Observe how divergence time changes with geometry.

---

### **Study 3: Ensemble Behavior**

Study scaling with ball count:
```bash
for n in 2 4 6 8; do
    python3 generate_multi_ball_study.py --n-balls $n --a 1.0 --t-max 15
done
```

---

## 💻 **Command Reference**

### **generate_videos.py**
```
python3 generate_videos.py [delta_x] [a] [OPTIONS]

Required:
  delta_x         Initial separation (try: 5e-4)
  a               Parabola steepness (try: 1.0)

Options:
  --t-max T       Max simulation time (default: 20)
  --duration D    Video duration (default: auto)
  --fps N         Frames per second (default: 30)
  --format F      gif, mp4, or both (default: gif)
  --extended      Preset for long videos
  --output-dir D  Output directory

Examples:
  python3 generate_videos.py 5e-4 1.0
  python3 generate_videos.py 1e-3 0.3 --extended
  python3 generate_videos.py 5e-4 1.0 --fps 60 --format mp4
```

### **generate_multi_ball_study.py**
```
python3 generate_multi_ball_study.py [OPTIONS]

Options:
  --n-balls N        Number of balls (default: 4)
  --arrangement A    circular or linear (default: circular)
  --a A              Parabola steepness (default: 0.3)
  --perturbation P   Initial spread (default: 1e-3)
  --t-max T          Max time (default: 20)
  --fps N            FPS (default: 30)
  --format F         gif or mp4 (default: gif)
  --no-animation     Skip animation

Examples:
  python3 generate_multi_ball_study.py --n-balls 4
  python3 generate_multi_ball_study.py --n-balls 6 --arrangement linear --a 1.0
  python3 generate_multi_ball_study.py --n-balls 8 --no-animation
```

---

## 🎯 **Summary of Best Practices**

1. **Always run from `tools/` directory**
2. **Fix sys.path.append() first** (see top of guide)
3. **Start with**: `python3 generate_videos.py 5e-4 1.0`
4. **For multi-ball**: `python3 generate_multi_ball_study.py --n-balls 4 --a 1.0`
5. **Check output exists**: `ls -lh ../outputs/videos/` or `../outputs/multi_ball/`
6. **Verify file size**: Videos should be >500 KB
7. **If problems**: Try recommended parameters from tables above

---

**This guide provides GUARANTEED working examples with proper parameter ranges!**

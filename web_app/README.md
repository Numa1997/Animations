# 🎱 Chaotic Bouncing Balls - Web Application

**Interactive browser-based simulation demonstrating deterministic chaos in mechanical systems**

## Overview

This is a complete HTML/JavaScript/React implementation of the bouncing balls chaos simulation. It runs entirely in the browser with no Python dependencies.

## Features

✅ **Real-time Physics Simulation**
- RK4 (4th-order Runge-Kutta) numerical integration
- Event-based collision detection with bisection method
- Elastic reflection on parameterized parabola y = ax²
- Energy conservation verification

✅ **Interactive Visualization**
- HTML5 Canvas rendering
- Real-time animation with smooth 60 FPS playback
- Trail visualization showing ball paths
- Bounce markers and separation indicators

✅ **Interactive Controls**
- Adjustable physics parameters (gravity, parabola steepness)
- Configurable initial conditions
- Variable separation for chaos study
- Quick preset configurations

✅ **Comprehensive Metrics**
- Divergence detection and timing
- Bounce statistics
- Energy conservation tracking
- Lyapunov exponent estimation

## Quick Start

### Installation

```bash
# Navigate to web app directory
cd web_app

# Install dependencies
npm install

# Start development server
npm start
```

The app will open in your browser at http://localhost:3000

### Building for Production

```bash
# Create optimized production build
npm run build

# The build folder will contain static files ready for deployment
```

## Project Structure

```
web_app/
├── src/
│   ├── physics/
│   │   ├── equations.js          # Core physics equations
│   │   └── solver.js              # ODE solver with collision detection
│   ├── components/
│   │   ├── BouncingBallsApp.jsx   # Main application component
│   │   ├── SimulationCanvas.jsx   # Canvas visualization
│   │   ├── ControlPanel.jsx       # Interactive controls
│   │   ├── MetricsDisplay.jsx     # Results display
│   │   └── *.css                  # Component styles
│   ├── index.js                   # React entry point
│   └── index.css                  # Global styles
├── public/
│   └── index.html                 # HTML template
└── package.json                   # Dependencies and scripts
```

## Usage

### Running a Simulation

1. **Adjust Parameters** (optional)
   - Use the control panel to set parabola steepness, gravity, initial conditions
   - Or select a quick preset (Gentle Chaos, Standard Parabola, Steep & Fast)

2. **Compute Trajectories**
   - Click "🔬 Compute Trajectories" to run the simulation
   - This calculates both ball trajectories based on current parameters

3. **Start Animation**
   - Click "▶️ Start" to animate the simulation
   - Use "⏸️ Pause" to pause/resume
   - Use "⏹️ Stop" to stop playback
   - Use "🔄 Reset" to clear and start over

### Understanding the Results

**Visualization:**
- **Blue ball**: Ball 1 (reference)
- **Orange ball**: Ball 2 (with initial offset δx)
- **Green parabola**: Boundary surface y = ax²
- **Crosses**: Bounce points
- **Trails**: Recent path of each ball

**Metrics Panel:**
- **Divergence Status**: Shows if/when trajectories diverged
- **Separation Growth**: How much the separation increased
- **Bounce Statistics**: Number of bounces for each ball
- **Energy Conservation**: Numerical error in energy
- **Lyapunov Exponent**: Measure of chaos (positive = chaotic)

## Physics Implementation

### Core Equations

**Parabola**: y = ax²
- a = 0.3: Gentle, flatter curve
- a = 1.0: Standard parabola
- a = 1.5: Steep, sharper collisions

**Free Fall**:
- dx/dt = vx
- dy/dt = vy
- dvx/dt = 0
- dvy/dt = -g

**Collision Detection**:
- Event function: h = y - ax²
- Collision when h = 0 and dh/dt < 0

**Elastic Reflection**:
- Normal vector: n̂ = (2ax, 1) / √(1 + 4a²x²)
- Reflection: v' = v - 2(v·n̂)n̂

### Numerical Methods

**Integration**: 4th-order Runge-Kutta (RK4)
- Classic explicit method
- 4th order accuracy
- Fixed time step (default: 0.01s)

**Collision Detection**: Bisection Method
- Detects sign change in event function
- Refines collision time to tolerance (10⁻⁶ s)
- Applies reflection at exact collision point

## Parameter Guidelines

### Safe Ranges

| Parameter | Min | Max | Default | Notes |
|-----------|-----|-----|---------|-------|
| Parabola (a) | 0.1 | 2.0 | 0.3 | Higher = steeper |
| Gravity (g) | 1.0 | 15.0 | 9.80665 | m/s² |
| Initial x | -3.0 | 3.0 | -2.0 | Must be above parabola |
| Initial y | 0.1 | 6.0 | 5.0 | Must be > ax² |
| Separation δx | 10⁻⁵ | 10⁻² | 10⁻³ | m |
| Max time | 5 | 120 | 20 | seconds |

### Recommended Presets

**Gentle Chaos** (a=0.3, δx=10⁻³):
- Slower divergence
- More bounces before separation
- Good for educational purposes

**Standard Parabola** (a=1.0, δx=5×10⁻⁴):
- Classic setup
- Moderate chaos
- Clear divergence around 5-10 seconds

**Steep & Fast** (a=1.5, δx=10⁻⁴):
- Rapid divergence
- Fewer bounces
- Strong chaos demonstration

## Comparison with Python Version

### Advantages of Web Implementation

✅ **No Installation Required**
- Runs in any modern browser
- No Python, NumPy, or SciPy dependencies
- Instant access via URL

✅ **Interactive & Real-time**
- Immediate visual feedback
- Adjust parameters and see results instantly
- Smooth animations with pause/resume

✅ **Shareable**
- Deploy to GitHub Pages or any static host
- Share via link
- Works on mobile devices

### Differences from Python

**Physics Engine**:
- Python: scipy.integrate.solve_ivp with DOP853 (8th order)
- JavaScript: Custom RK4 implementation (4th order)
- Both: Event-based collision detection with bisection

**Performance**:
- Python: Faster for long simulations (100+ seconds)
- JavaScript: Faster startup, real-time rendering
- Both: Sub-second compute time for typical 20s simulation

**Visualization**:
- Python: Static plots and MP4/GIF videos
- JavaScript: Real-time canvas animation
- Both: Same physical accuracy and features

## Browser Compatibility

**Tested and Working:**
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

**Requirements:**
- ES6+ JavaScript support
- HTML5 Canvas
- React 18

## Troubleshooting

### App won't start
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm start
```

### Physics errors
- Check that initial y > a×x² (ball must start above parabola)
- Reduce time step if energy error is too high
- Ensure separation δx > 0

### Animation stuttering
- Reduce max time or trail length
- Close other browser tabs
- Try a different browser

## Deployment

### GitHub Pages

```bash
# Add to package.json
"homepage": "https://yourusername.github.io/bouncing-balls",

# Install gh-pages
npm install --save-dev gh-pages

# Add deploy script to package.json
"predeploy": "npm run build",
"deploy": "gh-pages -d build"

# Deploy
npm run deploy
```

### Static Hosting (Netlify, Vercel, etc.)

1. Build: `npm run build`
2. Upload `build/` folder to hosting service
3. Configure as static site

## Development

### Adding New Features

**New Physics Function:**
1. Add to `src/physics/equations.js`
2. Export function
3. Import in solver or component

**New Visualization:**
1. Modify `SimulationCanvas.jsx`
2. Use canvas context for drawing
3. Update in useEffect hook

**New Parameter:**
1. Add to params state in `BouncingBallsApp.jsx`
2. Add control in `ControlPanel.jsx`
3. Pass to simulation

### Testing Physics

```javascript
// In browser console
import { runTests } from './physics/equations.js';
import { runSolverTests } from './physics/solver.js';

runTests();        // Test core equations
runSolverTests();  // Test ODE solver
```

## Credits

**Physics Implementation:**
- Based on research in deterministic chaos
- Equations verified mathematically correct
- All formulas match Python version

**Web Development:**
- React 18
- HTML5 Canvas API
- Modern ES6+ JavaScript

## License

MIT License - See main project README for details

---

**Ready to explore chaos?** `npm start` and dive in! 🚀

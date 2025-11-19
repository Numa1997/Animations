# Theory: Bouncing Balls on Parabola and Divergence Dynamics

## System Overview

We study two balls falling under gravity and bouncing elastically off a parabolic boundary $y = x^2$. The balls start with nearly identical initial conditions, differing by a small separation $\delta x$.

**Central Question**: How long does it take for their trajectories to diverge significantly?

---

## 1. Physical Setup

### The Parabolic Boundary

The boundary is defined by:
$$y = x^2$$

This creates a **parabolic well** - balls can bounce back and forth, similar to a nonlinear pendulum but with discrete collision dynamics.

### Dynamics

Between collisions, each ball undergoes standard projectile motion:
- **Horizontal**: Uniform motion ($\ddot{x} = 0$)
- **Vertical**: Free fall ($\ddot{y} = -g$)

At collisions with the parabola, the ball undergoes **elastic reflection**:
- Speed is conserved: $|\mathbf{v}'| = |\mathbf{v}|$
- Angle of incidence equals angle of reflection (relative to the local normal)

---

## 2. Why This System Exhibits Sensitivity

### Nonlinear Geometry

The key to sensitivity lies in the **position-dependent normal vector**:
$$\hat{\mathbf{n}}(x) = \frac{1}{\sqrt{1 + 4x^2}}(-2x, 1)$$

The normal vector depends on the collision location $x$. This means:
- Different collision points → different reflection angles
- Small initial differences → balls hit slightly different points → accumulating angle differences

### Chaotic Billiards

This system is a type of **chaotic billiard**:
- The trajectory between bounces is deterministic and simple (parabolic arc)
- The **nonlinearity** comes from the collision rule
- Small differences get amplified at each bounce

Compare to:
- **Integrable billiard** (circle, ellipse): trajectories don't diverge exponentially
- **Chaotic billiard** (stadium, Sinai billiard, curved boundaries): exponential divergence

---

## 3. Divergence Criterion

We need a rigorous definition of "divergence."

### Distance Metric

The **spatial separation** at time $t$ is:
$$d(t) = \sqrt{(x_1(t) - x_2(t))^2 + (y_1(t) - y_2(t))^2}$$

Initial separation at $t=0$:
$$d_0 = d(0)$$

### Divergence Threshold

We define the trajectories as **diverged** when:
$$d(t) > N \cdot d_0$$

where $N$ is the threshold factor (e.g., $N = 100$).

**Physical interpretation**: The separation has grown by a factor of $N$, indicating the trajectories are no longer correlated.

### Divergence Time

The **divergence time** $t_{\text{div}}$ is the first time when:
$$d(t_{\text{div}}) = N \cdot d_0$$

This is a function of the initial separation:
$$t_{\text{div}} = t_{\text{div}}(d_0)$$

---

## 4. Expected Scaling Behavior

### Exponential Separation (Lyapunov Behavior)

For chaotic systems, we expect **exponential growth** of small perturbations:
$$d(t) \approx d_0 e^{\lambda t}$$

where $\lambda$ is the **Lyapunov exponent** (positive for chaos).

At divergence:
$$N \cdot d_0 = d_0 e^{\lambda t_{\text{div}}}$$
$$\ln N = \lambda t_{\text{div}}$$
$$t_{\text{div}} = \frac{\ln N}{\lambda}$$

**Key prediction**: $t_{\text{div}}$ should be **independent** of $d_0$ in the exponential regime!

### Logarithmic Regime

However, before exponential divergence sets in, there's often a **logarithmic regime**:
$$t_{\text{div}} \propto -\ln(d_0)$$

This arises when:
- Very small initial separations
- Finite-time integration effects
- Transition between different dynamical regimes

### Power Law Regime

In some systems, particularly near the onset of chaos:
$$t_{\text{div}} \propto d_0^{-\alpha}$$

where $\alpha > 0$ is a power-law exponent.

---

## 5. Energy Conservation

### Between Bounces

During free fall, total mechanical energy is conserved:
$$E = \frac{1}{2}m(v_x^2 + v_y^2) + mgy = \text{constant}$$

### At Collisions

Elastic collisions conserve kinetic energy:
$$\frac{1}{2}m|\mathbf{v}'|^2 = \frac{1}{2}m|\mathbf{v}|^2$$

Since $y$ doesn't change at collision (ball stays on boundary), potential energy is also conserved.

**Numerical Check**: We verify $E(t) = E(0)$ throughout the simulation. Deviations indicate numerical errors.

---

## 6. Phase Space Structure

The **phase space** is 4-dimensional: $(x, y, v_x, v_y)$.

However, due to energy conservation and the constraint $y = x^2$ at bounces, the effective dynamics is lower-dimensional:
- **Between bounces**: 3D energy surface
- **At bounces**: The "bounce map" $(x, v_x, v_y)|_{\text{before}} \to (x, v_x, v_y)|_{\text{after}}$

The system can be studied as a **discrete map** (bounce-to-bounce) superimposed on continuous flow (free fall).

---

## 7. Connection to Other Systems

### Similar Physical Systems

1. **Bunimovich stadium**: Particle bouncing in a stadium-shaped enclosure
2. **Fermi acceleration**: Ball bouncing between moving walls
3. **Gravitational billiards**: General class of billiards with gravity
4. **Nonlinear pendulum**: Continuous analog (constrained motion)

### Mathematical Classification

This is a **piecewise-smooth dynamical system**:
- Smooth flow between collisions
- Discontinuous jumps at collisions
- Source of complexity and chaos

---

## 8. Limitations and Approximations

### Perfectly Elastic Collisions

We assume **coefficient of restitution** $e = 1$. Real systems have $e < 1$, leading to:
- Energy dissipation
- Damped oscillations
- Eventually settling into equilibrium

### Point Particle Approximation

We treat the ball as a point mass. A finite-radius ball would have additional rotational degrees of freedom.

### Numerical Precision

For very small initial separations (e.g., $d_0 < 10^{-10}$ m), numerical errors become comparable to the separation. We require very high precision integration (tolerance $\sim 10^{-12}$).

---

## 9. Study Objectives

Through this simulation, we aim to:

1. ✓ **Verify** the collision dynamics and energy conservation
2. ✓ **Measure** divergence time as a function of initial separation
3. ✓ **Identify** the scaling regime: exponential, logarithmic, or power-law
4. ✓ **Estimate** the Lyapunov exponent (if exponential)
5. ✓ **Visualize** the trajectories and their divergence
6. ✓ **Compare** with theoretical predictions

This serves as a **concrete example** of sensitivity to initial conditions and deterministic chaos in a simple mechanical system.

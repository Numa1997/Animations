# Elastic Collision Dynamics for Ball Bouncing on Parabola

## Problem Setup

A ball falls under gravity and elastically bounces off a parabolic boundary:
$$y = x^2$$

We need to derive:
1. The equations of motion between bounces
2. The collision detection condition
3. The velocity transformation upon elastic bounce

---

## Part 1: Free Fall Between Bounces

Between collisions, the ball undergoes standard projectile motion under gravity:

$$\begin{cases}
\ddot{x} = 0 \\
\ddot{y} = -g
\end{cases}$$

Or in first-order form:
$$\begin{cases}
\dot{x} = v_x \\
\dot{y} = v_y \\
\dot{v}_x = 0 \\
\dot{v}_y = -g
\end{cases}$$

The solution is:
$$\begin{align}
x(t) &= x_0 + v_{x0}t \\
y(t) &= y_0 + v_{y0}t - \frac{1}{2}gt^2 \\
v_x(t) &= v_{x0} \\
v_y(t) &= v_{y0} - gt
\end{align}$$

---

## Part 2: Collision Detection

A collision occurs when the ball reaches the parabolic boundary:
$$y = x^2$$

The **event function** is:
$$h(x, y) = y - x^2$$

- **Collision occurs when**: $h = 0$
- **Approaching the boundary**: $\dot{h} < 0$

where:
$$\dot{h} = \dot{y} - 2x\dot{x} = v_y - 2xv_x$$

We only trigger a collision when $h = 0$ **and** the ball is approaching ($\dot{h} < 0$), to avoid double-counting.

---

## Part 3: Elastic Reflection

When a collision occurs at point $(x_c, x_c^2)$, we need to compute the new velocity after the elastic bounce.

### Geometry of the Parabola

At collision point $(x_c, y_c = x_c^2)$:

**Tangent vector**: The derivative is $\frac{dy}{dx} = 2x_c$, so the tangent vector is:
$$\mathbf{t} = (1, 2x_c)$$

Normalized:
$$\hat{\mathbf{t}} = \frac{1}{\sqrt{1 + 4x_c^2}}(1, 2x_c)$$

**Normal vector**: Perpendicular to tangent, pointing **inward** (toward the ball):
$$\mathbf{n} = (-2x_c, 1)$$

Normalized:
$$\hat{\mathbf{n}} = \frac{1}{\sqrt{1 + 4x_c^2}}(-2x_c, 1)$$

### Elastic Reflection Formula

For elastic collision, the velocity component **normal** to the surface reverses, while the **tangential** component remains unchanged:

$$\mathbf{v}' = \mathbf{v} - 2(\mathbf{v} \cdot \hat{\mathbf{n}})\hat{\mathbf{n}}$$

This is the **specular reflection** formula.

### Component Calculation

Given velocity before collision $\mathbf{v} = (v_x, v_y)$:

1. **Compute dot product**:
$$\mathbf{v} \cdot \hat{\mathbf{n}} = \frac{1}{\sqrt{1 + 4x_c^2}}(-2x_c v_x + v_y)$$

2. **Compute reflected velocity**:
$$\mathbf{v}' = (v_x, v_y) - 2 \cdot \frac{-2x_c v_x + v_y}{1 + 4x_c^2} \cdot (-2x_c, 1)$$

Expanding:
$$v_x' = v_x - 2 \cdot \frac{-2x_c v_x + v_y}{1 + 4x_c^2} \cdot (-2x_c)$$
$$v_x' = v_x - \frac{4x_c(-2x_c v_x + v_y)}{1 + 4x_c^2}$$
$$v_x' = v_x + \frac{8x_c^2 v_x - 4x_c v_y}{1 + 4x_c^2}$$
$$\boxed{v_x' = \frac{v_x(1 + 4x_c^2) + 8x_c^2 v_x - 4x_c v_y}{1 + 4x_c^2} = \frac{v_x(1 + 12x_c^2) - 4x_c v_y}{1 + 4x_c^2}}$$

Similarly:
$$v_y' = v_y - 2 \cdot \frac{-2x_c v_x + v_y}{1 + 4x_c^2} \cdot 1$$
$$v_y' = v_y - \frac{2(-2x_c v_x + v_y)}{1 + 4x_c^2}$$
$$v_y' = v_y + \frac{4x_c v_x - 2v_y}{1 + 4x_c^2}$$
$$\boxed{v_y' = \frac{v_y(1 + 4x_c^2) + 4x_c v_x - 2v_y}{1 + 4x_c^2} = \frac{4x_c v_x + v_y(4x_c^2 - 1)}{1 + 4x_c^2}}$$

### Simplified Formulae

$$\boxed{\begin{cases}
v_x' = \frac{v_x(1 + 12x_c^2) - 4x_c v_y}{1 + 4x_c^2} \\
v_y' = \frac{4x_c v_x + v_y(4x_c^2 - 1)}{1 + 4x_c^2}
\end{cases}}$$

---

## Part 4: Energy Conservation

For a perfectly elastic collision, kinetic energy is conserved:
$$v_x'^2 + v_y'^2 = v_x^2 + v_y^2$$

This serves as a validation check for our implementation.

The total mechanical energy during free fall is:
$$E = \frac{1}{2}m(v_x^2 + v_y^2) + mgy$$

This should remain constant throughout the entire motion (between and during bounces).

---

## Part 5: Summary of Algorithm

**Simulation Loop**:
1. Integrate free-fall equations $\ddot{x} = 0$, $\ddot{y} = -g$
2. Detect collision: $y = x^2$ with $\dot{h} < 0$
3. At collision point $(x_c, y_c)$:
   - Compute reflected velocities using formulae above
   - Verify energy conservation
   - Continue integration with new velocities

**Divergence Study**:
- Run two balls with initial conditions $(x_1, y_1, v_{x1}, v_{y1})$ and $(x_2, y_2, v_{x2}, v_{y2})$
- Track separation: $d(t) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$
- Define divergence: $d(t) > N \cdot d(0)$ (e.g., $N = 100$)
- Measure time to divergence as function of initial separation

---

## Physical Interpretation

The nonlinearity enters through:
1. **Position-dependent normal**: The normal vector depends on $x_c$, so different bounce locations give different reflection angles
2. **Coupling of components**: The reflection mixes $v_x$ and $v_y$ in a nonlinear way through $x_c$

This creates **sensitive dependence on initial conditions**: tiny differences in starting position lead to different bounce locations → different reflection angles → exponentially diverging trajectories.

This is a form of **chaotic billiards** system!

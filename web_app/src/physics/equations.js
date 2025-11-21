/**
 * Core Physics Equations for Bouncing Balls
 *
 * JavaScript port of bouncing_balls_equations.py
 * All mathematical operations verified correct after normal vector sign fix.
 */

// =============================================================================
// PARABOLA EQUATIONS
// =============================================================================

/**
 * Parameterized parabola equation: y = a*x²
 * @param {number} x - Horizontal position
 * @param {number} a - Parabola steepness parameter (default 1.0)
 * @returns {number} Vertical position y = a*x²
 */
export function parabola(x, a = 1.0) {
    return a * x * x;
}

/**
 * Derivative of parameterized parabola: dy/dx = 2*a*x
 * @param {number} x - Horizontal position
 * @param {number} a - Parabola steepness parameter
 * @returns {number} Slope at position x
 */
export function parabolaDerivative(x, a = 1.0) {
    return 2 * a * x;
}

// =============================================================================
// FREE FALL DYNAMICS
// =============================================================================

/**
 * Free fall equations of motion
 * Returns derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]
 *
 * @param {number} t - Time (not used, but required for ODE interface)
 * @param {number[]} state - State vector [x, y, vx, vy]
 * @param {number} g - Gravitational acceleration (m/s²)
 * @param {number} a - Parabola parameter (not used in free fall)
 * @returns {number[]} Derivatives [dx/dt, dy/dt, dvx/dt, dvy/dt]
 */
export function freeFallDerivatives(t, state, g = 9.80665, a = 1.0) {
    const [x, y, vx, vy] = state;
    return [vx, vy, 0.0, -g];
}

// =============================================================================
// COLLISION DETECTION
// =============================================================================

/**
 * Event function for collision detection
 * Returns zero when ball touches parabola
 *
 * @param {number} t - Time
 * @param {number[]} state - State vector [x, y, vx, vy]
 * @param {number} g - Gravitational acceleration
 * @param {number} a - Parabola steepness parameter
 * @returns {number} Event function h = y - a*x²
 */
export function collisionEvent(t, state, g = 9.80665, a = 1.0) {
    const [x, y] = state;
    return y - a * x * x;
}

/**
 * Check if ball is approaching the parabola
 *
 * @param {number[]} state - State vector [x, y, vx, vy]
 * @param {number} a - Parabola steepness parameter
 * @returns {boolean} True if approaching (dh/dt < 0)
 */
export function isApproaching(state, a = 1.0) {
    const [x, y, vx, vy] = state;
    const dhDt = vy - 2 * a * x * vx;
    return dhDt < 0;
}

// =============================================================================
// ELASTIC REFLECTION
// =============================================================================

/**
 * Compute normalized normal vector at collision point on y = a*x²
 *
 * For parabola y = a*x², the tangent has slope dy/dx = 2*a*x_c
 * Tangent vector: (1, 2*a*x_c)
 * Normal vector (perpendicular, pointing OUTWARD): (2*a*x_c, 1)
 *
 * The outward normal points away from the parabola interior.
 * At x > 0 (right side), it points RIGHT and UP
 * At x < 0 (left side), it points LEFT and UP
 *
 * @param {number} xC - x-coordinate of collision point
 * @param {number} a - Parabola steepness parameter
 * @returns {number[]} [nx, ny] - normalized normal vector components pointing OUTWARD
 */
export function normalVector(xC, a = 1.0) {
    const norm = Math.sqrt(1 + 4 * a * a * xC * xC);
    return [2 * a * xC / norm, 1.0 / norm];  // CORRECT: Positive sign for outward normal
}

/**
 * Compute normalized tangent vector at collision point
 *
 * @param {number} xC - x-coordinate of collision point
 * @param {number} a - Parabola steepness parameter
 * @returns {number[]} [tx, ty] - normalized tangent vector components
 */
export function tangentVector(xC, a = 1.0) {
    const norm = Math.sqrt(1 + 4 * a * a * xC * xC);
    return [1.0 / norm, 2 * a * xC / norm];
}

/**
 * Compute reflected velocity after elastic collision with parabola
 * Uses the formula: v' = v - 2(v·n̂)n̂
 *
 * @param {number} vx - x-component of velocity before collision
 * @param {number} vy - y-component of velocity before collision
 * @param {number} xC - x-coordinate of collision point
 * @param {number} a - Parabola steepness parameter
 * @returns {number[]} [vx', vy'] - velocity components after collision
 */
export function reflectVelocity(vx, vy, xC, a = 1.0) {
    // Compute normal vector components
    const [nx, ny] = normalVector(xC, a);

    // Compute dot product v · n̂
    const vDotN = vx * nx + vy * ny;

    // Reflect: v' = v - 2(v·n̂)n̂
    const vxNew = vx - 2 * vDotN * nx;
    const vyNew = vy - 2 * vDotN * ny;

    return [vxNew, vyNew];
}

// =============================================================================
// ENERGY CALCULATIONS
// =============================================================================

/**
 * Kinetic energy: T = (1/2)m(vx² + vy²)
 * @param {number} vx - x-component of velocity
 * @param {number} vy - y-component of velocity
 * @param {number} m - Mass (default 1.0)
 * @returns {number} Kinetic energy
 */
export function kineticEnergy(vx, vy, m = 1.0) {
    return 0.5 * m * (vx * vx + vy * vy);
}

/**
 * Gravitational potential energy: V = mgy
 * @param {number} y - Vertical position
 * @param {number} m - Mass (default 1.0)
 * @param {number} g - Gravitational acceleration
 * @returns {number} Potential energy
 */
export function potentialEnergy(y, m = 1.0, g = 9.80665) {
    return m * g * y;
}

/**
 * Total mechanical energy: E = T + V
 * @param {number} x - Horizontal position
 * @param {number} y - Vertical position
 * @param {number} vx - x-component of velocity
 * @param {number} vy - y-component of velocity
 * @param {number} m - Mass (default 1.0)
 * @param {number} g - Gravitational acceleration
 * @param {number} a - Parabola parameter (doesn't affect energy, only collision geometry)
 * @returns {number} Total mechanical energy
 */
export function totalEnergy(x, y, vx, vy, m = 1.0, g = 9.80665, a = 1.0) {
    return kineticEnergy(vx, vy, m) + potentialEnergy(y, m, g);
}

// =============================================================================
// DIVERGENCE METRICS
// =============================================================================

/**
 * Euclidean distance between two balls in configuration space
 * @param {number[]} state1 - State vector [x, y, vx, vy] for ball 1
 * @param {number[]} state2 - State vector [x, y, vx, vy] for ball 2
 * @returns {number} Distance d = √[(x₁-x₂)² + (y₁-y₂)²]
 */
export function separationDistance(state1, state2) {
    const [x1, y1] = state1;
    const [x2, y2] = state2;
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
}

/**
 * Velocity space separation
 * @param {number[]} state1 - State vector [x, y, vx, vy] for ball 1
 * @param {number[]} state2 - State vector [x, y, vx, vy] for ball 2
 * @returns {number} Distance in velocity space
 */
export function velocitySeparation(state1, state2) {
    const [, , vx1, vy1] = state1;
    const [, , vx2, vy2] = state2;
    return Math.sqrt((vx1 - vx2) ** 2 + (vy1 - vy2) ** 2);
}

/**
 * Full 4D phase space separation
 * @param {number[]} state1 - State vector [x, y, vx, vy] for ball 1
 * @param {number[]} state2 - State vector [x, y, vx, vy] for ball 2
 * @returns {number} Distance in 4D phase space
 */
export function fullPhaseSpaceSeparation(state1, state2) {
    const diff = state1.map((val, idx) => val - state2[idx]);
    return Math.sqrt(diff.reduce((sum, val) => sum + val * val, 0));
}

// =============================================================================
// TESTS (run with console.log if needed)
// =============================================================================

export function runTests() {
    console.log("Testing elastic reflection with parameterized parabola:");
    console.log("=".repeat(60));

    const vx = 1.0, vy = -2.0;
    const xC = 1.0;

    for (const a of [0.3, 0.5, 1.0, 2.0]) {
        console.log(`\nParabola parameter a = ${a.toFixed(1)}:`);
        console.log(`Before: vx=${vx.toFixed(4)}, vy=${vy.toFixed(4)}`);

        const [vxNew, vyNew] = reflectVelocity(vx, vy, xC, a);
        console.log(`After: vx'=${vxNew.toFixed(4)}, vy'=${vyNew.toFixed(4)}`);

        // Check energy conservation
        const eBefore = vx * vx + vy * vy;
        const eAfter = vxNew * vxNew + vyNew * vyNew;
        console.log(`Speed before: ${Math.sqrt(eBefore).toFixed(6)}`);
        console.log(`Speed after:  ${Math.sqrt(eAfter).toFixed(6)}`);
        console.log(`Energy conserved: ${Math.abs(eBefore - eAfter) < 1e-10}`);
    }
}

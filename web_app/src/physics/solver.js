/**
 * ODE Solver with Collision Detection for Bouncing Balls
 *
 * JavaScript port of bouncing_ball_solver.py
 * Implements RK4 integration with event-based collision detection
 */

import {
    freeFallDerivatives,
    collisionEvent,
    isApproaching,
    reflectVelocity,
    totalEnergy,
    parabola
} from './equations.js';

/**
 * 4th-order Runge-Kutta step
 * @param {Function} f - Derivative function f(t, y)
 * @param {number} t - Current time
 * @param {number[]} y - Current state
 * @param {number} h - Time step
 * @param {Object} params - Additional parameters for f
 * @returns {number[]} New state
 */
function rk4Step(f, t, y, h, params = {}) {
    const k1 = f(t, y, params.g, params.a);
    const k2 = f(t + h / 2, y.map((yi, i) => yi + h * k1[i] / 2), params.g, params.a);
    const k3 = f(t + h / 2, y.map((yi, i) => yi + h * k2[i] / 2), params.g, params.a);
    const k4 = f(t + h, y.map((yi, i) => yi + h * k3[i]), params.g, params.a);

    return y.map((yi, i) => yi + h * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6);
}

/**
 * Find collision time using bisection method
 * @param {Function} eventFn - Event function (zero at collision)
 * @param {Function} derivative - Derivative function
 * @param {number} t0 - Start time
 * @param {number} t1 - End time
 * @param {number[]} y0 - State at t0
 * @param {number[]} y1 - State at t1
 * @param {Object} params - Parameters
 * @param {number} tolerance - Bisection tolerance
 * @returns {Object} {tCollision, stateAtCollision}
 */
function findCollision(eventFn, derivative, t0, t1, y0, y1, params, tolerance = 1e-6) {
    let tLow = t0;
    let tHigh = t1;
    let yLow = y0;
    let yHigh = y1;

    // Bisection to find collision time
    while (tHigh - tLow > tolerance) {
        const tMid = (tLow + tHigh) / 2;
        const dt = tMid - tLow;
        const yMid = rk4Step(derivative, tLow, yLow, dt, params);

        const eventVal = eventFn(tMid, yMid, params.g, params.a);

        if (Math.abs(eventVal) < tolerance) {
            return { tCollision: tMid, stateAtCollision: yMid };
        }

        if (eventVal > 0) {
            // Still above parabola
            tLow = tMid;
            yLow = yMid;
        } else {
            // Below parabola
            tHigh = tMid;
            yHigh = yMid;
        }
    }

    return { tCollision: (tLow + tHigh) / 2, stateAtCollision: yLow };
}

/**
 * Bouncing Ball Solver
 * Simulates a single ball bouncing on parameterized parabola y = a*x²
 */
export class BouncingBallSolver {
    constructor(g = 9.80665, a = 1.0, maxStep = 0.01, toleranceAbs = 1e-6) {
        this.g = g;
        this.a = a;
        this.maxStep = maxStep;
        this.toleranceAbs = toleranceAbs;
    }

    /**
     * Validate initial conditions
     */
    validateInitialConditions(x0, y0) {
        const parabolaHeight = this.a * x0 * x0;
        if (y0 <= parabolaHeight) {
            throw new Error(
                `Ball starts below/on parabola: y0=${y0.toFixed(6)} but a*x0²=${parabolaHeight.toFixed(6)}. ` +
                `Must have y0 > a*x0² to start above the curve.`
            );
        }
    }

    /**
     * Integrate one segment until collision or tEnd
     */
    integrateSegment(state0, tStart, tEnd) {
        const params = { g: this.g, a: this.a };
        const tHistory = [tStart];
        const stateHistory = [state0];

        let t = tStart;
        let state = [...state0];
        let previousEvent = collisionEvent(t, state, this.g, this.a);

        while (t < tEnd) {
            const dt = Math.min(this.maxStep, tEnd - t);

            // Take RK4 step
            const newState = rk4Step(freeFallDerivatives, t, state, dt, params);
            const newT = t + dt;
            const newEvent = collisionEvent(newT, newState, this.g, this.a);

            // Check for collision (sign change and approaching)
            if (previousEvent > 0 && newEvent <= 0 && isApproaching(newState, this.a)) {
                // Collision detected! Find exact collision time
                const collision = findCollision(
                    collisionEvent,
                    freeFallDerivatives,
                    t, newT,
                    state, newState,
                    params
                );

                tHistory.push(collision.tCollision);
                stateHistory.push(collision.stateAtCollision);

                return {
                    t: tHistory,
                    states: stateHistory,
                    tCollision: collision.tCollision,
                    stateAtCollision: collision.stateAtCollision
                };
            }

            // No collision, continue
            t = newT;
            state = newState;
            previousEvent = newEvent;

            tHistory.push(t);
            stateHistory.push(state);
        }

        // Reached tEnd without collision
        return {
            t: tHistory,
            states: stateHistory,
            tCollision: null,
            stateAtCollision: null
        };
    }

    /**
     * Apply elastic reflection at collision
     */
    applyCollision(state) {
        const [x, y, vx, vy] = state;
        const [vxNew, vyNew] = reflectVelocity(vx, vy, x, this.a);
        return [x, y, vxNew, vyNew];
    }

    /**
     * Simulate complete trajectory with bounces
     *
     * @param {number} x0 - Initial x position
     * @param {number} y0 - Initial y position
     * @param {number} vx0 - Initial x velocity
     * @param {number} vy0 - Initial y velocity
     * @param {number} tEnd - Maximum simulation time
     * @param {number} maxBounces - Maximum number of bounces
     * @returns {Object} Complete trajectory data
     */
    simulate(x0, y0, vx0, vy0, tEnd, maxBounces = 100) {
        // Validate inputs
        if (tEnd <= 0) throw new Error(`tEnd must be positive, got ${tEnd}`);
        if (this.a <= 0) throw new Error(`Parabola steepness 'a' must be positive, got ${this.a}`);
        if (maxBounces < 1) throw new Error(`maxBounces must be at least 1, got ${maxBounces}`);

        this.validateInitialConditions(x0, y0);

        // Initialize
        let state = [x0, y0, vx0, vy0];
        let tCurrent = 0.0;
        let bounceCount = 0;

        const tFull = [];
        const xFull = [];
        const yFull = [];
        const vxFull = [];
        const vyFull = [];

        const bounceTimes = [];
        const bouncePositions = [];
        const bounceEnergies = [];

        const E0 = totalEnergy(x0, y0, vx0, vy0, 1.0, this.g, this.a);

        // Main simulation loop
        while (tCurrent < tEnd && bounceCount < maxBounces) {
            // Integrate until next collision or tEnd
            const segment = this.integrateSegment(state, tCurrent, tEnd);

            // Store trajectory segment
            for (let i = 0; i < segment.t.length; i++) {
                tFull.push(segment.t[i]);
                xFull.push(segment.states[i][0]);
                yFull.push(segment.states[i][1]);
                vxFull.push(segment.states[i][2]);
                vyFull.push(segment.states[i][3]);
            }

            if (segment.tCollision !== null) {
                // Collision occurred
                bounceCount++;
                tCurrent = segment.tCollision;
                state = segment.stateAtCollision;

                const [xC, yC, vxC, vyC] = state;

                // Record bounce
                bounceTimes.push(tCurrent);
                bouncePositions.push([xC, yC]);

                const E = totalEnergy(xC, yC, vxC, vyC, 1.0, this.g, this.a);
                bounceEnergies.push(E);

                // Apply reflection
                state = this.applyCollision(state);

                // Verify energy conservation
                const [, , vxNew, vyNew] = state;
                const EAfter = totalEnergy(xC, yC, vxNew, vyNew, 1.0, this.g, this.a);
                const energyError = Math.abs(EAfter - E) / E0;

                if (energyError > 1e-6) {
                    console.warn(`Energy error at bounce ${bounceCount}: ${energyError.toExponential(2)}`);
                }
            } else {
                // No collision, reached tEnd
                break;
            }
        }

        // Calculate final energy
        const [xF, yF, vxF, vyF] = [xFull[xFull.length - 1], yFull[yFull.length - 1],
        vxFull[vxFull.length - 1], vyFull[vyFull.length - 1]];
        const EFinal = totalEnergy(xF, yF, vxF, vyF, 1.0, this.g, this.a);

        return {
            t: tFull,
            x: xFull,
            y: yFull,
            vx: vxFull,
            vy: vyFull,
            bounces: {
                times: bounceTimes,
                positions: bouncePositions,
                count: bounceCount
            },
            energy: {
                initial: E0,
                final: EFinal,
                conservationError: Math.abs(EFinal - E0) / E0
            }
        };
    }
}

// =============================================================================
// TESTS
// =============================================================================

export function runSolverTests() {
    console.log("Testing BouncingBallSolver with parameterized parabola");
    console.log("=".repeat(60));

    for (const aVal of [0.3, 1.0]) {
        console.log(`\n${"=".repeat(60)}`);
        console.log(`Testing with a = ${aVal} (parabola: y = ${aVal}x²)`);
        console.log(`${"=".repeat(60)}`);

        const solver = new BouncingBallSolver(9.80665, aVal);

        // Drop ball from (-2, 5) at rest
        const result = solver.simulate(-2.0, 5.0, 0.0, 0.0, 10.0, 50);

        console.log(`Simulated ${result.t.length} time points`);
        console.log(`Number of bounces: ${result.bounces.count}`);
        console.log(`Energy conservation error: ${result.energy.conservationError.toExponential(2)}`);
        console.log(`Initial energy: ${result.energy.initial.toFixed(4)} J`);
        console.log(`Final energy: ${result.energy.final.toFixed(4)} J`);

        console.log("\nFirst 5 bounces:");
        for (let i = 0; i < Math.min(5, result.bounces.times.length); i++) {
            const t = result.bounces.times[i];
            const [x, y] = result.bounces.positions[i];
            console.log(`  Bounce ${i + 1}: t=${t.toFixed(3)}s at (x=${x.toFixed(3)}, y=${y.toFixed(3)})`);
        }
    }
}

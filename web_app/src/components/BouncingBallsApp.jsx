/**
 * Main Bouncing Balls React Application
 *
 * Interactive web-based simulation of chaotic bouncing balls
 */

import React, { useState, useEffect, useRef } from 'react';
import { BouncingBallSolver } from '../physics/solver.js';
import { separationDistance } from '../physics/equations.js';
import SimulationCanvas from './SimulationCanvas.jsx';
import ControlPanel from './ControlPanel.jsx';
import MetricsDisplay from './MetricsDisplay.jsx';
import './BouncingBallsApp.css';

const BouncingBallsApp = () => {
    // Simulation parameters
    const [params, setParams] = useState({
        a: 0.3,                 // Parabola steepness
        g: 9.80665,            // Gravity
        x0: -2.0,              // Initial x position
        y0: 5.0,               // Initial y position
        vx0: 0.0,              // Initial x velocity
        vy0: 0.0,              // Initial y velocity
        deltaX: 1e-3,          // Initial separation for ball 2
        tMax: 20.0,            // Max simulation time
        maxBounces: 100,       // Max bounces
        thresholdFactor: 100.0 // Divergence threshold
    });

    // Simulation state
    const [isRunning, setIsRunning] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [trajectory1, setTrajectory1] = useState(null);
    const [trajectory2, setTrajectory2] = useState(null);
    const [metrics, setMetrics] = useState(null);

    // Animation refs
    const animationRef = useRef(null);
    const startTimeRef = useRef(null);

    // Run simulation
    const runSimulation = () => {
        console.log("Running simulation with parameters:", params);

        try {
            const solver = new BouncingBallSolver(params.g, params.a);

            // Simulate ball 1
            const traj1 = solver.simulate(
                params.x0,
                params.y0,
                params.vx0,
                params.vy0,
                params.tMax,
                params.maxBounces
            );

            // Simulate ball 2 (with slight offset)
            const traj2 = solver.simulate(
                params.x0 + params.deltaX,
                params.y0,
                params.vx0,
                params.vy0,
                params.tMax,
                params.maxBounces
            );

            setTrajectory1(traj1);
            setTrajectory2(traj2);

            // Calculate metrics
            calculateMetrics(traj1, traj2);

            console.log("Simulation complete!");
            console.log(`Ball 1: ${traj1.bounces.count} bounces`);
            console.log(`Ball 2: ${traj2.bounces.count} bounces`);
        } catch (error) {
            console.error("Simulation error:", error);
            alert(`Simulation error: ${error.message}`);
        }
    };

    // Calculate divergence metrics
    const calculateMetrics = (traj1, traj2) => {
        const nPoints = Math.min(traj1.t.length, traj2.t.length);
        const separations = [];
        const times = [];

        for (let i = 0; i < nPoints; i++) {
            const state1 = [traj1.x[i], traj1.y[i], traj1.vx[i], traj1.vy[i]];
            const state2 = [traj2.x[i], traj2.y[i], traj2.vx[i], traj2.vy[i]];
            const sep = separationDistance(state1, state2);
            separations.push(sep);
            times.push(traj1.t[i]);
        }

        const dInitial = separations[0];
        const dFinal = separations[separations.length - 1];
        const threshold = params.thresholdFactor * dInitial;

        // Find divergence time
        let diverged = false;
        let tDivergence = null;

        for (let i = 0; i < separations.length; i++) {
            if (separations[i] > threshold) {
                diverged = true;
                tDivergence = times[i];
                break;
            }
        }

        setMetrics({
            dInitial,
            dFinal,
            threshold,
            diverged,
            tDivergence,
            separations,
            times,
            growthFactor: dFinal / dInitial,
            bounces1: traj1.bounces.count,
            bounces2: traj2.bounces.count,
            energyError1: traj1.energy.conservationError,
            energyError2: traj2.energy.conservationError
        });
    };

    // Start animation
    const startAnimation = () => {
        if (!trajectory1 || !trajectory2) {
            runSimulation();
        }
        setIsRunning(true);
        setIsPaused(false);
        setCurrentTime(0);
        startTimeRef.current = Date.now();
    };

    // Pause/Resume animation
    const togglePause = () => {
        setIsPaused(!isPaused);
    };

    // Stop animation
    const stopAnimation = () => {
        setIsRunning(false);
        setIsPaused(false);
        setCurrentTime(0);
        if (animationRef.current) {
            cancelAnimationFrame(animationRef.current);
        }
    };

    // Reset simulation
    const resetSimulation = () => {
        stopAnimation();
        setTrajectory1(null);
        setTrajectory2(null);
        setMetrics(null);
        setCurrentTime(0);
    };

    // Update parameter
    const updateParam = (key, value) => {
        setParams(prev => ({ ...prev, [key]: value }));
    };

    // Animation loop
    useEffect(() => {
        if (!isRunning || !trajectory1 || isPaused) return;

        const animate = () => {
            const elapsed = (Date.now() - startTimeRef.current) / 1000; // seconds
            const simTime = Math.min(elapsed, params.tMax);

            setCurrentTime(simTime);

            if (simTime >= params.tMax || simTime >= trajectory1.t[trajectory1.t.length - 1]) {
                setIsRunning(false);
                return;
            }

            animationRef.current = requestAnimationFrame(animate);
        };

        animationRef.current = requestAnimationFrame(animate);

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [isRunning, isPaused, trajectory1, params.tMax]);

    return (
        <div className="bouncing-balls-app">
            <header className="app-header">
                <h1>🎱 Chaotic Bouncing Balls Simulator</h1>
                <p>Interactive demonstration of deterministic chaos in mechanical systems</p>
            </header>

            <div className="app-layout">
                <div className="left-panel">
                    <ControlPanel
                        params={params}
                        updateParam={updateParam}
                        isRunning={isRunning}
                        isPaused={isPaused}
                        onStart={startAnimation}
                        onPause={togglePause}
                        onStop={stopAnimation}
                        onReset={resetSimulation}
                        onRunSimulation={runSimulation}
                    />

                    {metrics && (
                        <MetricsDisplay
                            metrics={metrics}
                            params={params}
                        />
                    )}
                </div>

                <div className="center-panel">
                    <SimulationCanvas
                        trajectory1={trajectory1}
                        trajectory2={trajectory2}
                        currentTime={currentTime}
                        params={params}
                        metrics={metrics}
                    />
                </div>
            </div>

            <footer className="app-footer">
                <p>
                    Simulates two balls bouncing on parabola y = {params.a}x² with initial separation δx = {params.deltaX.toExponential(1)} m
                </p>
                <p className="small">
                    Physics: Elastic collisions + Newtonian gravity | Integration: RK4 with event detection
                </p>
            </footer>
        </div>
    );
};

export default BouncingBallsApp;

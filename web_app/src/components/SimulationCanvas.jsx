/**
 * Simulation Canvas Component
 *
 * Renders the bouncing balls animation on HTML5 canvas
 */

import React, { useRef, useEffect } from 'react';
import { parabola } from '../physics/equations.js';

const SimulationCanvas = ({ trajectory1, trajectory2, currentTime, params, metrics }) => {
    const canvasRef = useRef(null);

    // Find state at current time
    const getStateAtTime = (trajectory, t) => {
        if (!trajectory || trajectory.t.length === 0) return null;

        // Find closest time index
        let idx = 0;
        for (let i = 0; i < trajectory.t.length; i++) {
            if (trajectory.t[i] > t) break;
            idx = i;
        }

        return {
            x: trajectory.x[idx],
            y: trajectory.y[idx],
            vx: trajectory.vx[idx],
            vy: trajectory.vy[idx],
            t: trajectory.t[idx]
        };
    };

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear canvas
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, width, height);

        // Set up coordinate transform
        // Physical: x ∈ [-3, 3], y ∈ [0, 6]
        const xMin = -3, xMax = 3;
        const yMin = 0, yMax = 6;

        const scaleX = width / (xMax - xMin);
        const scaleY = height / (yMax - yMin);

        const toCanvasX = (x) => (x - xMin) * scaleX;
        const toCanvasY = (y) => height - (y - yMin) * scaleY;

        // Draw parabola
        ctx.strokeStyle = '#228b22';
        ctx.fillStyle = 'rgba(34, 139, 34, 0.1)';
        ctx.lineWidth = 2;

        ctx.beginPath();
        for (let x = xMin; x <= xMax; x += 0.01) {
            const y = parabola(x, params.a);
            const cx = toCanvasX(x);
            const cy = toCanvasY(y);

            if (x === xMin) {
                ctx.moveTo(cx, cy);
            } else {
                ctx.lineTo(cx, cy);
            }
        }
        ctx.stroke();

        // Fill below parabola
        ctx.lineTo(toCanvasX(xMax), toCanvasY(0));
        ctx.lineTo(toCanvasX(xMin), toCanvasY(0));
        ctx.closePath();
        ctx.fill();

        // Draw grid
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 0.5;

        for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
            ctx.beginPath();
            ctx.moveTo(toCanvasX(x), 0);
            ctx.lineTo(toCanvasX(x), height);
            ctx.stroke();
        }

        for (let y = Math.ceil(yMin); y <= Math.floor(yMax); y++) {
            ctx.beginPath();
            ctx.moveTo(0, toCanvasY(y));
            ctx.lineTo(width, toCanvasY(y));
            ctx.stroke();
        }

        // Draw axes
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 1;

        // Y-axis (x=0)
        ctx.beginPath();
        ctx.moveTo(toCanvasX(0), 0);
        ctx.lineTo(toCanvasX(0), height);
        ctx.stroke();

        // X-axis (y=0)
        ctx.beginPath();
        ctx.moveTo(0, toCanvasY(0));
        ctx.lineTo(width, toCanvasY(0));
        ctx.stroke();

        // Draw axis labels
        ctx.fillStyle = '#000000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'center';

        for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
            ctx.fillText(x.toString(), toCanvasX(x), toCanvasY(0) + 15);
        }

        ctx.textAlign = 'right';
        for (let y = Math.ceil(yMin) + 1; y <= Math.floor(yMax); y++) {
            ctx.fillText(y.toString(), toCanvasX(0) - 5, toCanvasY(y) + 4);
        }

        // Draw trajectories if available
        if (trajectory1 && trajectory2) {
            const drawTrajectory = (trajectory, color, trailLength = 150) => {
                // Find current index
                let currentIdx = 0;
                for (let i = 0; i < trajectory.t.length; i++) {
                    if (trajectory.t[i] > currentTime) break;
                    currentIdx = i;
                }

                // Draw trail
                const startIdx = Math.max(0, currentIdx - trailLength);
                ctx.strokeStyle = color;
                ctx.globalAlpha = 0.4;
                ctx.lineWidth = 1.5;

                ctx.beginPath();
                for (let i = startIdx; i <= currentIdx; i++) {
                    const cx = toCanvasX(trajectory.x[i]);
                    const cy = toCanvasY(trajectory.y[i]);

                    if (i === startIdx) {
                        ctx.moveTo(cx, cy);
                    } else {
                        ctx.lineTo(cx, cy);
                    }
                }
                ctx.stroke();
                ctx.globalAlpha = 1.0;

                // Draw current ball
                if (currentIdx < trajectory.t.length) {
                    const cx = toCanvasX(trajectory.x[currentIdx]);
                    const cy = toCanvasY(trajectory.y[currentIdx]);

                    ctx.fillStyle = color;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 8, 0, 2 * Math.PI);
                    ctx.fill();

                    ctx.strokeStyle = '#000000';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }

                // Draw bounces
                if (trajectory.bounces && trajectory.bounces.positions) {
                    ctx.fillStyle = color;
                    ctx.globalAlpha = 0.5;

                    for (const [x, y] of trajectory.bounces.positions) {
                        const cx = toCanvasX(x);
                        const cy = toCanvasY(y);

                        ctx.beginPath();
                        ctx.moveTo(cx - 5, cy);
                        ctx.lineTo(cx + 5, cy);
                        ctx.moveTo(cx, cy - 5);
                        ctx.lineTo(cx, cy + 5);
                        ctx.stroke();
                    }
                    ctx.globalAlpha = 1.0;
                }
            };

            drawTrajectory(trajectory1, '#1f77b4'); // Blue
            drawTrajectory(trajectory2, '#ff7f0e'); // Orange
        }

        // Draw time display
        ctx.fillStyle = '#000000';
        ctx.font = 'bold 16px Arial';
        ctx.textAlign = 'left';
        ctx.fillText(`t = ${currentTime.toFixed(3)} s`, 10, 25);

        // Draw parabola equation
        ctx.font = '14px Arial';
        ctx.fillText(`y = ${params.a}x²`, 10, 45);

        // Draw divergence status
        if (metrics) {
            ctx.font = '12px Arial';
            const state1 = getStateAtTime(trajectory1, currentTime);
            const state2 = getStateAtTime(trajectory2, currentTime);

            if (state1 && state2) {
                const sep = Math.sqrt(
                    (state1.x - state2.x) ** 2 + (state1.y - state2.y) ** 2
                );

                ctx.fillText(`Separation: ${sep.toExponential(3)} m`, 10, 65);

                if (metrics.diverged && currentTime >= metrics.tDivergence) {
                    ctx.fillStyle = '#ff0000';
                    ctx.font = 'bold 14px Arial';
                    ctx.fillText('DIVERGED!', 10, 85);
                }
            }
        }

        // Draw legend
        const legendX = width - 120;
        const legendY = 20;

        ctx.fillStyle = '#1f77b4';
        ctx.fillRect(legendX, legendY, 15, 15);
        ctx.fillStyle = '#000000';
        ctx.font = '12px Arial';
        ctx.textAlign = 'left';
        ctx.fillText('Ball 1', legendX + 20, legendY + 12);

        ctx.fillStyle = '#ff7f0e';
        ctx.fillRect(legendX, legendY + 20, 15, 15);
        ctx.fillStyle = '#000000';
        ctx.fillText('Ball 2', legendX + 20, legendY + 32);

    }, [trajectory1, trajectory2, currentTime, params, metrics]);

    return (
        <div className="simulation-canvas-container">
            <canvas
                ref={canvasRef}
                width={800}
                height={600}
                style={{
                    border: '2px solid #333',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                }}
            />
        </div>
    );
};

export default SimulationCanvas;

/**
 * Metrics Display Component
 *
 * Shows simulation results and chaos metrics
 */

import React from 'react';
import './MetricsDisplay.css';

const MetricsDisplay = ({ metrics, params }) => {
    if (!metrics) return null;

    const {
        dInitial,
        dFinal,
        threshold,
        diverged,
        tDivergence,
        growthFactor,
        bounces1,
        bounces2,
        energyError1,
        energyError2
    } = metrics;

    return (
        <div className="metrics-display">
            <h2>📊 Simulation Metrics</h2>

            {/* Divergence Status */}
            <div className="metric-section">
                <h3>Divergence Analysis</h3>

                <div className={`divergence-status ${diverged ? 'diverged' : 'not-diverged'}`}>
                    {diverged ? (
                        <>
                            <div className="status-icon">✅</div>
                            <div className="status-text">
                                <strong>DIVERGED</strong>
                                <p>at t = {tDivergence.toFixed(3)} s</p>
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="status-icon">⏱️</div>
                            <div className="status-text">
                                <strong>NO DIVERGENCE</strong>
                                <p>within {params.tMax} seconds</p>
                            </div>
                        </>
                    )}
                </div>

                <div className="metric-row">
                    <span className="metric-label">Initial Separation (δ₀):</span>
                    <span className="metric-value">{dInitial.toExponential(3)} m</span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Final Separation:</span>
                    <span className="metric-value">{dFinal.toExponential(3)} m</span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Growth Factor:</span>
                    <span className="metric-value highlight">
                        {growthFactor.toFixed(1)}×
                    </span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Threshold:</span>
                    <span className="metric-value">{threshold.toExponential(3)} m</span>
                </div>
            </div>

            {/* Bounce Statistics */}
            <div className="metric-section">
                <h3>Bounce Statistics</h3>

                <div className="metric-row">
                    <span className="metric-label">Ball 1 Bounces:</span>
                    <span className="metric-value" style={{ color: '#1f77b4' }}>
                        {bounces1}
                    </span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Ball 2 Bounces:</span>
                    <span className="metric-value" style={{ color: '#ff7f0e' }}>
                        {bounces2}
                    </span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Bounce Difference:</span>
                    <span className="metric-value">
                        {Math.abs(bounces1 - bounces2)}
                    </span>
                </div>
            </div>

            {/* Energy Conservation */}
            <div className="metric-section">
                <h3>Energy Conservation</h3>

                <div className="metric-row">
                    <span className="metric-label">Ball 1 Error:</span>
                    <span className={`metric-value ${energyError1 < 1e-4 ? 'good' : 'warning'}`}>
                        {energyError1.toExponential(2)}
                        {energyError1 < 1e-4 && ' ✓'}
                    </span>
                </div>

                <div className="metric-row">
                    <span className="metric-label">Ball 2 Error:</span>
                    <span className={`metric-value ${energyError2 < 1e-4 ? 'good' : 'warning'}`}>
                        {energyError2.toExponential(2)}
                        {energyError2 < 1e-4 && ' ✓'}
                    </span>
                </div>

                {(energyError1 < 1e-4 && energyError2 < 1e-4) && (
                    <div className="info-box good">
                        ✅ Energy conserved within tolerance!
                    </div>
                )}
            </div>

            {/* Physics Explanation */}
            <div className="metric-section">
                <h3>💡 What's Happening?</h3>
                <div className="explanation-box">
                    <p>
                        <strong>Deterministic Chaos:</strong> Even though the physics
                        is completely deterministic (no randomness), tiny differences
                        in initial conditions lead to drastically different outcomes.
                    </p>
                    <p>
                        The two balls start only <strong>{dInitial.toExponential(1)} meters</strong> apart,
                        but after bouncing, they've separated by {' '}
                        <strong>{growthFactor.toFixed(0)}× more</strong>!
                    </p>
                    {diverged && (
                        <p className="highlight-text">
                            🎯 Divergence occurred in just {tDivergence.toFixed(2)} seconds,
                            demonstrating extreme sensitivity to initial conditions.
                        </p>
                    )}
                </div>
            </div>

            {/* Lyapunov Estimate */}
            {diverged && (
                <div className="metric-section">
                    <h3>Chaos Characterization</h3>

                    <div className="metric-row">
                        <span className="metric-label">Estimated Lyapunov Exponent:</span>
                        <span className="metric-value highlight">
                            λ ≈ {(Math.log(growthFactor) / tDivergence).toFixed(4)} s⁻¹
                        </span>
                    </div>

                    <div className="info-box">
                        <p>
                            <strong>Lyapunov exponent λ</strong> measures the rate of exponential divergence.
                            Positive λ indicates chaos!
                        </p>
                        <p className="small">
                            Formula: λ ≈ ln(d_final/d_initial) / t
                        </p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default MetricsDisplay;

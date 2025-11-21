/**
 * Control Panel Component
 *
 * Interactive controls for simulation parameters
 */

import React from 'react';
import './ControlPanel.css';

const ControlPanel = ({
    params,
    updateParam,
    isRunning,
    isPaused,
    onStart,
    onPause,
    onStop,
    onReset,
    onRunSimulation
}) => {
    const handleInputChange = (key, value) => {
        updateParam(key, parseFloat(value));
    };

    return (
        <div className="control-panel">
            <h2>⚙️ Simulation Controls</h2>

            {/* Playback Controls */}
            <div className="control-section">
                <h3>Playback</h3>
                <div className="button-group">
                    <button
                        onClick={onStart}
                        disabled={isRunning && !isPaused}
                        className="btn btn-primary"
                    >
                        {isRunning && !isPaused ? '▶️ Running' : '▶️ Start'}
                    </button>

                    <button
                        onClick={onPause}
                        disabled={!isRunning}
                        className="btn btn-warning"
                    >
                        {isPaused ? '▶️ Resume' : '⏸️ Pause'}
                    </button>

                    <button
                        onClick={onStop}
                        disabled={!isRunning}
                        className="btn btn-danger"
                    >
                        ⏹️ Stop
                    </button>

                    <button
                        onClick={onReset}
                        className="btn btn-secondary"
                    >
                        🔄 Reset
                    </button>
                </div>

                <button
                    onClick={onRunSimulation}
                    className="btn btn-success btn-full"
                    style={{ marginTop: '10px' }}
                >
                    🔬 Compute Trajectories
                </button>
            </div>

            {/* Physics Parameters */}
            <div className="control-section">
                <h3>Physics Parameters</h3>

                <div className="param-group">
                    <label>
                        Parabola Steepness (a):
                        <input
                            type="number"
                            step="0.1"
                            min="0.1"
                            max="2.0"
                            value={params.a}
                            onChange={(e) => handleInputChange('a', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">y = {params.a}x²</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Gravity (g):
                        <input
                            type="number"
                            step="0.1"
                            min="1.0"
                            max="15.0"
                            value={params.g}
                            onChange={(e) => handleInputChange('g', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">m/s²</span>
                    </label>
                </div>
            </div>

            {/* Initial Conditions */}
            <div className="control-section">
                <h3>Initial Conditions</h3>

                <div className="param-group">
                    <label>
                        Initial X Position:
                        <input
                            type="number"
                            step="0.1"
                            min="-3.0"
                            max="3.0"
                            value={params.x0}
                            onChange={(e) => handleInputChange('x0', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">m</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Initial Y Position:
                        <input
                            type="number"
                            step="0.1"
                            min="0.1"
                            max="6.0"
                            value={params.y0}
                            onChange={(e) => handleInputChange('y0', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">m</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Initial X Velocity:
                        <input
                            type="number"
                            step="0.1"
                            min="-5.0"
                            max="5.0"
                            value={params.vx0}
                            onChange={(e) => handleInputChange('vx0', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">m/s</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Initial Y Velocity:
                        <input
                            type="number"
                            step="0.1"
                            min="-5.0"
                            max="5.0"
                            value={params.vy0}
                            onChange={(e) => handleInputChange('vy0', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">m/s</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Separation δx:
                        <select
                            value={params.deltaX}
                            onChange={(e) => handleInputChange('deltaX', e.target.value)}
                            className="param-select"
                        >
                            <option value="1e-5">10⁻⁵ m (0.01 mm)</option>
                            <option value="1e-4">10⁻⁴ m (0.1 mm)</option>
                            <option value="5e-4">5×10⁻⁴ m (0.5 mm)</option>
                            <option value="1e-3">10⁻³ m (1 mm)</option>
                            <option value="5e-3">5×10⁻³ m (5 mm)</option>
                            <option value="1e-2">10⁻² m (1 cm)</option>
                        </select>
                    </label>
                </div>
            </div>

            {/* Simulation Settings */}
            <div className="control-section">
                <h3>Simulation Settings</h3>

                <div className="param-group">
                    <label>
                        Max Time:
                        <input
                            type="number"
                            step="5"
                            min="5"
                            max="120"
                            value={params.tMax}
                            onChange={(e) => handleInputChange('tMax', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">seconds</span>
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Max Bounces:
                        <input
                            type="number"
                            step="10"
                            min="10"
                            max="500"
                            value={params.maxBounces}
                            onChange={(e) => handleInputChange('maxBounces', e.target.value)}
                            className="param-input"
                        />
                    </label>
                </div>

                <div className="param-group">
                    <label>
                        Divergence Threshold:
                        <input
                            type="number"
                            step="10"
                            min="10"
                            max="1000"
                            value={params.thresholdFactor}
                            onChange={(e) => handleInputChange('thresholdFactor', e.target.value)}
                            className="param-input"
                        />
                        <span className="param-hint">× initial separation</span>
                    </label>
                </div>
            </div>

            {/* Presets */}
            <div className="control-section">
                <h3>📋 Quick Presets</h3>
                <div className="preset-buttons">
                    <button
                        onClick={() => {
                            updateParam('a', 0.3);
                            updateParam('x0', -2.0);
                            updateParam('y0', 5.0);
                            updateParam('deltaX', 1e-3);
                        }}
                        className="btn btn-preset"
                    >
                        Gentle Chaos
                    </button>

                    <button
                        onClick={() => {
                            updateParam('a', 1.0);
                            updateParam('x0', -1.5);
                            updateParam('y0', 4.0);
                            updateParam('deltaX', 5e-4);
                        }}
                        className="btn btn-preset"
                    >
                        Standard Parabola
                    </button>

                    <button
                        onClick={() => {
                            updateParam('a', 1.5);
                            updateParam('x0', -1.0);
                            updateParam('y0', 3.0);
                            updateParam('deltaX', 1e-4);
                        }}
                        className="btn btn-preset"
                    >
                        Steep & Fast
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ControlPanel;

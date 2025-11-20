#!/usr/bin/env python3
"""
Interactive Streamlit Dashboard for Bouncing Balls Chaos Study

Features:
- Interactive parameter exploration
- Real-time simulation visualization
- Parameter sweep studies
- Results caching with SQLite
- Plotly-based interactive charts
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import sqlite3
from pathlib import Path
import sys
import json
from datetime import datetime

# Add paths
sys.path.append('implementation/simulations')
sys.path.append('implementation/solvers')
sys.path.append('equations/definitions')

from divergence_study import DivergenceStudy

# Page configuration
st.set_page_config(
    page_title="Bouncing Balls Chaos Study",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database setup
DB_PATH = Path("outputs/streamlit_cache.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def init_database():
    """Initialize SQLite database for results caching."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulation_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            delta_x REAL,
            a REAL,
            x1_0 REAL,
            y1_0 REAL,
            vx1_0 REAL,
            vy1_0 REAL,
            t_max REAL,
            diverged INTEGER,
            t_divergence REAL,
            bounce_count_1 INTEGER,
            bounce_count_2 INTEGER,
            d_initial REAL,
            d_final REAL,
            trajectory_data TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_params
        ON simulation_results(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max)
    """)

    conn.commit()
    conn.close()


def get_cached_result(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max):
    """Retrieve cached simulation result if available."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT diverged, t_divergence, bounce_count_1, bounce_count_2,
               d_initial, d_final, trajectory_data
        FROM simulation_results
        WHERE ABS(delta_x - ?) < 1e-15
          AND ABS(a - ?) < 1e-10
          AND ABS(x1_0 - ?) < 1e-10
          AND ABS(y1_0 - ?) < 1e-10
          AND ABS(vx1_0 - ?) < 1e-10
          AND ABS(vy1_0 - ?) < 1e-10
          AND ABS(t_max - ?) < 1e-10
        LIMIT 1
    """, (delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max))

    result = cursor.fetchone()
    conn.close()

    if result:
        diverged, t_div, bc1, bc2, d_init, d_final, traj_data = result
        trajectory = json.loads(traj_data)
        return {
            'diverged': bool(diverged),
            't_divergence': t_div,
            'bounce_count_1': bc1,
            'bounce_count_2': bc2,
            'd_initial': d_init,
            'd_final': d_final,
            'trajectory': trajectory
        }
    return None


def cache_result(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max, result):
    """Cache simulation result to database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Prepare trajectory data (downsample for storage)
    traj1 = result.trajectory_1
    traj2 = result.trajectory_2

    # Downsample to max 1000 points
    n_points = len(traj1['t'])
    if n_points > 1000:
        idx = np.linspace(0, n_points-1, 1000, dtype=int)
        trajectory_data = {
            't': [float(traj1['t'][i]) for i in idx],
            'x1': [float(traj1['x'][i]) for i in idx],
            'y1': [float(traj1['y'][i]) for i in idx],
            'vx1': [float(traj1['vx'][i]) for i in idx],
            'vy1': [float(traj1['vy'][i]) for i in idx],
            'x2': [float(traj2['x'][i]) for i in idx],
            'y2': [float(traj2['y'][i]) for i in idx],
            'vx2': [float(traj2['vx'][i]) for i in idx],
            'vy2': [float(traj2['vy'][i]) for i in idx],
        }
    else:
        trajectory_data = {
            't': [float(t) for t in traj1['t']],
            'x1': [float(x) for x in traj1['x']],
            'y1': [float(y) for y in traj1['y']],
            'vx1': [float(vx) for vx in traj1['vx']],
            'vy1': [float(vy) for vy in traj1['vy']],
            'x2': [float(x) for x in traj2['x']],
            'y2': [float(y) for y in traj2['y']],
            'vx2': [float(vx) for vx in traj2['vx']],
            'vy2': [float(vy) for vy in traj2['vy']],
        }

    cursor.execute("""
        INSERT INTO simulation_results
        (timestamp, delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max,
         diverged, t_divergence, bounce_count_1, bounce_count_2,
         d_initial, d_final, trajectory_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max,
        int(result.diverged),
        float(result.t_divergence) if result.diverged else None,
        result.bounce_count_1,
        result.bounce_count_2,
        result.d_initial,
        result.d_final,
        json.dumps(trajectory_data)
    ))

    conn.commit()
    conn.close()


@st.cache_data
def run_simulation(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max):
    """Run simulation with caching."""
    # Try to get cached result
    cached = get_cached_result(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max)
    if cached:
        return cached

    # Run new simulation
    study = DivergenceStudy(a=a, threshold_factor=100.0, tolerance_abs=1e-12)

    result = study.simulate_pair(
        x1_0=x1_0,
        y1_0=y1_0,
        vx1_0=vx1_0,
        vy1_0=vy1_0,
        delta_x=delta_x,
        t_max=t_max,
        max_bounces=200,
        dt_sample=0.01
    )

    # Cache result
    cache_result(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max, result)

    # Return processed result
    traj1 = result.trajectory_1
    traj2 = result.trajectory_2

    return {
        'diverged': result.diverged,
        't_divergence': result.t_divergence,
        'bounce_count_1': result.bounce_count_1,
        'bounce_count_2': result.bounce_count_2,
        'd_initial': result.d_initial,
        'd_final': result.d_final,
        'trajectory': {
            't': list(traj1['t']),
            'x1': list(traj1['x']),
            'y1': list(traj1['y']),
            'vx1': list(traj1['vx']),
            'vy1': list(traj1['vy']),
            'x2': list(traj2['x']),
            'y2': list(traj2['y']),
            'vx2': list(traj2['vx']),
            'vy2': list(traj2['vy']),
        }
    }


def plot_trajectories(result, a):
    """Create interactive trajectory plot with Plotly."""
    traj = result['trajectory']
    t = np.array(traj['t'])
    x1 = np.array(traj['x1'])
    y1 = np.array(traj['y1'])
    x2 = np.array(traj['x2'])
    y2 = np.array(traj['y2'])

    # Create parabola
    x_para = np.linspace(-3, 3, 500)
    y_para = a * x_para**2

    fig = go.Figure()

    # Parabola
    fig.add_trace(go.Scatter(
        x=x_para, y=y_para,
        mode='lines',
        name=f'Parabola: y={a}x²',
        line=dict(color='green', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 0, 0.1)'
    ))

    # Ball 1 trajectory
    fig.add_trace(go.Scatter(
        x=x1, y=y1,
        mode='lines+markers',
        name='Ball 1',
        line=dict(color='blue', width=2),
        marker=dict(size=4, color='blue')
    ))

    # Ball 2 trajectory
    fig.add_trace(go.Scatter(
        x=x2, y=y2,
        mode='lines+markers',
        name='Ball 2',
        line=dict(color='orange', width=2),
        marker=dict(size=4, color='orange')
    ))

    fig.update_layout(
        title='Bouncing Ball Trajectories',
        xaxis_title='x (m)',
        yaxis_title='y (m)',
        hovermode='closest',
        height=500,
        showlegend=True
    )

    fig.update_xaxes(range=[-3, 3])
    fig.update_yaxes(range=[0, 6])

    return fig


def plot_separation(result):
    """Create separation vs time plot."""
    traj = result['trajectory']
    t = np.array(traj['t'])
    x1 = np.array(traj['x1'])
    y1 = np.array(traj['y1'])
    x2 = np.array(traj['x2'])
    y2 = np.array(traj['y2'])

    sep = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t, y=sep,
        mode='lines',
        name='Separation',
        line=dict(color='blue', width=2)
    ))

    # Add threshold line
    threshold = 100 * result['d_initial']
    fig.add_hline(
        y=threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Threshold (100×d₀)"
    )

    # Add initial separation line
    fig.add_hline(
        y=result['d_initial'],
        line_dash="dash",
        line_color="green",
        annotation_text="d₀"
    )

    # Mark divergence point if diverged
    if result['diverged']:
        fig.add_vline(
            x=result['t_divergence'],
            line_dash="dot",
            line_color="red",
            annotation_text=f"Divergence at t={result['t_divergence']:.2f}s"
        )

    fig.update_layout(
        title='Separation Distance vs Time',
        xaxis_title='Time (s)',
        yaxis_title='Separation (m)',
        yaxis_type='log',
        hovermode='x',
        height=400
    )

    return fig


def plot_phase_space(result):
    """Create phase space plot (x vs vx)."""
    traj = result['trajectory']
    x1 = np.array(traj['x1'])
    vx1 = np.array(traj['vx1'])
    x2 = np.array(traj['x2'])
    vx2 = np.array(traj['vx2'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x1, y=vx1,
        mode='lines',
        name='Ball 1',
        line=dict(color='blue', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=x2, y=vx2,
        mode='lines',
        name='Ball 2',
        line=dict(color='orange', width=2)
    ))

    fig.update_layout(
        title='Phase Space (x vs vₓ)',
        xaxis_title='Position x (m)',
        yaxis_title='Velocity vₓ (m/s)',
        hovermode='closest',
        height=400
    )

    return fig


def main():
    """Main Streamlit app."""
    # Initialize database
    init_database()

    # Title
    st.title("⚽ Bouncing Balls Chaos Study")
    st.markdown("Interactive exploration of chaotic dynamics in bouncing ball systems")

    # Sidebar - Parameters
    st.sidebar.header("🎛️ Simulation Parameters")

    # Mode selection
    mode = st.sidebar.radio(
        "Mode",
        ["Single Simulation", "Parameter Sweep"],
        help="Single simulation or sweep over multiple parameter values"
    )

    if mode == "Single Simulation":
        run_single_simulation()
    else:
        run_parameter_sweep()


def run_single_simulation():
    """Run single simulation mode."""
    st.sidebar.subheader("Physical Parameters")

    # Initial separation
    delta_x = st.sidebar.number_input(
        "Initial separation δx (m)",
        min_value=1e-6,
        max_value=1e-2,
        value=1e-3,
        format="%.2e",
        help="Initial horizontal separation between balls"
    )

    # Parabola steepness
    a = st.sidebar.slider(
        "Parabola steepness a",
        min_value=0.1,
        max_value=2.0,
        value=0.3,
        step=0.1,
        help="Parabola equation: y = a*x²"
    )

    st.sidebar.subheader("Initial Conditions")

    # Initial position
    x1_0 = st.sidebar.slider(
        "Initial x position (m)",
        min_value=-2.5,
        max_value=-0.5,
        value=-2.0,
        step=0.1
    )

    y1_0 = st.sidebar.slider(
        "Initial y position (m)",
        min_value=2.0,
        max_value=8.0,
        value=5.0,
        step=0.5
    )

    # Initial velocity
    vx1_0 = st.sidebar.slider(
        "Initial vₓ (m/s)",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )

    vy1_0 = st.sidebar.slider(
        "Initial vᵧ (m/s)",
        min_value=-5.0,
        max_value=5.0,
        value=0.0,
        step=0.5
    )

    st.sidebar.subheader("Simulation Settings")

    t_max = st.sidebar.slider(
        "Max simulation time (s)",
        min_value=10.0,
        max_value=120.0,
        value=20.0,
        step=5.0
    )

    # Run button
    if st.sidebar.button("🚀 Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            result = run_simulation(delta_x, a, x1_0, y1_0, vx1_0, vy1_0, t_max)

        # Display results
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Diverged", "Yes" if result['diverged'] else "No")

        with col2:
            if result['diverged']:
                st.metric("Divergence Time", f"{result['t_divergence']:.3f} s")
            else:
                st.metric("Divergence Time", "N/A")

        with col3:
            st.metric("Ball 1 Bounces", result['bounce_count_1'])

        with col4:
            st.metric("Ball 2 Bounces", result['bounce_count_2'])

        # Plots
        st.subheader("📊 Visualizations")

        # Trajectory plot
        st.plotly_chart(plot_trajectories(result, a), use_container_width=True)

        # Two columns for separation and phase space
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(plot_separation(result), use_container_width=True)

        with col2:
            st.plotly_chart(plot_phase_space(result), use_container_width=True)

        # Additional info
        with st.expander("📈 Detailed Statistics"):
            st.write(f"**Initial separation:** {result['d_initial']:.6e} m")
            st.write(f"**Final separation:** {result['d_final']:.6e} m")
            st.write(f"**Separation growth:** {result['d_final']/result['d_initial']:.1f}×")
            st.write(f"**Ball 1 bounces:** {result['bounce_count_1']}")
            st.write(f"**Ball 2 bounces:** {result['bounce_count_2']}")
            if result['diverged']:
                st.write(f"**Time to divergence:** {result['t_divergence']:.3f} s")


def run_parameter_sweep():
    """Run parameter sweep mode."""
    st.sidebar.subheader("Sweep Parameters")

    # Choose what to sweep
    sweep_var = st.sidebar.selectbox(
        "Sweep variable",
        ["Initial separation (δx)", "Parabola steepness (a)"],
        help="Which parameter to vary in the sweep"
    )

    if sweep_var == "Initial separation (δx)":
        # Sweep delta_x
        delta_x_min = st.sidebar.number_input(
            "Min δx (m)",
            min_value=1e-6,
            max_value=1e-2,
            value=1e-5,
            format="%.2e"
        )

        delta_x_max = st.sidebar.number_input(
            "Max δx (m)",
            min_value=1e-6,
            max_value=1e-2,
            value=1e-2,
            format="%.2e"
        )

        n_points = st.sidebar.slider(
            "Number of points",
            min_value=5,
            max_value=30,
            value=15
        )

        # Fixed parameters
        a = st.sidebar.slider("Parabola steepness a", 0.1, 2.0, 0.3, 0.1)

        delta_x_values = np.logspace(
            np.log10(delta_x_min),
            np.log10(delta_x_max),
            n_points
        )
        a_values = [a] * n_points

    else:
        # Sweep a
        a_min = st.sidebar.slider("Min a", 0.1, 2.0, 0.1, 0.1)
        a_max = st.sidebar.slider("Max a", 0.1, 2.0, 2.0, 0.1)

        n_points = st.sidebar.slider(
            "Number of points",
            min_value=5,
            max_value=30,
            value=15
        )

        # Fixed parameters
        delta_x = st.sidebar.number_input(
            "Initial separation δx (m)",
            min_value=1e-6,
            max_value=1e-2,
            value=1e-3,
            format="%.2e"
        )

        a_values = np.linspace(a_min, a_max, n_points)
        delta_x_values = [delta_x] * n_points

    # Initial conditions (same for all)
    st.sidebar.subheader("Initial Conditions")
    x1_0 = st.sidebar.slider("Initial x (m)", -2.5, -0.5, -2.0, 0.1)
    y1_0 = st.sidebar.slider("Initial y (m)", 2.0, 8.0, 5.0, 0.5)
    vx1_0 = st.sidebar.slider("Initial vₓ (m/s)", -5.0, 5.0, 0.0, 0.5)
    vy1_0 = st.sidebar.slider("Initial vᵧ (m/s)", -5.0, 5.0, 0.0, 0.5)

    t_max = st.sidebar.slider("Max time (s)", 10.0, 60.0, 20.0, 5.0)

    # Run sweep
    if st.sidebar.button("🚀 Run Parameter Sweep", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        results = []

        for i, (dx, a_val) in enumerate(zip(delta_x_values, a_values)):
            status_text.text(f"Running simulation {i+1}/{n_points}...")
            progress_bar.progress((i + 1) / n_points)

            result = run_simulation(dx, a_val, x1_0, y1_0, vx1_0, vy1_0, t_max)

            results.append({
                'delta_x': dx,
                'a': a_val,
                'diverged': result['diverged'],
                't_divergence': result['t_divergence'] if result['diverged'] else t_max,
                'bounce_count_1': result['bounce_count_1'],
                'bounce_count_2': result['bounce_count_2'],
                'd_final': result['d_final'],
                'd_initial': result['d_initial']
            })

        status_text.text("✅ Sweep complete!")

        # Create DataFrame
        df = pd.DataFrame(results)

        # Plot results
        st.subheader("📊 Parameter Sweep Results")

        if sweep_var == "Initial separation (δx)":
            x_col = 'delta_x'
            x_label = 'Initial Separation δx (m)'
        else:
            x_col = 'a'
            x_label = 'Parabola Steepness a'

        # Divergence time plot
        fig = go.Figure()

        colors = ['green' if d else 'red' for d in df['diverged']]

        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df['t_divergence'],
            mode='markers+lines',
            marker=dict(
                size=10,
                color=colors,
                line=dict(width=1, color='black')
            ),
            line=dict(color='blue', width=2),
            name='Divergence Time'
        ))

        fig.update_layout(
            title='Divergence Time vs Parameter',
            xaxis_title=x_label,
            yaxis_title='Divergence Time (s)',
            xaxis_type='log' if sweep_var == "Initial separation (δx)" else 'linear',
            hovermode='closest',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Bounce count comparison
        col1, col2 = st.columns(2)

        with col1:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df[x_col],
                y=df['bounce_count_1'],
                mode='markers+lines',
                name='Ball 1',
                line=dict(color='blue')
            ))
            fig2.add_trace(go.Scatter(
                x=df[x_col],
                y=df['bounce_count_2'],
                mode='markers+lines',
                name='Ball 2',
                line=dict(color='orange')
            ))
            fig2.update_layout(
                title='Bounce Counts',
                xaxis_title=x_label,
                yaxis_title='Number of Bounces',
                xaxis_type='log' if sweep_var == "Initial separation (δx)" else 'linear',
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col2:
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(
                x=df[x_col],
                y=df['d_final'] / df['d_initial'],
                mode='markers+lines',
                line=dict(color='purple')
            ))
            fig3.update_layout(
                title='Separation Growth',
                xaxis_title=x_label,
                yaxis_title='Final / Initial Separation',
                xaxis_type='log' if sweep_var == "Initial separation (δx)" else 'linear',
                yaxis_type='log',
                height=400
            )
            st.plotly_chart(fig3, use_container_width=True)

        # Data table
        with st.expander("📋 View Data Table"):
            st.dataframe(df, use_container_width=True)


if __name__ == '__main__':
    main()

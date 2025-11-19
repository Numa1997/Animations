# Input Definitions

This directory contains all input specifications for physical phenomena studies.

## Structure

### `phenomena/`
Define the physical phenomena to be studied. Each phenomenon should include:
- Name and description
- Relevant physical laws
- Key variables and observables
- Expected behaviors
- Boundary/initial conditions

**Example**: Create `phenomena/pendulum.json` or `phenomena/pendulum.py`

### `parameters/`
Parameter configurations for studies:
- Physical constants
- System parameters
- Simulation parameters (timesteps, duration, etc.)
- Visualization parameters

**Example**: Create `parameters/simple_pendulum_params.json`

## Format

Files can be in JSON, YAML, or Python format. Use structured data that can be easily parsed by the implementation layer.

### Example Phenomenon Definition

```json
{
  "name": "Simple Pendulum",
  "description": "A point mass suspended by a massless string",
  "governing_laws": ["Newton's Second Law", "Gravitational Force"],
  "variables": {
    "theta": "Angular displacement",
    "omega": "Angular velocity",
    "L": "Length of pendulum",
    "m": "Mass",
    "g": "Gravitational acceleration"
  },
  "equations": ["d²θ/dt² = -(g/L)sin(θ)"]
}
```

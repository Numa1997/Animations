# Equations and Mathematics

Mathematical formulations and derivations for physical phenomena.

## Structure

### `definitions/`
Symbolic equation definitions:
- Governing equations
- Conservation laws
- Constitutive relations
- Approximations and limits

Store equations in symbolic form (SymPy, LaTeX, or structured format)

**Example**: `definitions/pendulum_equations.py`
```python
from sympy import symbols, Function, Derivative, sin

t = symbols('t')
theta = Function('theta')
g, L = symbols('g L', positive=True, real=True)

# Equation of motion
equation = Derivative(theta(t), t, 2) + (g/L)*sin(theta(t))
```

### `derivations/`
Step-by-step mathematical derivations:
- From first principles to final equations
- Approximations and their validity
- Dimensional analysis
- Special cases and limits

Store as Markdown, Jupyter notebooks, or LaTeX

**Example**: `derivations/pendulum_small_angle.md`

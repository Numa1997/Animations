# Animator

Animation and visualization system for physics phenomena.

## Structure

### `renderers/`
Rendering engines and backends:
- Matplotlib animations
- Manim scenes
- Plotly interactive plots
- 3D visualizations (Mayavi, PyVista)
- Custom renderers

**Example**: `renderers/matplotlib_animator.py`

### `scenes/`
Scene definitions and compositions:
- Camera setups
- Object arrangements
- Timing and choreography
- Transitions
- Multi-panel layouts

Define what to show and when.

### `styles/`
Visual styles and themes:
- Color schemes
- Line styles and widths
- Fonts and labels
- Plot aesthetics
- Branding/consistency

## Visualization Types

### Time Evolution
- Animated trajectories
- Phase space plots
- State evolution over time

### Parameter Space
- Heatmaps
- Contour plots
- Bifurcation diagrams

### Comparative
- Side-by-side comparisons
- Overlays of different cases
- Before/after visualizations

### Explanatory
- Annotated diagrams
- Force vectors
- Energy landscapes
- Geometric constructions

## Best Practices

1. **Clear labels** - all axes, quantities, units
2. **Physical intuition** - show what matters physically
3. **Appropriate speed** - not too fast or slow
4. **Key frames** - highlight important moments
5. **Color coding** - consistent and meaningful
6. **Scale bars** - provide visual reference
7. **Annotations** - guide viewer attention

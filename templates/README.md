# Templates

Reusable templates for studies and visualizations.

## Structure

### `study_templates/`
Templates for complete study reports:
- LaTeX templates
- Jupyter notebook templates
- Markdown templates
- HTML report templates

Each template should have:
- Placeholder sections
- Standard formatting
- Citation style
- Figure/table layouts

**Example**: `study_templates/standard_physics_study.tex`

### `visualization_templates/`
Standard visualization configurations:
- Plot style templates
- Animation templates
- Multi-panel layouts
- Interactive dashboard templates

Define reusable visual patterns.

## Usage

Templates should be:
1. **Parameterized** - easy to customize
2. **Well-documented** - clear instructions
3. **Validated** - tested with examples
4. **Consistent** - follow common conventions

## Example Template Structure

```python
# visualization_templates/phase_space_template.py

def phase_space_plot(data, xlabel='Position', ylabel='Velocity',
                     title='Phase Space', style='default'):
    """
    Standard phase space plot template.

    Parameters:
    -----------
    data : array-like
        Data with columns [position, velocity]
    xlabel, ylabel : str
        Axis labels
    title : str
        Plot title
    style : str
        Visual style preset
    """
    # Implementation
    pass
```

## Creating New Templates

1. Identify repeated patterns in your studies
2. Extract common structure
3. Parameterize variable elements
4. Document usage and examples
5. Add to appropriate subdirectory

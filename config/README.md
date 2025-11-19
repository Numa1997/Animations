# Configuration

System-wide configuration files and settings.

## Configuration Files

### `system_config.yaml`
Global system settings:
- Default solvers and tolerances
- Output directories
- Logging levels
- Resource limits (memory, CPU)

### `renderer_config.yaml`
Default rendering settings:
- Default renderer (matplotlib, manim, etc.)
- Resolution and DPI
- Frame rates for animations
- Export formats

### `physics_constants.py`
Physical constants:
- SI units
- Natural units
- Common conversion factors

### Example Configuration

```yaml
# system_config.yaml
defaults:
  solver: 'scipy_odeint'
  tolerance: 1e-8
  timestep: 0.01

output:
  base_dir: './outputs'
  save_intermediate: false

visualization:
  default_renderer: 'matplotlib'
  dpi: 300
  format: 'png'

logging:
  level: 'INFO'
  file: 'physics_study.log'
```

## Environment Variables

- `PHYSICS_STUDY_ROOT` - Root directory
- `PHYSICS_STUDY_CONFIG` - Config file path
- `PHYSICS_STUDY_OUTPUT` - Output directory

## Usage

Load configuration in your scripts:

```python
import yaml

with open('config/system_config.yaml') as f:
    config = yaml.safe_load(f)

tolerance = config['defaults']['tolerance']
```

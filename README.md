# Martial Arts Breaking Calculator

This Python script calculates the force (in lbf) and pressure (PSI) required to break stacks of materials commonly used in martial arts demonstrations, such as pine boards, paulownia boards, or concrete slabs. It supports pegged (spaced) and unpegged (stacked without spacing) configurations, multiple layers, and correlates the force to approximate human bone breaking thresholds for educational purposes.

The script is designed for both command-line interface (CLI) and interactive use, with options for matrix outputs, CSV generation, plotting, and unit tests. Calculations are based on empirical data, simplified physics models (e.g., beam theory for flexible materials, momentum transfer for spacing assistance), and user-configurable parameters.

## Features
- **Materials Supported**: Pine, paulownia (flexible woods), concrete (brittle). Easily extendable via `materials.json`.
- **Configurations**: Pegged (with spacing: penny 1.52 mm, pencil 6.35 mm, or custom) or unpegged.
- **Scaling Models**: 
  - Unpegged flexible: Superlinear scaling (`F = F1 * n**exponent`, default exponent=1.5 for empirical fit).
  - Unpegged brittle: Linear scaling (`F = F1 * n`).
  - Pegged: Additive base force with momentum-based reduction from spacing.
- **Customizable Constants**: Impact time (default 0.005 s), contact area (default 2.5 in²), scaling exponent (default 1.5).
- **Outputs**: Force, PSI, correlated bones (e.g., clavicle if force >=147 lbf).
- **Modes**: Single calculation, matrix (1-10 layers), CSV for all materials/configs.
- **Visualization**: Optional plotting of force vs. layers (requires matplotlib).
- **Testing**: Built-in unit tests.
- **Data Sources**: Updated as of August 02, 2025, with references to empirical studies (e.g., Harvard karate demos, bone breaking forces from Discovery.com).

**Note**: Calculations are approximations; actual breaking varies by technique and material. Bone correlations are educational only—not medical advice.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/JLPennington/break.git
   cd break
   ```
2. Ensure Python 3.12+ is installed.
3. Install optional dependencies:
   - For plotting: `pip install matplotlib`
   - No other external libraries are required for core functionality.

## Usage

### Interactive Mode
Run the script without arguments to enter interactive mode:
```
python break.py
```
- Follow prompts for mode (single/matrix/CSV), material, configuration, spacing, constants, and layers.
- Example: Select single calculation, pine, unpegged, 2 layers → Outputs force ~565.7 lbf, PSI ~226.3, correlated bones.

### CLI Mode
Use arguments for scripted runs:
```
python break.py --material pine --layers 2 --config unpegged
```
- Outputs: Layers: 2, Force: 565.7 lbf, PSI: 226.3  
  Correlated Bones: Clavicle, Skull (fracture), Ulna, Skull (crush)

#### Key Arguments
- `--material`: pine, paulownia, concrete (or custom from JSON).
- `--layers`: Number of layers (>=1, warning for >10).
- `--config`: pegged or unpegged (default: unpegged).
- `--spacing`: Custom spacing in mm for pegged.
- `--pencil`: Use 6.35 mm spacing for pegged.
- `--matrix`: Output table for 1-10 layers.
- `--all-csv <file>`: Generate CSV for all materials/configs.
- `--impact-time <float>`: Impact duration (default 0.005).
- `--contact-area <float>`: Contact area (default 2.5).
- `--scaling-exponent <float>`: Exponent for flexible unpegged (default 1.5).
- `--plot`: Generate force plot (matrix mode only, requires matplotlib).
- `--test`: Run unit tests.
- `--update-data`: Check data status (placeholder).

#### Examples
- Matrix for concrete pegged:
  ```
  python break.py --material concrete --config pegged --matrix --plot
  ```
  - Outputs table and saves `force_plot.png`.
- CSV generation:
  ```
  python break.py --all-csv breaking_matrix.csv
  ```
- Custom constants:
  ```
  python break.py --material pine --layers 3 --config unpegged --scaling-exponent 1.8
  ```

### Customizing Materials
Create `materials.json` in the script directory:
```json
{
  "pine": {"F1": 200, "m": 0.8, "type": "flexible"},
  "brick": {"F1": 600, "m": 6.0, "type": "brittle"}
}
```
- `F1`: Single-layer force (lbf).
- `m`: Mass (kg).
- `type`: flexible or brittle.

## Assumptions and Limitations
- Based on empirical data (e.g., ~200 lbf for single pine board).
- Flexible unpegged scaling adjusted to 1.5 exponent for realism (previously quadratic).
- Spacing assistance uses free-fall momentum; clamped for realism.
- No internet/package installation in code execution tools.
- For layers >10, approximations may be less accurate.

## Running Tests
```
python break.py --test
```
- Verifies core calculations (e.g., single pine: 200 lbf).

## References
- Physics of board breaking: [DonTow](https://www.dontow.com/2008/06/the-physics-of-martial-arts-breaking-boards/), Harvard/ITKD studies.
- Bone forces: [Discovery.com](https://www.discovery.com/science/force-to-break-bone).

## License
MIT License. See LICENSE file for details.

© 2025 GitHub, Inc.
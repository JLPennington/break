# Martial Arts Breaking Calculator

A command-line tool for estimating the force (in lbf) and pressure (in PSI) required to break stacks of materials commonly used in martial arts demonstrations, such as pine boards, paulownia boards, and concrete slabs. Now includes correlations to human bone breaking forces for educational comparison (e.g., ribs, femur, skull; approximations only, not medical advice). Supports pegged (spaced) and unpegged configurations, with options for custom spacing. Calculations are approximations based on empirical data and physics models.

## Features
- Calculate force and PSI for 1-10 layers of materials, with correlated human bones that could potentially break under similar force.
- Supports pegged (with spacing options: penny, pencil, or custom) and unpegged stacks.
- Interactive mode for easy use without arguments.
- Generate matrices for 1-10 layers in console or CSV format.
- Export a full matrix CSV for all materials and configurations.
- Material-specific models: flexible (wood) vs. brittle (concrete) for realistic scaling.

## Installation
Clone the repository and run the script with Python 3:

```bash
git clone https://github.com/yourusername/martial-arts-breaking-calculator.git
cd martial-arts-breaking-calculator
python breaking_calculator.py
```

No additional dependencies required beyond standard libraries (argparse, math, sys, csv).

## Usage

### Interactive Mode
Run without arguments:
```bash
python breaking_calculator.py
```

Follow the prompts to select mode, material, configuration, spacing, and layers.

### Command-Line Examples
- Single calculation for 2 layers of concrete, unpegged:
  ```bash
  python breaking_calculator.py --material concrete --layers 2 --config unpegged
  ```

- Matrix for pine, pegged with pencil spacing:
  ```bash
  python breaking_calculator.py --material pine --config pegged --pencil --matrix
  ```

- Generate CSV for all materials:
  ```bash
  python breaking_calculator.py --all-csv breaking_matrix.csv
  ```

## Models and Assumptions
- **Force Calculations**: Based on empirical breaking forces, scaled for stacks.
  - Unpegged: Quadratic for wood (beam theory), linear for concrete.
  - Pegged: Additive base with reduction from fragment assistance (momentum from falling pieces).
- **PSI**: Force divided by contact area (2.5 in², from strike biomechanics).
- **Bone Correlations**: Compares calculated force to approximate human bone breaking thresholds (e.g., ribs ~742 lbf, femur ~899 lbf); lists bones that could potentially fracture under equivalent force.
- Approximations only—actual breaking depends on technique, material quality, and safety gear. Use for educational purposes; consult experts for real training or medical advice.

## Contributing
Pull requests welcome! For major changes, open an issue first.

## License
MIT License. See LICENSE for details.
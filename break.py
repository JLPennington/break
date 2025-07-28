#python
import argparse
import math

# Assumptions:
# - Base forces (F1 in lbf) for single layer derived from empirical data:
#   - Pine: 200 lbf
#   - Paulownia (as poplar alternative): 100 lbf
#   - Concrete: 500 lbf
#   - Roof Tile: 270 lbf
# - Contact area A = 2.5 in² for PSI calculation (from biomechanical strike data).
# - For unpegged stacks: Force scales approximately linearly with layers due to dynamic impacts:
#   F_unpegged = F1 * (1 + 0.9 * (n - 1))
#   This fits empirical data better than quadratic beam theory for martial arts breaking.
# - For pegged stacks: Base force is additive F_pegged_base = F1 * n
#   However, spacing (h in mm) affects due to fragment assistance: broken pieces from upper layers fall and help break lower ones.
#   Assist per gap calculated as:
#     h_m = h / 1000  # mm to m
#     v = sqrt(2 * g * h_m)  # fall velocity, g=9.8 m/s²
#     p = m * v  # momentum, m in kg (material mass)
#     F_N = p / dt  # force in Newtons, dt=0.005 s (empirical impact duration from karate strikes)
#     F_lbf_assist = F_N / 4.448  # convert to lbf
#   Total F_pegged = F1 * n - (n - 1) * F_lbf_assist
#   This reduces force for larger h; for n=1, no assist.
#   Masses (m in kg) approximated from densities and dimensions:
#     - Pine: ~0.8 kg (12x12x0.75 inch, density ~450 kg/m³)
#     - Paulownia: ~0.5 kg (similar dimensions, density ~280 kg/m³)
#     - Concrete: 5.5 kg (16x8x1.625 inch slab, empirical ~12 lb for breaking)
#     - Tile: 2.7 kg (~12x12 inch terracotta, ~6 lb)
#   Note: Assist can't make F negative; clamped to max( F1 * n * 0.5, F ) for realism.
# - Default spacing: US penny (1.52 mm)
# - Carpenter pencil: 6.35 mm
# - For very small h (<1 mm), assist negligible, but may approach unpegged if too small; not modeled here as typical h >=1.5 mm.
# - Calculations are approximations; actual breaking varies with technique, material variability (±20-30%).
# - PSI = F / A

MATERIALS = {
    'pine': {'F1': 200, 'm': 0.8},
    'paulownia': {'F1': 100, 'm': 0.5},
    'concrete': {'F1': 500, 'm': 5.5},
    'tile': {'F1': 270, 'm': 2.7},
}

G = 9.8  # m/s²
DT = 0.005  # s
A = 2.5  # in²
N_TO_LBF = 1 / 4.448  # conversion factor

def calculate_force(material_data, n, config, spacing=None):
    F1 = material_data['F1']
    m = material_data['m']
    
    if config == 'unpegged':
        # Unpegged force calculation: F = F1 * (1 + 0.9 * (n - 1))
        return F1 * (1 + 0.9 * (n - 1))
    
    elif config == 'pegged':
        # Base pegged: F = F1 * n
        F_base = F1 * n
        if n == 1 or spacing is None or spacing <= 0:
            return F_base
        # Assist per gap
        h_m = spacing / 1000.0  # mm to m
        v = math.sqrt(2 * G * h_m)  # v = sqrt(2gh)
        p = m * v  # p = m * v
        F_N = p / DT  # F = p / dt in N
        F_lbf_assist = F_N * N_TO_LBF  # to lbf
        # Total reduction: (n-1) * assist (approximate cumulative help)
        reduction = (n - 1) * F_lbf_assist
        # Clamp to prevent negative or unrealistic low
        F = max(F_base - reduction, F1 * max(1, n * 0.5))
        return F

def print_result(n, force, psi):
    print(f"Layers: {n}, Force: {force:.1f} lbf, PSI: {psi:.1f}")

def print_matrix(material_data, config, spacing=None):
    print(f"Matrix for {config} ({'spacing ' + str(spacing) + ' mm' if config == 'pegged' and spacing else ''}):")
    print("| Layers | Force (lbf) | PSI |")
    print("|---|---|---|")
    for n in range(1, 11):
        force = calculate_force(material_data, n, config, spacing)
        psi = force / A
        print(f"| {n} | {force:.1f} | {psi:.1f} |")

def main():
    parser = argparse.ArgumentParser(description="CLI tool to calculate breaking force and PSI for martial arts materials.")
    parser.add_argument('--material', required=True, choices=['pine', 'paulownia', 'concrete', 'tile'], help="Material type.")
    parser.add_argument('--layers', type=int, default=1, help="Number of layers (1-10). Ignored if --matrix.")
    parser.add_argument('--config', default='unpegged', choices=['pegged', 'unpegged'], help="Configuration: pegged or unpegged.")
    parser.add_argument('--spacing', type=float, default=None, help="Spacing in mm for pegged (overrides defaults).")
    parser.add_argument('--pencil', action='store_true', help="Use carpenter pencil spacing (6.35 mm) for pegged.")
    parser.add_argument('--matrix', action='store_true', help="Generate matrix for 1-10 layers instead of single calculation.")
    
    args = parser.parse_args()
    
    if args.layers < 1 or args.layers > 10:
        print("Error: Layers must be between 1 and 10.")
        return
    
    material_data = MATERIALS[args.material]
    
    spacing = None
    if args.config == 'pegged':
        if args.spacing is not None:
            spacing = args.spacing
        elif args.pencil:
            spacing = 6.35
        else:
            spacing = 1.52  # default penny
    
    if args.matrix:
        print_matrix(material_data, args.config, spacing)
    else:
        force = calculate_force(material_data, args.layers, args.config, spacing)
        psi = force / A
        print_result(args.layers, force, psi)

if __name__ == "__main__":
    main()
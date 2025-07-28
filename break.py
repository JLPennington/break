
import argparse
import math
import sys
import csv

# Assumptions (Updated as of July 28, 2025; no major changes in standards from empirical data and EN 538 for tiles):
# - Base forces (F1 in lbf) for single layer derived from empirical data:
#   - Pine: 200 lbf (adjusted from initial 150 based on dynamic tests; aligns with ~1,100 N averages for 0.75" pine)
#   - Paulownia (as poplar alternative): 100 lbf (scaled via MOR ratio ~0.5-0.7 vs. pine; density 280-300 kg/m³)
#   - Concrete: 500 lbf (empirical range 300-1,100 lbf; average for low-density patio slabs)
# - Contact area A = 2.5 in² for PSI calculation (from biomechanical strike data).
# - Materials classified as 'flexible' (wood: pine, paulownia) or 'brittle' (concrete) to model differences in breaking behavior.
# - For unpegged stacks: Force scales with square for flexible (beam theory approximation for dynamic impacts), linear for brittle:
#   Flexible: F_unpegged = F1 * n**2
#   Brittle: F_unpegged = F1 * n
#   This makes unpegged harder than pegged for flexible (empirical for boards), similar or slightly harder for brittle.
# - For pegged stacks: Base force is additive F_pegged_base = F1 * n
#   For all, spacing affects due to fragment assistance, but stronger for brittle:
#   Assist per gap calculated as before, but multiplied by factor: 0.5 for flexible, 1.0 for brittle (less assistance as wood fragments less effective).
#   Total F_pegged = F1 * n - (n - 1) * F_lbf_assist * factor
#   This reduces force more for brittle, ensuring pegged < unpegged for all, but with nuanced differences.
#   Masses (m in kg) approximated from densities and dimensions (verified with 2025 sources):
#     - Pine: ~0.8 kg (12x12x0.75 inch, density ~450 kg/m³)
#     - Paulownia: ~0.5 kg (similar dimensions, density ~280 kg/m³)
#     - Concrete: 5.5 kg (16x8x1.625 inch slab, empirical ~12 lb for breaking)
#   Note: Assist can't make F negative; clamped to max( F1 * n * 0.5, F ) for realism.
# - Default spacing: US penny (1.52 mm)
# - Carpenter pencil: 6.35 mm
# - For very small h (<1 mm), assist negligible, but may approach unpegged if too small; not modeled here as typical h >=1.5 mm.
# - Calculations are approximations; actual breaking varies with technique, material quality (±20-30%).
# - PSI = F / A
# - Bone correlations: After calculating force, compare to average breaking forces for human bones (healthy adult; approximations only, vary by individual factors like age, density).
#   Bone data (lbf): Ribs (742), Femur (899), Skull (517 crush/196 fracture), Humerus (787), Tibia (900), Clavicle (147), Ulna (337).
#   Outputs bones where material force >= bone force (could potentially break that bone; for educational purposes only, not medical advice).

MATERIALS_DICT = {
    'pine': {'F1': 200, 'm': 0.8, 'type': 'flexible'},
    'paulownia': {'F1': 100, 'm': 0.5, 'type': 'flexible'},
    'concrete': {'F1': 500, 'm': 5.5, 'type': 'brittle'},
}

MATERIAL_MAP = {
    '1': MATERIALS_DICT['pine'],
    '2': MATERIALS_DICT['paulownia'],
    '3': MATERIALS_DICT['concrete'],
}

BONE_DATA = {
    'Clavicle': 147,
    'Skull (fracture)': 196,
    'Ulna': 337,
    'Skull (crush)': 517,
    'Ribs': 742,
    'Humerus': 787,
    'Femur': 899,
    'Tibia': 900,
}

G = 9.8  # m/s²
DT = 0.005  # s
A = 2.5  # in²
N_TO_LBF = 1 / 4.448  # conversion factor

def calculate_force(material_data, n, config, spacing=None):
    F1 = material_data['F1']
    m = material_data['m']
    mat_type = material_data['type']
    
    if config == 'unpegged':
        if mat_type == 'flexible':
            return F1 * (n ** 2)
        else:
            return F1 * n
    
    elif config == 'pegged':
        F_base = F1 * n
        if n == 1 or spacing is None or spacing <= 0:
            return F_base
        h_m = spacing / 1000.0  # mm to m
        v = math.sqrt(2 * G * h_m)  # v = sqrt(2gh)
        p = m * v  # p = m * v
        F_N = p / DT  # F = p / dt in N
        F_lbf_assist = F_N * N_TO_LBF  # to lbf
        factor = 0.5 if mat_type == 'flexible' else 1.0
        reduction = (n - 1) * F_lbf_assist * factor
        F = max(F_base - reduction, F1 * max(1, n * 0.5))
        return F

def get_correlated_bones(force):
    bones = [bone for bone, bone_force in BONE_DATA.items() if force >= bone_force]
    return ', '.join(bones) if bones else 'None (below typical bone breaking thresholds)'

def print_result(n, force, psi):
    print(f"Layers: {n}, Force: {force:.1f} lbf, PSI: {psi:.1f}")
    print(f"Correlated Bones (could potentially break): {get_correlated_bones(force)}")
    print("(Note: Bone data approximations for healthy adults; not medical advice.)")

def print_matrix(material_data, config, spacing=None):
    print(f"Matrix for {config} ({'spacing ' + str(spacing) + ' mm' if config == 'pegged' and spacing else ''}):")
    print("| Layers | Force (lbf) | PSI | Correlated Bones |")
    print("|---|---|---|---|")
    for n in range(1, 11):
        force = calculate_force(material_data, n, config, spacing)
        psi = force / A
        bones = get_correlated_bones(force)
        print(f"| {n} | {force:.1f} | {psi:.1f} | {bones} |")

def generate_csv(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Material', 'Config', 'Spacing_mm', 'Layers', 'Force_lbf', 'PSI', 'Correlated_Bones'])
        for mat_name, material_data in MATERIALS_DICT.items():
            for config in ['pegged', 'unpegged']:
                spacing = 1.52 if config == 'pegged' else None
                spacing_str = spacing if spacing else 'N/A'
                for n in range(1, 11):
                    force = calculate_force(material_data, n, config, spacing)
                    psi = force / A
                    bones = get_correlated_bones(force)
                    writer.writerow([mat_name, config, spacing_str, n, round(force, 1), round(psi, 1), bones])

def interactive_mode():
    print("Martial Arts Breaking Calculator")
    print("This tool calculates force and PSI for breaking materials.")
    print("Select mode:")
    print("1. single calculation (default)")
    print("2. matrix (1-10 layers)")
    print("3. CSV matrix for all materials")
    mode_choice = input("Enter number (1-3) [default 1]: ").strip() or '1'
    while mode_choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter 1-3.")
        mode_choice = input("Enter number (1-3): ").strip()
    
    if mode_choice == '3':
        filename = input("Enter CSV filename [default: breaking_matrix.csv]: ").strip() or 'breaking_matrix.csv'
        generate_csv(filename)
        return
    
    print("\nSelect material by number:")
    print("1. pine")
    print("2. paulownia")
    print("3. concrete")
    
    material_choice = input("Enter number (1-3): ").strip() or ''
    while material_choice not in ['1', '2', '3']:
        print("Invalid choice. Please enter 1-3.")
        material_choice = input("Enter number (1-3): ").strip()
    
    print("\nSelect configuration:")
    print("1. pegged")
    print("2. unpegged (default)")
    config_choice = input("Enter number (1-2) [default 2]: ").strip() or '2'
    while config_choice not in ['1', '2']:
        print("Invalid choice. Please enter 1-2.")
        config_choice = input("Enter number (1-2): ").strip()
    config = {'1': 'pegged', '2': 'unpegged'}[config_choice]
    
    spacing = None
    if config == 'pegged':
        print("\nSelect spacing:")
        print("1. penny (1.52 mm, default)")
        print("2. pencil (6.35 mm)")
        print("3. custom")
        spacing_choice = input("Enter number (1-3) [default 1]: ").strip() or '1'
        while spacing_choice not in ['1', '2', '3']:
            print("Invalid choice. Please enter 1-3.")
            spacing_choice = input("Enter number (1-3): ").strip()
        if spacing_choice == '1':
            spacing = 1.52
        elif spacing_choice == '2':
            spacing = 6.35
        elif spacing_choice == '3':
            while True:
                try:
                    spacing = float(input("Enter custom spacing in mm: "))
                    break
                except ValueError:
                    print("Invalid number. Please enter a float.")
    
    material_data = MATERIAL_MAP[material_choice]
    
    if mode_choice == '2':
        print_matrix(material_data, config, spacing)
    else:
        while True:
            layers_str = input("\nEnter number of layers (1-10) [default: 1]: ").strip() or '1'
            try:
                layers = int(layers_str)
                if 1 <= layers <= 10:
                    break
                print("Layers must be between 1 and 10.")
            except ValueError:
                print("Invalid number. Please enter an integer.")
        
        force = calculate_force(material_data, layers, config, spacing)
        psi = force / A
        print_result(layers, force, psi)

def main():
    parser = argparse.ArgumentParser(description="CLI tool to calculate breaking force and PSI for martial arts materials.")
    parser.add_argument('--material', choices=['pine', 'paulownia', 'concrete'], help="Material type.")
    parser.add_argument('--layers', type=int, default=1, help="Number of layers (1-10). Ignored if --matrix or --all-csv.")
    parser.add_argument('--config', default='unpegged', choices=['pegged', 'unpegged'], help="Configuration: pegged or unpegged.")
    parser.add_argument('--spacing', type=float, default=None, help="Spacing in mm for pegged (overrides defaults).")
    parser.add_argument('--pencil', action='store_true', help="Use carpenter pencil spacing (6.35 mm) for pegged.")
    parser.add_argument('--matrix', action='store_true', help="Generate matrix for 1-10 layers instead of single calculation.")
    parser.add_argument('--all-csv', type=str, help="Generate CSV matrix for all materials pegged/unpegged to the specified file.")
    
    args = parser.parse_args()
    
    if args.all_csv:
        generate_csv(args.all_csv)
        return
    
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    if args.layers < 1 or args.layers > 10:
        print("Error: Layers must be between 1 and 10.")
        return
    
    if args.material is None:
        print("Error: --material is required when using command-line arguments (except for --all-csv).")
        parser.print_help()
        return
    
    material_data = MATERIALS_DICT[args.material]
    
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
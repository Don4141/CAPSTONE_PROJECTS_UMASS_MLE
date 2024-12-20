import os
import csv

# Directory containing the energies_*.txt files
input_dir = "./PositionScanOut"
output_csv = "./combined_energies_differences.csv"

# Header for the output CSV
header = [
    "Mutation", "dTotal_Energy", "dBackbone_Hbond", "dSidechain_Hbond", "dVan_der_Waals", "dElectrostatics",
    "dSolvation_Polar", "dSolvation_Hydrophobic", "dVan_der_Waals_Clashes", "dEntropy_Sidechain",
    "dEntropy_Mainchain", "dShort_Loop_Entropy", "dMedium_Loop_Entropy", "dCis_Bond", "dTorsional_Clash",
    "dBackbone_Clash", "dHelix_Dipole", "dWater_Bridge", "dDisulfide", "dElectrostatic_kon",
    "dPartial_Covalent_Bonds", "dIonization_Energy", "dEntropy_Complex"
]

# Create the output CSV file and write the header
with open(output_csv, mode="w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # Iterate through all energies_*.txt files in the directory
    for filename in os.listdir(input_dir):
        if filename.startswith("energies_") and filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)

            # Read the file contents
            with open(file_path, "r") as file:
                lines = file.readlines()

                # Ensure there are at least two rows (WTref and Mutant)
                if len(lines) < 2:
                    print(f"Skipping {filename}: insufficient data.")
                    continue

                # Extract WTref and Mutant rows
                wt_values = lines[0].strip().split("\t")
                mut_values = lines[1].strip().split("\t")

                # Extract mutation name and energy values
                mutation_name = mut_values[0]
                wt_energy_values = list(map(float, wt_values[1:]))
                mut_energy_values = list(map(float, mut_values[1:]))

                # Calculate the differences between Mutant and WTref
                differences = [mut - wt for mut, wt in zip(mut_energy_values, wt_energy_values)]

                # Write the mutation name and differences to the output CSV
                writer.writerow([mutation_name] + differences)

print(f"Combined CSV with differences written to {output_csv}")

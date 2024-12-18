#!/bin/bash

# Directory containing the Raw files
input_dir="./BuildModel"

# Output CSV file
output_file="./combined_output2.csv"

# Add header to the output file
echo "Pdb,Total_energy,Backbone_Hbond,Sidechain_Hbond,Van_der_Waals,Electrostatics,Solvation_Polar,Solvation_hydrophobic,Van_der_Waals_clashes,Entropy_sidechain,Entropy_mainchain,sloop_entropy,mloop_entropy,Cis_bond,Torsional_clash,Backbone_clash,Helix_dipole,Water_bridge,Disulfide,Electrostatic_kon,Partial_covalent_bonds,Energy_Ionisation,Entropy_complex" > "$output_file"

# Iterate through each Raw_*.fxout file in the directory
for file in "$input_dir"/Raw_*.fxout; do
    # Extract only the lines containing actual data and append them to the output file
    awk '/Pdb/{flag=1; next} /Jesper Borg/{flag=0} flag' "$file" | \
    sed 's/[[:space:]]\+/,/g' >> "$output_file"
done

echo "Combined CSV file created at $output_file"

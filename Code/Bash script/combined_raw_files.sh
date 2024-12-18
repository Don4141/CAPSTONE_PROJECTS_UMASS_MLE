#!/bin/bash

# Directory containing the Raw files
input_dir="./BuildModel"

# Output CSV file
output_file="./combined_output2.csv"

# Add header to the output file
echo "Pdb,total energy,Backbone Hbond,Sidechain Hbond,Van der Waals,Electrostatics,Solvation Polar,Solvation Hydrophobic,Van der Waals clashes,entropy sidechain,entropy mainchain,sloop_entropy,mloop_entropy,cis_bond,torsional clash,backbone clash,helix dipole,water bridge,disulfide,electrostatic kon,partial covalent bonds,energy Ionisation,Entropy Complex" > "$output_file"

# Iterate through each Raw_*.fxout file in the directory
for file in "$input_dir"/Raw_*.fxout; do
    # Extract only the lines containing actual data and append them to the output file
    awk '/Pdb/{flag=1; next} /Jesper Borg/{flag=0} flag' "$file" | \
    sed 's/[[:space:]]\+/,/g' >> "$output_file"
done

echo "Combined CSV file created at $output_file"

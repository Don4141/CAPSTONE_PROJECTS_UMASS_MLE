#!/bin/bash

# Define file paths
txt_file="/home/sadjei65320/UMASS_CapstoneProject/src/uniprot_results.txt"
csv_file="/home/sadjei65320/UMASS_CapstoneProject/src/compiled.csv"

# Prepare the output file
echo "PDB_ID" > "$csv_file"

# Read through the text file line by line
while IFS= read -r line; do
    # Extract the gene name and identifier
    gene_name=$(echo "$line" | awk -F': ' '{print $1}')
    identifier=$(echo "$line" | awk -F', ' '{print $1}' | cut -d' ' -f2)

    # Check if this gene name is in the csv file
    if grep -q "$gene_name" "$csv_file"; then
        # Construct the PDB ID
        pdb_id="AF-${identifier}-F1-model_v1.pdb"

        # Append the PDB ID to the output file
        echo "$pdb_id" >> "$csv_file"
    fi
done < "$txt_file"

echo "Processing complete. Output appended to $csv_file."

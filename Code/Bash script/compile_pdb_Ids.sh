#!/bin/bash

# Define file paths
txt_file="/home/sadjei65320/UMASS_CapstoneProject/src/uniprot_results.txt"
compile_file="/home/sadjei65320/UMASS_CapstoneProject/src/compiled.txt"

# Prepare the output file
echo "PDB_ID" > "$compile_file"

# Read through the text file line by line
while IFS= read -r line; do
    # Extract the gene name and identifier
    gene_name=$(echo "$line" | awk -F': ' '{print $1}')
    identifier=$(echo "$line" | awk -F', ' '{print $1}' | cut -d' ' -f2)

    # Count occurrences of the gene name in the compile file
    count=$(awk -v gene="$gene_name" -F',' '{if ($1 == gene) count++ } END { print count+0 }' "$compile_file")

    echo "Processing $gene_name: found $count occurrences"

    # Only proceed if the gene name was found in the text file
    if [[ $count -gt 0 ]]; then
        # Construct the PDB ID
        pdb_id="AF-${identifier}-F1-model_v1"

        # Append PDB ID to the compile file as many times as it appears in the text file
        for (( i=0; i<count; i++ )); do
            echo "$pdb_id" >> "$compile_file"
        done
    fi
done < "$txt_file"

echo "Processing complete. Output appended to $compile_file."

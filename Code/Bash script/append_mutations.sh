#!/bin/bash

# Input files
af_rows_file="./AF_rows.csv"
output_file="./AF_rows_with_variants.csv"
mutation_dir="./"  # Directory containing *_mutations.txt files

# Ensure the input file exists
if [ ! -f "$af_rows_file" ]; then
    echo "Input file not found: $af_rows_file"
    exit 1
fi

# Add a "variant" column header to the output file
header=$(head -n 1 "$af_rows_file")
echo "$header,variant" > "$output_file"

# Process each row in AF_rows.csv, skipping the header
tail -n +2 "$af_rows_file" | while IFS=, read -r pdb_row; do
    # Extract the base name of the PDB file up to "_v1"
    pdb_truncated=$(echo "$pdb_row" | grep -oE '.*_v1')
    mutation_file="${mutation_dir}/${pdb_truncated}_mutations.txt"

    # Check if the mutation file exists
    if [ -f "$mutation_file" ]; then
        # Read the mutations from the file
        mutations=($(cat "$mutation_file"))
        # Get the index of the PDB file to fetch the corresponding mutation
        index=$(echo "$pdb_row" | grep -o -E '_[0-9]+\.pdb' | grep -o -E '[0-9]+')
        mutation="${mutations[$((index - 1))]}"
    else
        mutation=""
    fi

    # Append the row with the mutation to the output file
    echo "$pdb_row,$mutation" >> "$output_file"
done

echo "AF_rows.csv updated with variants and saved to $output_file"

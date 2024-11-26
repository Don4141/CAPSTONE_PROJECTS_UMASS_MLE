#!/bin/bash

# Define the input and output file paths
input_file="./TrainBenign.txt"
output_file="./TrainBenign_out2.txt"

awk -F, -v OFS=',' '
{
    # Skip the specific line "PDB_ID,A,POS,REF,ALT"
    if ($1 == "PDB_ID" && $2 == "A" && $3 == "POS" && $4 == "REF" && $5 == "ALT") {
        next
    }

    # Print the original first column, new "Chain" column with "A", and the rest of the columns
    print $1, "A", $2, $3, $4
}' "$input_file" > "$output_file"

echo "The 'Chain' column has been added and the specific line has been excluded. Results are saved in $output_file."

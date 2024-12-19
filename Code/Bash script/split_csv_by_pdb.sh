#!/bin/bash

# Input file
input_file="./combined_output2.csv"

# Output files
wt_output_file="./WT_rows.csv"
af_output_file="./AF_rows.csv"

# Ensure the input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file not found: $input_file"
    exit 1
fi

# Extract the header
header=$(head -n 1 "$input_file")

# Create the WT output file with the header
echo "$header" > "$wt_output_file"
# Extract rows starting with WT and append to the WT output file
awk -F, '$1 ~ /^WT/' "$input_file" >> "$wt_output_file"

# Create the AF output file with the header
echo "$header" > "$af_output_file"
# Extract rows starting with AF and append to the AF output file
awk -F, '$1 ~ /^AF/' "$input_file" >> "$af_output_file"

echo "WT rows saved to $wt_output_file"
echo "AF rows saved to $af_output_file"

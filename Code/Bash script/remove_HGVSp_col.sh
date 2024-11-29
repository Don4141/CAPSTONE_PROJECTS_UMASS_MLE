#!/bin/bash

# Define the input and output file paths
input_file="./training_benign.txt"
output_file="./TrainBenign.txt"

# Process the file
awk -F, '{
    # Start output with the second column
    out = $2;
    # Loop through the remaining columns and append them to 'out'
    for (i = 3; i <= NF; i++) {
        out = out "," $i;
    }
    # Print the output line
    print out;
}' "$input_file" > "$output_file"

echo "The first column has been removed. Results are saved in $output_file."

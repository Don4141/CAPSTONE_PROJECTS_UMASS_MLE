#!/bin/bash

# Define the input file path
input_file="./processed_SIGMA.txt"

# Define the output files for each category
training_benign="./SplitSIGMA/training_benign.txt"
training_pathogenic="./SplitSIGMA/training_pathogenic.txt"
test_benign="./SplitSIGMA/test_benign.txt"
test_pathogenic="./SplitSIGMA/test_pathogenic.txt"

# Header extraction and write headers to each file
header=$(head -1 "$input_file")
echo "$header" > "$training_benign"
echo "$header" > "$training_pathogenic"
echo "$header" > "$test_benign"
echo "$header" > "$test_pathogenic"

# Read the input file line by line excluding the header
tail -n +2 "$input_file" | while IFS= read -r line; do
    # Determine the category and write the line to the appropriate file
    train_test_label=$(echo "$line" | awk -F'\t' '{print $3}') # Adjust the column number if necessary
    class=$(echo "$line" | awk -F'\t' '{print $4}')            # Adjust the column number if necessary

    if [[ "$train_test_label" == "Training" && "$class" == "Benign" ]]; then
        echo "$line" >> "$training_benign"
    elif [[ "$train_test_label" == "Training" && "$class" == "Pathogenic" ]]; then
        echo "$line" >> "$training_pathogenic"
    elif [[ "$train_test_label" == "Test" && "$class" == "Benign" ]]; then
        echo "$line" >> "$test_benign"
    elif [[ "$train_test_label" == "Test" && "$class" == "Pathogenic" ]]; then
        echo "$line" >> "$test_pathogenic"
    fi
done

echo "Files have been created:"
echo "  - $training_benign"
echo "  - $training_pathogenic"
echo "  - $test_benign"
echo "  - $test_pathogenic"

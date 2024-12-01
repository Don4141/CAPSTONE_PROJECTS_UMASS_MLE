from collections import defaultdict

def split_file_by_category(input_file):
    # Create a dictionary to hold lines for each category
    data = defaultdict(list)

    # Read the input file and group lines by the first column
    with open(input_file, 'r') as file:
        for line in file:
            if line.strip():  # Skip empty lines
                # Split the line into columns
                columns = line.split()
                # The first column is the category
                category = columns[0]
                # Join the remaining columns without spaces
                rest_of_line = ''.join(columns[1:])
                # Append the processed line to the appropriate category list
                data[category].append(rest_of_line)

    # Write each group of lines to a separate file named after the category
    for category, lines in data.items():
        # Remove '.pdb' and append '_mutations.txt'
        category_base = category.replace('.pdb', '')
        output_file = f"{category_base}_mutations.txt"
        with open(output_file, 'w') as file:
            file.write("\n".join(lines))

    print("Data has been split into separate files with '_mutations.txt' extension.")

# Specify the input file path
input_file = "./TrainPathogenic.txt"  # Replace with your actual input file path
split_file_by_category(input_file)

import pandas as pd

# Map of single-letter amino acids to three-letter codes
amino_acid_map = {
    "A": "ALA", "R": "ARG", "N": "ASN", "D": "ASP", "C": "CYS",
    "E": "GLU", "Q": "GLN", "G": "GLY", "H": "HIS", "I": "ILE",
    "L": "LEU", "K": "LYS", "M": "MET", "F": "PHE", "P": "PRO",
    "S": "SER", "T": "THR", "W": "TRP", "Y": "TYR", "V": "VAL"
}

# Read the CSV file
input_csv = "./AF_rows_with_variants.csv"  # Replace with your actual file name
df = pd.read_csv(input_csv)

# Function to modify the Pdb name
def modify_pdb(row):
    variant = row['variant']
    if pd.notnull(variant) and ";" in variant:
        # Extract numeric position and the last amino acid
        position = ''.join(filter(str.isdigit, variant))
        aa_code = amino_acid_map.get(variant[-2], "")
        return f"{aa_code}_{position}_{row['Pdb']}"
    return row['Pdb']

# Apply the modification to the Pdb column
df['Pdb'] = df.apply(modify_pdb, axis=1)

# Save the modified DataFrame to a new CSV file
output_csv = "./modified_AF_rows_with_variants.csv"
df.to_csv(output_csv, index=False)

print(f"Modified file saved to {output_csv}")

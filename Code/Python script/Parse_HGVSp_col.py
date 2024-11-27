import os
import re
import pandas as pd

# Conversion dictionary from three-letter to one-letter code
conversion = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D',
    'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
    'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S',
    'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

def process_location_column(input_file, out_file):
    """Extract Reference residue, Reference position, and Alt residue from Location column and convert them."""
    # Load the data
    df = pd.read_csv(input_file, sep='\t')
    
    # Function to split the Location column
    def split_location(location):
        match = re.match(r'NP_\d+\.\d+:p\.([A-Za-z]{3})(\d+)([A-Za-z]{3})', location)
        if match:
            ref_res = conversion.get(match.group(1), None)
            position = match.group(2)
            alt_res = conversion.get(match.group(3), None)
            return pd.Series([ref_res, position, alt_res])
        return pd.Series([None, None, None])
    
    # Apply the function to create new columns
    df[['Reference residue', 'Reference position', 'Alt residue']] = df['Location'].apply(split_location)
    
    # Save the updated dataframe back to a new file
    df.to_csv(out_file, index=False, sep='\t')

if __name__ == "__main__":
    input_file = "./subset_dt.txt"  # Path to your input file
    out_file = "./processed_subset_dt.txt"  # Path to save the processed file

    process_location_column(input_file, out_file)

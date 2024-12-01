import csv
import os
from Bio.PDB import PDBParser

def three_letter_code(one_letter_code):
    """Convert one-letter amino acid code to three-letter code."""
    conversion = {
        'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP',
        'C': 'CYS', 'E': 'GLU', 'Q': 'GLN', 'G': 'GLY',
        'H': 'HIS', 'I': 'ILE', 'L': 'LEU', 'K': 'LYS',
        'M': 'MET', 'F': 'PHE', 'P': 'PRO', 'S': 'SER',
        'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL'
    }
    return conversion.get(one_letter_code.upper(), None)

def find_chain(pdb_file, position, residue):
    """Find the chain of a residue at a given position in a PDB file."""
    parser = PDBParser()
    structure = parser.get_structure("PDB", pdb_file)
    for model in structure:
        for chain in model:
            for res in chain:
                if res.get_id()[1] == position and res.get_resname() == three_letter_code(residue):
                    return chain.id
    return None

def process_mutations(input_file, pdb_dir):
    with open(input_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        print("Detected fieldnames:", reader.fieldnames)  # Debugging line to print fieldnames
        for row in reader:
            print("Current row:", row)  # Additional debug to see rows
            try:
                pdb_id = row['PDB_ID']
                # Further processing...
            except KeyError as e:
                print(f"Key error: {e} - this key is not in the row dictionary. Available keys: {row.keys()}")
            position = int(row['POS'])
            ref_residue = row['REF']
            mutant_residue = row['ALT']
            pdb_file = os.path.join(pdb_dir, f"{pdb_id}")
            
            if os.path.exists(pdb_file):
                chain = find_chain(pdb_file, position, ref_residue)
                if chain:
                    print(f"Chain found: {chain} for {pdb_id} at position {position}")
                else:
                    print(f"No chain found for {pdb_id} at position {position}")
            else:
                print(f"File not found: {pdb_file}")

if __name__ == "__main__":
    input_csv = "./compile.txt"  # This txt should contain columns: PDB_ID, Position, Reference_Residue, Mutant_Residue
    pdb_dir = "./downloaded_structures"  # Ensure this directory contains your PDB files
    process_mutations(input_csv, pdb_dir)

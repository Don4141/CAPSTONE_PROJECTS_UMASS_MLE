import os
import requests

def download_alphafold_structure(uniprot_id, output_dir):
    """Download an AlphaFold predicted structure for a given UniProt ID."""
    base_url = "https://alphafold.ebi.ac.uk/files/"
    pdb_filename = f"AF-{uniprot_id}-F1-model_v1.pdb"
    url = f"{base_url}{pdb_filename}"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(output_dir, pdb_filename), 'wb') as f:
            f.write(response.content)
        return f"Downloaded {pdb_filename}"
    else:
        return f"Failed to download PDB for {uniprot_id}: Status code {response.status_code}"

def process_uniprot_ids(input_file, output_dir):
    """Process a list of UniProt IDs to download corresponding AlphaFold structures."""
    with open(input_file, 'r') as file:
        uniprot_ids = file.read().splitlines()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    results = []
    for uniprot_id in uniprot_ids:
        result = download_alphafold_structure(uniprot_id, output_dir)
        results.append(result)

    return results

if __name__ == "__main__":
    input_file = "../parse_uniprot_ids/accession_num.txt"  # File containing UniProt IDs
    output_dir = "./downloaded_structures"  # Directory to store downloaded PDB files
    results = process_uniprot_ids(input_file, output_dir)
    for result in results:
        print(result)

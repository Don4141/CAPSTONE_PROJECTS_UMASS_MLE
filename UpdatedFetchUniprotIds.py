import requests

def fetch_uniprot_info(protein_name):
    """Fetch the UniProt accession number and entry name for a given protein or gene name.
       The script read gene names from input_genes.txt, fetch their corresponding Uniprot IDs and entry name using UniProt REST API,
       and output the results to uniprot_results2.txt.
    """
    url = f"https://rest.uniprot.org/uniprotkb/search?query=gene_exact:{protein_name} AND reviewed:true&fields=accession,id&format=tsv" #Constructs a URL to query Uniprot database with given gene name and fetches Uniprot ID if available.
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split('\n')
        if len(lines) > 2 and lines[1].strip():
            data = lines[1].split('\t')
            return data[0].strip(), data[1].strip()  # Return both the UniProt accession and the entry name
        else:
            return None, f"No results found for {protein_name}."
    else:
        return None, f"Failed to fetch data for {protein_name}: Status code {response.status_code}, Response: {response.text}"

def process_gene_names(input_file, output_file):
    with open(input_file, 'r') as file:
        gene_names = file.read().splitlines()
    
    results = []
    for gene_name in gene_names:
        accession, entry_name = fetch_uniprot_info(gene_name)
        if accession and entry_name:
            results.append(f"{gene_name}: {accession}, Entry Name: {entry_name}")
        else:
            results.append(f"{gene_name}: {entry_name}")

    with open(output_file, 'w') as file:
        file.write('\n'.join(results))

if __name__ == "__main__":
    input_file = "./input_genes.txt"  # File where gene names are listed
    output_file = "./uniprot_results2.txt"  # File to output the UniProt IDs and entry names
    process_gene_names(input_file, output_file)
    print(f"Results have been written to {output_file}.")

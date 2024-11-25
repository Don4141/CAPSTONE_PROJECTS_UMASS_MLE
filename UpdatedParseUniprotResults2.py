import os

def process_uniprot_ids(input_file, out_file):
    """Extract gene names, accession names, and uniprot names from uniprot_ids file."""
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Prepare output files
    with open(f"{out_file}/gene_name.txt", "w") as gene_name_file, \
         open(f"{out_file}/accession_num.txt", "w") as accession_num_file, \
         open(f"{out_file}/uniprot_ids.txt", "w") as uniprot_ids_file:

        for line in lines:
            if not line.strip():
                continue  # Skip any empty lines

            # Skip known error messages
            if "Failed to fetch data" in line or "Status code" in line or "Error messages" in line:
                print(f"Skipping error line: {line.strip()}")
                continue

            parts = line.split(", Entry Name: ")
            if len(parts) != 2:
                print(f"Skipping malformed line: {line.strip()}")
                continue

            gene_info = parts[0].split(": ")
            if len(gene_info) != 2:
                print(f"Skipping malformed gene info: {parts[0].strip()}")
                continue

            gene_name = gene_info[0].strip()
            accession_num = gene_info[1].strip()
            uniprot_id = parts[1].strip()

            gene_name_file.write(gene_name + "\n")
            accession_num_file.write(accession_num + "\n")
            uniprot_ids_file.write(uniprot_id + "\n")

if __name__ == "__main__":
    input_file = "./uniprot_results.txt"  # This txt should contain columns: Gene name:Accession number, Entry Name:Uniprot name
    out_file = "./parse_uniprot_ids"  # Ensure this directory contains the various components in the file

    if not os.path.exists(out_file):
        os.makedirs(out_file)

    process_uniprot_ids(input_file, out_file)
    print(f"Results have been written to {out_file}.")

#Capstone projects for Machine Learning Engineering and AI bootcamp at UMASS Global

The original dataset from SIGMA publication has 7 columns, namely HGVSc, HGVSp, Location, SYMBOL, Laste Evaluated, Train_Test Lable, and Class. The first two columns provides information about the variants under study including the coding DNA sequence of variants, and 

the protein-level confidence,respectively. The third column is the genomic location of the variants, followed by the gene names associated with the variants. The last three columns include the dates the variants were recorded, the context in which the data was used and 

the clinical significance of each of the variants, respectively. The columns of interest in this study include HGVSp, the dataset-classifications, their clinical significance, and the gene names. 

Let's extract the reference residues, their positions within their protein sequences, and their mutant/alternative residues from HGVSp column. We will append the new columns to the same dataset. Use the python script parse_HGVSp_col.py for this purpose.

Now, we don't need the HGVSp, Train_Test Lable and Class column anymore, let's write a bash script to remove this column. Use the bash script remove_HGVSp_col.sh 

The first tool to install is FoldX. This is a computational tool widely used in the field of bioinformatics and computational biology for analyzing the stability of proteins and their complexes. 

Foldx enables researchers to study the effects of mutations on the stability of protein structures, predict changes in the free energy of proteins upon mutation (ΔΔG), and assess the impact of these mutations on protein function. 

Example of some key aspects of Foldx is Protein Stability Prediction.

FoldX can predict the stability changes caused by point mutations in a protein. 

It accomplishes this by calculating the difference in Gibbs free energy between a wild-type protein and its mutated form.

This helps in understanding how mutations can affect protein stability.

Download FoldX from its official website. Ideally, this requires downloading a binary file that matches your operating system.

Extract and install Foldx and ensure that it is correctly installed on your system. 

Steps:

1) Visit the FoldX official FoldX website to get the latest version. You need need to register or request access per their distribution policy.
 
Choose the appropriate version for Linux from the download link you will receive from them. Ensure you download the Linux binary. Create folder in your home directory (e.g Downloads) and navigate into it and download Foldx as follows.

Example: wget https://foldxsuite.crg.eu/system/files/foldx5Linux64_1.zip

2) Extract and Install FoldX:

The foldx5_1Linux64.zip is a .zip file. Extract the file on a Linux system like Ubuntu as follows:

      1: Install Unzip Tool: Ensure you have unzip utility installed on your system. You can install it using apt if it's not already installed:
          sudo apt install unzip
   
      2: Extract the ZIP File: Create another folder in your home directory (e.g FoldxFiles).
   
         #Navigate to the directory containing the downloaded .zip file, and use the unzip command to extract it as follows:
   
         cd ~/Downloads  #wherever your download folder is
   
         unzip foldx5_1Linux64.zip -d ~/FoldxFiles # extracts the contents of foldx5_1Linux64.zip into FoldxFiles in home directory. Adjust the path as needed based on where you want to install FoldX
   
         ls ~/FoldxFiles # List contents in the directory after extraction. Content include foldx_20241231 which is FoldX executable (verify with the command: file foldx_20241231)
   
         #Rename executable to something more manageable, e.g FoldX.
   
      3: To make running FoldX even simpler, add Foldx to your shell configuration file or PATH (e.g .bashrc).
   
         #Create a folder in your home directory (e.g foldx). Move the renamed Foldx executable (was renamed Foldx) into your new folder (foldx) as follows:
   
         mkdir foldx
   
         mv ~/FoldxFiles/Foldx foldx # Replace foldx with the path to the directory containing the FoldX executable if it's different.
   
         #Open your .bashrc file in a text editor:
   
         nano ~/.bashrc
   
         #Append this line to the file:
   
         export PATH=$PATH:$HOME/foldx
   
         #Save and exit the editor (press Ctrl+O, Enter, and then Ctrl+X). Then, to reload the changes, run:
   
         source ~/.bashrc
   
         #Verify the Command by running the following
   
         Foldx --help # This should correctly display the help information for FoldX
   
         #Alternatively, to append export PATH=$PATH:$HOME/foldx to to your .bashrc file on the terminal, run:
   
          echo 'export PATH=$PATH:$HOME/foldx' >> ~/.bashrc
         
The study aims at accessing the impact of mutations on the stability of proteins using multiple PDB files.

We will automate the process by creating a systematic workflow that utilizes Foldx. 

Step-by-step guide:

 1) Prepare files and environment:

- Organize PDB files:

To run Foldx, we need to supply the PDB file of the gene or protein name under study, and for each PDB file, we have to create a text file listing all the mutations to analyze. NB: Test file should be in a format that Foldx can process. 

The raw dataset provides us with a list of all the protein names they convered. To manually download all the protein structures from the AlphaFold Database or from Uniprot using the protein names is going to be tiresome. 

We will automate the download process to do this in a single run. But first, we need to have a list of the protein identifiers. 

AlphaFold uses Uniprot IDs for indexing protein structures, hence, we have to resolve the list of protein names to Uniprot Ids, which can be used to download structures from AlphaFold databases. 

Let's automate the process with a Python script. Create a text file and list the protein names, one name per line. Name file as protein_names.txt or as you prefer. 

Use the Python script to fetch the uniprot IDs associated with the list of protein names. Install requests library if not already.

The output of python script is a structured text or a list of key-value-like statements. We need to parse the output file to extract the Uniprot accession number/IDs of the genes, then using the list of Uniprot IDs, we can dowload the PDB files. 

Let's create a Python script to parse the structured text file. The script will generate three separate files that will contain the gene names, accession numbers/Uniprot IDs, and Uniprot entry names. 

Let's follow up with another python script that will read the accession numbers/Uniprot IDs from an input file and download their AlphaFold predicted structures from AlphaFold database hosted by the European Bioinformatics Institute (EBI).

- Create mutation files and run Foldx:

Since we are interested in the energy difference between the reference residues (WT) and their variants, we will run FoldX with the BuildModel command. BuildModel requires a mutant-file (enlisting the mutations) to run. 

FoldX operates two ways of defining mutations, that's Mutant file or Individual list mode. We will use Individual list mode as the Mutant file mode requires the sequences of the mutants and is ideal if studying several mutations in a protein.

In Individual list mode, the file individual_list.txt contains the mutations we want to make, in the classical FoldX format (WT residue, chain, residue position, mutant residue). It is required than the name of the file containing the mutations starts by individual_list. Don't include any space on the mutation lines.

The mutation file format requires the chain identifier for each mutation. The dataset we have prepared so far does not include this information. Let's create a script that extract these IDs associated with the mutations. 

This requires a different file format. We will create another version of the dataset we are working with to include a PDB_IDs, reference residue, position and mutant residue columns. We will name this file compile.txt. The reference residue, position and mutant residue columns can be extracted from the dataset but we have to create the PDB_IDs of the mutations. 

The PDBs of the proteins since they are alphafold predicted structiures should follow this format: AF-${identifier}-F1-model_v1, where identifier is the accession number of the protein/gene.

The key-value like ouput statements from the Uniprot output file include genes and their accession numbers. The new dataset we have created also has genes as one of the columns. 

Let's create a bash script that process the key-value statements from the Uniprot output to extract the gene names and accession numbers then cross-reference these genes with the compile dataset to identify shared entries. 

For matching genes, it will generate a list of PDB IDs in the format AF-${identifier}-F1-model_v1.pdb and append this to the dataset. Use the script compile_pdb_Ids.sh for this purpose.

Let's create a new version of the compile dataset and name it compile_v2.txt. Reorder the columns to match the following order: PDB_ID, reference residue, position, and mutant residue. Trim white spaces around column values. 

Use the script extract_ChainID.py to extract the chain IDs. Add these chain IDs as a new column in the compile dataset using the script add_chain_col.sh. Also, append a new column containing semi-colons as placeholders or delimiters. 

The format of the rows should follow the format: [AF-Q00266-F1-model_v1.pdb   P       A       357     L       ;]

Next, let's create a bash script to split the compile dataset into four separate text files: TestBenign, TestPathogenic, TrianBenign, TrainPathogenic. 

The script will read the compile txt file as input file, check the conditions for each row based on the dataset-classification and clinical significance columns, and then append the row to the appropriate output file. 

Rows will be classified based on the dataset labels (Train or Test) and clinical significance (Benign or Pathogenic).

Finally, let's create individual mutation file for each PDB_ID. Use the script split_file_by_category.py to process each of the four input files (TestBenign.txt, TestPathogenic.txt, TrainBenign.txt, and TrainPathogenic.txt) and split their contents into separate output files based on the PDB IDs in the first column. 

The script generates one file for each unique PDB ID, named with the PDB ID followed by _mutations.txt. 

Run FoldX with the BuildModel command. In the run_FoldX.sh script, modify the path and run separately for each of the four datasets. The path should include a folder with PDBs and mutation files.

The output files from running FoldX provides detailed information about the effects of the mutations on the PDB structures. These files include:

Average_*.fxout reports the average ΔΔG (Gibbs free energy change) and other calculated energy terms for each mutation.

Dif_*.fxout: Provides the difference in free energy (ΔΔG) between the wild-type and mutant PDB structures caused by the mutations.

Raw_*.fxout: Provides detailed breakdown of energy components for wild-type and mutant structures.

The content of Raw_*.fxout include:

 - A header line describing the energy terms and categories calculated from each analyzed PDB structure.
   
 - Pdb: Name of the analyzed PDB file.
   
 - total energy: Overall Gibbs free energy (G) of the structure, combining all components.
   
 - Backbone Hbond: Contribution of backbone hydrogen bonding to the energy.
   
 - Sidechain Hbond: Contribution of side-chain hydrogen bonding to the energy.
   
 - Van der Waals: Contribution from van der Waals interactions.
   
 - Electrostatics: Contribution from electrostatic interactions.
   
 - Solvation Polar: Energy penalty from polar solvation.
   
 - Solvation Hydrophobic: Energy gain from burying hydrophobic residues.
   
 - Van der Waals clashes: Energy penalty from steric clashes.
   
 - entropy sidechain: Entropic penalty from side-chain flexibility.
   
 - entropy mainchain: Entropic penalty from main-chain flexibility.
   
 - cis_bond, torsional clash, backbone clash, etc.

Let's write a bash script that will iterate through all the Raw_*.fxout files in a directory of any of the data categories, extract their contents, and write the combined output into a csv file. Use the script combined_raw_files.sh

The output csv file has rows containing energy values for wild-type structures and those for the mutants structures. We will work with the energy information for the mutant structures now. 

Let's write a script that will split the rows in the csv file into two separate csv files: one containing rows with wild-type energy values and the other with information on the mutants.

Use the script split_csv_by_pdb_type.sh. This generates two files named AF_rows.csv (contains mutant energy values) and WT_rows.csv (contains wild-type energy values).

For AF_rows.csv file for each dataset category, let's write a script that will iterate through its mutation files and append the mutations from their _mutations.txt files to the correct rows in the FA_rows.csv, ensuring that the mutations align with their corresponding PDB names. Use the script append_mutations.sh

Next, we will run PositionScan which is another functionality in the FoldX suite. PositionScan systematically analyzes the impact of mutating every possible residue at a specific position in a protein struture. We will run this to understand the effects of the mutations on their PDB structures, and predict the functional consequences of sequence changes in the PDB structures when the mutations are introduced.

Let's run PositionScan for each dataset category with their associated PDBs and *_mutation.txt as input files. Use the script PositionScan.sh

After running PositionScan there will be a number of files to look at. Given output-file="TAG" the output files will inlcude: PS_TAG_scanning_output file containing ΔΔG upon mutation (DDG=DGMut-DGWt).

PS_TAG_energies.txt containing raw energy calculations for the wild-type residues at each position and the energetic contributions of each mutation analyzed at the position. 

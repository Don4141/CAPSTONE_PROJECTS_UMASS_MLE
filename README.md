#Capstone projects for Machine Learning Engineering and AI bootcamp at UMASS Global
The first tool to install is FoldX. This is a computational tool widely used in the field of bioinformatics and computational biology for analyzing the stability of proteins and their complexes. 
Foldx enables researchers to study the effects of mutations on the stability of protein structures, predict changes in the free energy of proteins upon mutation (ΔΔG), and assess the impact of 
these mutations on protein function. 
Example of some key aspects of Foldx is Protein Stability Prediction
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
         

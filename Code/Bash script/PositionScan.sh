#!/bin/bash
PDB_PATH="/home/sadjei65320/UMASS_CapstoneProject/src/BuildModel/RunFoldxTestBenign/mutation_file/"

cd "$PDB_PATH" || { echo "Failed to change directory to $PDB_PATH"; exit 1; }

for pdb in *.pdb; do
    base_name=$(basename "$pdb" .pdb)
    mutation_file="${base_name}_mutations.txt"
    
    if [ -f "$mutation_file" ]; then
        # Construct the --positions argument from the mutation file
        positions=""
        while IFS= read -r line; do
            # Remove any trailing semicolon and whitespace
            line=$(echo "$line" | tr -d ';' | xargs)
            
            # The mutation file format is: OriginalResidueChainPositionMutantResidue
            original_residue=${line:0:1}
            chain=${line:1:1}
            position=""
            i=2
            while [[ ${line:i:1} =~ [0-9] ]]; do
                position+="${line:i:1}"
                i=$((i + 1))
            done
            mutant_residue=${line:i:1}
            
            # Construct the mutation specification
            positions+="${original_residue}${chain}${position}${mutant_residue},"
        done < "$mutation_file"
        
        # Remove the trailing comma from positions
        positions="${positions%,}"
        
        # Run FoldX with PositionScan
        FoldX --command=PositionScan --pdb="$pdb" --positions="$positions"
        echo "Running FoldX PositionScan for $pdb with positions $positions"
    else
        echo "Mutation file $mutation_file not found for $pdb"
    fi
done

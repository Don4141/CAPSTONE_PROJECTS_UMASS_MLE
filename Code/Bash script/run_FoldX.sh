#!/bin/bash
PDB_PATH="$HOME/UMASS_CapstoneProject/src/BuildModel/RunFoldxTrainPathogenic/"

cd "$PDB_PATH"
for pdb in *.pdb; do
    base_name=$(basename "$pdb" .pdb)
    if [ -f "${base_name}_mutations.txt" ]; then
        cp "${base_name}_mutations.txt" individual_list.txt
        FoldX --command=BuildModel --pdb="$pdb" --mutant-file=individual_list.txt
        echo "Running FoldX for $pdb with mutation file individual_list.txt"
    else
        echo "Mutation file for $pdb not found"
    fi
done

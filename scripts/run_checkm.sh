#!/bin/bash

# Check if a number is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <number>"
    exit 1
fi

# Set the filename dynamically
FILE_NUMBER=$1
FASTA_FILE="clean${FILE_NUMBER}.fasta"

# Convert Windows-style line endings to Unix for the FASTA file in the 'parts' folder
dos2unix parts/$FASTA_FILE

# Create and navigate to the 'edges' directory
mkdir -p edges$FILE_NUMBER
cd edges$FILE_NUMBER || exit 1

# Split the FASTA file into multiple files (using the file from the 'parts' folder)
awk '{ 
    if (substr($0, 1, 1) == ">") { 
        filename = substr($0, 2) ".fa" 
    } 
    print $0 > filename 
}' "../parts/$FASTA_FILE"

# Go back to the original directory
cd ..

# Rename files inside 'edges' by replacing spaces with underscores
find "edges${FILE_NUMBER}/" -name "* *" -type f | rename 's/ /_/g'

# Run CheckM taxonomy workflow
checkm taxonomy_wf -t 30 -x fa domain Bacteria "edges${FILE_NUMBER}/" "checkm_edges${FILE_NUMBER}/"

# Run CheckM QA process
checkm qa -t 30 "checkm_edges${FILE_NUMBER}/Bacteria.ms" "checkm_edges${FILE_NUMBER}/" \
    -f "checkm_edges_polished_results${FILE_NUMBER}.txt" --tab_table -o 2

# Create 'result' directory if it doesn't exist, then rename and move marker_gene_stats.tsv
mkdir -p result
mv "checkm_edges${FILE_NUMBER}/storage/marker_gene_stats.tsv" "result/marker_gene_stats${FILE_NUMBER}.tsv"
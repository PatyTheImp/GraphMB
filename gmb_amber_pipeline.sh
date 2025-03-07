#!/bin/bash

# Ensure a dataset name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <DATASET_NAME> [additional GraphMB options]"
    exit 1
fi

# Set dataset name (passed as argument)
DATASET_NAME=$1  # Example: "strong100", "aale", etc.

# Capture additional GraphMB options (if any)
shift  # Remove first argument (dataset name)
GRAPHMB_OPTIONS="$@"  # Store remaining arguments as GraphMB options

# Define directories
GRAPHMB_DIR=$(pwd)  # Assumes script is run from /graphmb/
AMBER_DIR="/repos/AMBER"

ASSEMBLY_DIR="$GRAPHMB_DIR/data/$DATASET_NAME"
OUTPUT_DIR="$GRAPHMB_DIR/results/$DATASET_NAME"

LABELS_FILE="$ASSEMBLY_DIR/labels.binning"
AMBER_OUTPUT="$AMBER_DIR/results/$DATASET_NAME"

# Step 1: Run GraphMB with additional options
echo "Running GraphMB on $DATASET_NAME with options: $GRAPHMB_OPTIONS"
graphmb --assembly "$ASSEMBLY_DIR" --outdir "$OUTPUT_DIR" --outname "$DATASET_NAME" --writebins --cuda $GRAPHMB_OPTIONS

# Step 2: Find all GraphMB output files ending in "_best_contig2bin.tsv"
GRAPHMB_OUTPUT_FILES=("$OUTPUT_DIR"/*_best_contig2bin.tsv)

# Check if at least one valid output file exists
if [ ${#GRAPHMB_OUTPUT_FILES[@]} -eq 0 ]; then
    echo "Error: No GraphMB output files found in $OUTPUT_DIR"
    exit 1
fi

# Step 3: Run AMBER inside its directory
echo "Running AMBER evaluation..."
cd "$AMBER_DIR" || exit 1
python3.11 amber.py -g "$LABELS_FILE" "${GRAPHMB_OUTPUT_FILES[@]}" -o "$AMBER_OUTPUT"

# Step 4: Return to GraphMB directory
cd "$GRAPHMB_DIR"

echo "Pipeline completed for $DATASET_NAME!"

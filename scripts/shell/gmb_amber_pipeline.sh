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
REMOVE_FILE="$ASSEMBLY_DIR/unique_common.tsv"
AMBER_OUTPUT="$AMBER_DIR/results/$DATASET_NAME"

# Step 1: Run GraphMB with additional options
echo "Running GraphMB on $DATASET_NAME with options: $GRAPHMB_OPTIONS"
graphmb --assembly "$ASSEMBLY_DIR" --outdir "$OUTPUT_DIR" --outname "$DATASET_NAME" --numcores 32 --cuda $GRAPHMB_OPTIONS

# Step 2: Find all GraphMB output files ending in "_best_contig2bin.tsv"
GRAPHMB_OUTPUT_FILES=("$OUTPUT_DIR"/*_best_contig2bin.tsv)

# Check if at least one valid output file exists
if [ ${#GRAPHMB_OUTPUT_FILES[@]} -eq 0 ]; then
    echo "Error: No GraphMB output files found in $OUTPUT_DIR"
    exit 1
fi

# Step 3: Set up and activate Python virtual environment for AMBER
echo "Setting up Python virtual environment for AMBER..."
cd "$AMBER_DIR" || exit 1

source myenv/bin/activate

# Run AMBER
echo "Running AMBER evaluation..."
python3 amber.py -g "$LABELS_FILE" "${GRAPHMB_OUTPUT_FILES[@]}" -o "$AMBER_OUTPUT"

if [ -f "$REMOVE_FILE" ]; then
    echo "$REMOVE_FILE exists, running the command..."
    python3 amber.py -g "$LABELS_FILE" -r "$REMOVE_FILE" -k "circular element" "${GRAPHMB_OUTPUT_FILES[@]}" -o "$AMBER_OUTPUT"
else
    echo "$REMOVE_FILE does not exist."
fi

# Step 4: Deactivate venv and return to GraphMB directory
deactivate
cd "$GRAPHMB_DIR"

echo "Pipeline completed for $DATASET_NAME!"
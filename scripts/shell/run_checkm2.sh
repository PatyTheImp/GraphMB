#!/bin/bash

# Define the base directory containing MAG folders
base_dir="./mag_folders/"

# Find all _bins folders and store them into an array (snapshot now)
mapfile -t mag_dirs < <(find "$base_dir" -mindepth 1 -maxdepth 1 -type d -name "*_bins")

# Check if any folders were found
if [[ ${#mag_dirs[@]} -eq 0 ]]; then
    echo "No MAG folders found."
    exit 1
fi

# Loop through the safe list
for mag_dir in "${mag_dirs[@]}"; do
    # Remove trailing slash and extract base name
    base_name=$(basename "$mag_dir" "_bins")

    # Define the output directory
    output_dir="./checkm2_output/${base_name}_output"

    # Create output directory
    mkdir -p "$output_dir"

    # Run CheckM2
    echo "Running CheckM2 on $mag_dir -> Output: $output_dir"
    checkm2 predict -i "$mag_dir" -o "$output_dir" -x fa --force --threads 30

    echo "Finished processing $mag_dir"
done
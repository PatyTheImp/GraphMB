import os
import pandas as pd

# Define the base directory (current directory)
base_dir = "."

# Output file to store results
output_file = "hq_bins_results.txt"

# Initialize results storage
results = {}

# Loop through all folders in the current directory
for folder in os.listdir(base_dir):
    if folder.endswith("_output"):  # Process only *_output folders
        report_path = os.path.join(base_dir, folder, "quality_report.tsv")

        if os.path.isfile(report_path):  # Check if the file exists
            try:
                # Read the TSV file
                df = pd.read_csv(report_path, sep='\t')

                # Ensure the required columns exist
                if "Completeness" in df.columns and "Contamination" in df.columns:
                    # Filter rows based on conditions
                    hq_bins = df[(df["Completeness"] > 90) & (df["Contamination"] < 5)].shape[0]

                    # Store the result
                    results[folder.replace("_output", "")] = hq_bins
                else:
                    print(f"Warning: Missing required columns in {report_path}")

            except Exception as e:
                print(f"Error reading {report_path}: {e}")
        else:
            print(f"Warning: quality_report.tsv not found in {folder}")

# Write results to a text file
with open(output_file, "w") as f:
    f.write("Number of HQ bins:\n")
    for key, value in sorted(results.items()):  # Sort alphabetically for better readability
        f.write(f"{key}: {value}\n")

print(f"✅ Results saved in {output_file}")
from pathlib import Path
import pandas as pd

# Path to the root directory containing all tool folders
root_dir = Path("genome") #/path/to/root_folder

# List to store results
rows = []

# Process each subfolder (assumes each subfolder is named after a tool)
for tool_dir in root_dir.iterdir():
    if tool_dir.is_dir():
        metrics_file = tool_dir / "metrics_per_bin.tsv"
        if metrics_file.exists():
            df = pd.read_csv(metrics_file, sep='\t')
            hq = df[(df["Purity (bp)"] >= 0.95) & (df["Completeness (bp)"] > 0.9)].shape[0]
            mq = df[(df["Purity (bp)"] >= 0.90) & (df["Completeness (bp)"] > 0.5)].shape[0]
            rows.append({"Tool": tool_dir.name, "#HQ Bins": hq, "#MQ Bins": mq})

# Create output DataFrame
result_df = pd.DataFrame(rows)

# Save to TSV
result_df.to_csv("bins.tsv", sep='\t', index=False)

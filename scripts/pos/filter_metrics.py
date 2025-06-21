import pandas as pd
import sys

def main():
    # Accept an input TSV file via command-line argument (default metrics_per_bin.tsv)
    input_file = sys.argv[1] if len(sys.argv) > 1 else "metrics_per_bin.tsv"
    # Read the TSV
    df = pd.read_csv(input_file, sep="\t")
    # Filter rows where "True size (bp)" is at least 200,000
    filtered = df[df["Bin size (bp)"] >= 200000]
    # Write out the filtered data
    filtered.to_csv("filtered_metrics.tsv", sep="\t", index=False)
    print(f"Filtered data written to filtered_metrics.tsv (kept {len(filtered)} rows)")

if __name__ == "__main__":
    main()

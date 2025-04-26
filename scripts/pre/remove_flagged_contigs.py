from Bio import SeqIO
import pandas as pd
import matplotlib.pyplot as plt

# File paths
FASTA_IN = "assembly.fasta"
FASTA_OUT = "assembly_clean.fasta"
DEPTH_IN = "assembly_depth.txt"
DEPTH_OUT = "assembly_depth_clean.txt"
FLAGGED_CONTIGS = "flagged_contigs.tsv"
PLOT_OUT = "gc_vs_coverage_cleaned.png"

def plot_gc_vs_coverage(depth_df, flagged_ids):
    plt.figure(figsize=(10, 6))

    # Normal contigs (not flagged)
    normal = depth_df[~depth_df['contigName'].isin(flagged_ids)]
    plt.scatter(normal['gc_content'], normal['coverage'], c='gray', alpha=0.5, label='Normal Contigs')

    # Flagged contigs (still showing them separately)
    flagged = depth_df[depth_df['contigName'].isin(flagged_ids)]
    plt.scatter(flagged['gc_content'], flagged['coverage'], c='red', alpha=0.8, label='Flagged Contigs')

    plt.xlabel('GC Content')
    plt.ylabel('Coverage (Total Avg Depth)')
    plt.title('GC Content vs Coverage (After Cleaning)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(PLOT_OUT, dpi=300)
    plt.show()

def main():
    # Load flagged contigs
    flagged_df = pd.read_csv(FLAGGED_CONTIGS, sep="\t")
    flagged_ids = set(flagged_df['contigName'])

    print(f"Number of flagged contigs to remove: {len(flagged_ids)}")

    # Filter FASTA
    records = list(SeqIO.parse(FASTA_IN, "fasta"))
    kept_records = [r for r in records if r.id not in flagged_ids]
    print(f"Keeping {len(kept_records)} out of {len(records)} contigs.")

    SeqIO.write(kept_records, FASTA_OUT, "fasta")
    print(f"Cleaned FASTA saved as {FASTA_OUT}")

    # Filter depth.txt
    depth_df = pd.read_csv(DEPTH_IN, sep="\t")
    clean_depth_df = depth_df[~depth_df['contigName'].isin(flagged_ids)]
    clean_depth_df.to_csv(DEPTH_OUT, sep="\t", index=False)
    print(f"Cleaned depth file saved as {DEPTH_OUT}")

    # Plotting (optional but cool)
    if 'gc_content' in depth_df.columns and 'coverage' in depth_df.columns:
        plot_gc_vs_coverage(depth_df, flagged_ids)
        print(f"Plot saved as {PLOT_OUT}")
    else:
        print("Warning: No 'gc_content' or 'coverage' in depth file. Skipping plot.")

if __name__ == "__main__":
    main()

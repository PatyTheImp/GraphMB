from Bio import SeqIO
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_gc_vs_coverage(depth_df, flagged_contigs):
    plt.figure(figsize=(10, 6))

    # Plot normal contigs
    normal = depth_df[~depth_df['contigName'].isin(flagged_contigs)]
    plt.scatter(normal['gc_content'], normal['coverage'], c='gray', alpha=0.5, label='Normal Contigs')

    # Plot flagged contigs
    flagged = depth_df[depth_df['contigName'].isin(flagged_contigs)]
    plt.scatter(flagged['gc_content'], flagged['coverage'], c='red', alpha=0.8, label='Flagged Contigs')

    plt.xlabel('GC Content')
    plt.ylabel('Coverage (Total Avg Depth)')
    plt.title('GC Content vs Coverage')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("gc_vs_coverage.png", dpi=300)
    plt.show()


# Input files
FASTA_FILE = "assembly.fasta"
DEPTH_FILE = "assembly_depth.txt"

# Thresholds
GC_STD_CUTOFF = 2.5     # Flag contigs >2.5 standard deviations from mean GC
COV_STD_CUTOFF = 2.5    # Flag contigs >2.5 standard deviations from mean coverage

def calculate_gc_content(seq):
    seq = seq.upper()
    g = seq.count('G')
    c = seq.count('C')
    return (g + c) / len(seq) if len(seq) > 0 else 0

def main():
    # Parse FASTA and compute GC content
    gc_content = {}
    for record in SeqIO.parse(FASTA_FILE, "fasta"):
        gc = calculate_gc_content(str(record.seq))
        gc_content[record.id] = gc

    # Load depth.txt
    depth_df = pd.read_csv(DEPTH_FILE, sep='\t')

    # Check column names
    print(depth_df.columns)

    # Use 'totalAvgDepth' as the coverage column
    depth_df['coverage'] = depth_df['totalAvgDepth']

    # Merge GC and coverage into one DataFrame
    depth_df['gc_content'] = depth_df['contigName'].map(gc_content)

    # Calculate means and stds
    gc_mean = depth_df['gc_content'].mean()
    gc_std = depth_df['gc_content'].std()

    cov_mean = depth_df['coverage'].mean()
    cov_std = depth_df['coverage'].std()

    # Flagging
    flagged_gc = depth_df[np.abs(depth_df['gc_content'] - gc_mean) > GC_STD_CUTOFF * gc_std]
    flagged_cov = depth_df[np.abs(depth_df['coverage'] - cov_mean) > COV_STD_CUTOFF * cov_std]

    # Combine flags
    flagged = pd.concat([flagged_gc, flagged_cov]).drop_duplicates()

    # Output
    print("Flagged contigs:")
    print(flagged[['contigName', 'gc_content', 'coverage']])

    flagged_ids = set(flagged['contigName'])
    plot_gc_vs_coverage(depth_df, flagged_ids)

    flagged.to_csv("flagged_contigs.tsv", sep="\t", index=False)
    print("\nSaved flagged contigs to flagged_contigs.tsv")

if __name__ == "__main__":
    main()
    

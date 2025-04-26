import os
import sys
from statistics import mean, median, mode, StatisticsError
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def read_fasta_lengths(fasta_path):
    lengths = []
    contig_seqs = []
    with open(fasta_path, 'r') as f:
        seq = ''
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if seq:
                    contig_seqs.append(seq)
                    lengths.append(len(seq))
                seq = ''
            else:
                seq += line.upper()
        if seq:
            contig_seqs.append(seq)
            lengths.append(len(seq))
    return lengths, contig_seqs

def compute_stats_and_plots(fasta_file, output_tsv):
    if not os.path.exists(fasta_file):
        print(f"ERROR: File not found: {fasta_file}")
        sys.exit(1)

    lengths, contigs = read_fasta_lengths(fasta_file)
    num_contigs = len(lengths)
    avg_len = mean(lengths)
    med_len = median(lengths)
    try:
        mode_len = mode(lengths)
    except StatisticsError:
        mode_len = "NA"

    min_len = min(lengths)
    max_len = max(lengths)
    contigs_with_N = sum(1 for seq in contigs if 'N' in seq)
    contigs_all_N = sum(1 for seq in contigs if set(seq) == {'N'})

    # Save TSV output
    with open(output_tsv, 'w') as f:
        f.write("Metric\tValue\n")
        f.write(f"Number_of_contigs\t{num_contigs}\n")
        f.write(f"Average_length_bp\t{avg_len:.2f}\n")
        f.write(f"Median_length_bp\t{med_len}\n")
        f.write(f"Mode_length_bp\t{mode_len}\n")
        f.write(f"Min_length_bp\t{min_len}\n")
        f.write(f"Max_length_bp\t{max_len}\n")
        f.write(f"Contigs_with_any_N\t{contigs_with_N}\n")
        f.write(f"Contigs_with_all_N\t{contigs_all_N}\n")

    print(f"Statistics saved to: {output_tsv}")

    # Use Seaborn style for prettier plots
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)

    # Plot histogram with log y-axis and stylish annotations
    plt.figure(figsize=(10, 5))
    plt.hist(lengths, bins=50, color="#98c1d9", edgecolor="#3d5a80")
    plt.yscale("log")

    # Title and labels
    plt.title("Contig Length Distribution (Log Scale)", fontsize=14, fontweight="bold")
    plt.xlabel("Contig Length (bp)")
    plt.ylabel("Frequency (log scale)")

    # Annotated lines
    plt.axvline(avg_len, color="#3a86ff", linestyle='--', linewidth=2, label=f'Mean: {avg_len:.0f}')
    plt.axvline(med_len, color="#06d6a0", linestyle='-', linewidth=2, label=f'Median: {med_len}')
    if isinstance(mode_len, (int, float)):
        plt.axvline(mode_len, color="#ff006e", linestyle='-.', linewidth=2, label=f'Mode: {mode_len}')

    # Legend and layout
    plt.legend(frameon=True, fancybox=True, shadow=True)
    plt.grid(True, which="both", linestyle=':', linewidth=0.5)
    plt.tight_layout()

    # Save and close
    hist_path = output_tsv.replace(".tsv", "_histogram.png")
    plt.savefig(hist_path, dpi=300)
    print(f"📊 Histogram saved to: {hist_path}")
    plt.close()


    # Prettier boxplot with Seaborn styling
    plt.figure(figsize=(8, 4))
    sns.set_theme(style="whitegrid", palette="pastel", font_scale=1.1)

    # Boxplot
    sns.boxplot(x=lengths, color="#98c1d9", linewidth=2)

    # Title and axis
    plt.title("Contig Length Boxplot", fontsize=14, fontweight="bold")
    plt.xlabel("Contig Length (bp)")
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.tight_layout()

    # Save and close
    box_path = output_tsv.replace(".tsv", "_boxplot.png")
    plt.savefig(box_path, dpi=300)
    print(f"📦 Boxplot saved to: {box_path}")
    plt.close()

if __name__ == "__main__":
    compute_stats_and_plots("assembly.fasta", "contig_stats.tsv")

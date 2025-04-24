import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from collections import defaultdict, Counter
import ast

# Load the marker gene stats file
file_path = "marker_gene_stats.tsv"
with open(file_path) as f:
    raw_lines = f.readlines()

# Parse contigs and SCGs
contig_scgs = {}
for line in raw_lines:
    contig_id, scg_data = line.strip().split('\t', 1)
    try:
        parsed = ast.literal_eval(scg_data)
        scgs = {scg for subdict in parsed.values() for scg in subdict}
        contig_scgs[contig_id] = scgs
    except Exception:
        contig_scgs[contig_id] = set()

# Efficient SCG overlap computation
def efficient_scg_overlap_distribution(contig_markers):
    scg_to_contigs = defaultdict(set)
    for contig, scgs in contig_markers.items():
        for scg in scgs:
            scg_to_contigs[scg].add(contig)

    pair_counts = Counter()
    for contigs in scg_to_contigs.values():
        for c1, c2 in combinations(sorted(contigs), 2):
            pair_counts[(c1, c2)] += 1

    overlap_distribution = Counter()
    for _, count in pair_counts.items():
        overlap_distribution[count] += 1

    return pd.DataFrame(
        sorted(overlap_distribution.items()),
        columns=["SCGs_in_common", "Number_of_pairs"]
    )

# Run the analysis
result_df = efficient_scg_overlap_distribution(contig_scgs)

# Save as TSV (optional)
result_df.to_csv("scg_overlap_distribution.tsv", sep="\t", index=False)

# Create histogram
# plt.figure(figsize=(10, 6))
# plt.bar(result_df["SCGs_in_common"], result_df["Number_of_pairs"])
# plt.xlabel("Number of SCGs in Common")
# plt.ylabel("Number of Contig Pairs")
# plt.title("Histogram of SCG Overlap Between Contig Pairs")
# plt.grid(True)
# plt.tight_layout()
# plt.savefig("scg_overlap_histogram.png")
# plt.show()

# Create histogram with log-scaled y-axis
plt.figure(figsize=(10, 6))
plt.bar(result_df["SCGs_in_common"], result_df["Number_of_pairs"])
plt.xlabel("Number of SCGs in Common")
plt.ylabel("Number of Contig Pairs (log scale)")
plt.title("Histogram of SCG Overlap Between Contig Pairs")
plt.yscale("log")  # <--- Log scale here
plt.grid(True, which="both", axis="y", linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig("scg_overlap_histogram.png")
plt.show()


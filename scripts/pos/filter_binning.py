from pathlib import Path
from collections import defaultdict

# Example file paths (change as needed)
fasta_file = "assembly.fasta"
binning_file = "marineP_s_md_5scg_0_best_contig2bin.tsv"
min_bin_length = 200000  # Hardcoded threshold

# --- Step 1: Parse FASTA file ---
def parse_fasta_lengths(fasta_path):
    contig_lengths = {}
    current_contig = None
    current_length = 0

    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_contig:
                    contig_lengths[current_contig] = current_length
                current_contig = line[1:].split()[0]
                current_length = 0
            else:
                current_length += len(line)
        if current_contig:
            contig_lengths[current_contig] = current_length
    return contig_lengths

# --- Step 2: Parse binning file ---
def parse_binning_file(binning_path):
    bin_to_contigs = defaultdict(list)
    contig_to_bin = {}

    with open(binning_path, 'r') as f:
        for line in f:
            if line.startswith("@"):  # Skip metadata lines
                continue
            contig, bin_id = line.strip().split()
            bin_to_contigs[bin_id].append(contig)
            contig_to_bin[contig] = bin_id
    return bin_to_contigs, contig_to_bin

# --- Step 3: Filter bins by length ---
def filter_bins_by_length(contig_lengths, bin_to_contigs, threshold):
    valid_bins = set()
    for bin_id, contigs in bin_to_contigs.items():
        total_len = sum(contig_lengths.get(contig, 0) for contig in contigs)
        if total_len >= threshold:
            valid_bins.add(bin_id)
    return valid_bins

# --- Step 4: Write filtered binning ---
def write_filtered_binning(original_binning, contig_to_bin, valid_bins):
    output_file = Path(original_binning).with_suffix(".binning")
    with open(output_file, 'w') as f:
        f.write("@Version:0.9.0\n@SampleID:SAMPLEID\n@@SEQUENCEID\tBINID\n")
        for contig, bin_id in contig_to_bin.items():
            if bin_id in valid_bins:
                f.write(f"{contig}\t{bin_id}\n")
    return output_file

# --- Main execution ---
if __name__ == "__main__":
    contig_lengths = parse_fasta_lengths(fasta_file)
    bin_to_contigs, contig_to_bin = parse_binning_file(binning_file)
    valid_bins = filter_bins_by_length(contig_lengths, bin_to_contigs, min_bin_length)
    output_path = write_filtered_binning(binning_file, contig_to_bin, valid_bins)
    print(f"Filtered binning written to: {output_path}")

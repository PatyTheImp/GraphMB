#!/usr/bin/env python3

import argparse
from collections import defaultdict
from Bio import SeqIO

def parse_fasta_lengths(fasta_path):
    """Returns a dict mapping contig IDs to their lengths."""
    contig_lengths = {}
    for record in SeqIO.parse(fasta_path, "fasta"):
        contig_lengths[record.id] = len(record.seq)
    return contig_lengths

def parse_binning_file(binning_path):
    """Returns a dict mapping bins to list of contigs, and a contig-to-bin map."""
    bin_to_contigs = defaultdict(list)
    contig_to_bin = {}
    with open(binning_path, "r") as f:
        for line in f:
            contig, bin_id = line.strip().split('\t')
            bin_to_contigs[bin_id].append(contig)
            contig_to_bin[contig] = bin_id
    return bin_to_contigs, contig_to_bin

def compute_bin_lengths(bin_to_contigs, contig_lengths):
    """Computes total length for each bin."""
    bin_lengths = {}
    for bin_id, contigs in bin_to_contigs.items():
        total_length = sum(contig_lengths.get(contig, 0) for contig in contigs)
        bin_lengths[bin_id] = total_length
    return bin_lengths

def filter_bins(bin_to_contigs, bin_lengths, min_length):
    """Returns a set of bin IDs that pass the length threshold."""
    return {bin_id for bin_id, length in bin_lengths.items() if length >= min_length}

def write_filtered_binning(min, bin_file, contig_to_bin, bins_to_keep):
    """Writes filtered binning file in the same format."""
    output_path = "filtered_" + min + "_" + bin_file
    with open(output_path, 'w') as out:
        for contig, bin_id in contig_to_bin.items():
            if bin_id in bins_to_keep:
                out.write(f"{contig}\t{bin_id}\n")

def main():
    parser = argparse.ArgumentParser(description="Filter binning file based on total bin length.")
    parser.add_argument("--fasta", help="FASTA file with contig sequences", default="assembly.fasta")
    parser.add_argument("--binning", help="TSV file mapping contigs to bins", default="plantP_pb_d_0_best_contig2bin.tsv")
    parser.add_argument("--min_length", type=int, help="Minimum total length (bp) for bins to be kept", default="100000")
    
    args = parser.parse_args()

    contig_lengths = parse_fasta_lengths(args.fasta)
    bin_to_contigs, contig_to_bin = parse_binning_file(args.binning)
    bin_lengths = compute_bin_lengths(bin_to_contigs, contig_lengths)
    bins_to_keep = filter_bins(bin_to_contigs, bin_lengths, args.min_length)
    write_filtered_binning(args.min_length, args.binnig, contig_to_bin, bins_to_keep)

if __name__ == "__main__":
    main()

import statistics

MIN_CONTIG_LENGTH = 1000

def process_contig(header, sequence, outfile, total_contigs, contigs_with_n,
                   discarded_only_N, discarded_too_short,
                   total_length, min_length, max_length, contig_lengths):
    """
    Processes a single contig: filters, counts, and writes to file if valid.
    """
    if sequence:
        total_contigs += 1
        contig_length = len(sequence)

        if all(base == "N" for base in sequence):
            discarded_only_N += 1
        elif contig_length < MIN_CONTIG_LENGTH:
            discarded_too_short += 1
        else:
            if "N" in sequence:
                contigs_with_n += 1
            outfile.write(f"{header}\n{sequence}\n")
            total_length += contig_length
            contig_lengths.append(contig_length)
            min_length = min(min_length, contig_length)
            max_length = max(max_length, contig_length)

    return (total_contigs, contigs_with_n, discarded_only_N, discarded_too_short,
            total_length, min_length, max_length, contig_lengths)

def process_fasta(input_fasta, output_fasta, output_info):
    total_contigs = 0
    contigs_with_n = 0
    discarded_only_N = 0
    discarded_too_short = 0
    total_length = 0
    min_length = float('inf')
    max_length = 0
    contig_lengths = []

    current_contig = None
    sequence = ""

    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"):
                if current_contig is not None:
                    (total_contigs, contigs_with_n, discarded_only_N, discarded_too_short,
                     total_length, min_length, max_length, contig_lengths) = process_contig(
                        current_contig, sequence, outfile, total_contigs, contigs_with_n,
                        discarded_only_N, discarded_too_short, total_length, min_length, max_length, contig_lengths
                    )
                current_contig = line
                sequence = ""
            else:
                sequence += line.upper()

        if current_contig is not None:
            (total_contigs, contigs_with_n, discarded_only_N, discarded_too_short,
             total_length, min_length, max_length, contig_lengths) = process_contig(
                current_contig, sequence, outfile, total_contigs, contigs_with_n,
                discarded_only_N, discarded_too_short, total_length, min_length, max_length, contig_lengths
            )

    filtered_contigs = total_contigs - discarded_only_N - discarded_too_short
    average_length = (total_length / filtered_contigs) if filtered_contigs > 0 else 0
    median_length = statistics.median(contig_lengths) if contig_lengths else 0
    try:
        mode_length = statistics.mode(contig_lengths)
    except statistics.StatisticsError:
        mode_length = "No unique mode"

    with open(output_info, 'w') as info_file:
        info_file.write(f"Total contigs before filtering: {total_contigs}\n")
        info_file.write(f"Total contigs after filtering: {filtered_contigs}\n")
        info_file.write(f"Contigs containing at least one 'N': {contigs_with_n}\n")
        info_file.write(f"Number of discarded contigs (only 'N's): {discarded_only_N}\n")
        info_file.write(f"Number of discarded contigs (too short < {MIN_CONTIG_LENGTH}): {discarded_too_short}\n")
        info_file.write(f"Average size of contigs: {average_length:.2f}\n")
        info_file.write(f"Median contig length: {median_length}\n")
        info_file.write(f"Mode contig length: {mode_length}\n")
        info_file.write(f"Minimum contig length: {min_length if filtered_contigs else 'N/A'}\n")
        info_file.write(f"Maximum contig length: {max_length if filtered_contigs else 'N/A'}\n")
        info_file.write(f"Filtered FASTA saved to: {output_fasta}\n")


# Usage: python clean_fasta.py input.fasta output.fasta output_info.txt
if __name__ == "__main__":

    input_fasta = "assembly.fasta"
    output_fasta = "clean.fasta"
    output_info = "cleaning_info.txt"
    process_fasta(input_fasta, output_fasta, output_info)

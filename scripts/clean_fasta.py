import sys

def process_contig(header, sequence, outfile, total_contigs, contigs_with_n, discarded_contigs):
    """
    Processes a single contig: filters, counts, and writes to file if valid.
    """
    if sequence:
        total_contigs += 1
        if all(base == "N" for base in sequence):  # Contig is only "N"
            discarded_contigs += 1
        else:
            if "N" in sequence:
                contigs_with_n += 1
            outfile.write(f"{header}\n{sequence}\n")  # Write valid contig

    return total_contigs, contigs_with_n, discarded_contigs

def process_fasta(input_fasta, output_fasta, output_info):
    total_contigs = 0
    contigs_with_n = 0
    discarded_contigs = 0
    current_contig = None
    sequence = ""

    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"):  # Header line
                if current_contig is not None:  
                    # Process the previous contig before starting a new one
                    total_contigs, contigs_with_n, discarded_contigs = process_contig(
                        current_contig, sequence, outfile, total_contigs, contigs_with_n, discarded_contigs
                    )
                # Start new contig
                current_contig = line
                sequence = ""
            else:
                sequence += line.upper()  # Accumulate sequence

        # Process the last contig
        if current_contig is not None:
            total_contigs, contigs_with_n, discarded_contigs = process_contig(
                current_contig, sequence, outfile, total_contigs, contigs_with_n, discarded_contigs
            )

    filtered_contigs = total_contigs - discarded_contigs

    # Save output statistics to a text file
    with open(output_info, 'w') as info_file:
        info_file.write(f"Total contigs before filtering: {total_contigs}\n")
        info_file.write(f"Total contigs after filtering: {filtered_contigs}\n")
        info_file.write(f"Contigs containing at least one 'N': {contigs_with_n}\n")
        info_file.write(f"Number of discarded contigs: {discarded_contigs}\n")
        info_file.write(f"Filtered FASTA saved to: {output_fasta}\n")

# Usage: python clean_fasta.py input.fasta output.fasta output_info.txt
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 clean_fasta.py <input.fasta> <output.fasta> <output_info.txt>")
        sys.exit(1)
    
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    output_info = sys.argv[3]
    process_fasta(input_fasta, output_fasta, output_info)

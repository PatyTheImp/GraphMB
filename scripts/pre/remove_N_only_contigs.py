from Bio import SeqIO

def filter_N_only_contigs(input_fasta, output_fasta):
    """
    Removes contigs that are composed only of 'N's from a fasta file.

    Args:
        input_fasta (str): Path to input fasta file.
        output_fasta (str): Path to output fasta file.
    """
    with open(output_fasta, "w") as out_handle:
        for record in SeqIO.parse(input_fasta, "fasta"):
            sequence = str(record.seq).upper()
            if set(sequence) != {"N"}:
                SeqIO.write(record, out_handle, "fasta")

if __name__ == "__main__":
    input_fasta = 'assembly.fasta'
    output_fasta = 'noAllNs.fasta'

    filter_N_only_contigs(input_fasta, output_fasta)

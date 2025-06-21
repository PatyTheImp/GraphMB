from Bio import SeqIO

INPUT = "Megahit_v1.1.4-2.fa"
OUTPUT = "Megahit-filtered.fasta"
MIN_LENGTH = 600

def filter_fasta():
    with open(OUTPUT, "w") as out_handle:
        for record in SeqIO.parse(INPUT, "fasta"):
            seq = str(record.seq).upper()
            if len(seq) < MIN_LENGTH:
                continue
            SeqIO.write(record, out_handle, "fasta")

if __name__ == "__main__":
    filter_fasta()

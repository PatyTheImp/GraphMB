from Bio import SeqIO

INPUT = "assembly.fasta"
OUTPUT = "noNs.fasta"
MIN_LENGTH = 1000

def filter_fasta():
    with open(OUTPUT, "w") as out_handle:
        for record in SeqIO.parse(INPUT, "fasta"):
            seq = str(record.seq).upper()
            if "N" in seq:
                continue
            if len(seq) < MIN_LENGTH:
                continue
            SeqIO.write(record, out_handle, "fasta")

if __name__ == "__main__":
    filter_fasta()

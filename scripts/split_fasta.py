import os

MAX_CONTIGS_PER_FILE = 100  # Maximum number of contigs per output file

def split_fasta(input_fasta):
    # Get base name without extension
    base_name = "clean"
    output_folder = f"{base_name} parts"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    file_count = 1
    contig_count = 0
    output_file = None
    outfile = None

    with open(input_fasta, 'r') as infile:
        for line in infile:
            line = line.strip()
            if line.startswith(">"):  # New contig starts
                if contig_count >= MAX_CONTIGS_PER_FILE or outfile is None:
                    # Start a new file
                    if outfile:
                        outfile.close()
                    output_file = os.path.join(output_folder, f"{base_name}{file_count}.fasta")
                    outfile = open(output_file, 'w')
                    file_count += 1
                    contig_count = 0  # Reset count for new file
                contig_count += 1  # Count contigs
            
            # Write to the current output file
            if outfile:
                outfile.write(line + "\n")

    # Close the last file
    if outfile:
        outfile.close()
    
    print(f"FASTA file split into {file_count - 1} parts inside '{output_folder}/'")

# Usage: python split_fasta.py input.fasta
if __name__ == "__main__":
    split_fasta("clean.fasta")

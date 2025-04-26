import sys

def build_header_mapping(fasta_file):
    mapping = {}
    with open(fasta_file, 'r') as infile:
        for line in infile:
            if line.startswith('>'):
                line = line.strip()
                parts = line.split('|')
                if len(parts) >= 4:
                    ref_id = parts[3]
                    rest = parts[4] if len(parts) > 4 else ''
                    coords = rest.split('_')[-1] if '_' in rest else ''
                    new_header = f"{ref_id}_{coords}"
                    mapping[line[1:]] = new_header  # Remove '>' for matching
                else:
                    mapping[line[1:]] = "contig_unknown"
    return mapping

def clean_fasta(input_fasta, output_fasta, mapping):
    with open(input_fasta, 'r') as infile, open(output_fasta, 'w') as outfile:
        for line in infile:
            if line.startswith('>'):
                old_header = line.strip()[1:]
                new_header = mapping.get(old_header, "contig_unknown")
                outfile.write(f">{new_header}\n")
            else:
                outfile.write(line)

def clean_depth(depth_file, output_depth_file, mapping):
    with open(depth_file, 'r') as infile, open(output_depth_file, 'w') as outfile:
        for line in infile:
            parts = line.strip().split('\t')
            if parts[0] in mapping:
                parts[0] = mapping[parts[0]]
            outfile.write('\t'.join(parts) + '\n')

if __name__ == "__main__":

    input_fasta = 'assembly-filtered.fa'
    output_fasta = 'assembly.fasta'
    input_depth = 'depth.txt'
    output_depth = 'assembly_depth.txt'

    # Build header mapping
    mapping = build_header_mapping(input_fasta)

    # Clean FASTA
    clean_fasta(input_fasta, output_fasta, mapping)

    # Clean depth file
    clean_depth(input_depth, output_depth, mapping)

    print(f"✅ Cleaned FASTA saved to: {output_fasta}")
    print(f"✅ Cleaned Depth saved to: {output_depth}")

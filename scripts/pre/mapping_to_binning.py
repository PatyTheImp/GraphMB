import csv

def transform_tsv(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        
        # Write custom header
        outfile.write("@Version:0.9.0\n")
        outfile.write("@SampleID:SAMPLEID\n")

        # Prepare output writer
        writer = csv.writer(outfile, delimiter='\t')
        writer.writerow(["@@SEQUENCEID", "BINID", "_LENGTH"])

        for row in reader:
            seq_id = row["#anonymous_contig_id"]
            bin_id = row["genome_id"]
            start = int(row["start_position"])
            end = int(row["end_position"])
            length = end - start + 1
            writer.writerow([seq_id, bin_id, length])

# Example usage
# transform_tsv("input.tsv", "output.tsv")
if __name__ == "__main__":
    input = "gsa_pooled_mapping.tsv"  # Replace with actual file path
    output = "labels.binning"
    transform_tsv(input, output)
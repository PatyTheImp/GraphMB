import csv

def extract_and_rename(input_tsv, output_tsv):
    with open(input_tsv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_tsv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Skip header
        header = next(reader, None)

        for row in reader:
            if not row:
                continue

            first_col = row[0]
            last_col = row[-1].strip().lower()

           # if last_col in ("virus", "plasmid", "unknown"):
            if last_col in ("virus", "plasmid"):
                last_col = "circular element"
            else:
                last_col = row[-1]  # original value preserved

            writer.writerow([first_col, last_col])


if __name__ == "__main__":
    extract_and_rename('metadata.tsv', 'unique_common.tsv')

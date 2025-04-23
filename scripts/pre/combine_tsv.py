
from pathlib import Path

def combine_tsv_files(folder_path):
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"Invalid folder path: {folder_path}")
        return

    tsv_files = sorted(folder.glob("*.tsv"))
    if not tsv_files:
        print("No TSV files found in the provided folder.")
        return

    output_path = Path(__file__).parent / "marker_gene_stats.tsv"

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for idx, file in enumerate(tsv_files):
            with open(file, 'r', encoding='utf-8') as infile:
                for line_num, line in enumerate(infile):
                    # Write header only from the first file
                    if idx == 0 or line_num > 0:
                        outfile.write(line)

    print(f"Combined file saved to: {output_path}")

if __name__ == "__main__":
    combine_tsv_files("./markers")

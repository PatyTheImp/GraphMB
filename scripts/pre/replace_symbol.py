import sys
import os

def replace_symbol(input_file, old_symbol, new_symbol, output_file):
    if not os.path.isfile(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)

    with open(input_file, 'r') as f:
        content = f.read()

    content = content.replace(old_symbol, new_symbol)

    with open(output_file, 'w') as f:
        f.write(content)

    print(f"Replaced '{old_symbol}' with '{new_symbol}' in {input_file} → {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 replace_symbol.py <old_symbol> <new_symbol>")
        sys.exit(1)

    _, old_symbol, new_symbol = sys.argv
    replace_symbol("marker_gene_stats_.tsv", old_symbol, new_symbol, "marker_gene_stats.tsv")

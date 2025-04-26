import ast

def simplify_contig_id(old_id):
    try:
        parts = old_id.split('_')
        ref_index = parts.index('ref')
        ref_id = parts[ref_index + 1]
        coords = parts[-1]
        return f"{ref_id}_{coords}"
    except (ValueError, IndexError):
        return "unknown_contig"

def simplify_subcontig_id(sub_id):
    try:
        parts = sub_id.split('_')
        ref_index = parts.index('ref')
        ref_id = parts[ref_index + 1]
        coords = parts[-2]  # 1-5871
        number = parts[-1]  # sub-region like _5
        return f"{ref_id}_{coords}_{number}"
    except (ValueError, IndexError):
        return "unknown_subcontig"

def fix_markers_file(input_markers, output_markers):
    with open(input_markers, 'r') as infile, open(output_markers, 'w') as outfile:
        for line in infile:
            if line.strip():
                parts = line.strip().split('\t', 1)
                old_id = parts[0]
                rest = parts[1] if len(parts) > 1 else '{}'

                # Simplify the main contig ID
                simplified_id = simplify_contig_id(old_id)

                # Parse and simplify internal dictionary
                try:
                    marker_dict = ast.literal_eval(rest)
                    new_marker_dict = {}
                    for sub_id, genes in marker_dict.items():
                        new_sub_id = simplify_subcontig_id(sub_id)
                        new_marker_dict[new_sub_id] = genes
                except Exception as e:
                    print(f"Warning: Couldn't parse dict for {old_id}: {e}")
                    new_marker_dict = {}

                outfile.write(f"{simplified_id}\t{new_marker_dict}\n")

    print(f"✅ Fully corrected markers file saved to: {output_markers}")

if __name__ == "__main__":  
    fix_markers_file('marker_gene_stats_.tsv', 'marker_gene_stats.tsv')

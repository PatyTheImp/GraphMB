#!/usr/bin/env python3
import ast

def main():
    infile = "marker_gene_stats.tsv"
    outfile = "marker_gene_stats_rename.tsv"
    with open(infile) as fin, open(outfile, "w") as fout:
        for line in fin:
            line = line.rstrip("\n")
            if not line:
                fout.write("\n")
                continue

            # split into bin and dict‐string
            parts = line.split("\t", 1)
            if len(parts) != 2:
                # not a two‐column line? just pass through
                fout.write(line + "\n")
                continue

            bin_id, dict_str = parts
            # 1) replace ALL underscores in the bin ID with pipes
            new_bin = bin_id.replace("_", "|")

            # 2) try to parse the dictionary on the RHS
            try:
                data = ast.literal_eval(dict_str)
            except Exception:
                # if it isn't valid Python, just emit the renamed bin
                fout.write(f"{new_bin}\t{dict_str}\n")
                continue

            # 3) rebuild contig names
            new_data = {}
            for contig, hits in data.items():
                # grab suffix after the last '_' in the original contig
                if "_" in contig:
                    suffix = contig.rsplit("_", 1)[1]
                else:
                    suffix = contig
                # build new contig name as NEW_BIN + "_" + suffix
                new_contig = f"{new_bin}_{suffix}"
                new_data[new_contig] = hits

            # 4) write out
            fout.write(f"{new_bin}\t{new_data!r}\n")


if __name__ == "__main__":
    main()

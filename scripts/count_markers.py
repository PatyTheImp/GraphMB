
def count_non_empty_entries(filepath):
    count = 0
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2 and parts[1].strip() != '{}':
                count += 1
    return count

if __name__ == "__main__":
    result = count_non_empty_entries('marker_gene_stats.tsv')
    print(f"Number of markers: {result}")

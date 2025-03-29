import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to process the TSV file
def process_f1_scores(input_tsv):
    # Load the TSV file
    df = pd.read_csv(input_tsv, sep='\t')

    # Calculate F1-score
    df['F1-score'] = 2 * (df['Purity (bp)'] * df['Completeness (bp)']) / (df['Purity (bp)'] + df['Completeness (bp)'])

    # Count bins based on F1-score thresholds
    total_bins = len(df)
    bins_f1_05 = len(df[df['F1-score'] > 0.5])
    bins_f1_06 = len(df[df['F1-score'] > 0.6])
    bins_f1_07 = len(df[df['F1-score'] > 0.7])
    bins_f1_08 = len(df[df['F1-score'] > 0.8])
    bins_f1_09 = len(df[df['F1-score'] > 0.9])

    # Save count information to a text file
    output_txt = "F1_bin_count.txt"
    with open(output_txt, 'w') as f:
        f.write(f"Total bins: {total_bins}\n")
        f.write(f"Bins with F1 > 0.5: {bins_f1_05}\n")
        f.write(f"Bins with F1 > 0.6: {bins_f1_06}\n")
        f.write(f"Bins with F1 > 0.7: {bins_f1_07}\n")
        f.write(f"Bins with F1 > 0.8: {bins_f1_08}\n")
        f.write(f"Bins with F1 > 0.9: {bins_f1_09}\n")

    # Prepare data for Seaborn stacked bar chart
    data = pd.DataFrame({
        'F1 Range': ['F1 > 0.9', 'F1 > 0.8', 'F1 > 0.7', 'F1 > 0.6', 'F1 > 0.5'],
        'Count': [bins_f1_09, 
                  bins_f1_08-bins_f1_09, 
                  bins_f1_07-bins_f1_08, 
                  bins_f1_06-bins_f1_07, 
                  bins_f1_05-bins_f1_06]
    })

    # Define colors matching the reference image
    colors = ["#FFFF33", "#41AB5D", "#1D91C0", "#253494", "#3F007D"]

    # Create a stacked bar chart using Seaborn
    plt.figure(figsize=(8, 2))
    sns.set_style("whitegrid")

    # Create a single stacked bar
    bottom = 0
    for i, (label, count) in enumerate(zip(data['F1 Range'], data['Count'])):
        sns.barplot(x=[count], y=["GraphMB"], color=colors[i], label=label, left=bottom)
        bottom += count

    # Labels and title
    plt.xlabel("Number of Bins")
    plt.title("Bin Count by F1 Score Ranges")
    plt.legend(title="F1 Ranges", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot
    output_png = "F1_bin_count_plot.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()

    print(f"Results saved in '{output_txt}' and '{output_png}'.")

# Example usage
if __name__ == "__main__":
    input_tsv = "metrics_per_bin.tsv"  # Replace with actual file path
    process_f1_scores(input_tsv)

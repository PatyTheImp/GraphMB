import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def load_checkm_report(file_path):
    df = pd.read_csv(file_path, sep='\t')
    df.columns = [col.lower() for col in df.columns]
    required_cols = ['completeness', 'contamination']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    return df

def classify_bins(df):
    conditions = []
    for _, row in df.iterrows():
        if row['completeness'] > 90 and row['contamination'] < 5:
            conditions.append('High-quality')
        elif row['completeness'] > 50 and row['contamination'] < 10:
            conditions.append('Medium-quality')
        else:
            conditions.append('Low-quality')
    df['quality_class'] = conditions
    return df

def plot_histogram(df, column, title, xlabel, output_path):
    plt.figure(figsize=(8,5))
    sns.set_theme(style="whitegrid", font_scale=1.1)
    sns.histplot(df[column], bins=30, kde=True, color="#5dade2")
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel)
    plt.ylabel("Number of Bins")
    plt.grid(True, linestyle=':', linewidth=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_scatter_completeness_vs_contamination(df, output_path):
    plt.figure(figsize=(8,6))
    sns.set_theme(style="whitegrid", font_scale=1.1)

    # Create a size column scaled for visualization
    df['Bin size (Mbp)'] = df['genome_size'] / 1e6  # Adjust divisor if needed
    df['Bin quality'] = df['quality_class']

    # Scatter plot using seaborn
    sns.scatterplot(
        data=df,
        x='completeness',
        y='contamination',
        hue='Bin quality',
        size='Bin size (Mbp)',
        sizes=(20, 500),  # Minimum and maximum bubble size
        alpha=0.6,
        edgecolor='w',
        linewidth=0.5,
        palette={'High-quality': 'green', 'Medium-quality': 'orange', 'Low-quality': 'red'}
    )

    # Cutoff lines
    plt.axhline(5, color='gray', linestyle='--', linewidth=1)
    plt.axvline(90, color='gray', linestyle='--', linewidth=1)

    # Title and labels
    plt.title("Completeness vs Contamination (CheckM2)", fontsize=14, fontweight='bold')
    plt.xlabel("Completeness (%)")
    plt.ylabel("Contamination (%)")

    # Clean layout
    plt.grid(True, linestyle=':', linewidth=0.7)
    plt.tight_layout()

    # Save and show
    plt.savefig(output_path, dpi=300)


def plot_quality_bar(df, output_path):
    plt.figure(figsize=(6,5))
    sns.set_theme(style="whitegrid", font_scale=1.1)
    sns.countplot(data=df, x='quality_class', hue='quality_class',
                  order=['High-quality', 'Medium-quality', 'Low-quality'],
                  palette='pastel', legend=False)
    plt.title("Bins per Quality Class (CheckM2)", fontsize=14, fontweight='bold')
    plt.xlabel("Quality Class")
    plt.ylabel("Number of Bins")
    plt.grid(True, axis='y', linestyle=':', linewidth=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_boxplot(df, column, title, ylabel, output_path):
    plt.figure(figsize=(6,5))
    sns.set_theme(style="whitegrid", font_scale=1.1)
    sns.boxplot(y=df[column], color="#a3c4f3")
    plt.title(title, fontsize=14, fontweight='bold')
    plt.ylabel(ylabel)
    plt.grid(True, axis='y', linestyle=':', linewidth=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

def generate_binning_report(input_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    df = load_checkm_report(input_file)
    df = classify_bins(df)

    total_bins = len(df)
    hq_bins = (df['quality_class'] == 'High-quality').sum()
    mq_bins = (df['quality_class'] == 'Medium-quality').sum()
    lq_bins = (df['quality_class'] == 'Low-quality').sum()
    hq_bin_percentage = round(hq_bins / total_bins * 100, 2)

    # Compute averages
    avg_completeness = df['completeness'].mean()
    avg_purity = (1 - df['contamination'] / 100).mean() * 100  # Purity in %

    print(f"✅ Total bins: {total_bins}")
    print(f"✅ High-quality bins: {hq_bins}")
    print(f"✅ Medium-quality bins: {mq_bins}")
    print(f"✅ Low-quality bins: {lq_bins}")
    print(f"✅ Average Completeness: {avg_completeness:.2f}%")
    print(f"✅ Average Purity: {avg_purity:.2f}%")

    # Save annotated table
    df.to_csv(os.path.join(output_folder, "annotated_quality_report.tsv"), sep='\t', index=False)

    # Save summary table
    summary_data = {
        'Metric': [
            'Total_bins',
            'High_quality_bins',
            'High_quality_percentage',
            'Medium_quality_bins',
            'Low_quality_bins',
            'Average_completeness',
            'Average_purity'
        ],
        'Value': [
            total_bins,
            hq_bins,
            hq_bin_percentage,
            mq_bins,
            lq_bins,
            round(avg_completeness, 2),
            round(avg_purity, 2)
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(output_folder, "binning_summary.tsv"), sep='\t', index=False)

    # Add Purity column temporarily for boxplot
    df['purity'] = (1 - df['contamination'] / 100) * 100

    # Generate plots
    plot_histogram(df, 'completeness', "Distribution of Bin Completeness (CheckM2)", "Completeness (%)",
                   os.path.join(output_folder, "completeness_histogram.png"))

    plot_histogram(df, 'contamination', "Distribution of Bin Contamination (CheckM2)", "Contamination (%)",
                   os.path.join(output_folder, "contamination_histogram.png"))

    plot_scatter_completeness_vs_contamination(df,
                   os.path.join(output_folder, "completeness_vs_contamination_scatter.png"))

    plot_quality_bar(df,
                   os.path.join(output_folder, "bins_per_quality_class_barplot.png"))

    plot_boxplot(df, 'completeness', "Bin Completeness Distribution (CheckM2)", "Completeness (%)",
                 os.path.join(output_folder, "completeness_boxplot.png"))

    plot_boxplot(df, 'purity', "Bin Purity Distribution (CheckM2)", "Purity (%)",
                 os.path.join(output_folder, "purity_boxplot.png"))

    print(f"📊 All plots and summaries saved to: {output_folder}")

if __name__ == "__main__":
    input_file = "quality_report.tsv"  # <-- adjust filename if needed
    output_folder = "checkm2_quality_report"
    generate_binning_report(input_file, output_folder)

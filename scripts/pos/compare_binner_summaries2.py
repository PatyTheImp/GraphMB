import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn.objects as so

def load_summaries_from_folders(base_dir):
    summary_rows = []
    bin_dataframes = []

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if not os.path.isdir(folder_path):
            continue

        # Expected files
        summary_path = os.path.join(folder_path, "binning_summary.tsv")
        annotated_path = os.path.join(folder_path, "annotated_quality_report.tsv")

        if not (os.path.exists(summary_path) and os.path.exists(annotated_path)):
            print(f"⚠️ Skipping {folder}: required files not found.")
            continue

        # Load and tag
        summary_df = pd.read_csv(summary_path, sep="\t")
        summary_dict = summary_df.set_index("Metric")["Value"].to_dict()
        summary_dict["binner"] = folder
        summary_rows.append(summary_dict)

        bin_df = pd.read_csv(annotated_path, sep="\t")
        bin_df["binner"] = folder
        # Ensure purity is present — calculate it if not
        if "purity" not in bin_df.columns and "contamination" in bin_df.columns:
            bin_df["purity"] = 1 - bin_df["contamination"] / 100  # assuming contamination is in %
        bin_dataframes.append(bin_df)

    summary_all = pd.DataFrame(summary_rows)
    bins_all = pd.concat(bin_dataframes, ignore_index=True)
    return summary_all, bins_all

def plot_bar(df, metric, ylabel, title, output_file):
    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")

    barplot = sns.barplot(
        data=df,
        y="binner",
        x=metric,
        hue="binner",
        dodge=False,
        palette="muted",
        legend=False
    )

    plt.xlabel(ylabel)
    plt.title(title)

    for i, bar in enumerate(barplot.patches):
            binner = df.iloc[i]["binner"]
            hq_pct = df.iloc[i]["High_quality_percentage"]
            total_bins = int(df.iloc[i]["Total_bins"])
            label = f"{hq_pct:.1f}%\n({total_bins} bins)"
            barplot.text(
                bar.get_width() + 1,  # Slightly to the right of the bar
                bar.get_y() + bar.get_height() / 2,
                label,
                va="center",
                fontsize=9
            )
        
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

def plot_stacked_quality_bar(df, output_file):
    # Prepare the data
    cols = [
        "High_quality_bins",
        "High_quality2_bins",
        "Medium_quality2_bins",
        "Medium_quality_bins"
    ]
    data = df[["binner"] + cols].copy()

    data_long = data.melt(id_vars="binner", var_name="Quality", value_name="Count")
    data_long["Quality"] = data_long["Quality"].replace({
        "High_quality_bins": "High-quality",
        "High_quality2_bins": "High-quality2",
        "Medium_quality2_bins": "Medium-quality2",
        "Medium_quality_bins": "Medium-quality"
    })

    custom_palette = {
        "High-quality": "#132a13",
        "High-quality2": "#31572c",
        "Medium-quality2": "#4f772d",
        "Medium-quality": "#90a955"
    }

    (
        so.Plot(data_long, y="binner", x="Count", color="Quality")
        .add(so.Bar(edgealpha=0), so.Stack())
        .scale(color=custom_palette)
        .label(x="Number of Bins", y="Software", title="High- and Medium-Quality Bins per Binner (Extended Classes)")
        .save(output_file, dpi=300, bbox_inches="tight")
    )


def plot_box(df, metric, ylabel, title, output_file):
    plt.figure(figsize=(8, 5))
    sns.set_theme(style="whitegrid")
    sns.boxplot(data=df, y="binner", x=metric, hue="binner", dodge=False, palette="muted", legend=False)
    plt.xlabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()

def plot_kde(data, metric, output_file, xlabel=None):
    (
        so.Plot(data, x=metric)  
        .add(so.Area(), so.KDE(), color="binner")
        .label(
            x=xlabel or metric.capitalize(),
            y="Density",
            color="Software",
            title=f"{metric.capitalize()} Distribution (KDE)"
        )
        .save(output_file, dpi=300, bbox_inches="tight")
    )

def main(base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    summary_df, bins_df = load_summaries_from_folders(base_dir)

    # Save combined summaries
    summary_df.to_csv(os.path.join(output_dir, "all_binners_summary.tsv"), sep='\t', index=False)
    bins_df.to_csv(os.path.join(output_dir, "all_binners_bins.tsv"), sep='\t', index=False)

    # Bar plots
    plot_stacked_quality_bar(summary_df, os.path.join(output_dir, "hq_mq_stacked_bar.png"))
    plot_bar(summary_df, "High_quality_percentage", "% High-Quality", "HQ Bin Percentage per Binner", os.path.join(output_dir, "hq_percentage.png"))

    # Boxplots
    plot_box(bins_df, "completeness", "Completeness (%)", "Completeness per Bin", os.path.join(output_dir, "completeness_boxplot.png"))
    plot_box(bins_df, "purity", "Purity", "Purity per Bin", os.path.join(output_dir, "purity_boxplot.png"))

    # KDE plots
    plot_kde(
        bins_df,
        metric="completeness",
        output_file=os.path.join(output_dir, "completeness_kde.png"),
        xlabel="Completeness (%)"
    )
    plot_kde(
        bins_df,
        metric="purity",
        output_file=os.path.join(output_dir, "purity_kde.png"),
        xlabel="Purity"
    )

    print("✅ Plots and summaries saved to:", output_dir)

if __name__ == "__main__":
    main('summaries2', 'plots2')

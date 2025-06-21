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

        summary_path = os.path.join(folder_path, "binning_summary.tsv")
        annotated_path = os.path.join(folder_path, "annotated_quality_report.tsv")

        if not (os.path.exists(summary_path) and os.path.exists(annotated_path)):
            print(f"⚠️ Skipping {folder}: required files not found.")
            continue

        summary_df = pd.read_csv(summary_path, sep="\t")
        summary_dict = summary_df.set_index("Metric")["Value"].to_dict()
        summary_dict["binner"] = folder
        summary_rows.append(summary_dict)

        bin_df = pd.read_csv(annotated_path, sep="\t")
        bin_df["binner"] = folder
        if "purity" not in bin_df.columns and "contamination" in bin_df.columns:
            bin_df["purity"] = 1 - bin_df["contamination"] / 100
        bin_dataframes.append(bin_df)

    summary_all = pd.DataFrame(summary_rows)
    bins_all = pd.concat(bin_dataframes, ignore_index=True)
    return summary_all, bins_all


def plot_combined(summary_df, bins_df, output_file):
    sns.set_theme(style="whitegrid")
    # Extract binner order and total bins
    binners = summary_df["binner"].tolist()
    total_bins_map = dict(zip(summary_df["binner"], summary_df["Total_bins"]))

    fig, axes = plt.subplots(1, 4, figsize=(32, 8), constrained_layout=True)

    # 1: Completeness boxplot with y-labels including bin counts
    sns.boxplot(
        data=bins_df,
        y="binner", x="completeness",
        order=binners,
        palette="muted",
        dodge=False,
        ax=axes[0]
    )
    axes[0].set_xlabel("Completeness (%)")
    axes[0].set_ylabel("")
    axes[0].set_title("Average Completeness")
    # Annotate y-tick labels with integer bin counts
    labels = [f"{b} ({int(total_bins_map[b])} bins)" for b in binners]
    axes[0].set_yticklabels(labels)

    # 2: Purity boxplot without y-tick labels
    sns.boxplot(
        data=bins_df,
        y="binner", x="purity",
        order=binners,
        palette="muted",
        dodge=False,
        ax=axes[1]
    )
    axes[1].set_xlabel("Purity")
    axes[1].set_ylabel("")
    axes[1].set_title("Average Purity")
    axes[1].set_yticklabels([])

    # 3: HQ percentage bar plot without y-tick labels
    sns.barplot(
        data=summary_df,
        y="binner",
        x="High_quality_percentage",
        order=binners,
        palette="muted",
        dodge=False,
        ax=axes[2]
    )
    axes[2].set_xlabel("% High-Quality")
    axes[2].set_ylabel("")
    axes[2].set_title("HQ Bins Percentage")
    axes[2].set_yticklabels([])

    # 4: Stacked HQ/MQ bar with matching order and no y-tick labels
    data = summary_df.set_index("binner").loc[binners, ["High_quality_bins", "Medium_quality_bins"]]
    custom_colors = ["#4f518c", "#907ad6"]
    data.plot(
        kind="barh",
        stacked=True,
        ax=axes[3],
        color=custom_colors,
        legend=False
    )
    axes[3].set_xlabel("Number of Bins")
    axes[3].set_ylabel("")
    axes[3].set_title("High- and Medium-Quality Bins")
    axes[3].invert_yaxis()
    axes[3].set_yticklabels([])

    # Save and close
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main(base_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    summary_df, bins_df = load_summaries_from_folders(base_dir)

    plot_combined(summary_df, bins_df, os.path.join(output_dir, "combined_1x4.png"))
    print("✅ Combined plot saved to:", output_dir)

if __name__ == "__main__":
    main('summaries', 'plots')

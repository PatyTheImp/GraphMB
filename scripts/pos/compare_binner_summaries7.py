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


def plot_combined(output_file):
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(32, 16), constrained_layout=True)

    # Flatten to a 1D list of length 6
    axes = axes.flatten()

    label_size = 40
    tick_size = 36

    for i in range(0,3):
        summary_df, _ = load_summaries_from_folders(f'summaries{i}')

        # Extract binner order and total bins
        binners = summary_df["binner"].tolist()

        if i == 0:
            ylabel = 'Cow Rumen'
        elif i == 1:
            ylabel = 'AalE'
        elif i == 2:
            ylabel = 'Soil'

        # 4: Stacked HQ/MQ bar with matching order and no y-tick labels
        data = summary_df.set_index("binner").loc[binners, ["High_quality_bins", "Medium_quality_bins"]]
        custom_colors = ["#4f518c", "#907ad6"]
        data.plot(
            kind="barh",
            stacked=True,
            ax=axes[i],
            color=custom_colors,
            legend=False
        )
        axes[i].set_xlabel("")
        axes[i].set_ylabel(ylabel, fontsize=label_size, fontweight='bold')
        axes[i].set_title("")
        axes[i].invert_yaxis()
        if i == 0 or i == 3:
            labels = [f"{b}" for b in binners]
            axes[i].set_yticklabels(labels, fontsize=label_size)
        else:
            axes[i].set_yticklabels([])
        axes[i].tick_params(axis='x', labelsize=tick_size)


    # Save and close
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main(output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plot_combined(os.path.join(output_dir, "combined.png"))
    print("✅ Combined plot saved to:", output_dir)

if __name__ == "__main__":
    main('plots')

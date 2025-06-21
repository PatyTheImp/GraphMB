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
    fig, axes = plt.subplots(4, 4, figsize=(32, 24), constrained_layout=True)

    title_size = 48
    label_size = 40
    tick_size = 36

    for i in range(0,4):
        summary_df, bins_df = load_summaries_from_folders(f'summaries{i}')

        # Extract binner order and total bins
        binners = summary_df["binner"].tolist()

        # 1: Completeness boxplot with y-labels including bin counts
        sns.boxplot(
            data=bins_df,
            y="binner", x="completeness",
            order=binners,
            palette="muted",
            dodge=False,
            ax=axes[i,0]
        )
        if i == 3:
            axes[i,0].set_xlabel("Completeness (%)", fontsize=label_size)
        else:
            axes[i,0].set_xlabel("")
        
        if i == 0:
            ylabel = 'Marine'
        elif i == 1:
            ylabel = 'Plant'
        elif i == 2:
            ylabel = 'CAMI-High'
        elif i == 3:
            ylabel = 'MetaHIT'

        axes[i,0].set_ylabel(ylabel, fontsize=label_size, fontweight='bold')
        if i == 0:
            axes[i,0].set_title("a", fontsize=title_size, fontweight='bold')
        else:
            axes[i,0].set_title("")
        # Annotate y-tick labels with integer bin counts
        labels = [f"{b}" for b in binners]
        axes[i,0].set_yticklabels(labels, fontsize=label_size)
        axes[i,0].tick_params(axis='x', labelsize=tick_size) 

        # 2: Purity boxplot without y-tick labels
        sns.boxplot(
            data=bins_df,
            y="binner", x="purity",
            order=binners,
            palette="muted",
            dodge=False,
            ax=axes[i,1]
        )
        if i == 3:
            axes[i,1].set_xlabel("Purity", fontsize=label_size)
        else:
            axes[i,1].set_xlabel("")
        axes[i,1].set_ylabel("")
        if i == 0:
            axes[i,1].set_title("b", fontsize=title_size, fontweight='bold')
        else:
            axes[i,1].set_title("")
        axes[i,1].set_yticklabels([])
        axes[i,1].tick_params(axis='x', labelsize=tick_size)

        # 3: HQ percentage bar plot without y-tick labels
        sns.barplot(
            data=summary_df,
            y="binner",
            x="High_quality_percentage",
            order=binners,
            palette="muted",
            dodge=False,
            ax=axes[i,2]
        )
        if i == 3:
            axes[i,2].set_xlabel("% High-Quality", fontsize=label_size)
        else:
            axes[i,2].set_xlabel("")
        axes[i,2].set_ylabel("")
        if i == 0:
            axes[i,2].set_title("c", fontsize=title_size, fontweight='bold')
        else:
            axes[i,2].set_title("")
        axes[i,2].set_yticklabels([])
        axes[i,2].tick_params(axis='x', labelsize=tick_size)

        # 4: Stacked HQ/MQ bar with matching order and no y-tick labels
        data = summary_df.set_index("binner").loc[binners, ["High_quality_bins", "Medium_quality_bins"]]
        custom_colors = ["#4f518c", "#907ad6"]
        data.plot(
            kind="barh",
            stacked=True,
            ax=axes[i,3],
            color=custom_colors,
            legend=False
        )
        if i == 3:
            axes[i,3].set_xlabel("Number of Bins", fontsize=label_size)
        else: 
            axes[i,3].set_xlabel("")
        axes[i,3].set_ylabel("")
        if i == 0:
            axes[i,3].set_title("d", fontsize=title_size, fontweight='bold')
        else:
            axes[i,3].set_title("")
        axes[i,3].invert_yaxis()
        axes[i,3].set_yticklabels([])
        axes[i,3].tick_params(axis='x', labelsize=tick_size)

    # Save and close
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main(output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plot_combined(os.path.join(output_dir, "combined.png"))
    print("✅ Combined plot saved to:", output_dir)

if __name__ == "__main__":
    main('plots')

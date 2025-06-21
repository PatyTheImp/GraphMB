import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1) Load + clean column names
df = pd.read_csv('times.tsv', sep='\t')
df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
code = df["code"].tolist()

# 2) Parse both time strings into minutes
df['time_A_m'] = pd.to_timedelta(df['time']).dt.total_seconds() / 60
df['time_B_m'] = pd.to_timedelta(df['time (m)']).dt.total_seconds() / 60

# 3) Melt to long form so hue works
df_long = df.melt(
    id_vars=['# Contigs'],
    value_vars=['time_A_m', 'time_B_m'],
    var_name='time_type',
    value_name='time_m'
)

# 4) Optional: give human‐friendly labels
label_map = {
    'time_A_m': 'without markers',
    'time_B_m': 'with markers'
}
df_long['time_type'] = df_long['time_type'].map(label_map)

# 5) Plot with lmplot + hue
sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(1, 3, figsize=(32, 12), constrained_layout=True)
label_size = 40
tick_size = 36

ax = axes[0]

for time_label, marker, color in [
    ('without markers', 'o', '#1f77b4'),
    ('with markers',    's', '#ff7f0e'),
]:
    subset = df_long[df_long['time_type'] == time_label]
    # scatter+fit line in one shot
    sns.regplot(
        data=subset,
        x='# Contigs',
        y='time_m',
        ax=ax,
        scatter=True,
        scatter_kws={'marker': marker, 's': 60, 'alpha': 0.7, 'color': color},
        line_kws   ={'linewidth': 2,               'color': color},
        ci=95
    )

ax.set_xlabel('# Contigs',      fontsize=label_size)
ax.set_ylabel('Time (minutes)', fontsize=label_size)
ax.tick_params(labelsize=tick_size)
# ax.legend(['without markers', '', '','with markers'], fontsize=tick_size, loc='upper left' )
# Define custom legend handles
legend_handles = [
    Line2D([0], [0],
           marker='o', linestyle='',
           markersize=10,
           markerfacecolor='#1f77b4',
           alpha=0.7,
           label='without markers'),
    Line2D([0], [0],
           marker='o', linestyle='',
           markersize=10,
           markerfacecolor='#ff7f0e',
           alpha=0.7,
           label='with markers'),
]

# Place the legend
ax.legend(
    handles=legend_handles,
    loc='upper left',
    fontsize=tick_size,
)

# 7) HQ/min
sns.barplot(
    data=df,
    y="code",
    x="HQ/min",
    order=code,
    palette="muted",
    dodge=False,
    ax=axes[1]
)
axes[1].set_xlabel("HQ/min", fontsize=label_size)
axes[1].set_ylabel("")
labels = [f"{c}" for c in code]
axes[1].set_yticklabels(labels, fontsize=label_size)
axes[1].tick_params(axis='x', labelsize=tick_size)

# 8) MQ/min
sns.barplot(
    data=df,
    y="code",
    x="MQ/min",
    order=code,
    palette="muted",
    dodge=False,
    ax=axes[2]
)
axes[2].set_xlabel("MQ/min", fontsize=label_size)
axes[2].set_ylabel("")
axes[2].set_yticklabels([])
axes[2].tick_params(axis='x', labelsize=tick_size)


# 9) Save
plt.savefig('times.png', dpi=300, bbox_inches='tight')
plt.close(fig)

    

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Load + clean column names
df = pd.read_csv('times.tsv', sep='\t')
df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

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
g = sns.lmplot(
    data=df_long,
    x='# Contigs',
    y='time_m',
    hue='time_type',
    markers=['o','s'],
    palette=['#1f77b4', '#ff7f0e'],
    scatter_kws={'s':60, 'alpha':0.7},
    line_kws={'linewidth':2},
    height=6,
    aspect=1.3,
    ci=95
)

# 6) Labels
plt.xlabel('# Contigs',      fontsize=14)
plt.ylabel('Time (minutes)', fontsize=14)
plt.tight_layout()

# 7) Save/show
plt.savefig('time_comparison_corrected.png', dpi=300)
plt.show()

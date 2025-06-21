import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Load TSV file
file_path = "bins.tsv"  # <--- Change this to your filename
file_name = Path(file_path).stem
df = pd.read_csv(file_path, sep='\t')

# Extract data
tools = df['Tool']
hq_gsa = df['#HQ bins (GSA)']
mq_gsa = df['#MQ bins (GSA)'] 
hq_ma = df['#HQ bins (MA)']
mq_ma = df['#MQ bins (MA)'] 

# Set bar positions
y = np.arange(len(tools)) * 2
bar_height = 0.8

# Plot
fig, ax = plt.subplots(figsize=(12, 8))

# You can define any colors you like here
color_mq_gsa = '#aec7e8'  # light blue
color_hq_gsa = '#1f77b4'  # blue 
color_mq_ma  = '#ffbb78'  # light orange 
color_hq_ma  = '#ff7f0e'  # orange

# Stacked bars for GSA
ax.barh(y, mq_gsa, height=bar_height, left=hq_gsa, label='MQ (GSA)', color=color_mq_gsa)
ax.barh(y, hq_gsa, height=bar_height, label='HQ (GSA)', color=color_hq_gsa)

# Stacked bars for MA
ax.barh(y + 1, mq_ma, height=bar_height, left=hq_ma, label='MQ (MA)', color=color_mq_ma)
ax.barh(y + 1, hq_ma, height=bar_height, label='HQ (MA)', color=color_hq_ma)

# Y-axis labels
yticks = y + 0.5
yticklabels = [f"{tool}" for tool in tools]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

# Final polish
ax.set_xlabel('Number of Bins')
ax.set_title('HQ and MQ Bins per Tool\nMarine Short Pooled (GSA vs MA)')
ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle='-', alpha=0.5)
ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig(f"{file_name}_stacked_chart.png", dpi=300)
plt.show()

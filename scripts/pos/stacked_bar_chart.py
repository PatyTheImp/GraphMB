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
hq = df['#HQ Bins']
mq = df['#MQ Bins'] - df['#HQ Bins']

# Set bar positions
y = np.arange(len(tools)) 
bar_height = 0.8

# Plot
fig, ax = plt.subplots(figsize=(10, 8))

# You can define any colors you like here
color_mq = '#61a5c2'  # light blue 
color_hq = '#014f86'  # blue

# Stacked bars for GSA
ax.barh(y, mq, height=bar_height, left=hq, label='#MQ Bins', color=color_mq)
ax.barh(y, hq, height=bar_height, label='#HQ Bins', color=color_hq)

# Stacked bars for MA
# ax.barh(y + 1, mq_ma, height=bar_height, left=hq_ma, label='#MQ (MA)', color=color_mq_ma)
# ax.barh(y + 1, hq_ma, height=bar_height, label='#HQ (MA)', color=color_hq_ma)

# Y-axis labels
yticks = y
yticklabels = [f"{tool}" for tool in tools]
ax.set_yticks(yticks)
ax.set_yticklabels(yticklabels)

# Final polish
ax.set_xlabel('Number of Bins')
ax.set_title('HQ and MQ Bins per Tool\nMarine Short Pooled')
ax.set_axisbelow(True)
ax.xaxis.grid(True, linestyle='-', alpha=0.5)
ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig(f"{file_name}_stacked_chart.png", dpi=300)
plt.show()

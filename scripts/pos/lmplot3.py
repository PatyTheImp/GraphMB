import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def ordinal(n):
    # Special case for 11th, 12th, 13th
    if 10 <= (n % 100) <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# 1) Load + clean column names
df = pd.read_csv('ranking.csv')
# df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)
binner = df["binner"].tolist()

# 5) Plot with lmplot + hue
sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(1, 4, figsize=(32, 6), constrained_layout=True)
label_size = 40
tick_size = 36
title_size = 48


# 7) HQ/min
sns.barplot(
    data=df,
    y="binner",
    x="Marine",
    order=binner,
    palette="muted",
    dodge=False,
    ax=axes[0]
)
axes[0].set_xlabel("")
axes[0].set_ylabel("")
labels = [f"{b}" for b in binner]
axes[0].set_yticklabels(labels, fontsize=label_size)
axes[0].tick_params(axis='x', labelsize=tick_size)
axes[0].set_title("Marine", fontsize=title_size, fontweight='bold')

# 1) Compute rank: smallest value → 1, next → 2, …
df['rank_Marine'] = df['Marine'].rank(method='first', ascending=True).astype(int)

# 2) Annotate each bar
for i, patch in enumerate(axes[0].patches):
    b = binner[i]
    r = df.loc[df['binner']==b, 'rank_Marine'].iloc[0]
    label = ordinal(r)       # e.g. "1st", "2nd", "3rd", "4th", …

    x = patch.get_width()
    y = patch.get_y() + patch.get_height()/2

    axes[0].text(
        x, y, label,
        va='center', ha='left',
        fontsize=label_size * 0.8,
        fontweight='bold'
    )

# 7) HQ/min
sns.barplot(
    data=df,
    y="binner",
    x="Plant",
    order=binner,
    palette="muted",
    dodge=False,
    ax=axes[1]
)
axes[1].set_xlabel("")
axes[1].set_ylabel("")
axes[1].set_yticklabels([])
axes[1].tick_params(axis='x', labelsize=tick_size)
axes[1].set_title("Plant", fontsize=title_size, fontweight='bold')

# 1) Compute rank: smallest value → 1, next → 2, …
df['rank_Plant'] = df['Plant'].rank(method='first', ascending=True).astype(int)

# 2) Annotate each bar
for i, patch in enumerate(axes[1].patches):
    b = binner[i]
    r = df.loc[df['binner']==b, 'rank_Plant'].iloc[0]
    label = ordinal(r)       # e.g. "1st", "2nd", "3rd", "4th", …

    x = patch.get_width()
    y = patch.get_y() + patch.get_height()/2

    axes[1].text(
        x, y, label,
        va='center', ha='left',
        fontsize=label_size * 0.8,
        fontweight='bold'
    )

# 7) HQ/min
sns.barplot(
    data=df,
    y="binner",
    x="Cami-High",
    order=binner,
    palette="muted",
    dodge=False,
    ax=axes[2]
)
axes[2].set_xlabel("")
axes[2].set_ylabel("")
axes[2].set_yticklabels([])
axes[2].tick_params(axis='x', labelsize=tick_size)
axes[2].set_title("Cami-High", fontsize=title_size, fontweight='bold')

# 1) Compute rank as before (smallest nonzero → 1, next → 2, …)
#    We do it on the full series, but you’ll check zeros below.
df['rank_Cami-High'] = df['Cami-High'].replace(0, pd.NA).rank(
    method='first', ascending=True).astype('Int64')  
                            

# 2) Annotate
for i, patch in enumerate(axes[2].patches):
    b = binner[i]
    val = df.loc[df['binner'] == b, 'Cami-High'].iloc[0]
    r   = df.loc[df['binner'] == b, 'rank_Cami-High'].iloc[0]

    if pd.isna(r) or val == 0:
        label = 'n/a'
    else:
        label = ordinal(int(r))

    x = patch.get_width()
    y = patch.get_y() + patch.get_height() / 2

    axes[2].text(
        x + 0.5, y, label,
        va='center', ha='left',
        fontsize=label_size * 0.8,
        fontweight='bold'
    )

# 7) HQ/min
sns.barplot(
    data=df,
    y="binner",
    x="MetaHIT",
    order=binner,
    palette="muted",
    dodge=False,
    ax=axes[3]
)
axes[3].set_xlabel("")
axes[3].set_ylabel("")
axes[3].set_yticklabels([])
axes[3].tick_params(axis='x', labelsize=tick_size)
axes[3].set_title("MetaHIT", fontsize=title_size, fontweight='bold')

# 1) Compute rank as before (smallest nonzero → 1, next → 2, …)
#    We do it on the full series, but you’ll check zeros below.
df['rank_MetaHIT'] = df['MetaHIT'].replace(0, pd.NA).rank(
    method='first', ascending=True).astype('Int64')  
                            

# 2) Annotate
for i, patch in enumerate(axes[3].patches):
    b = binner[i]
    val = df.loc[df['binner'] == b, 'MetaHIT'].iloc[0]
    r   = df.loc[df['binner'] == b, 'rank_MetaHIT'].iloc[0]

    if pd.isna(r) or val == 0:
        label = 'n/a'
    else:
        label = ordinal(int(r))

    x = patch.get_width()
    y = patch.get_y() + patch.get_height() / 2

    axes[3].text(
        x + 0.5, y, label,
        va='center', ha='left',
        fontsize=label_size * 0.8,
        fontweight='bold'
    )

# 9) Save
plt.savefig('ranking.png', dpi=300, bbox_inches='tight')
plt.close(fig)

    

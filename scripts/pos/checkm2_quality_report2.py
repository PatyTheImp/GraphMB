import pandas as pd
import os
import numpy as np

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
        elif row['completeness'] > 90 and row['contamination'] < 10:
            conditions.append('High-quality2')
        elif row['completeness'] > 50 and row['contamination'] < 5:
            conditions.append('Medium-quality2')
        elif row['completeness'] > 50 and row['contamination'] < 10:
            conditions.append('Medium-quality')
        else:
            conditions.append('Low-quality')
    df['quality_class'] = conditions
    return df

def generate_binning_report(input_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    df = load_checkm_report(input_file)
    df = classify_bins(df)

    # Compute purity
    df['purity'] = (1 - df['contamination'] / 100) * 100

    # Count each new class
    hq = (df['quality_class'] == 'High-quality').sum()
    hq2 = (df['quality_class'] == 'High-quality2').sum()
    mq2 = (df['quality_class'] == 'Medium-quality2').sum()
    mq = (df['quality_class'] == 'Medium-quality').sum()
    lq = (df['quality_class'] == 'Low-quality').sum()
    total_bins = len(df)
    hq_pct = round(hq / total_bins * 100, 2)

    # Compute averages and standard errors
    avg_completeness = df['completeness'].mean()
    sem_completeness = df['completeness'].std(ddof=1) / np.sqrt(total_bins)

    avg_purity = df['purity'].mean()
    sem_purity = df['purity'].std(ddof=1) / np.sqrt(total_bins)

    print(f"✅ Total bins: {total_bins}")
    print(f"✅ High-quality bins: {hq}")
    print(f"✅ High-quality2 bins: {hq2}")
    print(f"✅ Medium-quality bins: {mq}")
    print(f"✅ Medium-quality2 bins: {mq2}")
    print(f"✅ Low-quality bins: {lq}")
    print(f"✅ Average Completeness: {avg_completeness:.2f}% ± {sem_completeness:.2f}%")
    print(f"✅ Average Purity: {avg_purity:.2f}% ± {sem_purity:.2f}%")

    # Save annotated table
    df.to_csv(os.path.join(output_folder, "annotated_quality_report.tsv"), sep='\t', index=False)

    # Save summary table
    summary_data = {
        'Metric': [
            'Total_bins',
            'High_quality_bins',
            'High_quality2_bins',
            'High_quality_percentage',
            'Medium_quality2_bins',
            'Medium_quality_bins',
            'Low_quality_bins',
            'Average_completeness',
            'Std_error_completeness',
            'Average_purity',
            'Std_error_purity'
        ],
        'Value': [
            total_bins,
            hq,
            hq2,
            hq_pct,
            mq2,
            mq,
            lq,
            round(avg_completeness, 2),
            round(sem_completeness, 2),
            round(avg_purity, 2),
            round(sem_purity, 2)
        ]
    }

    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(os.path.join(output_folder, "binning_summary.tsv"), sep='\t', index=False)


if __name__ == "__main__":
    input_file = "quality_report.tsv"  # <-- adjust filename if needed
    output_folder = "checkm2_quality_report2"
    generate_binning_report(input_file, output_folder)

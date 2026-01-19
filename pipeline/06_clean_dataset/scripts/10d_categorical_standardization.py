import pandas as pd
from pathlib import Path

# Paths
input_file = Path('../output/10c_min_max_ranges_created.csv')
output_file = Path('../output/10d_categorical_standardized.csv')
report_file = Path('../output/10d_categorical_standardization_report.txt')

# Read data
df = pd.read_csv(input_file, encoding='utf-8', low_memory=False)
print(f"Initial rows: {len(df)}")

stats = {
    'dominant_type': 0,
    'seed_type': 0,
    'flowering_type': 0,
    'difficulty': 0,
    'awards_cleaned': 0
}

# Dominant Type standardization
dominant_type_map = {
    'indica': 'Indica',
    'indica dominant': 'Indica',
    'mostly indica': 'Indica',
    'sativa': 'Sativa',
    'sativa dominant': 'Sativa',
    'mostly sativa': 'Sativa',
    'hybrid': 'Hybrid',
    '50/50': 'Balanced',
    'balanced': 'Balanced',
    'balanced hybrid': 'Balanced'
}

if 'dominant_type_raw' in df.columns:
    df['dominant_type_clean'] = df['dominant_type_raw'].apply(
        lambda x: dominant_type_map.get(str(x).lower().strip(), None) if pd.notna(x) else None
    )
    stats['dominant_type'] = df['dominant_type_clean'].notna().sum()

# Seed Type standardization
seed_type_map = {
    'feminized': 'Feminized',
    'feminised': 'Feminized',
    'fem': 'Feminized',
    'autoflower': 'Autoflower',
    'auto': 'Autoflower',
    'automatic': 'Autoflower',
    'regular': 'Regular',
    'reg': 'Regular'
}

if 'seed_type_raw' in df.columns:
    df['seed_type_clean'] = df['seed_type_raw'].apply(
        lambda x: seed_type_map.get(str(x).lower().strip(), None) if pd.notna(x) else None
    )
    stats['seed_type'] = df['seed_type_clean'].notna().sum()

# Flowering Type standardization
flowering_type_map = {
    'photoperiod': 'Photoperiod',
    'photo': 'Photoperiod',
    'autoflower': 'Autoflower',
    'auto': 'Autoflower',
    'automatic': 'Autoflower'
}

if 'flowering_type_raw' in df.columns:
    df['flowering_type_clean'] = df['flowering_type_raw'].apply(
        lambda x: flowering_type_map.get(str(x).lower().strip(), None) if pd.notna(x) else None
    )
    stats['flowering_type'] = df['flowering_type_clean'].notna().sum()

# Difficulty standardization
difficulty_map = {
    'easy': 'Easy',
    'beginner': 'Easy',
    'moderate': 'Moderate',
    'intermediate': 'Moderate',
    'medium': 'Moderate',
    'difficult': 'Difficult',
    'hard': 'Difficult',
    'advanced': 'Difficult',
    'expert': 'Difficult'
}

if 'difficulty_raw' in df.columns:
    df['difficulty_clean'] = df['difficulty_raw'].apply(
        lambda x: difficulty_map.get(str(x).lower().strip(), None) if pd.notna(x) else None
    )
    stats['difficulty'] = df['difficulty_clean'].notna().sum()

# Awards cleanup (FALSE → NULL)
if 'awards_raw' in df.columns:
    false_count = (df['awards_raw'] == 'FALSE').sum()
    df.loc[df['awards_raw'] == 'FALSE', 'awards_raw'] = None
    stats['awards_cleaned'] = false_count

# Delete strain_name_no_aka (unnecessary)
if 'strain_name_no_aka' in df.columns:
    df = df.drop(columns=['strain_name_no_aka'])

# Save
df.to_csv(output_file, index=False, encoding='utf-8')

# Report
with open(report_file, 'w') as f:
    f.write("=== Step 10D: Categorical Standardization Report ===\n\n")
    f.write(f"Rows processed: {len(df)}\n\n")
    f.write("Standardization results:\n")
    f.write(f"  Dominant type standardized: {stats['dominant_type']}\n")
    f.write(f"  Seed type standardized: {stats['seed_type']}\n")
    f.write(f"  Flowering type standardized: {stats['flowering_type']}\n")
    f.write(f"  Difficulty standardized: {stats['difficulty']}\n")
    f.write(f"  Awards cleaned (FALSE -> NULL): {stats['awards_cleaned']}\n")
    f.write(f"\nColumns deleted: strain_name_no_aka\n")
    f.write(f"\nTotal standardizations: {sum(stats.values())}\n")

print(f"\n[SUCCESS] Step 10D complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")
print(f"Total standardizations: {sum(stats.values())}")

import pandas as pd

df = pd.read_csv('../output/pipeline_15_consolidated.csv', encoding='latin-1')

print('PIPELINE 15 FINAL DATASET\n')
print(f'Total strains: {len(df):,}')
print(f'Total columns: {len(df.columns)}')

print('\n=== BOTANICAL COLUMNS ===')
bot = [c for c in df.columns if any(x in c for x in ['thc', 'cbd', 'flowering', 'height', 'yield'])]
for c in bot:
    cov = df[c].notna().sum()
    pct = (cov/len(df))*100
    print(f'{c:30} {cov:6,} ({pct:5.1f}%)')

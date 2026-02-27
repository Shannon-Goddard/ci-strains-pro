import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load data
df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\input\pipeline_15_final.csv', encoding='latin-1', low_memory=False)

# Generate coverage report
coverage = []
for col in df.columns:
    non_null = df[col].notna().sum()
    pct = (non_null / len(df)) * 100
    dtype = df[col].dtype
    samples = df[col].dropna().head(5).tolist()
    
    coverage.append({
        'column_name': col,
        'non_null_count': non_null,
        'coverage_pct': round(pct, 2),
        'data_type': str(dtype),
        'sample_values': str(samples)
    })

coverage_df = pd.DataFrame(coverage).sort_values('coverage_pct')

# Save report
coverage_df.to_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\column_coverage_report.csv', index=False, encoding='latin-1')

print(f"✅ Coverage audit complete: {len(coverage_df)} columns analyzed")
print(f"\nColumns by coverage tier:")
print(f"  <5%: {len(coverage_df[coverage_df['coverage_pct'] < 5])}")
print(f"  5-20%: {len(coverage_df[(coverage_df['coverage_pct'] >= 5) & (coverage_df['coverage_pct'] < 20)])}")
print(f"  20-50%: {len(coverage_df[(coverage_df['coverage_pct'] >= 20) & (coverage_df['coverage_pct'] < 50)])}")
print(f"  50%+: {len(coverage_df[coverage_df['coverage_pct'] >= 50])}")
print(f"\nLowest coverage columns (<5%):")
print(coverage_df[coverage_df['coverage_pct'] < 5][['column_name', 'coverage_pct']])

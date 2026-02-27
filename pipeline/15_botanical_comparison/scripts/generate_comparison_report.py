import pandas as pd

df = pd.read_csv('../input/pipeline_14_final.csv', encoding='latin-1')

pairs = [
    ('thc_content_raw', 'thc_avg', 'thc_avg'),
    ('thc_min_raw', 'thc_min', 'thc_min'),
    ('thc_max_raw', 'thc_max', 'thc_max'),
    ('cbd_content_raw', 'cbd_avg', 'cbd_avg'),
    ('cbd_min_raw', 'cbd_min', 'cbd_min'),
    ('cbd_max_raw', 'cbd_max', 'cbd_max'),
    ('flowering_time_days_clean', 'flowering_days_avg', 'flowering_days_avg'),
    ('height_indoor_cm_clean', 'height_indoor_cm_min', 'height_indoor_cm_min'),
    ('height_outdoor_cm_clean', 'height_outdoor_cm_min', 'height_outdoor_cm_min'),
    ('yield_indoor_g_m2_clean', 'yield_indoor_g_m2_min', 'yield_indoor_g_m2_min'),
    ('yield_outdoor_g_plant_clean', 'yield_outdoor_g_plant_min', 'yield_outdoor_g_plant_min'),
]

report = []
total = len(df)

for old_col, new_col, final_col in pairs:
    if old_col not in df.columns or new_col not in df.columns:
        continue
    
    old_count = df[old_col].notna().sum()
    new_count = df[new_col].notna().sum()
    both_count = (df[old_col].notna() & df[new_col].notna()).sum()
    final_count = df[old_col].fillna(df[new_col]).notna().sum()
    
    old_pct = (old_count / total) * 100
    new_pct = (new_count / total) * 100
    final_pct = (final_count / total) * 100
    improvement = final_pct - max(old_pct, new_pct)
    
    report.append({
        'column': final_col,
        'old_coverage': f"{old_count:,} ({old_pct:.1f}%)",
        'new_coverage': f"{new_count:,} ({new_pct:.1f}%)",
        'overlap': f"{both_count:,}",
        'final_coverage': f"{final_count:,} ({final_pct:.1f}%)",
        'improvement': f"+{improvement:.1f}%" if improvement > 0 else f"{improvement:.1f}%"
    })

df_report = pd.DataFrame(report)

with open('../output/comparison_report.txt', 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("PIPELINE 15: BOTANICAL CONSOLIDATION REPORT\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"Total strains: {total:,}\n\n")
    f.write(df_report.to_string(index=False))
    f.write("\n\n" + "=" * 80 + "\n")

print(df_report.to_string(index=False))
print("\nReport saved to comparison_report.txt")

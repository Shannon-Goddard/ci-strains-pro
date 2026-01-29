import pandas as pd
from pathlib import Path

# Paths
input_file = Path('../input/master_strains_raw.csv')
output_file = Path('../output/01_deduped_urls.csv')
report_file = Path('../output/01_url_dedup_report.txt')

# Read raw data
df = pd.read_csv(input_file, encoding='latin-1', low_memory=False)

print(f"Initial rows: {len(df)}")

# Remove Seedsman HTML extraction (useless data, keep seedsman_js only)
seedsman_html = df[df['seed_bank'] == 'seedsman']
print(f"Seedsman HTML (bad extraction): {len(seedsman_html)}")
df = df[df['seed_bank'] != 'seedsman']
print(f"After removing Seedsman HTML: {len(df)}")

# Identify duplicates
duplicates = df[df.duplicated(subset=['source_url_raw'], keep='first')]
print(f"Duplicate URLs found: {len(duplicates)}")

# Remove duplicates (keep first occurrence)
df_clean = df.drop_duplicates(subset=['source_url_raw'], keep='first')

print(f"Final rows: {len(df_clean)}")
print(f"Removed: {len(df) - len(df_clean)} rows")

# Save cleaned data
df_clean.to_csv(output_file, index=False, encoding='utf-8')

# Generate report
with open(report_file, 'w') as f:
    f.write("=== Step 01: URL Deduplication Report ===\n\n")
    f.write(f"Initial rows: {23000}\n")
    f.write(f"Seedsman HTML removed: {len(seedsman_html)} (bad extraction, kept seedsman_js)\n")
    f.write(f"After Seedsman cleanup: {len(df)}\n")
    f.write(f"Duplicate URLs: {len(duplicates)}\n")
    f.write(f"Final rows: {len(df_clean)}\n")
    f.write(f"Total removed: {23000 - len(df_clean)} rows\n\n")
    f.write("Duplicate URLs:\n")
    for url in duplicates['source_url_raw'].unique():
        count = len(df[df['source_url_raw'] == url])
        f.write(f"  {url} ({count} occurrences)\n")

print(f"\n[SUCCESS] Step 01 complete")
print(f"Output: {output_file}")
print(f"Report: {report_file}")

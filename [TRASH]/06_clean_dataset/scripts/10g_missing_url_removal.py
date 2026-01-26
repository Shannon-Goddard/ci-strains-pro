"""
Step 10G: Missing URL Removal
Removes row with missing source_url_raw (unrecoverable).
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd

df = pd.read_csv('../../cleaning_csv/10f_non_cannabis_removed.csv', encoding='latin-1', low_memory=False)
print(f"Input: {len(df)} rows")

initial = len(df)
df = df[df['source_url_raw'].notna()]
removed = initial - len(df)
print(f"Removed missing URLs: {removed} rows")

df.to_csv('../../cleaning_csv/10g_missing_url_removed.csv', index=False, encoding='utf-8')
df.head(100).to_csv('output/10g_missing_url_removed_sample.csv', index=False, encoding='utf-8')
print(f"Output: {len(df)} rows -> ../../cleaning_csv/10g_missing_url_removed.csv")

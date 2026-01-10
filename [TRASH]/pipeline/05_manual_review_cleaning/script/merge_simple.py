#!/usr/bin/env python3
"""
Simple merge script without Unicode characters
"""

import pandas as pd

# Load datasets
main_df = pd.read_csv('../../../manual_review_cleaning.csv', encoding='latin-1')
batch_df = pd.read_csv('../failed_scrapes_validated_187.csv', encoding='utf-8-sig')

print(f"Main dataset: {len(main_df)} records")
print(f"Validated batch: {len(batch_df)} records")

# Create unique strain_ids for batch
max_strain_id = main_df['strain_id'].max()
batch_df['strain_id'] = range(max_strain_id + 1, max_strain_id + len(batch_df) + 1)

# Align columns
main_cols = set(main_df.columns)
batch_cols = set(batch_df.columns)

for col in main_cols - batch_cols:
    batch_df[col] = None

batch_df = batch_df[main_df.columns]

# Merge
merged_df = pd.concat([main_df, batch_df], ignore_index=True)

print(f"Merged dataset: {len(merged_df)} records")

# Check duplicates
duplicates = merged_df['strain_id'].duplicated().sum()
print(f"Duplicates: {duplicates}")

# Save
merged_df.to_csv('../../../Cannabis_Database_Validated_Complete.csv', index=False, encoding='utf-8')
print("Saved: Cannabis_Database_Validated_Complete.csv")
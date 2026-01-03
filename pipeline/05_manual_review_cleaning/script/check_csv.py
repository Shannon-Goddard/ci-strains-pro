#!/usr/bin/env python3
"""
Quick CSV column checker
"""
import pandas as pd

# Check the CSV structure
df = pd.read_csv('failed_scrapes_fixed_187.csv', encoding='latin-1')
print("CSV Shape:", df.shape)
print("\nColumn Names:")
for i, col in enumerate(df.columns):
    print(f"{i}: '{col}'")

print(f"\nFirst few rows:")
print(df.head(2))
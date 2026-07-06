import pandas as pd

INPUT = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\18_full_validation\input\pipeline_16_cleaned.csv"
OUTPUT = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation\input\pipeline_16_no_avg.csv"

df = pd.read_csv(INPUT, encoding='latin-1', low_memory=False)
print(f"Original: {df.shape[0]} rows x {df.shape[1]} columns")

df = df.drop(columns=['thc_avg', 'cbd_avg', 'flowering_days_avg'])
print(f"Removed: thc_avg, cbd_avg, flowering_days_avg")

df.to_csv(OUTPUT, index=False, encoding='latin-1')
print(f"Saved: {OUTPUT}")
print(f"New shape: {df.shape[0]} rows x {df.shape[1]} columns")

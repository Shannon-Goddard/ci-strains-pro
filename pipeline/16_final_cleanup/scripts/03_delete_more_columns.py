import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', encoding='latin-1', low_memory=False)

print(f"Starting: {len(df.columns)} columns")

df = df.drop(columns=['is_autoflower_clean', 'version', 'aka_strain_names'], errors='ignore')

print(f"✅ Deleted 3 columns")
print(f"Final: {len(df.columns)} columns")

df.to_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', index=False, encoding='latin-1')
print("✅ Saved")

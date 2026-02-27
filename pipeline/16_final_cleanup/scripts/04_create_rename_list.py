import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\pipeline_16_cleaned.csv', encoding='latin-1', low_memory=False, nrows=0)

rename_df = pd.DataFrame({
    'current_name': df.columns,
    'new_name': ''
})

rename_df.to_csv(r'c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\16_final_cleanup\output\columns_to_rename.csv', index=False, encoding='latin-1')
print(f"✅ Created columns_to_rename.csv with {len(df.columns)} columns")

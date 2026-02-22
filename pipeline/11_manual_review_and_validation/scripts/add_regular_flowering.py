import pandas as pd

df = pd.read_csv('output/strain_name_from_source_url.csv', encoding='latin-1', dtype={'is_fast_flowering': str})

df['is_regular_flowering'] = df['strain_name_from_source_url'].str.contains(
    r'\b(regular|reg)\b', 
    case=False, 
    na=False, 
    regex=True
)

df['is_regular_flowering'] = df['is_regular_flowering'].apply(lambda x: 'TRUE' if x else 'FALSE')

df.to_csv('output/strain_name_from_source_url.csv', index=False, encoding='latin-1')

print(f"Added is_regular_flowering column")
print(f"TRUE count: {(df['is_regular_flowering'] == 'TRUE').sum()}")
print(f"FALSE count: {(df['is_regular_flowering'] == 'FALSE').sum()}")

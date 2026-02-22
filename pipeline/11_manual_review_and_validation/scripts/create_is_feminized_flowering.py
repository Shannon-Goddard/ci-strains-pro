import pandas as pd

df = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')

# Check both URL path and strain name for feminized indicators
df['is_feminized_flowering'] = (
    df['source_url_raw'].str.contains(r'/feminized', case=False, na=False, regex=True) |
    df['strain_name_from_source_url'].str.contains(r'\b(feminized|feminised|fem)\b', case=False, na=False, regex=True)
).apply(lambda x: 'TRUE' if x else 'FALSE')

df[['strain_id', 'strain_name_from_source_url', 'is_feminized_flowering']].to_csv(
    'output/is_feminized_flowering.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Created is_feminized_flowering.csv")
print(f"TRUE count: {(df['is_feminized_flowering'] == 'TRUE').sum()}")
print(f"FALSE count: {(df['is_feminized_flowering'] == 'FALSE').sum()}")

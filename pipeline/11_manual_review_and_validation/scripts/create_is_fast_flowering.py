import pandas as pd

df = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')

df['is_fast_flowering'] = df['strain_name_from_source_url'].str.contains(
    r'\b(fast|ff|quick|rapid|speed)\b', 
    case=False, 
    na=False, 
    regex=True
).apply(lambda x: 'TRUE' if x else 'FALSE')

df[['strain_id', 'strain_name_from_source_url', 'is_fast_flowering']].to_csv(
    'output/is_fast_flowering.csv', 
    index=False, 
    encoding='latin-1'
)

print(f"Created is_fast_flowering.csv")
print(f"TRUE count: {(df['is_fast_flowering'] == 'TRUE').sum()}")
print(f"FALSE count: {(df['is_fast_flowering'] == 'FALSE').sum()}")

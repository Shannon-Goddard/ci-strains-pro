import pandas as pd

df = pd.read_csv('../../cleaning_csv/11b_breeder_merged.csv', encoding='latin-1', low_memory=False)
missing = df[df['breeder_name_clean'].isna()]

print(f'Missing breeders: {len(missing)} ({len(missing)/len(df)*100:.1f}%)')
print(f'\nBy seed bank:')
print(missing['seed_bank'].value_counts())

print(f'\nSample URLs by seed bank:')
for sb in missing['seed_bank'].unique():
    print(f'\n{sb}:')
    urls = missing[missing['seed_bank']==sb]['source_url_raw'].head(2).tolist()
    for url in urls:
        print(f'  {url}')

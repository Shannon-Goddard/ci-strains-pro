import pandas as pd

test_urls = [
    'https://amsterdammarijuanaseeds.com/420-carat-feminized/',
    'https://www.barneysfarm.com/us/black-cherry-gushers-weed-strain-700',
    'https://www.cropkingseeds.com/feminized-seeds/10gs-feminized-seeds/',
    'https://www.cannabis-seeds-bank.co.uk/doctor-s-choice-seeds-doctor-s-choice-1-auto/prod_8130',
    'https://www.royalqueenseeds.com/us/feminized-cannabis-seeds/494-cookies-gelato.html',
    'https://www.northatlanticseed.com/product/22/'
]

df = pd.read_csv('output/strain_name_from_source_url_v2.csv', encoding='latin-1')

for url in test_urls:
    result = df[df['source_url_raw'] == url]
    if len(result) > 0:
        print(f'{url}')
        print(f'  -> {result["strain_name_from_source_url"].values[0]}\n')
    else:
        print(f'{url}')
        print(f'  -> NOT FOUND\n')

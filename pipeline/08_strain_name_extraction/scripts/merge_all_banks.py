import pandas as pd
import os

def main():
    output_dir = '../output'
    
    # List all extraction files
    files = [
        'attitude_strain_names_v2.csv',
        'cropking_extracted.csv',
        'gorilla_extracted.csv',
        'north_atlantic_extracted.csv',
        'neptune_extracted.csv',
        'seedsman_extracted.csv',
        'amsterdam_extracted.csv',
        'herbies_extracted.csv',
        'sensi_seeds_extracted.csv',
        'multiverse_beans_extracted.csv',
        'seed_supreme_extracted.csv',
        'mephisto_genetics_extracted.csv',
        'exotic_extracted.csv',
        'ilgm_extracted.csv',
        'dutch_passion_extracted.csv',
        'barneys_farm_extracted.csv',
        'royal_queen_seeds_extracted.csv',
        'seeds_here_now_extracted.csv',
        'great_lakes_genetics_extracted.csv'
    ]
    
    dfs = []
    total_strains = 0
    
    print("Merging seed bank extractions...\n")
    
    for file in files:
        filepath = os.path.join(output_dir, file)
        if os.path.exists(filepath):
            df = pd.read_csv(filepath, encoding='latin-1')
            count = len(df)
            total_strains += count
            dfs.append(df)
            print(f"+ {file}: {count} strains")
        else:
            print(f"- {file}: NOT FOUND")
    
    # Merge all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Save merged file
    output_file = os.path.join(output_dir, 'all_strains_extracted.csv')
    merged_df.to_csv(output_file, index=False, encoding='latin-1')
    
    print(f"\n{'='*60}")
    print(f"TOTAL STRAINS: {total_strains}")
    print(f"Merged file saved: {output_file}")
    print(f"{'='*60}")
    
    # Show sample
    print("\nSample from merged file:")
    print(merged_df[['seed_bank', 'strain_name_extracted']].head(10).to_string(index=False))

if __name__ == '__main__':
    main()

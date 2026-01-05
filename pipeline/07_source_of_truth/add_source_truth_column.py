#!/usr/bin/env python3
"""
Add source_of_truth column to validated dataset before cleaning
"""
import pandas as pd
from pathlib import Path

def add_source_of_truth_column():
    """Add source_of_truth column based on failed URLs list"""
    
    # Load the validated dataset (put your CSV filename here)
    print("Looking for validated dataset...")
    
    # Common names for the validated dataset
    possible_files = [
        'Cannabis_Database_Validated_Complete.csv',
        'Cannabis_Database_Validated.csv', 
        'validated_dataset.csv'
    ]
    
    dataset_file = None
    for filename in possible_files:
        if Path(f'../../{filename}').exists():
            dataset_file = f'../../{filename}'
            break
    
    if not dataset_file:
        print("Please specify your validated dataset filename:")
        filename = input("Enter filename: ").strip()
        dataset_file = f'../../{filename}'
    
    print(f"Loading dataset: {dataset_file}")
    df = pd.read_csv(dataset_file, encoding='latin-1')
    print(f"Loaded {len(df)} strain records")
    
    # Load the failed URLs list
    failed_urls_file = 'urls_no_source_of_truth_summary.csv'
    if not Path(failed_urls_file).exists():
        print(f"Failed URLs file not found: {failed_urls_file}")
        return
    
    failed_df = pd.read_csv(failed_urls_file)
    failed_urls = set(failed_df['source_url'])
    print(f"Loaded {len(failed_urls)} failed URLs")
    
    # Add source_of_truth column
    # True = URL was successfully scraped (has HTML source)
    # False = URL failed scraping (no HTML source)
    df['source_of_truth'] = ~df['source_url'].isin(failed_urls)
    
    # Summary stats
    with_source = df['source_of_truth'].sum()
    without_source = (~df['source_of_truth']).sum()
    
    print(f"\n=== SOURCE OF TRUTH RESULTS ===")
    print(f"Strains WITH source of truth: {with_source:,} ({with_source/len(df)*100:.1f}%)")
    print(f"Strains WITHOUT source of truth: {without_source:,} ({without_source/len(df)*100:.1f}%)")
    
    # Save the updated dataset
    output_file = dataset_file.replace('.csv', '_with_source_truth.csv')
    df.to_csv(output_file, index=False, encoding='latin-1')
    print(f"\nSaved: {output_file}")
    
    # Create methodology file
    methodology = f"""# Source of Truth Flagging Methodology

## Process
1. Loaded validated dataset: {dataset_file} ({len(df):,} records)
2. Cross-referenced against failed HTML collection URLs ({len(failed_urls):,} URLs)
3. Added `source_of_truth` column:
   - `True`: HTML successfully collected and verified ({with_source:,} strains)
   - `False`: No HTML source available ({without_source:,} strains)

## Business Logic
- Strains with `source_of_truth = True` can be sold with confidence
- Strains with `source_of_truth = False` require "unverified" flag
- Provides legal protection and customer transparency

## Results
- Coverage rate: {with_source/len(df)*100:.1f}%
- Ready for lineage cleaning with source verification in place

*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
    
    with open('methodology.md', 'w') as f:
        f.write(methodology)
    
    print("✅ Source of truth column added successfully!")
    print(f"✅ Ready for lineage cleaning on: {output_file}")

if __name__ == "__main__":
    add_source_of_truth_column()
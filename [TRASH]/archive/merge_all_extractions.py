"""
Merge All Extraction Outputs
Combine 19 seed bank extractions into single master file

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
from pathlib import Path

output_files = [
    "attitude_strain_names_v2.csv",
    "cropking_extracted.csv",
    "north_atlantic_strain_names.csv",
    "gorilla_extracted.csv",
    "neptune_extracted.csv",
    "seedsman_extracted.csv",
    "multiverse_extracted.csv",
    "herbies_extracted.csv",
    "sensi_extracted.csv",
    "seedsupreme_extracted.csv",
    "mephisto_extracted.csv",
    "exotic_extracted.csv",
    "amsterdam_extracted.csv",
    "ilgm_extracted.csv",
    "dutchpassion_extracted.csv",
    "barneys_extracted.csv",
    "royalqueen_extracted.csv",
    "seedsherenow_extracted.csv",
    "greatlakes_extracted.csv",
]

if __name__ == "__main__":
    print("Merging all extraction outputs...")
    
    all_dfs = []
    total_strains = 0
    
    for filename in output_files:
        filepath = Path("../output") / filename
        if filepath.exists():
            df = pd.read_csv(filepath, encoding='utf-8')
            all_dfs.append(df)
            total_strains += len(df)
            print(f"OK {filename}: {len(df):,} strains")
        else:
            print(f"Missing: {filename}")
    
    if all_dfs:
        merged = pd.concat(all_dfs, ignore_index=True)
        merged.to_csv("../output/all_strains_extracted.csv", index=False, encoding='utf-8')
        
        print(f"\n{'='*60}")
        print(f"MERGE COMPLETE: {total_strains:,} total strains")
        print(f"Output: all_strains_extracted.csv")
        print(f"{'='*60}")
        
        print(f"\nBreakdown by seed bank:")
        print(merged['seed_bank'].value_counts().to_string())
    else:
        print("\nNo extraction files found!")

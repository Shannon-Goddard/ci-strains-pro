"""
Generate Data Sample and Statistics for Gemini Flash 2.0 Validation
Extracts first 100 rows + comprehensive statistics from master_strains_raw.csv
"""

import pandas as pd
import json
from pathlib import Path

# Paths
INPUT_CSV = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/master_strains_raw.csv")
OUTPUT_SAMPLE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/gemini_sample_100.csv")
OUTPUT_STATS = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/gemini_stats.json")

def generate_sample_and_stats():
    """Extract sample data and generate comprehensive statistics"""
    
    print("Reading master dataset...")
    df = pd.read_csv(INPUT_CSV, encoding='latin-1', low_memory=False)
    
    # Extract first 100 rows
    print("Extracting first 100 rows...")
    sample_df = df.head(100)
    sample_df.to_csv(OUTPUT_SAMPLE, index=False, encoding='utf-8')
    print(f"[OK] Sample saved: {OUTPUT_SAMPLE}")
    
    # Generate comprehensive statistics
    print("\nGenerating statistics...")
    
    stats = {
        "dataset_overview": {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "file_size_mb": round(INPUT_CSV.stat().st_size / (1024 * 1024), 2)
        },
        "seed_bank_distribution": df['seed_bank'].value_counts().to_dict(),
        "field_coverage": {},
        "data_types": {},
        "value_ranges": {},
        "null_patterns": {},
        "sample_values": {}
    }
    
    # Analyze each column
    for col in df.columns:
        if col in ['strain_id', 'seed_bank']:
            continue
            
        # Coverage
        non_null = df[col].notna().sum()
        fill_rate = round((non_null / len(df)) * 100, 2)
        stats["field_coverage"][col] = {
            "non_null_count": int(non_null),
            "fill_rate_percent": fill_rate
        }
        
        # Data type
        stats["data_types"][col] = str(df[col].dtype)
        
        # Null patterns by seed bank
        null_by_bank = df[df[col].isna()].groupby('seed_bank').size().to_dict()
        if null_by_bank:
            stats["null_patterns"][col] = null_by_bank
        
        # Sample values (first 5 non-null unique values)
        sample_vals = df[col].dropna().unique()[:5].tolist()
        stats["sample_values"][col] = [str(v) for v in sample_vals]
        
        # Value ranges for numeric-looking fields
        if 'percentage' in col or 'thc' in col or 'cbd' in col or 'cbn' in col:
            try:
                numeric_vals = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(numeric_vals) > 0:
                    stats["value_ranges"][col] = {
                        "min": float(numeric_vals.min()),
                        "max": float(numeric_vals.max()),
                        "mean": round(float(numeric_vals.mean()), 2),
                        "median": float(numeric_vals.median())
                    }
            except:
                pass
    
    # Top/Bottom 5 fields by coverage
    coverage_sorted = sorted(stats["field_coverage"].items(), 
                            key=lambda x: x[1]["fill_rate_percent"], 
                            reverse=True)
    stats["top_5_coverage"] = {k: v for k, v in coverage_sorted[:5]}
    stats["bottom_5_coverage"] = {k: v for k, v in coverage_sorted[-5:]}
    
    # Save statistics
    with open(OUTPUT_STATS, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"[OK] Statistics saved: {OUTPUT_STATS}")
    
    # Print summary
    print("\n" + "="*60)
    print("DATASET SUMMARY FOR GEMINI VALIDATION")
    print("="*60)
    print(f"\nTotal Records: {stats['dataset_overview']['total_records']:,}")
    print(f"Total Columns: {stats['dataset_overview']['total_columns']}")
    print(f"File Size: {stats['dataset_overview']['file_size_mb']} MB")
    
    print("\n--- Seed Bank Distribution ---")
    for bank, count in sorted(stats['seed_bank_distribution'].items(), 
                              key=lambda x: x[1], reverse=True)[:10]:
        print(f"{bank:20s}: {count:,} strains")
    
    print("\n--- Top 5 Fields by Coverage ---")
    for field, data in stats["top_5_coverage"].items():
        print(f"{field:30s}: {data['fill_rate_percent']:6.2f}%")
    
    print("\n--- Bottom 5 Fields by Coverage ---")
    for field, data in stats["bottom_5_coverage"].items():
        print(f"{field:30s}: {data['fill_rate_percent']:6.2f}%")
    
    print("\n" + "="*60)
    print("FILES READY FOR GEMINI VALIDATION:")
    print("="*60)
    print(f"1. Prompt: gemini_validation_prompt.md")
    print(f"2. Sample: {OUTPUT_SAMPLE.name}")
    print(f"3. Stats:  {OUTPUT_STATS.name}")
    print("\nNext: Send these files to Gemini Flash 2.0 for validation")

if __name__ == "__main__":
    generate_sample_and_stats()

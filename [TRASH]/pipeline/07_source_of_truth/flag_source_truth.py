#!/usr/bin/env python3
"""
Flag strains with source of truth based on HTML collection results
"""
import pandas as pd
import sqlite3
from pathlib import Path

def flag_source_of_truth():
    """Add source_of_truth column to main dataset"""
    
    # Load main dataset
    main_csv = Path('../Cannabis_Database_Validated_Complete.csv')
    if not main_csv.exists():
        print("Main dataset not found!")
        return
    
    df = pd.read_csv(main_csv, encoding='latin-1')
    print(f"Loaded {len(df)} strain records")
    
    # Connect to scraping results
    db_path = Path('06_html_collection/data/scraping_progress.db')
    if not db_path.exists():
        print("Scraping database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    
    # Get successful collections (both 'completed' and 'success' status)
    successful_df = pd.read_sql('''
        SELECT original_url 
        FROM scraping_progress 
        WHERE status IN ("completed", "success")
    ''', conn)
    
    successful_urls = set(successful_df['original_url'])
    print(f"Found {len(successful_urls)} successfully collected URLs")
    
    # Add source_of_truth column
    df['source_of_truth'] = df['source_url'].isin(successful_urls)
    
    # Summary stats
    with_source = df['source_of_truth'].sum()
    without_source = (~df['source_of_truth']).sum()
    
    print(f"\n=== SOURCE OF TRUTH RESULTS ===")
    print(f"Strains WITH source of truth: {with_source:,}")
    print(f"Strains WITHOUT source of truth: {without_source:,}")
    print(f"Coverage rate: {with_source/len(df)*100:.1f}%")
    
    # Save updated dataset
    output_path = Path('../Cannabis_Database_With_Source_Truth.csv')
    df.to_csv(output_path, index=False, encoding='latin-1')
    print(f"\nSaved: {output_path}")
    
    # Create summary report
    report = f"""# Source of Truth Flagging Report
Generated: {pd.Timestamp.now()}

## Results
- Total strains: {len(df):,}
- With source of truth: {with_source:,} ({with_source/len(df)*100:.1f}%)
- Without source of truth: {without_source:,} ({without_source/len(df)*100:.1f}%)

## Business Impact
- Verified strains ready for sale: {with_source:,}
- Strains requiring "unverified" flag: {without_source:,}
- Data integrity protection: COMPLETE

*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
    
    with open('../source_of_truth_report.md', 'w') as f:
        f.write(report)
    
    conn.close()
    print("✅ Source of truth flagging complete!")

if __name__ == "__main__":
    flag_source_of_truth()
#!/usr/bin/env python3
"""
Extract URLs without source of truth for manual review
"""
import pandas as pd
from pathlib import Path

def extract_no_source_urls():
    """Extract URLs that don't have HTML source of truth"""
    
    # Load the flagged dataset
    df = pd.read_csv('../Cannabis_Database_With_Source_Truth.csv', encoding='latin-1')
    
    # Filter for strains without source of truth
    no_source = df[df['source_of_truth'] == False].copy()
    
    print(f"Found {len(no_source)} strains without source of truth")
    
    # Get unique URLs and their strain counts
    url_summary = no_source.groupby('source_url').agg({
        'strain_name': 'count',
        'strain_id': lambda x: list(x)
    }).rename(columns={'strain_name': 'strain_count'})
    
    url_summary = url_summary.reset_index()
    url_summary = url_summary.sort_values('strain_count', ascending=False)
    
    print(f"Unique URLs without source: {len(url_summary)}")
    
    # Save detailed list
    no_source[['source_url', 'strain_name', 'strain_id', 'breeder_name', 'bank_name']].to_csv(
        '../urls_no_source_of_truth_detailed.csv', index=False
    )
    
    # Save URL summary
    url_summary.to_csv('../urls_no_source_of_truth_summary.csv', index=False)
    
    # Top domains without source
    print("\nTop domains without source of truth:")
    domains = no_source['source_url'].str.extract(r'https?://([^/]+)')[0]
    domain_counts = domains.value_counts().head(10)
    for domain, count in domain_counts.items():
        print(f"  {domain}: {count} strains")
    
    print(f"\nFiles saved:")
    print(f"- urls_no_source_of_truth_detailed.csv ({len(no_source)} records)")
    print(f"- urls_no_source_of_truth_summary.csv ({len(url_summary)} unique URLs)")

if __name__ == "__main__":
    extract_no_source_urls()
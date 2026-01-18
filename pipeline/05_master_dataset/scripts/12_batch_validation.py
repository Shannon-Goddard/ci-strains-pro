"""
Batch Validation - All 23,000 Rows
Processes in 50 batches of 460 rows each
"""

import pandas as pd
import json
import boto3
import google.generativeai as genai
from pathlib import Path
import time
from datetime import datetime

# Paths
INPUT_CSV = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/master_strains_raw.csv")
OUTPUT_DIR = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/batch_validation")
OUTPUT_DIR.mkdir(exist_ok=True)

BATCH_SIZE = 460
BATCH_RESULTS = OUTPUT_DIR / "batch_results.json"
FINAL_REPORT = OUTPUT_DIR / "gemini_full_validation_report.md"

def get_gemini_api_key():
    """Retrieve Gemini API key from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='cannabis-gemini-api')
    secret_dict = json.loads(response['SecretString'])
    return secret_dict['cannabis-gemini-api']

def process_batch(model, batch_df, batch_num, total_batches):
    """Process a single batch"""
    
    csv_string = batch_df.to_csv(index=False)
    
    prompt = f"""Analyze this batch ({batch_num}/{total_batches}) of {len(batch_df)} cannabis strains.

## Tasks:
1. Count anomalies:
   - THC > 40%
   - indica% + sativa% != 100% (tolerance ±5%)
   - Negative/impossible values
   - Placeholder text ("N/A", "Unknown", "TBD")

2. Find duplicates:
   - Exact name matches (case-insensitive)
   - List all duplicate strain names found

3. Seed bank quality (for banks in this batch):
   - Average fill rate per seed bank
   - Count strains with >50% fields populated

4. Field quality:
   - For each field, count non-null values
   - Identify top 3 data quality issues

Return results as JSON:
{{
  "batch_num": {batch_num},
  "strains_analyzed": {len(batch_df)},
  "anomalies": {{"thc_over_40": 0, "percentage_mismatch": 0, "impossible_values": 0, "placeholders": 0}},
  "duplicates": ["strain1", "strain2"],
  "seed_bank_quality": {{"bank_name": {{"fill_rate": 0.0, "strains_over_50": 0}}}},
  "field_coverage": {{"field_name": 0}},
  "issues": ["issue1", "issue2", "issue3"]
}}

Data:
```csv
{csv_string}
```"""
    
    response = model.generate_content(prompt)
    return response.text

def aggregate_results(batch_results):
    """Aggregate all batch results into final report"""
    
    total_anomalies = {
        "thc_over_40": 0,
        "percentage_mismatch": 0,
        "impossible_values": 0,
        "placeholders": 0
    }
    
    all_duplicates = set()
    seed_bank_totals = {}
    field_totals = {}
    all_issues = []
    
    for result in batch_results:
        # Parse JSON from response
        try:
            data = json.loads(result.strip('```json\n').strip('```'))
            
            # Aggregate anomalies
            for key in total_anomalies:
                total_anomalies[key] += data.get("anomalies", {}).get(key, 0)
            
            # Collect duplicates
            all_duplicates.update(data.get("duplicates", []))
            
            # Aggregate seed bank quality
            for bank, stats in data.get("seed_bank_quality", {}).items():
                if bank not in seed_bank_totals:
                    seed_bank_totals[bank] = {"fill_rate_sum": 0, "count": 0, "strains_over_50": 0}
                seed_bank_totals[bank]["fill_rate_sum"] += stats.get("fill_rate", 0)
                seed_bank_totals[bank]["count"] += 1
                seed_bank_totals[bank]["strains_over_50"] += stats.get("strains_over_50", 0)
            
            # Aggregate field coverage
            for field, count in data.get("field_coverage", {}).items():
                field_totals[field] = field_totals.get(field, 0) + count
            
            # Collect issues
            all_issues.extend(data.get("issues", []))
            
        except Exception as e:
            print(f"Warning: Could not parse batch result: {e}")
            continue
    
    # Calculate averages
    for bank in seed_bank_totals:
        if seed_bank_totals[bank]["count"] > 0:
            seed_bank_totals[bank]["avg_fill_rate"] = seed_bank_totals[bank]["fill_rate_sum"] / seed_bank_totals[bank]["count"]
    
    return {
        "total_anomalies": total_anomalies,
        "duplicates": sorted(list(all_duplicates)),
        "seed_bank_quality": seed_bank_totals,
        "field_coverage": field_totals,
        "top_issues": list(set(all_issues))[:20]
    }

def batch_validate():
    """Main batch validation process"""
    
    print("="*60)
    print("FULL DATASET BATCH VALIDATION")
    print("="*60)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    print("\nLoading dataset...")
    df = pd.read_csv(INPUT_CSV, encoding='latin-1', low_memory=False)
    print(f"Loaded: {len(df):,} strains")
    
    # Calculate batches
    total_batches = (len(df) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Batch size: {BATCH_SIZE} rows")
    print(f"Total batches: {total_batches}")
    print(f"Estimated time: {total_batches * 2} minutes")
    print(f"Estimated cost: ${total_batches * 0.05:.2f}")
    
    # Get API key
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Process batches
    batch_results = []
    
    print("\n" + "="*60)
    print("PROCESSING BATCHES")
    print("="*60)
    
    for i in range(total_batches):
        start_idx = i * BATCH_SIZE
        end_idx = min((i + 1) * BATCH_SIZE, len(df))
        batch_df = df.iloc[start_idx:end_idx]
        
        print(f"\nBatch {i+1}/{total_batches}: Rows {start_idx:,}-{end_idx:,} ({len(batch_df)} strains)")
        
        try:
            result = process_batch(model, batch_df, i+1, total_batches)
            batch_results.append(result)
            print(f"  [OK] Batch {i+1} complete")
            
            # Save progress
            with open(BATCH_RESULTS, 'w', encoding='utf-8') as f:
                json.dump(batch_results, f, indent=2)
            
            # Rate limit handling (wait 60 seconds every 10 batches)
            if (i + 1) % 10 == 0 and i + 1 < total_batches:
                print(f"  [WAIT] Rate limit cooldown (60 seconds)...")
                time.sleep(60)
            else:
                time.sleep(2)  # Small delay between batches
                
        except Exception as e:
            print(f"  [ERROR] Batch {i+1} failed: {e}")
            batch_results.append(f'{{"error": "Batch {i+1} failed: {str(e)}"}}')
            time.sleep(5)
    
    # Aggregate results
    print("\n" + "="*60)
    print("AGGREGATING RESULTS")
    print("="*60)
    
    aggregated = aggregate_results(batch_results)
    
    # Generate final report
    report = f"""# Full Dataset Validation Report - All 23,000 Strains
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Batches Processed**: {total_batches}
**Total Strains**: {len(df):,}

## Anomaly Detection (Exact Counts)

- **THC > 40%**: {aggregated['total_anomalies']['thc_over_40']:,} strains
- **Percentage Mismatch** (indica + sativa != 100%): {aggregated['total_anomalies']['percentage_mismatch']:,} strains
- **Impossible Values**: {aggregated['total_anomalies']['impossible_values']:,} strains
- **Placeholder Text**: {aggregated['total_anomalies']['placeholders']:,} strains

## Duplicate Detection

**Total Duplicates Found**: {len(aggregated['duplicates']):,} unique strain names

Top 20 Duplicates:
{chr(10).join(f"- {dup}" for dup in aggregated['duplicates'][:20])}

## Seed Bank Quality Rankings

| Seed Bank | Avg Fill Rate | Strains >50% Fields |
|-----------|---------------|---------------------|
{chr(10).join(f"| {bank} | {stats['avg_fill_rate']:.1%} | {stats['strains_over_50']:,} |" for bank, stats in sorted(aggregated['seed_bank_quality'].items(), key=lambda x: x[1]['avg_fill_rate'], reverse=True))}

## Field Coverage (Top 20)

{chr(10).join(f"- **{field}**: {count:,} strains ({count/len(df)*100:.1f}%)" for field, count in sorted(aggregated['field_coverage'].items(), key=lambda x: x[1], reverse=True)[:20])}

## Top Data Quality Issues

{chr(10).join(f"{i+1}. {issue}" for i, issue in enumerate(aggregated['top_issues']))}

---
**Processing Complete**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save final report
    with open(FINAL_REPORT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n[OK] Final report saved: {FINAL_REPORT}")
    print("\n" + "="*60)
    print("VALIDATION COMPLETE!")
    print("="*60)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    batch_validate()

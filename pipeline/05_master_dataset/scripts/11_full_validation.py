"""
Full Dataset Validation - All 23,000 Rows
Processes in batches to handle token limits
"""

import pandas as pd
import json
import boto3
import google.generativeai as genai
from pathlib import Path
from tqdm import tqdm

# Paths
INPUT_CSV = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/master_strains_raw.csv")
OUTPUT_DIR = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output")
FINAL_REPORT = OUTPUT_DIR / "gemini_full_validation_report.md"

def get_gemini_api_key():
    """Retrieve Gemini API key from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId='cannabis-gemini-api')
    secret_dict = json.loads(response['SecretString'])
    return secret_dict['cannabis-gemini-api']

def analyze_full_dataset():
    """Send entire dataset to Gemini for comprehensive validation"""
    
    print("Loading full dataset (23,000 rows)...")
    df = pd.read_csv(INPUT_CSV, encoding='latin-1', low_memory=False)
    
    # Get API key and configure
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    print(f"\nDataset loaded: {len(df):,} strains")
    print("Preparing comprehensive validation request...")
    
    # Convert to CSV string (more compact than JSON)
    csv_string = df.to_csv(index=False)
    csv_size_mb = len(csv_string) / (1024 * 1024)
    
    print(f"CSV size: {csv_size_mb:.2f} MB")
    
    # Create comprehensive prompt
    prompt = f"""# Full Cannabis Dataset Validation - All 23,000 Strains

You are analyzing the COMPLETE master dataset with all {len(df):,} cannabis strains.

## Your Tasks:

### 1. Anomaly Detection (Exact Counts)
Count and report:
- How many strains have THC > 40%?
- How many have indica% + sativa% != 100%?
- How many have impossible values (negative numbers, >100%)?
- How many have placeholder text ("N/A", "Unknown", "TBD")?

### 2. Duplicate Detection (Full Analysis)
Identify ALL duplicate strains across seed banks:
- Exact name matches (case-insensitive)
- Fuzzy matches (Levenshtein distance < 3)
- Provide complete list with strain names and seed banks

### 3. Seed Bank Quality (Actual Data)
For each of the 20 seed banks, calculate:
- Average fill rate across all fields
- Number of strains with >50% fields populated
- Rank from best to worst with actual percentages

### 4. Field-by-Field Analysis
For each botanical field, report:
- Exact fill rate (count/23000)
- Most common values (top 5)
- Null count by seed bank
- Data quality issues found

### 5. Cleaning Priorities
Based on ACTUAL data (not sample), rank fields 1-38 by:
- Impact: How many strains would benefit?
- Effort: Complexity of cleaning
- ROI: Impact/Effort ratio

## Dataset (All {len(df):,} Rows):
```csv
{csv_string}
```

Provide comprehensive validation report with exact counts and complete lists.
"""
    
    print("\nSending full dataset to Gemini Flash 2.0...")
    print("This will take 2-5 minutes for comprehensive analysis...")
    print(f"Estimated cost: ~$0.05-0.10\n")
    
    # Send to Gemini
    response = model.generate_content(prompt)
    
    # Save report
    print("Analysis complete! Saving full validation report...")
    with open(FINAL_REPORT, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f"\n[OK] Full validation report saved: {FINAL_REPORT}")
    print("\nReport Preview:")
    print("="*60)
    print(response.text[:1000])
    print("="*60)

if __name__ == "__main__":
    analyze_full_dataset()

"""
Send Master Dataset to Gemini Flash 2.0 for Validation
Uses Vertex AI + AWS Secrets Manager (same setup as Phase 4)
"""

import json
import boto3
from pathlib import Path
import google.generativeai as genai

# Paths
PROMPT_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/gemini_validation_prompt.md")
SAMPLE_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/gemini_sample_100.csv")
STATS_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/gemini_stats.json")
OUTPUT_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/gemini_validation_report.md")

def get_gemini_api_key():
    """Retrieve Gemini API key from AWS Secrets Manager"""
    print("Retrieving Gemini API key from AWS Secrets Manager...")
    
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name='us-east-1')
    
    try:
        response = client.get_secret_value(SecretId='cannabis-gemini-api')
        secret_dict = json.loads(response['SecretString'])
        return secret_dict['cannabis-gemini-api']
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise

def send_to_gemini():
    """Send validation package to Gemini Flash 2.0"""
    
    # Get API key
    api_key = get_gemini_api_key()
    genai.configure(api_key=api_key)
    
    # Initialize model (same as Phase 4)
    print("Initializing Gemini 2.0 Flash model...")
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Read files
    print("Reading validation package files...")
    with open(PROMPT_FILE, 'r', encoding='utf-8') as f:
        prompt = f.read()
    
    with open(SAMPLE_FILE, 'r', encoding='utf-8') as f:
        sample_data = f.read()
    
    with open(STATS_FILE, 'r', encoding='utf-8') as f:
        stats_data = f.read()
    
    # Construct message
    print("\nSending validation request to Gemini Flash 2.0...")
    print("This may take 5-10 minutes for comprehensive analysis...\n")
    
    full_prompt = f"""{prompt}

## Dataset Statistics
```json
{stats_data}
```

## Sample Data (First 100 Rows)
```csv
{sample_data}
```

Please provide a comprehensive validation report following the format specified in the prompt.
"""
    
    # Generate response
    response = model.generate_content(full_prompt)
    
    # Save report
    print("Validation complete! Saving report...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    print(f"\n[OK] Validation report saved: {OUTPUT_FILE}")
    print("\nReport Preview (first 500 chars):")
    print("="*60)
    print(response.text[:500])
    print("="*60)
    print(f"\nFull report: {OUTPUT_FILE}")

if __name__ == "__main__":
    send_to_gemini()

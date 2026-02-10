"""
Breeder Extraction from S3 HTML Archives

Focuses ONLY on extracting breeder names from HTML for "Unknown" breeders.
Uses Gemini 1.5 Pro to read S3 archives and identify breeders.

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import boto3
import json
import time
import re
from bs4 import BeautifulSoup
from vertexai.generative_models import GenerativeModel
import vertexai

# Configuration
PROJECT_ID = "gen-lang-client-0100184589"  # Same as Phase 9
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.0-flash-exp"  # Same as Phase 9
S3_BUCKET = "ci-strains-html-archive"
BATCH_SIZE = 50
CONFIDENCE_THRESHOLD = 0.85

# Paths
INPUT_CSV = "output/pipeline_11_manual_review.csv"
OUTPUT_CSV = "output/pipeline_11_breeder_extracted.csv"

# Initialize
s3_client = boto3.client('s3')
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel(MODEL_NAME)

def get_html_from_s3(s3_key):
    """Fetch HTML from S3 and extract text only"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        html_content = response['Body'].read().decode('latin-1')
        
        # Strip HTML to text only (reduces tokens by ~70%)
        soup = BeautifulSoup(html_content, 'html.parser')
        text_only = ' '.join(soup.stripped_strings)
        return text_only[:50000]  # Still limit for safety
    except Exception as e:
        print(f"Error fetching {s3_key}: {e}")
        return None

def extract_json(text):
    """Robust JSON extraction using regex"""
    try:
        # Find JSON object in text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(text)
    except:
        return None

def extract_breeder_with_gemini(html_content, seed_bank, retry_count=0):
    """Extract breeder name from HTML using Gemini with retry logic"""
    
    prompt = f"""You are a cannabis breeder extraction specialist. Read this text and identify the BREEDER (not the seed bank).

CRITICAL RULES:
1. The BREEDER is who created the genetics (e.g., "Barney's Farm", "Royal Queen Seeds", "00 Seeds")
2. The SEED BANK is who sells the seeds (e.g., "The Attitude Seedbank", "Neptune Seed Bank")
3. Seed Bank for this strain: {seed_bank}
4. If the text mentions a specific breeder name, extract it
5. Look in: product title, breeder field, manufacturer, brand, genetics info
6. If you cannot find a breeder, return "Unknown"

Respond ONLY with valid JSON:
{{
  "breeder": "breeder name or Unknown",
  "confidence": 0.0-1.0,
  "reasoning": "where you found it"
}}

Text Content:
{html_content}
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Robust JSON extraction
        result = extract_json(result_text)
        if result:
            return result
        else:
            return {"breeder": "Unknown", "confidence": 0.0, "reasoning": "Failed to parse JSON"}
            
    except Exception as e:
        # Retry logic for rate limits (429, 503)
        if retry_count < 3 and ('429' in str(e) or '503' in str(e)):
            print(f"Rate limit hit, retrying in 10 seconds... (attempt {retry_count + 1}/3)")
            time.sleep(10)
            return extract_breeder_with_gemini(html_content, seed_bank, retry_count + 1)
        
        print(f"Error: {e}")
        return {"breeder": "Unknown", "confidence": 0.0, "reasoning": f"Error: {str(e)}"}

def process_batch(df_batch, start_idx):
    """Process batch of Unknown breeders"""
    results = []
    
    for idx, row in df_batch.iterrows():
        print(f"Processing {idx - start_idx + 1}/{len(df_batch)} (Overall: {idx + 1})")
        
        if pd.isna(row['s3_html_key_raw']):
            results.append({
                'strain_id': row['strain_id'],
                'breeder_extracted': 'Unknown',
                'breeder_confidence': 0.0,
                'breeder_reasoning': 'No S3 HTML key'
            })
            continue
        
        # Fetch HTML
        html_content = get_html_from_s3(row['s3_html_key_raw'])
        if not html_content:
            results.append({
                'strain_id': row['strain_id'],
                'breeder_extracted': 'Unknown',
                'breeder_confidence': 0.0,
                'breeder_reasoning': 'Failed to fetch HTML'
            })
            continue
        
        # Extract breeder with retry logic
        extraction = extract_breeder_with_gemini(html_content, row['seed_bank_display_manual'])
        
        results.append({
            'strain_id': row['strain_id'],
            'breeder_extracted': extraction.get('breeder', 'Unknown'),
            'breeder_confidence': extraction.get('confidence', 0.0),
            'breeder_reasoning': extraction.get('reasoning', '')
        })
        
        # Rate limiting (increased to avoid 429 errors)
        time.sleep(3)  # Increased from 1 to 3 seconds
    
    return results

def main():
    print("=" * 80)
    print("Breeder Extraction from S3 HTML Archives")
    print("=" * 80)
    
    # Load CSV
    print(f"\nLoading: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV, encoding='latin-1')
    print(f"Total strains: {len(df):,}")
    
    # Filter Unknown breeders
    df_unknown = df[df['breeder_display_manual'] == 'Unknown'].copy()
    print(f"Unknown breeders: {len(df_unknown):,}")
    
    if len(df_unknown) == 0:
        print("\nNo Unknown breeders found!")
        return
    
    # Process in batches
    all_results = []
    total_batches = (len(df_unknown) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(df_unknown))
        
        print(f"\n{'=' * 80}")
        print(f"Batch {batch_num + 1}/{total_batches} (Rows {start_idx + 1}-{end_idx})")
        print(f"{'=' * 80}")
        
        df_batch = df_unknown.iloc[start_idx:end_idx]
        batch_results = process_batch(df_batch, start_idx)
        all_results.extend(batch_results)
        
        # Save progress
        results_df = pd.DataFrame(all_results)
        merged_df = df.merge(results_df, on='strain_id', how='left')
        merged_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
        print(f"\nProgress saved to {OUTPUT_CSV}")
    
    # Final stats
    print(f"\n{'=' * 80}")
    print("Extraction Complete!")
    print(f"{'=' * 80}")
    
    results_df = pd.DataFrame(all_results)
    
    extracted = (results_df['breeder_extracted'] != 'Unknown').sum()
    avg_confidence = results_df[results_df['breeder_extracted'] != 'Unknown']['breeder_confidence'].mean()
    low_confidence = (results_df['breeder_confidence'] < CONFIDENCE_THRESHOLD).sum()
    
    print(f"\nTotal processed: {len(results_df):,}")
    print(f"Breeders extracted: {extracted:,} ({extracted/len(results_df):.1%})")
    print(f"Still Unknown: {len(results_df) - extracted:,}")
    print(f"Average confidence: {avg_confidence:.2%}")
    print(f"Low confidence (<{CONFIDENCE_THRESHOLD}): {low_confidence:,}")
    
    # Show top extracted breeders
    print(f"\nTop 10 Extracted Breeders:")
    print("-" * 80)
    breeder_counts = results_df[results_df['breeder_extracted'] != 'Unknown']['breeder_extracted'].value_counts()
    for breeder, count in breeder_counts.head(10).items():
        print(f"{breeder:40} {count:>6,} strains")
    
    print("\n" + "=" * 80)
    print("Next Steps:")
    print("1. Review output/pipeline_11_breeder_extracted.csv")
    print("2. Check breeder_extracted column for new breeder names")
    print("3. Review low confidence items")
    print("4. Copy accepted breeders to breeder_display_manual")
    print("=" * 80)

if __name__ == "__main__":
    main()

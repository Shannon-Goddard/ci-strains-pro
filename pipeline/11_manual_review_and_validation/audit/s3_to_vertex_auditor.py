"""
S3-to-Vertex Auditor for Phase 11 Manual Corrections

This script audits Shannon's manual corrections by comparing them against
the original S3 HTML archives using Gemini 1.5 Pro.

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import boto3
import json
import time
from pathlib import Path
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part
import vertexai

# Configuration
PROJECT_ID = "ci-strains-pro"
LOCATION = "us-central1"
MODEL_NAME = "gemini-1.5-pro"
S3_BUCKET = "ci-strains-html-archive"
BATCH_SIZE = 50  # Process in batches to manage rate limits
CONFIDENCE_THRESHOLD = 0.90  # Flag items below this score

# Paths
INPUT_CSV = "pipeline/11_manual_review_and_validation/output/pipeline_11_manual_review.csv"
OUTPUT_CSV = "pipeline/11_manual_review_and_validation/audit/audit_results.csv"
FLAGGED_CSV = "pipeline/11_manual_review_and_validation/audit/audit_flagged.csv"

# Initialize clients
s3_client = boto3.client('s3')
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel(MODEL_NAME)

def get_html_from_s3(s3_key):
    """Fetch HTML content from S3 bucket"""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        html_content = response['Body'].read().decode('latin-1')
        return html_content
    except Exception as e:
        print(f"Error fetching {s3_key}: {e}")
        return None

def audit_row_with_gemini(row, html_content):
    """Send HTML and manual corrections to Gemini for audit"""
    
    prompt = f"""You are a botanical data auditor. Review the provided HTML and verify if the following CSV data is correct:

Seed Bank: {row['seed_bank_display_manual']}
Breeder: {row['breeder_display_manual']}
Strain Name: {row['strain_name_display_manual']}

CRITICAL RULES:
1. If the HTML mentions a specific breeder (e.g., "Barney's Farm", "Royal Queen Seeds", "00 Seeds"), but the CSV says "Unbranded" or "Bulk" or the seed bank name, you MUST flag this as an error and provide the correct breeder name.
2. Seed banks sell seeds from multiple breeders. The breeder is who created the genetics, not who sells them.
3. Strain names should not include suffixes like "Feminized", "Auto" (unless at the start), pack sizes, or codes.
4. Check if the seed bank name matches what's in the HTML.

Respond ONLY with valid JSON in this exact format:
{{
  "seed_bank_correct": true/false,
  "breeder_correct": true/false,
  "strain_name_correct": true/false,
  "confidence": 0.0-1.0,
  "suggested_corrections": {{
    "seed_bank": "corrected value or null",
    "breeder": "corrected value or null",
    "strain_name": "corrected value or null"
  }},
  "reasoning": "Brief explanation of findings"
}}

HTML Content:
{html_content[:50000]}
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        
        result = json.loads(result_text.strip())
        return result
    except Exception as e:
        print(f"Error auditing row {row['strain_id']}: {e}")
        return {
            "seed_bank_correct": None,
            "breeder_correct": None,
            "strain_name_correct": None,
            "confidence": 0.0,
            "suggested_corrections": {},
            "reasoning": f"Error: {str(e)}"
        }

def process_batch(df_batch, start_idx):
    """Process a batch of rows"""
    results = []
    
    for idx, row in df_batch.iterrows():
        print(f"Processing {idx + 1}/{len(df_batch)} (Overall: {start_idx + idx + 1})")
        
        # Skip if no S3 key
        if pd.isna(row['s3_html_key_raw']):
            results.append({
                'strain_id': row['strain_id'],
                'audit_seed_bank_correct': None,
                'audit_breeder_correct': None,
                'audit_strain_name_correct': None,
                'audit_confidence': 0.0,
                'audit_suggested_corrections': json.dumps({}),
                'audit_reasoning': 'No S3 HTML key available',
                'audit_flagged': True
            })
            continue
        
        # Fetch HTML from S3
        html_content = get_html_from_s3(row['s3_html_key_raw'])
        if not html_content:
            results.append({
                'strain_id': row['strain_id'],
                'audit_seed_bank_correct': None,
                'audit_breeder_correct': None,
                'audit_strain_name_correct': None,
                'audit_confidence': 0.0,
                'audit_suggested_corrections': json.dumps({}),
                'audit_reasoning': 'Failed to fetch HTML from S3',
                'audit_flagged': True
            })
            continue
        
        # Audit with Gemini
        audit_result = audit_row_with_gemini(row, html_content)
        
        # Format result
        results.append({
            'strain_id': row['strain_id'],
            'audit_seed_bank_correct': audit_result.get('seed_bank_correct'),
            'audit_breeder_correct': audit_result.get('breeder_correct'),
            'audit_strain_name_correct': audit_result.get('strain_name_correct'),
            'audit_confidence': audit_result.get('confidence', 0.0),
            'audit_suggested_corrections': json.dumps(audit_result.get('suggested_corrections', {})),
            'audit_reasoning': audit_result.get('reasoning', ''),
            'audit_flagged': audit_result.get('confidence', 0.0) < CONFIDENCE_THRESHOLD
        })
        
        # Rate limiting
        time.sleep(1)
    
    return results

def main():
    print("=" * 80)
    print("Phase 11: S3-to-Vertex Auditor")
    print("=" * 80)
    
    # Load CSV
    print(f"\nLoading CSV: {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV, encoding='latin-1')
    print(f"Total strains: {len(df)}")
    
    # Filter rows with manual corrections
    df_to_audit = df[
        df['seed_bank_display_manual'].notna() |
        df['breeder_display_manual'].notna() |
        df['strain_name_display_manual'].notna()
    ].copy()
    print(f"Strains with manual corrections: {len(df_to_audit)}")
    
    if len(df_to_audit) == 0:
        print("\nNo manual corrections found. Exiting.")
        return
    
    # Process in batches
    all_results = []
    total_batches = (len(df_to_audit) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(df_to_audit))
        
        print(f"\n{'=' * 80}")
        print(f"Batch {batch_num + 1}/{total_batches} (Rows {start_idx + 1}-{end_idx})")
        print(f"{'=' * 80}")
        
        df_batch = df_to_audit.iloc[start_idx:end_idx]
        batch_results = process_batch(df_batch, start_idx)
        all_results.extend(batch_results)
        
        # Save progress after each batch
        results_df = pd.DataFrame(all_results)
        merged_df = df.merge(results_df, on='strain_id', how='left')
        merged_df.to_csv(OUTPUT_CSV, index=False, encoding='latin-1')
        print(f"\nProgress saved to {OUTPUT_CSV}")
    
    # Final results
    print(f"\n{'=' * 80}")
    print("Audit Complete!")
    print(f"{'=' * 80}")
    
    results_df = pd.DataFrame(all_results)
    
    # Statistics
    total_audited = len(results_df)
    flagged_count = results_df['audit_flagged'].sum()
    avg_confidence = results_df['audit_confidence'].mean()
    
    print(f"\nTotal audited: {total_audited}")
    print(f"Average confidence: {avg_confidence:.2%}")
    print(f"Flagged for review: {flagged_count} ({flagged_count/total_audited:.1%})")
    
    # Merge with original data
    merged_df = df.merge(results_df, on='strain_id', how='left')
    merged_df.to_csv(OUTPUT_CSV, index=False, encoding='latin-1')
    print(f"\nFull results saved to: {OUTPUT_CSV}")
    
    # Save flagged items
    flagged_df = merged_df[merged_df['audit_flagged'] == True]
    flagged_df.to_csv(FLAGGED_CSV, index=False, encoding='latin-1')
    print(f"Flagged items saved to: {FLAGGED_CSV}")
    
    print("\n" + "=" * 80)
    print("Next Steps:")
    print("1. Review flagged items in audit/audit_flagged.csv")
    print("2. Compare Gemini suggestions with manual corrections")
    print("3. Make final decisions on discrepancies")
    print("4. Merge finalized data to final/all_strains_phase11_final.csv")
    print("=" * 80)

if __name__ == "__main__":
    main()

"""
Vertex AI Validation Script - Strain Names & Breeders
Validates and corrects extracted strain names and breeder names using Gemini 2.0 Flash
"""

import pandas as pd
import json
import time
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
from pathlib import Path
from datetime import datetime

class VertexValidator:
    """Validate strain names and breeders using Vertex AI"""
    
    def __init__(self):
        # Initialize Vertex AI (uses default credentials from environment)
        self.project_id = "gen-lang-client-0100184589"
        self.region = 'us-central1'
        aiplatform.init(project=self.project_id, location=self.region)
        
        # Initialize Gemini model
        self.model = GenerativeModel('gemini-2.0-flash-exp')
        
        # Stats tracking
        self.total_processed = 0
        self.total_corrections = 0
        self.total_cost = 0.0
        self.flagged_count = 0
        
    def create_validation_prompt(self, batch_data):
        """Create prompt for batch validation"""
        prompt = """You are a cannabis strain name validator. Review each strain's extracted name and breeder.

RULES:
1. Strain names should NOT contain breeder names, seed types (feminized/auto), or pack sizes
2. Preserve strain numbers (e.g., "Project 4516", "Haze 13")
3. Remove "Auto" suffix unless it's at the start (preserve "Auto 1", "Auto Moonrocks")
4. Breeder names should be clean company names (e.g., "Barney's Farm", "Mephisto Genetics")
5. If breeder is unknown/unclear, return "Unknown"

For each strain, provide:
- corrected_strain_name (or "CORRECT" if no changes needed)
- corrected_breeder (or "CORRECT" if no changes needed)
- confidence (0-100)
- reasoning (brief explanation)

INPUT DATA:
"""
        for idx, row in batch_data.iterrows():
            prompt += f"\n{idx}. URL: {row['source_url_raw']}\n"
            prompt += f"   Seed Bank: {row['seed_bank']}\n"
            prompt += f"   Extracted Strain: {row['strain_name_extracted']}\n"
            prompt += f"   Extracted Breeder: {row.get('breeder_extracted', 'N/A')}\n"
        
        prompt += """\n\nRESPOND IN JSON FORMAT:
{
  "validations": [
    {
      "index": 0,
      "corrected_strain_name": "CORRECT" or "New Name",
      "corrected_breeder": "CORRECT" or "Breeder Name",
      "confidence": 95,
      "reasoning": "Brief explanation"
    }
  ]
}"""
        return prompt
    
    def validate_batch(self, batch_data, retry_count=0, max_retries=5):
        """Validate a batch of strains with exponential backoff"""
        try:
            prompt = self.create_validation_prompt(batch_data)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith('```'):
                response_text = response_text[3:-3].strip()
            
            result = json.loads(response_text)
            
            # Estimate cost (Gemini Flash: ~$0.00001 per 1K tokens)
            # Rough estimate: 200 tokens per strain
            estimated_tokens = len(batch_data) * 200
            batch_cost = (estimated_tokens / 1000) * 0.00001
            self.total_cost += batch_cost
            
            return result['validations']
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle rate limiting with exponential backoff
            if '429' in error_msg or 'Resource exhausted' in error_msg:
                if retry_count < max_retries:
                    wait_time = (2 ** retry_count) * 5  # 5, 10, 20, 40, 80 seconds
                    print(f"  Rate limit hit. Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}...")
                    time.sleep(wait_time)
                    return self.validate_batch(batch_data, retry_count + 1, max_retries)
                else:
                    print(f"  Max retries reached. Skipping batch.")
                    return None
            
            print(f"Error validating batch: {e}")
            return None
    
    def process_dataset(self, input_csv, output_csv, batch_size=50, confidence_threshold=90):
        """Process entire dataset in batches"""
        print(f"Loading dataset from {input_csv}...")
        df = pd.read_csv(input_csv, encoding='latin-1')
        
        # Check for checkpoint file
        checkpoint_file = output_csv.replace('.csv', '_checkpoint.csv')
        if Path(checkpoint_file).exists():
            print(f"\n[CHECKPOINT FOUND] Resuming from {checkpoint_file}...")
            df = pd.read_csv(checkpoint_file, encoding='utf-8')
            # Count already processed
            already_processed = df['validation_attempted'].sum() if 'validation_attempted' in df.columns else 0
            print(f"Already processed: {already_processed} strains")
        else:
            # Add validation columns
            df['strain_name_validated'] = df['strain_name_extracted']
            df['breeder_validated'] = df.get('breeder_extracted', 'Unknown')
            df['validation_confidence'] = 0
            df['validation_reasoning'] = ''
            df['validation_changes'] = ''
            df['flagged_for_review'] = False
            df['validation_attempted'] = False
        
        print(f"Total strains to validate: {len(df)}")
        print(f"Batch size: {batch_size}")
        print(f"Confidence threshold: {confidence_threshold}%")
        print("-" * 60)
        
        # Process in batches
        total_batches = (len(df) + batch_size - 1) // batch_size
        failed_batches = []
        
        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(df))
            batch_data = df.iloc[start_idx:end_idx]
            
            print(f"\nProcessing batch {batch_num + 1}/{total_batches} (rows {start_idx}-{end_idx})...")
            
            validations = self.validate_batch(batch_data)
            
            if validations:
                for validation in validations:
                    idx = start_idx + validation['index']
                    
                    # Apply corrections
                    changes = []
                    if validation['corrected_strain_name'] != 'CORRECT':
                        df.at[idx, 'strain_name_validated'] = validation['corrected_strain_name']
                        changes.append(f"Strain: {df.at[idx, 'strain_name_extracted']} -> {validation['corrected_strain_name']}")
                        self.total_corrections += 1
                    
                    if validation['corrected_breeder'] != 'CORRECT':
                        df.at[idx, 'breeder_validated'] = validation['corrected_breeder']
                        changes.append(f"Breeder: {df.at[idx, 'breeder_validated']} -> {validation['corrected_breeder']}")
                        self.total_corrections += 1
                    
                    df.at[idx, 'validation_confidence'] = validation['confidence']
                    df.at[idx, 'validation_reasoning'] = validation['reasoning']
                    df.at[idx, 'validation_changes'] = '; '.join(changes) if changes else 'No changes'
                    df.at[idx, 'validation_attempted'] = True
                    
                    # Flag low confidence items
                    if validation['confidence'] < confidence_threshold:
                        df.at[idx, 'flagged_for_review'] = True
                        self.flagged_count += 1
                
                self.total_processed += len(batch_data)
                print(f"  Processed: {self.total_processed}/{len(df)}")
                print(f"  Corrections: {self.total_corrections}")
                print(f"  Flagged: {self.flagged_count}")
                print(f"  Estimated cost: ${self.total_cost:.4f}")
            else:
                # Track failed batch
                failed_batches.append((batch_num, start_idx, end_idx))
                print(f"  Batch failed - will retry later")
            
            # Rate limiting (avoid API throttling)
            time.sleep(3)  # Increased from 1 to 3 seconds
            
            # Save checkpoint every 10 batches
            if (batch_num + 1) % 10 == 0:
                df.to_csv(checkpoint_file, index=False, encoding='utf-8')
                print(f"  [Checkpoint saved]")
        
        # Retry failed batches
        if failed_batches:
            print(f"\n{'='*60}")
            print(f"RETRYING {len(failed_batches)} FAILED BATCHES")
            print(f"{'='*60}")
            
            for batch_num, start_idx, end_idx in failed_batches:
                batch_data = df.iloc[start_idx:end_idx]
                print(f"\nRetrying batch {batch_num + 1}/{total_batches} (rows {start_idx}-{end_idx})...")
                
                validations = self.validate_batch(batch_data)
                
                if validations:
                    for validation in validations:
                        idx = start_idx + validation['index']
                        
                        changes = []
                        if validation['corrected_strain_name'] != 'CORRECT':
                            df.at[idx, 'strain_name_validated'] = validation['corrected_strain_name']
                            changes.append(f"Strain: {df.at[idx, 'strain_name_extracted']} -> {validation['corrected_strain_name']}")
                            self.total_corrections += 1
                        
                        if validation['corrected_breeder'] != 'CORRECT':
                            df.at[idx, 'breeder_validated'] = validation['corrected_breeder']
                            changes.append(f"Breeder: {df.at[idx, 'breeder_validated']} -> {validation['corrected_breeder']}")
                            self.total_corrections += 1
                        
                        df.at[idx, 'validation_confidence'] = validation['confidence']
                        df.at[idx, 'validation_reasoning'] = validation['reasoning']
                        df.at[idx, 'validation_changes'] = '; '.join(changes) if changes else 'No changes'
                        df.at[idx, 'validation_attempted'] = True
                        
                        if validation['confidence'] < confidence_threshold:
                            df.at[idx, 'flagged_for_review'] = True
                            self.flagged_count += 1
                    
                    self.total_processed += len(batch_data)
                    print(f"  SUCCESS - Processed: {self.total_processed}/{len(df)}")
                else:
                    print(f"  Still failed - skipping")
                
                time.sleep(5)  # Longer delay for retries
        
        # Save results
        print(f"\nSaving validated dataset to {output_csv}...")
        df.to_csv(output_csv, index=False, encoding='latin-1')
        
        # Delete checkpoint file on successful completion
        if Path(checkpoint_file).exists():
            Path(checkpoint_file).unlink()
            print(f"[Checkpoint file deleted]")
        
        # Save flagged items
        flagged_df = df[df['flagged_for_review'] == True]
        if len(flagged_df) > 0:
            flagged_csv = output_csv.replace('.csv', '_flagged.csv')
            print(f"Saving {len(flagged_df)} flagged items to {flagged_csv}...")
            flagged_df.to_csv(flagged_csv, index=False, encoding='latin-1')
        
        # Generate report
        self.generate_report(df, output_csv.replace('.csv', '_report.txt'))
        
        print("\n" + "=" * 60)
        print("VALIDATION COMPLETE")
        print("=" * 60)
        print(f"Total strains processed: {self.total_processed}")
        print(f"Total corrections made: {self.total_corrections}")
        print(f"Items flagged for review: {self.flagged_count}")
        print(f"Estimated total cost: ${self.total_cost:.4f}")
        print("=" * 60)
    
    def generate_report(self, df, report_path):
        """Generate validation report"""
        with open(report_path, 'w') as f:
            f.write("VERTEX AI VALIDATION REPORT\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Total Strains: {len(df)}\n")
            f.write(f"Corrections Made: {self.total_corrections}\n")
            f.write(f"Flagged for Review: {self.flagged_count}\n")
            f.write(f"Estimated Cost: ${self.total_cost:.4f}\n\n")
            
            f.write("CONFIDENCE DISTRIBUTION:\n")
            f.write(f"  95-100%: {len(df[df['validation_confidence'] >= 95])}\n")
            f.write(f"  90-94%:  {len(df[(df['validation_confidence'] >= 90) & (df['validation_confidence'] < 95)])}\n")
            f.write(f"  80-89%:  {len(df[(df['validation_confidence'] >= 80) & (df['validation_confidence'] < 90)])}\n")
            f.write(f"  <80%:    {len(df[df['validation_confidence'] < 80])}\n\n")
            
            f.write("CORRECTIONS BY SEED BANK:\n")
            for bank in df['seed_bank'].unique():
                bank_df = df[df['seed_bank'] == bank]
                corrections = len(bank_df[bank_df['validation_changes'] != 'No changes'])
                f.write(f"  {bank}: {corrections}/{len(bank_df)}\n")

if __name__ == '__main__':
    # Configuration
    INPUT_CSV = '../input/all_strains_extracted.csv'
    OUTPUT_CSV = '../output/all_strains_validated.csv'
    BATCH_SIZE = 50
    CONFIDENCE_THRESHOLD = 90
    
    # Run validation
    validator = VertexValidator()
    validator.process_dataset(INPUT_CSV, OUTPUT_CSV, BATCH_SIZE, CONFIDENCE_THRESHOLD)

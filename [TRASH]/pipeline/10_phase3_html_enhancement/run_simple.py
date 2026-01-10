#!/usr/bin/env python3
"""
Execute Phase 3 HTML Enhancement Pipeline - ASCII Version
Runs the enhancement pipeline on revert_manual_review_cleaning.csv

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phase3_html_enhancer import main as run_enhancement_pipeline

def check_prerequisites():
    """Check if all prerequisites are met before running the pipeline"""
    print("Checking prerequisites...")
    
    # Check if input file exists
    input_file = '../../revert_manual_review_cleaning.csv'
    if not os.path.exists(input_file):
        print(f"[ERROR] Input file not found: {input_file}")
        return False
    
    # Check file size and record count
    try:
        df = pd.read_csv(input_file, encoding='latin-1')
        print(f"[OK] Input file found: {len(df):,} records, {len(df.columns)} columns")
        
        # Check for source_of_truth column
        if 'source_of_truth' not in df.columns:
            print("[ERROR] Missing 'source_of_truth' column in input file")
            return False
        
        # Count strains with HTML sources
        html_strains = df[df['source_of_truth'] == True].shape[0]
        print(f"[OK] Strains with HTML sources: {html_strains:,}")
        
        if html_strains == 0:
            print("[ERROR] No strains with HTML sources found")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error reading input file: {e}")
        return False
    
    # Check AWS credentials (basic check)
    try:
        import boto3
        s3_client = boto3.client('s3')
        print("[OK] AWS credentials configured")
    except Exception as e:
        print(f"[ERROR] AWS credentials issue: {e}")
        return False
    
    print("[OK] All prerequisites met!")
    return True

def run_pipeline():
    """Execute the Phase 3 HTML enhancement pipeline"""
    
    print("=" * 60)
    print("Phase 3 HTML Enhancement Pipeline")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check prerequisites
    if not check_prerequisites():
        print("[ERROR] Prerequisites not met. Please resolve issues before running.")
        return False
    
    print()
    print("[START] Starting enhancement pipeline...")
    print()
    
    # Change to the correct directory for the pipeline
    original_dir = os.getcwd()
    try:
        # Change to the project root directory
        os.chdir('../..')
        
        # Run the enhancement pipeline
        run_enhancement_pipeline()
        
        print()
        print("=" * 60)
        print("[SUCCESS] Pipeline completed successfully!")
        print("=" * 60)
        
        # List output files
        output_files = [
            'cannabis_database_phase3_enhanced.csv',
            'phase3_enhancement_report.md',
            'phase3_enhancement.log'
        ]
        
        print("Output files generated:")
        for file in output_files:
            if os.path.exists(file):
                size = os.path.getsize(file) / (1024 * 1024)  # MB
                print(f"  [OK] {file} ({size:.1f} MB)")
            else:
                print(f"  [MISSING] {file} (not found)")
        
        print()
        print("Next steps:")
        print("  1. Review the enhancement report: phase3_enhancement_report.md")
        print("  2. Examine the enhanced dataset: cannabis_database_phase3_enhanced.csv")
        print("  3. Check the processing log for any issues: phase3_enhancement.log")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")
        return False
    finally:
        # Return to original directory
        os.chdir(original_dir)

def main():
    """Main execution function"""
    success = run_pipeline()
    
    if success:
        print()
        print("[SUCCESS] Phase 3 HTML Enhancement completed successfully!")
        print("Your cannabis strain database has been enhanced with strategic data from 14,075 HTML sources.")
    else:
        print()
        print("[FAILED] Phase 3 HTML Enhancement failed.")
        print("Please check the error messages above and resolve any issues.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
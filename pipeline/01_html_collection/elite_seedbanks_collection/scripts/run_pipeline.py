#!/usr/bin/env python3
"""
Pipeline 06: Master Orchestrator - The 20K Breakthrough
Run the complete pipeline from URL generation to 20,000+ strains

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

def run_step(step_num, name, script, estimated_time):
    """Run a pipeline step"""
    print("\n" + "="*70)
    print(f"STEP {step_num}: {name}")
    print(f"Estimated Time: {estimated_time}")
    print("="*70)
    
    start = datetime.now()
    
    try:
        result = subprocess.run(
            [sys.executable, script],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )
        
        duration = datetime.now() - start
        
        if result.returncode == 0:
            print(f"\nPASS Step {step_num} completed in {duration}")
            return True
        else:
            print(f"\nFAIL Step {step_num} failed after {duration}")
            return False
            
    except Exception as e:
        print(f"\nFAIL Step {step_num} error: {e}")
        return False

def main():
    """Run the complete Pipeline 06"""
    
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              PIPELINE 06: THE 20K BREAKTHROUGH                   ║
║                                                                  ║
║  Target: 8 Elite Seedbanks | ~3,083 New Strains                 ║
║  Goal: Break 20,000 Total Strains                               ║
║                                                                  ║
║  Logic designed by Amazon Q, verified by Shannon Goddard         ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
    
    pipeline_start = datetime.now()
    
    steps = [
        (1, "Generate Catalog URLs", "01_generate_catalog_urls.py", "1.5 seconds"),
        (2, "Collect Catalog Pages", "02_collect_catalogs.py", "30-45 minutes"),
        (3, "Collect Product Pages", "03_collect_products.py", "4-6 hours"),
    ]
    
    for step_num, name, script, time_est in steps:
        success = run_step(step_num, name, script, time_est)
        
        if not success:
            print(f"\nWARNING Pipeline stopped at Step {step_num}")
            print("Fix the issue and re-run to continue")
            return False
    
    total_duration = datetime.now() - pipeline_start
    
    print("\n" + "="*70)
    print("PIPELINE 06 COLLECTION COMPLETE!")
    print("="*70)
    print(f"Total Duration: {total_duration}")
    print("\nNext Steps:")
    print("1. Run extraction scripts for each seedbank")
    print("2. Generate final 20K+ database report")
    print("3. Celebrate breaking 20,000 strains!")
    print("="*70)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

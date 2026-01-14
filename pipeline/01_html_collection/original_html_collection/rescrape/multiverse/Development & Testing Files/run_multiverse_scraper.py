#!/usr/bin/env python3
"""
Multiverse Beans Scraper Execution Script
Simple runner for the S3 HTML archive processing

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to Python path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

def main():
    """Execute the Multiverse Beans scraper"""
    
    print("🌿 CANNABIS INTELLIGENCE - MULTIVERSE BEANS PROCESSOR")
    print("="*60)
    print("📊 Reading from S3 HTML Archive: ci-strains-html-archive")
    print("🎯 Target: 1,227 Multiverse Beans strains")
    print("🔧 Method: 4-Method Extraction (Structured + Description + Patterns + Fallback)")
    print("📈 Expected Success Rate: 95%+")
    print("="*60)
    
    try:
        # Import and run the scraper
        from multiverse_s3_4method_scraper import main as run_scraper
        
        print("\n🚀 Starting Multiverse Beans processing...")
        run_scraper()
        
        print("\n✅ Processing completed successfully!")
        print("📁 Check the 'output' directory for CSV results")
        print("☁️  Results uploaded to S3: processed_data/multiverse_beans/")
        
    except ImportError as e:
        print(f"\n❌ Error: Could not import scraper module: {e}")
        print("Make sure multiverse_s3_4method_scraper.py is in the same directory")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error during processing: {e}")
        print("Check the logs for detailed error information")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
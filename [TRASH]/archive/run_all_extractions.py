"""
Master Extraction Script - Run All 19 Seed Banks
Phase 8: Strain Name Extraction

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import subprocess
import sys
from pathlib import Path

scripts = [
    ("extract_attitude.py", "Attitude", 7673),
    ("extract_cropking.py", "Crop King", 3336),
    ("extract_north_atlantic.py", "North Atlantic", 2726),
    ("extract_gorilla.py", "Gorilla", 2000),
    ("extract_neptune.py", "Neptune", 1995),
    ("extract_seedsman.py", "Seedsman JS", 866),
    ("extract_multiverse.py", "Multiverse Beans", 528),
    ("extract_herbies.py", "Herbies", 753),
    ("extract_sensi.py", "Sensi Seeds", 620),
    ("extract_seedsupreme.py", "Seed Supreme", 350),
    ("extract_mephisto.py", "Mephisto Genetics", 245),
    ("extract_exotic.py", "Exotic Genetix", 227),
    ("extract_amsterdam.py", "Amsterdam", 163),
    ("extract_ilgm.py", "ILGM JS", 133),
    ("extract_dutchpassion.py", "Dutch Passion", 119),
    ("extract_barneys.py", "Barney's Farm", 88),
    ("extract_royalqueen.py", "Royal Queen Seeds", 67),
    ("extract_seedsherenow.py", "Seeds Here Now", 39),
    ("extract_greatlakes.py", "Great Lakes", 16),
]

def run_extraction(script_name, seed_bank, expected_count):
    """Run individual extraction script"""
    print(f"\n{'='*60}")
    print(f"Running: {seed_bank} ({expected_count} strains)")
    print(f"{'='*60}")
    
    result = subprocess.run([sys.executable, script_name], 
                          capture_output=True, 
                          text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print(f"ERROR in {seed_bank}:")
        print(result.stderr)
        return False

if __name__ == "__main__":
    print("Phase 8: Strain Name Extraction - Master Run")
    print(f"Total: {sum(s[2] for s in scripts):,} strains across 19 seed banks\n")
    
    success_count = 0
    failed = []
    
    for script_name, seed_bank, expected_count in scripts:
        if run_extraction(script_name, seed_bank, expected_count):
            success_count += 1
        else:
            failed.append(seed_bank)
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {success_count}/{len(scripts)} seed banks extracted")
    print(f"{'='*60}")
    
    if failed:
        print(f"\nFailed: {', '.join(failed)}")
    else:
        print("\nALL EXTRACTIONS COMPLETE!")
        print("\nNext step: Run merge script to combine all outputs")

"""
Crop King - Breeder Extraction
Self-branded: all strains are "Crop King"
Logic designed by Amazon Q, verified by Shannon Goddard.
"""
import pandas as pd

# Load dataset
print("Loading master dataset...")
df = pd.read_csv('input/master_strains_raw.csv', encoding='latin-1', low_memory=False)
crop_king = df[df['seed_bank'] == 'crop_king'].copy()
print(f"Crop King strains: {len(crop_king)}")

# Set all to "Crop King"
crop_king['breeder_extracted'] = 'Crop King'

print(f"\nResults:")
print(f"  Extracted: {len(crop_king)} (100.0%)")

# Save
crop_king.to_csv('output/crop_king_breeders.csv', index=False, encoding='utf-8')
crop_king.head(100).to_csv('output/crop_king_breeders_sample.csv', index=False, encoding='utf-8')
print(f"\nOutput: output/crop_king_breeders.csv")

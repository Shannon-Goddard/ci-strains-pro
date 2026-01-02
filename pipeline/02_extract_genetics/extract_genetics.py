import pandas as pd
import re

def extract_genetics_data(csv_path):
    # Load the CSV with proper encoding
    df = pd.read_csv(csv_path, encoding='latin-1')
    
    # Initialize counters
    generation_count = 0
    phenotype_count = 0
    lineage_count = 0
    
    for idx, row in df.iterrows():
        about_info = str(row.get('about_info_cleaned', ''))
        
        # Extract Generation (F1, F2, F3, etc.)
        if pd.isna(row.get('generation')) or row.get('generation') == '':
            generation_match = re.search(r'\bF\d+\b', about_info, re.IGNORECASE)
            if generation_match:
                df.at[idx, 'generation'] = generation_match.group().upper()
                generation_count += 1
        
        # Extract Phenotype (#33, #2, etc.)
        if pd.isna(row.get('phenotype')) or row.get('phenotype') == '':
            phenotype_match = re.search(r'#\d+', about_info)
            if phenotype_match:
                df.at[idx, 'phenotype'] = phenotype_match.group()
                phenotype_count += 1
        
        # Extract Lineage (StrainA x StrainB format)
        if pd.isna(row.get('lineage')) or row.get('lineage') == '':
            # Look for genetics patterns like "Genetics: StrainA x StrainB"
            lineage_patterns = [
                r'Genetics:\s*([^.\n]+?)(?:\s*Type:|$)',
                r'Lineage:\s*([^.\n]+?)(?:\s*Type:|$)',
                r'Cross:\s*([^.\n]+?)(?:\s*Type:|$)',
                r'Parents:\s*([^.\n]+?)(?:\s*Type:|$)'
            ]
            
            for pattern in lineage_patterns:
                lineage_match = re.search(pattern, about_info, re.IGNORECASE)
                if lineage_match:
                    lineage = lineage_match.group(1).strip()
                    # Clean up common suffixes
                    lineage = re.sub(r'\s*(flowering|flower|type|variety).*$', '', lineage, flags=re.IGNORECASE)
                    if len(lineage) > 5 and 'x' in lineage.lower():  # Basic validation
                        df.at[idx, 'lineage'] = lineage
                        lineage_count += 1
                        break
    
    # Save the updated CSV
    output_path = csv_path.replace('.csv', '_genetics_extracted.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Extraction complete!")
    print(f"Generation extracted: {generation_count}")
    print(f"Phenotype extracted: {phenotype_count}")
    print(f"Lineage extracted: {lineage_count}")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    extract_genetics_data("Cannabis_Database.csv")
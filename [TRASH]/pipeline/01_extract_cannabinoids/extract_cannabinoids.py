import pandas as pd
import re

def extract_cannabinoid_data(csv_path):
    # Load CSV
    df = pd.read_csv(csv_path, encoding='latin-1')
    
    # Initialize counters
    sativa_count = indica_count = thc_count = cbd_count = 0
    
    for idx, row in df.iterrows():
        strain_info = str(row.get('strain_info', ''))
        
        # Extract Sativa percentage
        if pd.isna(row.get('sativa_percentage')) or row.get('sativa_percentage') == '':
            sativa_match = re.search(r'(\d+)%\s*Sativa', strain_info, re.IGNORECASE)
            if sativa_match:
                df.at[idx, 'sativa_percentage'] = int(sativa_match.group(1))
                sativa_count += 1
        
        # Extract Indica percentage
        if pd.isna(row.get('indica_percentage')) or row.get('indica_percentage') == '':
            indica_match = re.search(r'(\d+)%\s*Indica', strain_info, re.IGNORECASE)
            if indica_match:
                df.at[idx, 'indica_percentage'] = int(indica_match.group(1))
                indica_count += 1
        
        # Extract THC values
        thc_patterns = [
            r'THC[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%',  # THC: 20-25%
            r'THC[:\s]*(\d+(?:\.\d+)?)%',  # THC: 20%
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%\s*THC',  # 20-25% THC
            r'up to\s*(\d+(?:\.\d+)?)%.*THC',  # up to 25% THC
        ]
        
        for pattern in thc_patterns:
            thc_match = re.search(pattern, strain_info, re.IGNORECASE)
            if thc_match:
                if len(thc_match.groups()) == 2 and thc_match.group(2):  # Range
                    if pd.isna(row.get('thc_min')) or row.get('thc_min') == '':
                        df.at[idx, 'thc_min'] = float(thc_match.group(1))
                    if pd.isna(row.get('thc_max')) or row.get('thc_max') == '':
                        df.at[idx, 'thc_max'] = float(thc_match.group(2))
                else:  # Single value
                    if pd.isna(row.get('thc')) or row.get('thc') == '':
                        df.at[idx, 'thc'] = float(thc_match.group(1))
                thc_count += 1
                break
        
        # Extract CBD values
        cbd_patterns = [
            r'CBD[:\s]*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%',  # CBD: 1-3%
            r'CBD[:\s]*(\d+(?:\.\d+)?)%',  # CBD: 1%
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%\s*CBD',  # 1-3% CBD
            r'up to\s*(\d+(?:\.\d+)?)%.*CBD',  # up to 3% CBD
        ]
        
        for pattern in cbd_patterns:
            cbd_match = re.search(pattern, strain_info, re.IGNORECASE)
            if cbd_match:
                if len(cbd_match.groups()) == 2 and cbd_match.group(2):  # Range
                    if pd.isna(row.get('cbd_min')) or row.get('cbd_min') == '':
                        df.at[idx, 'cbd_min'] = float(cbd_match.group(1))
                    if pd.isna(row.get('cbd_max')) or row.get('cbd_max') == '':
                        df.at[idx, 'cbd_max'] = float(cbd_match.group(2))
                else:  # Single value
                    if pd.isna(row.get('cbd')) or row.get('cbd') == '':
                        df.at[idx, 'cbd'] = float(cbd_match.group(1))
                cbd_count += 1
                break
    
    # Save updated CSV
    output_path = csv_path.replace('.csv', '_cannabinoids_extracted.csv')
    df.to_csv(output_path, index=False)
    
    print(f"Cannabinoid extraction complete!")
    print(f"Sativa percentages extracted: {sativa_count}")
    print(f"Indica percentages extracted: {indica_count}")
    print(f"THC values extracted: {thc_count}")
    print(f"CBD values extracted: {cbd_count}")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    extract_cannabinoid_data("Cannabis_Database.csv")
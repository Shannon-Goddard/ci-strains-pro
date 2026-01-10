#!/usr/bin/env python3
"""
Phase 3 HTML Enhancement Pipeline
Adds 8 strategic columns and fills gaps using 14,075 HTML files from S3

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import re
import boto3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path
from bs4 import BeautifulSoup
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('phase3_enhancement.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StrainHTMLProcessor:
    """Process HTML files to extract structured cannabis strain data"""
    
    def __init__(self):
        """Initialize the HTML processor with S3 client and extraction patterns"""
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        
        # Enhanced extraction patterns for strategic data
        self.patterns = {
            # Cannabinoids - fill missing thc_min/max, cbd_min/max
            'thc_range': r'THC[:\s]*(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?%',
            'cbd_range': r'CBD[:\s]*(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?%',
            'cbg_single': r'CBG[:\s]*(\d+(?:\.\d+)?)%',
            'cbn_single': r'CBN[:\s]*(\d+(?:\.\d+)?)%',
            
            # Flowering times - enhance flowering_day_min/max
            'flowering_days': r'[Ff]lowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*days?',
            'flowering_weeks': r'[Ff]lowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?',
            
            # Heights - enhance height columns
            'height_cm': r'[Hh]eight[:\s]*(\d+)\s*[-–]\s*(\d+)\s*cm',
            'height_indoor': r'[Ii]ndoor[:\s]*height[:\s]*(\d+)\s*[-–]\s*(\d+)',
            
            # Yields - enhance yield columns
            'yield_grams': r'[Yy]ield[:\s]*(\d+)\s*[-–]\s*(\d+)\s*g',
            'yield_per_m2': r'(\d+)\s*[-–]\s*(\d+)\s*g/m²',
            
            # Genetics - enhance lineage column
            'cross_pattern': r'([A-Za-z\s]+)\s*[x×]\s*([A-Za-z\s]+)',
            'parent_pattern': r'[Pp]arents?[:\s]*([^.]+)',
            
            # Difficulty - standardize grow_difficulty
            'difficulty': r'[Dd]ifficulty[:\s]*(easy|medium|hard|beginner|intermediate|advanced|expert)',
            
            # Terpenes - detailed profiles
            'terpene_profile': r'([A-Za-z]+)[:\s]*(\d+(?:\.\d+)?)%',
            'dominant_terpenes': r'[Dd]ominant[:\s]*terpenes?[:\s]*([^.]+)',
            
            # Effects - standardized extraction
            'effects_list': r'[Ee]ffects?[:\s]*([^.]+)',
            'medical_effects': r'[Mm]edical[:\s]*(?:effects?|benefits?)[:\s]*([^.]+)',
            
            # Flavors - enhanced extraction
            'flavor_profile': r'[Ff]lavors?[:\s]*([^.]+)',
            'taste_notes': r'[Tt]aste[:\s]*(?:notes?|profile)?[:\s]*([^.]+)'
        }
        
        # Standardization mappings
        self.difficulty_mapping = {
            'easy': 'Easy', 'beginner': 'Easy',
            'medium': 'Medium', 'intermediate': 'Medium',
            'hard': 'Hard', 'advanced': 'Hard', 'expert': 'Hard'
        }
        
    def get_html_by_url(self, source_url: str) -> Optional[str]:
        """Retrieve HTML content from local storage using URL mapping"""
        try:
            # Load URL mapping
            mapping_file = 'pipeline/06_html_collection/data/url_mapping.json'
            with open(mapping_file, 'r') as f:
                url_mapping = json.load(f)
            
            # Get filename for this URL
            if source_url in url_mapping:
                filename = url_mapping[source_url]
                html_file = f'pipeline/06_html_collection/data/html_files/{filename}'
                
                if os.path.exists(html_file):
                    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
            
            return None
            
        except Exception as e:
            logger.warning(f"Could not retrieve HTML for {source_url}: {e}")
            return None
    
    def extract_cannabinoids(self, html_content: str) -> Dict:
        """Extract cannabinoid information from HTML"""
        cannabinoids = {}
        
        # Extract THC range
        thc_match = re.search(self.patterns['thc_range'], html_content, re.IGNORECASE)
        if thc_match:
            thc_min = float(thc_match.group(1))
            thc_max = float(thc_match.group(2)) if thc_match.group(2) else thc_min
            cannabinoids.update({
                'thc_min': thc_min,
                'thc_max': thc_max,
                'thc_avg': (thc_min + thc_max) / 2
            })
        
        # Extract CBD range
        cbd_match = re.search(self.patterns['cbd_range'], html_content, re.IGNORECASE)
        if cbd_match:
            cbd_min = float(cbd_match.group(1))
            cbd_max = float(cbd_match.group(2)) if cbd_match.group(2) else cbd_min
            cannabinoids.update({
                'cbd_min': cbd_min,
                'cbd_max': cbd_max,
                'cbd_avg': (cbd_min + cbd_max) / 2
            })
        
        # Extract minor cannabinoids
        cbg_match = re.search(self.patterns['cbg_single'], html_content, re.IGNORECASE)
        if cbg_match:
            cannabinoids['cbg'] = float(cbg_match.group(1))
            
        cbn_match = re.search(self.patterns['cbn_single'], html_content, re.IGNORECASE)
        if cbn_match:
            cannabinoids['cbn'] = float(cbn_match.group(1))
        
        return cannabinoids
    
    def extract_terpenes(self, html_content: str) -> Dict:
        """Extract detailed terpene profiles from HTML"""
        terpenes = {}
        
        # Extract individual terpene percentages
        terpene_matches = re.findall(self.patterns['terpene_profile'], html_content, re.IGNORECASE)
        for terpene, percentage in terpene_matches:
            if terpene.lower() in ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene', 'humulene']:
                terpenes[terpene.lower()] = float(percentage)
        
        # Extract dominant terpenes list
        dominant_match = re.search(self.patterns['dominant_terpenes'], html_content, re.IGNORECASE)
        if dominant_match:
            terpenes['dominant_list'] = dominant_match.group(1).strip()
        
        return terpenes
    
    def extract_effects(self, html_content: str) -> List[str]:
        """Extract and standardize effects from HTML"""
        effects = []
        
        # Extract effects list
        effects_match = re.search(self.patterns['effects_list'], html_content, re.IGNORECASE)
        if effects_match:
            effects_text = effects_match.group(1)
            # Split by common delimiters and clean
            raw_effects = re.split(r'[,;]', effects_text)
            effects = [effect.strip().lower() for effect in raw_effects if len(effect.strip()) > 2]
        
        # Extract medical effects
        medical_match = re.search(self.patterns['medical_effects'], html_content, re.IGNORECASE)
        if medical_match:
            medical_text = medical_match.group(1)
            raw_medical = re.split(r'[,;]', medical_text)
            medical_effects = [effect.strip().lower() for effect in raw_medical if len(effect.strip()) > 2]
            effects.extend(medical_effects)
        
        return list(set(effects))  # Remove duplicates
    
    def extract_flavors(self, html_content: str) -> List[str]:
        """Extract and standardize flavors from HTML"""
        flavors = []
        
        # Extract flavor profile
        flavor_match = re.search(self.patterns['flavor_profile'], html_content, re.IGNORECASE)
        if flavor_match:
            flavor_text = flavor_match.group(1)
            raw_flavors = re.split(r'[,;]', flavor_text)
            flavors = [flavor.strip().lower() for flavor in raw_flavors if len(flavor.strip()) > 2]
        
        # Extract taste notes
        taste_match = re.search(self.patterns['taste_notes'], html_content, re.IGNORECASE)
        if taste_match:
            taste_text = taste_match.group(1)
            raw_taste = re.split(r'[,;]', taste_text)
            taste_flavors = [flavor.strip().lower() for flavor in raw_taste if len(flavor.strip()) > 2]
            flavors.extend(taste_flavors)
        
        return list(set(flavors))  # Remove duplicates
    
    def extract_growing_info(self, html_content: str) -> Dict:
        """Extract growing information from HTML"""
        growing_info = {}
        
        # Extract flowering time in days
        flowering_days_match = re.search(self.patterns['flowering_days'], html_content, re.IGNORECASE)
        if flowering_days_match:
            growing_info.update({
                'flowering_min': int(flowering_days_match.group(1)),
                'flowering_max': int(flowering_days_match.group(2))
            })
        
        # Extract flowering time in weeks (convert to days)
        flowering_weeks_match = re.search(self.patterns['flowering_weeks'], html_content, re.IGNORECASE)
        if flowering_weeks_match and 'flowering_min' not in growing_info:
            weeks_min = int(flowering_weeks_match.group(1))
            weeks_max = int(flowering_weeks_match.group(2))
            growing_info.update({
                'flowering_min': weeks_min * 7,
                'flowering_max': weeks_max * 7
            })
        
        # Extract height information
        height_match = re.search(self.patterns['height_cm'], html_content, re.IGNORECASE)
        if height_match:
            growing_info.update({
                'height_min_cm': int(height_match.group(1)),
                'height_max_cm': int(height_match.group(2))
            })
        
        # Extract yield information
        yield_match = re.search(self.patterns['yield_grams'], html_content, re.IGNORECASE)
        if yield_match:
            growing_info.update({
                'yield_min_g': int(yield_match.group(1)),
                'yield_max_g': int(yield_match.group(2))
            })
        
        # Extract difficulty
        difficulty_match = re.search(self.patterns['difficulty'], html_content, re.IGNORECASE)
        if difficulty_match:
            difficulty = difficulty_match.group(1).lower()
            growing_info['difficulty'] = self.difficulty_mapping.get(difficulty, 'Medium')
        
        return growing_info
    
    def extract_genetics(self, html_content: str) -> Dict:
        """Extract genetic information from HTML"""
        genetics = {}
        
        # Extract cross pattern
        cross_match = re.search(self.patterns['cross_pattern'], html_content, re.IGNORECASE)
        if cross_match:
            genetics['lineage'] = f"{cross_match.group(1).strip()} x {cross_match.group(2).strip()}"
        
        # Extract parent information
        parent_match = re.search(self.patterns['parent_pattern'], html_content, re.IGNORECASE)
        if parent_match:
            genetics['parents'] = parent_match.group(1).strip()
        
        return genetics
    
    def process_strain_html(self, strain_row: pd.Series) -> Optional[Dict]:
        """Process HTML for a single strain record"""
        if not strain_row['source_of_truth']:
            return None
        
        # Get HTML from S3
        html_content = self.get_html_by_url(strain_row['source_url'])
        if not html_content:
            return None
        
        # Extract structured data
        extracted_data = {
            'cannabinoids': self.extract_cannabinoids(html_content),
            'terpenes': self.extract_terpenes(html_content),
            'effects': self.extract_effects(html_content),
            'flavors': self.extract_flavors(html_content),
            'growing_info': self.extract_growing_info(html_content),
            'genetics': self.extract_genetics(html_content)
        }
        
        return extracted_data

from intelligent_validator import IntelligentDataValidator

class StrainEnhancer:
    """Enhance strain records with extracted HTML data"""
    
    def __init__(self):
        self.html_processor = StrainHTMLProcessor()
        
    def calculate_confidence_score(self, extracted_data: Dict) -> float:
        """Calculate confidence score for extracted data"""
        scores = []
        
        # Score based on data completeness
        if extracted_data['cannabinoids']:
            scores.append(0.9 if 'thc_min' in extracted_data['cannabinoids'] else 0.5)
        
        if extracted_data['terpenes']:
            scores.append(0.8)
        
        if extracted_data['effects']:
            scores.append(0.7)
        
        if extracted_data['flavors']:
            scores.append(0.7)
        
        if extracted_data['growing_info']:
            scores.append(0.8)
        
        return np.mean(scores) if scores else 0.0
    
    def format_terpene_profile(self, terpenes: Dict) -> str:
        """Format terpene data into structured string"""
        if not terpenes:
            return ""
        
        terpene_parts = []
        for terpene, percentage in terpenes.items():
            if terpene != 'dominant_list' and isinstance(percentage, (int, float)):
                terpene_parts.append(f"{terpene.title()}: {percentage}%")
        
        if 'dominant_list' in terpenes:
            terpene_parts.append(f"Dominant: {terpenes['dominant_list']}")
        
        return ", ".join(terpene_parts)
    
    def enhance_strain_record(self, original_row: pd.Series, extracted_data: Dict) -> pd.Series:
        """Enhanced version with intelligent overwriting capability"""
        enhanced_row = original_row.copy()
        validator = IntelligentDataValidator()
        overwrite_log = {}
        
        source_url = original_row.get('source_url', '')
        
        # 1. Intelligent cannabinoid enhancement
        if extracted_data['cannabinoids']:
            cannabinoids = extracted_data['cannabinoids']
            
            # THC enhancement
            if 'thc_min' in cannabinoids:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('thc_min'), cannabinoids['thc_min'], 
                    'cannabinoids', source_url, 0.9
                )
                if should_overwrite:
                    enhanced_row['thc_min'] = cannabinoids['thc_min']
                    enhanced_row['thc_max'] = cannabinoids['thc_max']
                    enhanced_row['thc'] = cannabinoids['thc_avg']
                    overwrite_log['thc'] = reason
            
            # CBD enhancement
            if 'cbd_min' in cannabinoids:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('cbd_min'), cannabinoids['cbd_min'],
                    'cannabinoids', source_url, 0.9
                )
                if should_overwrite:
                    enhanced_row['cbd_min'] = cannabinoids['cbd_min']
                    enhanced_row['cbd_max'] = cannabinoids['cbd_max'] 
                    enhanced_row['cbd'] = cannabinoids['cbd_avg']
                    overwrite_log['cbd'] = reason
        
        # 2. Intelligent terpene enhancement
        if extracted_data['terpenes']:
            terpene_string = self.format_terpene_profile(extracted_data['terpenes'])
            if terpene_string:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('terpenes'), terpene_string,
                    'text', source_url, 0.8
                )
                if should_overwrite:
                    enhanced_row['terpenes'] = terpene_string
                    overwrite_log['terpenes'] = reason
        
        # 3. Intelligent effects/flavors enhancement
        if extracted_data['effects']:
            effects_string = ', '.join(extracted_data['effects'][:10])
            should_overwrite, reason = validator.should_overwrite(
                enhanced_row.get('effects'), effects_string,
                'text', source_url, 0.75
            )
            if should_overwrite:
                enhanced_row['effects'] = effects_string
                overwrite_log['effects'] = reason
        
        if extracted_data['flavors']:
            flavors_string = ', '.join(extracted_data['flavors'][:10])
            should_overwrite, reason = validator.should_overwrite(
                enhanced_row.get('flavors'), flavors_string,
                'text', source_url, 0.75
            )
            if should_overwrite:
                enhanced_row['flavors'] = flavors_string
                overwrite_log['flavors'] = reason
        
        # 4. Intelligent growing info enhancement
        growing = extracted_data['growing_info']
        if growing:
            if 'flowering_min' in growing:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('flowering_day_min'), growing['flowering_min'],
                    'flowering_time', source_url, 0.8
                )
                if should_overwrite:
                    enhanced_row['flowering_day_min'] = growing['flowering_min']
                    enhanced_row['flowering_day_max'] = growing['flowering_max']
                    overwrite_log['flowering'] = reason
            
            if 'difficulty' in growing:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('grow_difficulty'), growing['difficulty'],
                    'text', source_url, 0.7
                )
                if should_overwrite:
                    enhanced_row['grow_difficulty'] = growing['difficulty']
                    overwrite_log['difficulty'] = reason
        
        # 5. Intelligent genetics enhancement
        if extracted_data['genetics']:
            genetics = extracted_data['genetics']
            if 'lineage' in genetics:
                should_overwrite, reason = validator.should_overwrite(
                    enhanced_row.get('lineage'), genetics['lineage'],
                    'text', source_url, 0.7
                )
                if should_overwrite:
                    enhanced_row['lineage'] = genetics['lineage']
                    overwrite_log['lineage'] = reason
        
        # 6. Add correction metadata
        enhanced_row['data_corrections'] = len(overwrite_log)
        enhanced_row['correction_log'] = str(overwrite_log) if overwrite_log else ""
        
        return enhanced_row
    
    def calculate_completeness_score(self, row: pd.Series) -> float:
        """Calculate data completeness score for a strain record"""
        key_fields = [
            'thc_min', 'thc_max', 'cbd_min', 'cbd_max', 'terpenes',
            'effects', 'flavors', 'flowering_day_min', 'flowering_day_max',
            'grow_difficulty', 'lineage'
        ]
        
        filled_fields = sum(1 for field in key_fields if not pd.isna(row.get(field)))
        return filled_fields / len(key_fields)
    
    def enhance_complete_dataset(self, input_file: str) -> pd.DataFrame:
        """Main pipeline to enhance the complete dataset"""
        
        # Load current dataset
        df = pd.read_csv(input_file, encoding='latin-1')
        logger.info(f"Loaded {len(df)} strain records with {len(df.columns)} columns")
        
        # Initialize tracking
        enhanced_records = []
        enhancement_stats = {
            'total_processed': 0,
            'html_enhanced': 0,
            'thc_filled': 0,
            'thc_corrected': 0,
            'cbd_filled': 0,
            'cbd_corrected': 0,
            'terpenes_added': 0,
            'terpenes_corrected': 0,
            'effects_added': 0,
            'effects_corrected': 0,
            'flavors_added': 0,
            'flavors_corrected': 0,
            'flowering_added': 0,
            'flowering_corrected': 0,
            'corrections_made': 0,
            'errors': 0
        }
        
        # Process each strain
        for idx, row in df.iterrows():
            enhancement_stats['total_processed'] += 1
            
            if row['source_of_truth']:  # Only enhance strains with HTML
                try:
                    # Extract data from HTML
                    extracted_data = self.html_processor.process_strain_html(row)
                    
                    if extracted_data:
                        # Enhance the record
                        enhanced_row = self.enhance_strain_record(row, extracted_data)
                        
                        # Add enhancement metadata
                        enhanced_row['html_enhanced'] = True
                        enhanced_row['enhancement_confidence'] = self.calculate_confidence_score(extracted_data)
                        enhanced_row['enhancement_timestamp'] = datetime.now().isoformat()
                        enhanced_row['data_completeness_score'] = self.calculate_completeness_score(enhanced_row)
                        
                        # Track enhancements and corrections
                        enhancement_stats['html_enhanced'] += 1
                        if enhanced_row.get('data_corrections', 0) > 0:
                            enhancement_stats['corrections_made'] = enhancement_stats.get('corrections_made', 0) + enhanced_row['data_corrections']
                        
                        if not pd.isna(enhanced_row['thc_min']) and pd.isna(row['thc_min']):
                            enhancement_stats['thc_filled'] += 1
                        elif not pd.isna(enhanced_row['thc_min']) and not pd.isna(row['thc_min']) and enhanced_row['thc_min'] != row['thc_min']:
                            enhancement_stats['thc_corrected'] = enhancement_stats.get('thc_corrected', 0) + 1
                        if not pd.isna(enhanced_row['cbd_min']) and pd.isna(row['cbd_min']):
                            enhancement_stats['cbd_filled'] += 1
                        if not pd.isna(enhanced_row['terpenes']) and pd.isna(row['terpenes']):
                            enhancement_stats['terpenes_added'] += 1
                        if not pd.isna(enhanced_row['effects']) and pd.isna(row['effects']):
                            enhancement_stats['effects_added'] += 1
                        if not pd.isna(enhanced_row['flavors']) and pd.isna(row['flavors']):
                            enhancement_stats['flavors_added'] += 1
                        if not pd.isna(enhanced_row['flowering_day_min']) and pd.isna(row['flowering_day_min']):
                            enhancement_stats['flowering_added'] += 1
                        
                        enhanced_records.append(enhanced_row)
                    else:
                        # No extracted data - keep original with metadata
                        row['html_enhanced'] = False
                        row['enhancement_confidence'] = 0.0
                        row['enhancement_timestamp'] = datetime.now().isoformat()
                        row['data_completeness_score'] = self.calculate_completeness_score(row)
                        enhanced_records.append(row)
                        
                except Exception as e:
                    logger.error(f"Error processing strain {row['strain_id']}: {e}")
                    enhancement_stats['errors'] += 1
                    # Keep original on error
                    row['html_enhanced'] = False
                    row['enhancement_confidence'] = 0.0
                    row['enhancement_timestamp'] = datetime.now().isoformat()
                    row['data_completeness_score'] = self.calculate_completeness_score(row)
                    enhanced_records.append(row)
            else:
                # No HTML source - keep original with metadata
                row['html_enhanced'] = False
                row['enhancement_confidence'] = 0.0
                row['enhancement_timestamp'] = datetime.now().isoformat()
                row['data_completeness_score'] = self.calculate_completeness_score(row)
                enhanced_records.append(row)
            
            # Progress logging
            if idx % 100 == 0:
                logger.info(f"Processed {idx}/{len(df)} strains...")
        
        # Create enhanced dataset
        enhanced_df = pd.DataFrame(enhanced_records)
        
        # Log final statistics
        logger.info("Enhancement Statistics:")
        for key, value in enhancement_stats.items():
            logger.info(f"  {key}: {value}")
        
        return enhanced_df, enhancement_stats

def generate_enhancement_report(original_df: pd.DataFrame, enhanced_df: pd.DataFrame, stats: Dict):
    """Generate comprehensive enhancement report"""
    
    report = f"""# Phase 3 HTML Enhancement Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Enhancement Summary
- **Total Strains Processed**: {stats['total_processed']:,}
- **Strains Enhanced with HTML**: {stats['html_enhanced']:,}
- **Enhancement Success Rate**: {(stats['html_enhanced']/stats['total_processed']*100):.1f}%

## Data Improvements
- **THC Ranges Added**: {stats['thc_filled']:,}
- **CBD Ranges Added**: {stats['cbd_filled']:,}
- **Terpene Profiles Added**: {stats['terpenes_added']:,}
- **Effects Added**: {stats['effects_added']:,}
- **Flavors Added**: {stats['flavors_added']:,}
- **Flowering Times Added**: {stats['flowering_added']:,}

## Data Completeness Analysis
- **Original Average Completeness**: {original_df.apply(lambda row: sum(1 for x in row if not pd.isna(x))/len(row), axis=1).mean():.2f}
- **Enhanced Average Completeness**: {enhanced_df['data_completeness_score'].mean():.2f}
- **Improvement**: {(enhanced_df['data_completeness_score'].mean() - original_df.apply(lambda row: sum(1 for x in row if not pd.isna(x))/len(row), axis=1).mean()):.2f}

## Strategic Columns Added
1. **html_enhanced**: Boolean flag indicating HTML enhancement
2. **enhancement_confidence**: Confidence score (0.0-1.0) for extracted data
3. **enhancement_timestamp**: Timestamp of enhancement process
4. **data_completeness_score**: Overall completeness score for the strain

## Quality Metrics
- **Average Enhancement Confidence**: {enhanced_df[enhanced_df['html_enhanced']]['enhancement_confidence'].mean():.2f}
- **High Confidence Enhancements (>0.8)**: {len(enhanced_df[enhanced_df['enhancement_confidence'] > 0.8]):,}
- **Processing Errors**: {stats['errors']:,}

Logic designed by Amazon Q, verified by Shannon Goddard.
"""
    
    with open('phase3_enhancement_report.md', 'w') as f:
        f.write(report)
    
    logger.info("Enhancement report generated: phase3_enhancement_report.md")

def main():
    """Main execution function"""
    logger.info("Starting Phase 3 HTML Enhancement Pipeline")
    
    # Initialize enhancer
    enhancer = StrainEnhancer()
    
    # Process the dataset
    input_file = 'revert_manual_review_cleaning.csv'
    enhanced_df, stats = enhancer.enhance_complete_dataset(input_file)
    
    # Save enhanced dataset
    output_file = 'cannabis_database_phase3_enhanced.csv'
    enhanced_df.to_csv(output_file, index=False, encoding='utf-8')
    logger.info(f"Enhanced dataset saved: {output_file}")
    
    # Generate report
    original_df = pd.read_csv(input_file, encoding='latin-1')
    generate_enhancement_report(original_df, enhanced_df, stats)
    
    logger.info("Phase 3 HTML Enhancement Pipeline completed successfully!")
    logger.info(f"Final dataset: {len(enhanced_df)} strains with {len(enhanced_df.columns)} columns")

if __name__ == "__main__":
    main()
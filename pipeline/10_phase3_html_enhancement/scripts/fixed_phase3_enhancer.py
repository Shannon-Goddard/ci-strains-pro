#!/usr/bin/env python3
"""
Fixed Phase 3 HTML Enhancement Pipeline
Properly accesses S3 HTML files and implements all 8 strategic columns

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import re
import json
import boto3
import hashlib
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FixedHTMLProcessor:
    """Fixed HTML processor with correct S3 access pattern"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.progress_db_path = '../06_html_collection/data/scraping_progress.db'
        
        # Load URL to S3 path mapping from database
        self.url_to_s3_map = self._load_s3_mapping()
        
        # Enhanced extraction patterns
        self.patterns = {
            'thc_range': r'THC[:\s]*(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?%',
            'cbd_range': r'CBD[:\s]*(\d+(?:\.\d+)?)(?:\s*[-–]\s*(\d+(?:\.\d+)?))?%',
            'terpene_with_percent': r'([A-Za-z]+)[:\s]*(\d+(?:\.\d+)?)%',
            'terpene_list': r'(?:terpenes?|terps?)[:\s]*([^.]{10,100})',
            'medical_uses': r'(?:treats?|helps?|relieves?|good for|medical)[:\s]*([^.]{5,100})',
            'conditions': r'\b(anxiety|depression|pain|insomnia|nausea|appetite|ptsd|adhd|stress|inflammation|seizures|cancer|epilepsy|glaucoma|arthritis)\b',
            'harvest_outdoor': r'(?:harvest|ready)[:\s]*([^.]*(?:september|october|november|early|late|mid)[^.]*)',
            'clone_available': r'(?:clone|cutting)s?\s*(?:available|offered|in stock|for sale)',
            'difficulty_level': r'(?:difficulty|grow level)[:\s]*(easy|medium|hard|beginner|intermediate|advanced|expert)',
            'lab_tested': r'lab\s*tested|tested\s*by|analysis\s*by|certificate|coa',
            'breeder_verified': r'breeder[:\s]*(?:verified|approved|official|authentic)',
        }
    
    def _load_s3_mapping(self) -> Dict[str, str]:
        """Load URL to S3 path mapping from scraping database"""
        mapping = {}
        try:
            if os.path.exists(self.progress_db_path):
                conn = sqlite3.connect(self.progress_db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT original_url, s3_path FROM scraping_progress WHERE status = 'completed'")
                for url, s3_path in cursor.fetchall():
                    mapping[url] = s3_path
                conn.close()
                logger.info(f"Loaded {len(mapping)} URL-to-S3 mappings")
            else:
                logger.warning(f"Scraping database not found: {self.progress_db_path}")
        except Exception as e:
            logger.error(f"Error loading S3 mapping: {e}")
        return mapping
    
    def get_html_for_strain(self, source_url: str) -> Optional[str]:
        """Retrieve HTML content using correct S3 path"""
        try:
            # First try direct mapping from database
            if source_url in self.url_to_s3_map:
                s3_key = self.url_to_s3_map[source_url]
                response = self.s3_client.get_object(Bucket=self.bucket, Key=s3_key)
                return response['Body'].read().decode('utf-8', errors='ignore')
            
            # Fallback: try hash-based approach
            url_hash = hashlib.sha256(source_url.encode()).hexdigest()[:16]
            s3_key = f'html/{url_hash}.html'
            
            response = self.s3_client.get_object(Bucket=self.bucket, Key=s3_key)
            return response['Body'].read().decode('utf-8', errors='ignore')
            
        except Exception as e:
            logger.debug(f"HTML retrieval failed for {source_url}: {e}")
            return None
    
    def extract_terpene_profile_structured(self, html_content: str) -> Dict:
        """Extract structured terpene data"""
        terpenes = {}
        
        # Extract terpene percentages
        terpene_matches = re.findall(self.patterns['terpene_with_percent'], html_content, re.IGNORECASE)
        known_terpenes = ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene', 'humulene', 'terpinolene', 'ocimene']
        
        for terpene, percentage in terpene_matches:
            terpene_clean = terpene.lower().strip()
            if any(known in terpene_clean for known in known_terpenes):
                try:
                    terpenes[terpene_clean] = float(percentage)
                except ValueError:
                    continue
        
        # Extract from terpene lists
        terpene_list_matches = re.findall(self.patterns['terpene_list'], html_content, re.IGNORECASE)
        for terpene_text in terpene_list_matches:
            for known_terpene in known_terpenes:
                if known_terpene in terpene_text.lower() and known_terpene not in terpenes:
                    terpenes[known_terpene] = 0.5  # Presence indicator
        
        return terpenes
    
    def extract_medical_applications(self, html_content: str) -> List[str]:
        """Extract medical applications"""
        medical_uses = set()
        
        # Extract from medical use statements
        medical_matches = re.findall(self.patterns['medical_uses'], html_content, re.IGNORECASE)
        for match in medical_matches:
            uses = re.split(r'[,;]', match.strip())
            for use in uses:
                clean_use = use.strip()
                if len(clean_use) > 3 and clean_use.lower() not in ['and', 'the', 'for', 'with', 'that', 'this']:
                    medical_uses.add(clean_use.title())
        
        # Extract specific conditions
        condition_matches = re.findall(self.patterns['conditions'], html_content, re.IGNORECASE)
        for condition in condition_matches:
            medical_uses.add(condition.title())
        
        return list(medical_uses)[:8]  # Limit to 8 most relevant
    
    def extract_harvest_window_outdoor(self, html_content: str) -> Optional[str]:
        """Extract outdoor harvest timing"""
        harvest_match = re.search(self.patterns['harvest_outdoor'], html_content, re.IGNORECASE)
        if harvest_match:
            return harvest_match.group(1).strip()
        return None
    
    def extract_clone_availability(self, html_content: str) -> bool:
        """Extract clone availability"""
        return bool(re.search(self.patterns['clone_available'], html_content, re.IGNORECASE))
    
    def calculate_data_confidence_score(self, html_content: str, extracted_data: Dict) -> float:
        """Calculate data confidence score"""
        confidence_factors = []
        
        # HTML content quality
        if len(html_content) > 15000:
            confidence_factors.append(0.25)
        elif len(html_content) > 8000:
            confidence_factors.append(0.15)
        elif len(html_content) > 3000:
            confidence_factors.append(0.1)
        
        # Data extraction success
        if extracted_data.get('terpenes'):
            confidence_factors.append(0.2)
        if extracted_data.get('medical_uses'):
            confidence_factors.append(0.15)
        if extracted_data.get('cannabinoids'):
            confidence_factors.append(0.2)
        if extracted_data.get('harvest_timing'):
            confidence_factors.append(0.1)
        
        # Quality indicators
        if re.search(self.patterns['lab_tested'], html_content, re.IGNORECASE):
            confidence_factors.append(0.1)
        
        return min(sum(confidence_factors), 1.0)
    
    def extract_dominant_terpene(self, terpene_profile: Dict) -> Optional[str]:
        """Extract dominant terpene"""
        if not terpene_profile:
            return None
        return max(terpene_profile, key=terpene_profile.get).title()
    
    def calculate_cannabinoid_ratio(self, thc_val: Optional[float], cbd_val: Optional[float]) -> str:
        """Calculate cannabinoid ratio"""
        if thc_val is None and cbd_val is None:
            return "Unknown"
        
        thc_val = thc_val or 0
        cbd_val = cbd_val or 0
        
        if cbd_val < 0.5:
            return "High THC"
        elif thc_val < 0.5:
            return "High CBD"
        else:
            ratio = round(thc_val / cbd_val) if cbd_val > 0 else int(thc_val)
            return f"{ratio}:1 THC:CBD"
    
    def assess_extraction_source_quality(self, html_content: str, extracted_data: Dict) -> str:
        """Assess source quality"""
        quality_score = 0
        
        # Content richness
        if len(html_content) > 20000:
            quality_score += 3
        elif len(html_content) > 10000:
            quality_score += 2
        elif len(html_content) > 5000:
            quality_score += 1
        
        # Data extraction success
        if extracted_data.get('terpenes'):
            quality_score += 2
        if extracted_data.get('medical_uses'):
            quality_score += 1
        if extracted_data.get('cannabinoids'):
            quality_score += 2
        if extracted_data.get('harvest_timing'):
            quality_score += 1
        
        # Quality indicators
        if re.search(self.patterns['lab_tested'], html_content, re.IGNORECASE):
            quality_score += 2
        if re.search(self.patterns['breeder_verified'], html_content, re.IGNORECASE):
            quality_score += 1
        
        if quality_score >= 8:
            return "Premium"
        elif quality_score >= 5:
            return "Standard"
        else:
            return "Basic"

class FixedDataEnhancer:
    """Fixed data enhancer with proper HTML access"""
    
    def __init__(self):
        self.html_processor = FixedHTMLProcessor()
    
    def enhance_dataset(self, input_file: str) -> Tuple[pd.DataFrame, Dict]:
        """Enhance dataset with all 8 strategic columns"""
        
        # Load dataset
        df = pd.read_csv(input_file, encoding='latin-1')
        logger.info(f"Loaded {len(df)} strains for enhancement")
        
        # Initialize new columns
        new_columns = {
            'terpene_profile_structured': '',
            'medical_applications': '',
            'harvest_window_outdoor': '',
            'clone_availability': False,
            'data_confidence_score': 0.0,
            'dominant_terpene': '',
            'cannabinoid_ratio': '',
            'extraction_source_quality': 'Basic'
        }
        
        for col, default_val in new_columns.items():
            df[col] = default_val
        
        # Enhancement statistics
        stats = {
            'total_processed': 0,
            'html_enhanced': 0,
            'terpene_profiles_added': 0,
            'medical_apps_added': 0,
            'harvest_windows_added': 0,
            'clones_identified': 0,
            'premium_sources': 0,
            'errors': 0
        }
        
        # Process strains with source_of_truth = True
        source_truth_strains = df[df['source_of_truth'] == True]
        logger.info(f"Processing {len(source_truth_strains)} strains with source_of_truth=True")
        
        for idx, row in source_truth_strains.iterrows():
            stats['total_processed'] += 1
            
            try:
                # Get HTML content
                html_content = self.html_processor.get_html_for_strain(row['source_url'])
                
                if html_content and len(html_content) > 1000:
                    # Extract all data
                    extracted_data = self.extract_all_data(html_content)
                    
                    # Enhance the row
                    enhanced_data = self.enhance_single_strain(html_content, extracted_data)
                    
                    # Update dataframe
                    for col, value in enhanced_data.items():
                        df.at[idx, col] = value
                    
                    # Update statistics
                    stats['html_enhanced'] += 1
                    if enhanced_data['terpene_profile_structured']:
                        stats['terpene_profiles_added'] += 1
                    if enhanced_data['medical_applications']:
                        stats['medical_apps_added'] += 1
                    if enhanced_data['harvest_window_outdoor']:
                        stats['harvest_windows_added'] += 1
                    if enhanced_data['clone_availability']:
                        stats['clones_identified'] += 1
                    if enhanced_data['extraction_source_quality'] == 'Premium':
                        stats['premium_sources'] += 1
                        
            except Exception as e:
                logger.error(f"Error processing strain {row.get('strain_id', idx)}: {e}")
                stats['errors'] += 1
            
            # Progress logging
            if stats['total_processed'] % 100 == 0:
                logger.info(f"Processed {stats['total_processed']}/{len(source_truth_strains)} strains...")
        
        # Log final statistics
        logger.info("Fixed Enhancement Statistics:")
        for key, value in stats.items():
            logger.info(f"  {key}: {value}")
        
        return df, stats
    
    def extract_all_data(self, html_content: str) -> Dict:
        """Extract all data patterns from HTML"""
        return {
            'terpenes': self.html_processor.extract_terpene_profile_structured(html_content),
            'medical_uses': self.html_processor.extract_medical_applications(html_content),
            'harvest_timing': self.html_processor.extract_harvest_window_outdoor(html_content),
            'clone_available': self.html_processor.extract_clone_availability(html_content),
            'cannabinoids': self.extract_cannabinoids(html_content)
        }
    
    def extract_cannabinoids(self, html_content: str) -> Dict:
        """Extract cannabinoid data"""
        cannabinoids = {}
        
        # THC extraction
        thc_match = re.search(self.html_processor.patterns['thc_range'], html_content, re.IGNORECASE)
        if thc_match:
            thc_min = float(thc_match.group(1))
            thc_max = float(thc_match.group(2)) if thc_match.group(2) else thc_min
            cannabinoids['thc'] = (thc_min + thc_max) / 2
        
        # CBD extraction
        cbd_match = re.search(self.html_processor.patterns['cbd_range'], html_content, re.IGNORECASE)
        if cbd_match:
            cbd_min = float(cbd_match.group(1))
            cbd_max = float(cbd_match.group(2)) if cbd_match.group(2) else cbd_min
            cannabinoids['cbd'] = (cbd_min + cbd_max) / 2
        
        return cannabinoids
    
    def enhance_single_strain(self, html_content: str, extracted_data: Dict) -> Dict:
        """Enhance single strain with all 8 strategic columns"""
        
        enhanced = {}
        
        # Column 1: terpene_profile_structured
        if extracted_data['terpenes']:
            enhanced['terpene_profile_structured'] = json.dumps(extracted_data['terpenes'])
        else:
            enhanced['terpene_profile_structured'] = ''
        
        # Column 2: medical_applications
        if extracted_data['medical_uses']:
            enhanced['medical_applications'] = ', '.join(extracted_data['medical_uses'])
        else:
            enhanced['medical_applications'] = ''
        
        # Column 3: harvest_window_outdoor
        enhanced['harvest_window_outdoor'] = extracted_data['harvest_timing'] or ''
        
        # Column 4: clone_availability
        enhanced['clone_availability'] = extracted_data['clone_available']
        
        # Column 5: data_confidence_score
        enhanced['data_confidence_score'] = self.html_processor.calculate_data_confidence_score(
            html_content, extracted_data
        )
        
        # Column 6: dominant_terpene
        enhanced['dominant_terpene'] = self.html_processor.extract_dominant_terpene(
            extracted_data['terpenes']
        ) or ''
        
        # Column 7: cannabinoid_ratio
        thc_val = extracted_data['cannabinoids'].get('thc')
        cbd_val = extracted_data['cannabinoids'].get('cbd')
        enhanced['cannabinoid_ratio'] = self.html_processor.calculate_cannabinoid_ratio(thc_val, cbd_val)
        
        # Column 8: extraction_source_quality
        enhanced['extraction_source_quality'] = self.html_processor.assess_extraction_source_quality(
            html_content, extracted_data
        )
        
        return enhanced

def main():
    """Execute fixed Phase 3 enhancement"""
    logger.info("Starting Fixed Phase 3 Enhancement Pipeline")
    
    # Initialize enhancer
    enhancer = FixedDataEnhancer()
    
    # Process dataset
    input_file = '../../revert_manual_review_cleaning.csv'
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return
    
    enhanced_df, stats = enhancer.enhance_dataset(input_file)
    
    # Save enhanced dataset
    output_file = 'cannabis_database_fixed_phase3_enhanced.csv'
    enhanced_df.to_csv(output_file, index=False, encoding='utf-8')
    
    # Generate report
    report_content = f"""# Fixed Phase 3 Enhancement Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Enhancement Statistics
- Total Processed: {stats['total_processed']}
- HTML Enhanced: {stats['html_enhanced']}
- Terpene Profiles Added: {stats['terpene_profiles_added']}
- Medical Applications Added: {stats['medical_apps_added']}
- Harvest Windows Added: {stats['harvest_windows_added']}
- Clones Identified: {stats['clones_identified']}
- Premium Sources: {stats['premium_sources']}
- Processing Errors: {stats['errors']}

## Success Rate
- HTML Retrieval Rate: {(stats['html_enhanced'] / stats['total_processed'] * 100):.1f}%
- Data Enhancement Rate: {((stats['terpene_profiles_added'] + stats['medical_apps_added']) / stats['html_enhanced'] * 100):.1f}%

## Output Files
- Enhanced Dataset: {output_file}
- Total Columns: {len(enhanced_df.columns)}
- New Strategic Columns: 8

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
    
    with open('fixed_phase3_enhancement_report.md', 'w') as f:
        f.write(report_content)
    
    logger.info(f"Fixed enhancement complete!")
    logger.info(f"Output: {output_file} with {len(enhanced_df.columns)} columns")
    logger.info(f"HTML Enhanced: {stats['html_enhanced']}/{stats['total_processed']} strains")

if __name__ == "__main__":
    main()
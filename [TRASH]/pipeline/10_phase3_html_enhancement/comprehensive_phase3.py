#!/usr/bin/env python3
"""
Complete Phase 3 Enhanced Analysis Pipeline
Implements all 8 strategic columns from PHASE_3_ENHANCED_ANALYSIS_PLAN.md

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import re
import json
import boto3
import hashlib
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ComprehensiveHTMLProcessor:
    """Complete HTML processor implementing all 8 strategic columns"""
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.progress_db = 'pipeline/06_html_collection/data/scraping_progress.db'
        
        # Enhanced extraction patterns for all 8 columns
        self.patterns = {
            # Cannabinoid extraction
            'thc_range': r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
            'cbd_range': r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
            'cannabinoid_ratio': r'(\d+):(\d+)\s*(?:THC:CBD|CBD:THC)',
            
            # Terpene extraction (Column 1: terpene_profile_structured)
            'terpene_with_percent': r'([A-Za-z]+)[:\s]*(\d+(?:\.\d+)?)%',
            'terpene_dominant': r'[Dd]ominant[:\s]*terpenes?[:\s]*([A-Za-z\s,]+)',
            'terpene_list': r'[Tt]erpenes?[:\s]*([^.]+)',
            
            # Medical applications (Column 2: medical_applications)
            'medical_uses': r'(?:[Tt]reats?|[Hh]elps?|[Rr]elieves?|[Gg]ood for)[:\s]*([^.]+)',
            'conditions': r'(anxiety|depression|pain|insomnia|nausea|appetite|ptsd|adhd|stress|inflammation|seizures)',
            'medical_benefits': r'[Mm]edical[:\s]*(?:uses?|benefits?)[:\s]*([^.]+)',
            
            # Harvest timing (Column 3: harvest_window_outdoor)
            'harvest_outdoor': r'[Hh]arvest[:\s]*([^.]*(?:September|October|November|Early|Late|Mid)[^.]*)',
            'outdoor_ready': r'[Oo]utdoor[:\s]*(?:harvest|ready)[:\s]*([^.]+)',
            
            # Clone availability (Column 4: clone_availability)
            'clone_available': r'(?:clone|cutting)s?\s*(?:available|offered|in stock)',
            'propagation': r'[Pp]ropagation[:\s]*([^.]*(?:clone|cutting)[^.]*)',
            
            # Growing difficulty and quality indicators
            'difficulty_level': r'[Dd]ifficulty[:\s]*(easy|medium|hard|beginner|intermediate|advanced|expert)',
            'grow_level': r'[Gg]row[:\s]*(?:level|difficulty)[:\s]*(easy|medium|hard|beginner|intermediate|advanced)',
            
            # Data quality indicators
            'detailed_info': r'(?:genetics|lineage|parents)[:\s]*([^.]+)',
            'lab_tested': r'lab[:\s]*tested|tested[:\s]*by|analysis[:\s]*by',
            'breeder_verified': r'breeder[:\s]*(?:verified|approved|official)',
        }
    
    def get_html_for_strain(self, source_url: str) -> Optional[str]:
        """Retrieve HTML content for a strain's source URL"""
        try:
            # Hash URL to find S3 object (matching collection method)
            url_hash = hashlib.sha256(source_url.encode()).hexdigest()[:16]
            
            # Try S3 retrieval
            response = self.s3_client.get_object(
                Bucket=self.bucket,
                Key=f'html/{url_hash}.html'
            )
            return response['Body'].read().decode('utf-8', errors='ignore')
            
        except Exception as e:
            logger.debug(f"S3 retrieval failed for {source_url}: {e}")
            return None
    
    def extract_terpene_profile_structured(self, html_content: str) -> Dict:
        """Extract structured terpene data for Column 1"""
        terpenes = {}
        
        # Extract individual terpene percentages
        terpene_matches = re.findall(self.patterns['terpene_with_percent'], html_content, re.IGNORECASE)
        for terpene, percentage in terpene_matches:
            terpene_clean = terpene.lower().strip()
            if terpene_clean in ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene', 'humulene', 'terpinolene', 'ocimene']:
                try:
                    terpenes[terpene_clean] = float(percentage)
                except ValueError:
                    continue
        
        # Extract from terpene lists
        terpene_list_match = re.search(self.patterns['terpene_list'], html_content, re.IGNORECASE)
        if terpene_list_match:
            terpene_text = terpene_list_match.group(1)
            known_terpenes = ['myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene', 'humulene']
            for terpene in known_terpenes:
                if terpene in terpene_text.lower() and terpene not in terpenes:
                    terpenes[terpene] = 0.5  # Default presence indicator
        
        return terpenes
    
    def extract_medical_applications(self, html_content: str) -> List[str]:
        """Extract medical applications for Column 2"""
        medical_uses = set()
        
        # Extract from medical use statements
        medical_matches = re.findall(self.patterns['medical_uses'], html_content, re.IGNORECASE)
        for match in medical_matches:
            # Clean and split medical uses
            uses = re.split(r'[,;]', match.strip())
            for use in uses:
                clean_use = use.strip().lower()
                if len(clean_use) > 3 and clean_use not in ['and', 'the', 'for', 'with']:
                    medical_uses.add(clean_use.title())
        
        # Extract specific conditions
        condition_matches = re.findall(self.patterns['conditions'], html_content, re.IGNORECASE)
        for condition in condition_matches:
            medical_uses.add(condition.title())
        
        # Extract from medical benefits section
        benefits_match = re.search(self.patterns['medical_benefits'], html_content, re.IGNORECASE)
        if benefits_match:
            benefits_text = benefits_match.group(1)
            benefits = re.split(r'[,;]', benefits_text)
            for benefit in benefits:
                clean_benefit = benefit.strip()
                if len(clean_benefit) > 3:
                    medical_uses.add(clean_benefit.title())
        
        return list(medical_uses)[:8]  # Limit to 8 most relevant
    
    def extract_harvest_window_outdoor(self, html_content: str) -> Optional[str]:
        """Extract outdoor harvest timing for Column 3"""
        # Try harvest outdoor pattern
        harvest_match = re.search(self.patterns['harvest_outdoor'], html_content, re.IGNORECASE)
        if harvest_match:
            return harvest_match.group(1).strip()
        
        # Try outdoor ready pattern
        outdoor_match = re.search(self.patterns['outdoor_ready'], html_content, re.IGNORECASE)
        if outdoor_match:
            return outdoor_match.group(1).strip()
        
        return None
    
    def extract_clone_availability(self, html_content: str) -> bool:
        """Extract clone availability for Column 4"""
        # Check for clone availability mentions
        clone_match = re.search(self.patterns['clone_available'], html_content, re.IGNORECASE)
        if clone_match:
            return True
        
        # Check propagation methods
        prop_match = re.search(self.patterns['propagation'], html_content, re.IGNORECASE)
        if prop_match and 'clone' in prop_match.group(1).lower():
            return True
        
        return False
    
    def calculate_data_confidence_score(self, html_content: str, extracted_data: Dict) -> float:
        """Calculate data confidence score for Column 5"""
        confidence_factors = []
        
        # HTML content quality
        if len(html_content) > 10000:
            confidence_factors.append(0.2)
        elif len(html_content) > 5000:
            confidence_factors.append(0.1)
        
        # Data extraction success
        if extracted_data.get('terpenes'):
            confidence_factors.append(0.15)
        if extracted_data.get('medical_uses'):
            confidence_factors.append(0.1)
        if extracted_data.get('cannabinoids'):
            confidence_factors.append(0.2)
        if extracted_data.get('harvest_timing'):
            confidence_factors.append(0.1)
        
        # Source quality indicators
        if re.search(self.patterns['lab_tested'], html_content, re.IGNORECASE):
            confidence_factors.append(0.15)
        if re.search(self.patterns['breeder_verified'], html_content, re.IGNORECASE):
            confidence_factors.append(0.1)
        
        return min(sum(confidence_factors), 1.0)
    
    def extract_dominant_terpene(self, terpene_profile: Dict) -> Optional[str]:
        """Extract dominant terpene for Column 6"""
        if not terpene_profile:
            return None
        
        # Return terpene with highest percentage
        return max(terpene_profile, key=terpene_profile.get).title()
    
    def calculate_cannabinoid_ratio(self, thc_val: float, cbd_val: float) -> str:
        """Calculate cannabinoid ratio for Column 7"""
        if thc_val is None or cbd_val is None:
            return "Unknown"
        
        if cbd_val < 0.5:
            return "High THC"
        elif thc_val < 0.5:
            return "High CBD"
        else:
            # Calculate ratio
            thc_ratio = round(thc_val / cbd_val) if cbd_val > 0 else thc_val
            cbd_ratio = 1
            return f"{thc_ratio}:{cbd_ratio} THC:CBD"
    
    def assess_extraction_source_quality(self, html_content: str, extracted_data: Dict) -> str:
        """Assess source quality for Column 8"""
        quality_score = 0
        
        # Content richness
        if len(html_content) > 15000:
            quality_score += 2
        elif len(html_content) > 8000:
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
        if re.search(self.patterns['detailed_info'], html_content, re.IGNORECASE):
            quality_score += 1
        
        # Classify quality
        if quality_score >= 8:
            return "Premium"
        elif quality_score >= 5:
            return "Standard"
        else:
            return "Basic"

class ComprehensiveDataEnhancer:
    """Complete data enhancer implementing all 8 strategic columns"""
    
    def __init__(self):
        self.html_processor = ComprehensiveHTMLProcessor()
    
    def enhance_complete_dataset(self, input_file: str) -> pd.DataFrame:
        """Enhance dataset with all 8 strategic columns"""
        
        # Load dataset
        df = pd.read_csv(input_file, encoding='latin-1')
        logger.info(f"Loaded {len(df)} strains for comprehensive enhancement")
        
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
        
        # Process each strain
        for idx, row in df.iterrows():
            stats['total_processed'] += 1
            
            if row['source_of_truth']:
                try:
                    # Get HTML content
                    html_content = self.html_processor.get_html_for_strain(row['source_url'])
                    
                    if html_content:
                        # Extract all data
                        extracted_data = self.extract_all_data(html_content)
                        
                        # Enhance the row
                        enhanced_row = self.enhance_single_strain(row, html_content, extracted_data)
                        
                        # Update dataframe
                        for col in new_columns.keys():
                            df.at[idx, col] = enhanced_row[col]
                        
                        # Update statistics
                        stats['html_enhanced'] += 1
                        if enhanced_row['terpene_profile_structured']:
                            stats['terpene_profiles_added'] += 1
                        if enhanced_row['medical_applications']:
                            stats['medical_apps_added'] += 1
                        if enhanced_row['harvest_window_outdoor']:
                            stats['harvest_windows_added'] += 1
                        if enhanced_row['clone_availability']:
                            stats['clones_identified'] += 1
                        if enhanced_row['extraction_source_quality'] == 'Premium':
                            stats['premium_sources'] += 1
                            
                except Exception as e:
                    logger.error(f"Error processing strain {row['strain_id']}: {e}")
                    stats['errors'] += 1
            
            # Progress logging
            if idx % 100 == 0:
                logger.info(f"Processed {idx}/{len(df)} strains...")
        
        # Log final statistics
        logger.info("Comprehensive Enhancement Statistics:")
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
            cannabinoids['thc'] = (float(thc_match.group(1)) + float(thc_match.group(2))) / 2
        
        # CBD extraction
        cbd_match = re.search(self.html_processor.patterns['cbd_range'], html_content, re.IGNORECASE)
        if cbd_match:
            cannabinoids['cbd'] = (float(cbd_match.group(1)) + float(cbd_match.group(2))) / 2
        
        return cannabinoids
    
    def enhance_single_strain(self, strain_row: pd.Series, html_content: str, extracted_data: Dict) -> Dict:
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
    """Execute comprehensive Phase 3 enhancement"""
    logger.info("Starting Comprehensive Phase 3 Enhancement Pipeline")
    
    # Initialize enhancer
    enhancer = ComprehensiveDataEnhancer()
    
    # Process dataset
    input_file = 'revert_manual_review_cleaning.csv'
    enhanced_df, stats = enhancer.enhance_complete_dataset(input_file)
    
    # Save enhanced dataset
    output_file = 'cannabis_database_comprehensive_phase3.csv'
    enhanced_df.to_csv(output_file, index=False, encoding='utf-8')
    
    logger.info(f"Comprehensive enhancement complete!")
    logger.info(f"Output: {output_file} with {len(enhanced_df.columns)} columns")
    logger.info(f"Added 8 strategic columns: {len(enhanced_df.columns) - 41} new columns")

if __name__ == "__main__":
    main()
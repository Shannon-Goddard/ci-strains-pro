#!/usr/bin/env python3
"""
Intelligent Data Validation and Correction Module
Overwrites existing data when HTML sources are more reliable

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import re
from typing import Dict, Tuple, Optional

class IntelligentDataValidator:
    """Validates and corrects existing data using HTML sources"""
    
    def __init__(self):
        # Confidence thresholds for overwriting existing data
        self.overwrite_thresholds = {
            'cannabinoids': 0.85,  # High confidence needed for THC/CBD
            'terpenes': 0.80,      # Medium-high for terpenes
            'effects': 0.75,       # Medium for effects/flavors
            'flavors': 0.75,
            'growing_info': 0.80,  # High for growing data
            'genetics': 0.70       # Lower for genetics (often subjective)
        }
        
        # Data quality indicators
        self.quality_indicators = {
            'high_quality_sources': [
                'mephistogenetics.com',
                'royalqueenseeds.com', 
                'barneysfarm.com',
                'greenhouseseeds.nl'
            ],
            'suspect_patterns': [
                r'^\d+$',  # Just a number
                r'^[a-z]+$',  # All lowercase
                r'unknown|n/a|tbd|coming soon',  # Placeholder text
                r'^\s*$'  # Empty/whitespace
            ]
        }
    
    def assess_source_reliability(self, source_url: str) -> float:
        """Assess reliability of the HTML source"""
        if not source_url:
            return 0.0
            
        # High-quality breeder sites get higher reliability
        for quality_source in self.quality_indicators['high_quality_sources']:
            if quality_source in source_url.lower():
                return 0.95
        
        # Seed banks get medium reliability
        if any(bank in source_url.lower() for bank in ['seedbank', 'seeds']):
            return 0.80
            
        # Default reliability
        return 0.70
    
    def assess_existing_data_quality(self, value: any, field_type: str) -> float:
        """Assess quality of existing data"""
        if pd.isna(value):
            return 0.0  # Missing data has no quality
            
        value_str = str(value).lower().strip()
        
        # Check for suspect patterns
        for pattern in self.quality_indicators['suspect_patterns']:
            if re.search(pattern, value_str, re.IGNORECASE):
                return 0.2  # Low quality
        
        # Field-specific quality checks
        if field_type == 'cannabinoids':
            try:
                num_val = float(value)
                if 0 <= num_val <= 40:  # Reasonable THC/CBD range
                    return 0.8
                else:
                    return 0.3  # Unreasonable range
            except:
                return 0.4
                
        elif field_type == 'flowering_time':
            try:
                num_val = float(value)
                if 30 <= num_val <= 120:  # Reasonable flowering range
                    return 0.8
                else:
                    return 0.3
            except:
                return 0.4
        
        elif field_type == 'text':
            if len(value_str) > 3 and ',' in value_str:  # Structured text
                return 0.7
            elif len(value_str) > 10:  # Decent length
                return 0.6
            else:
                return 0.4
        
        return 0.6  # Default quality
    
    def should_overwrite(self, existing_value: any, extracted_value: any, 
                        field_type: str, source_url: str, extraction_confidence: float) -> Tuple[bool, str]:
        """Determine if existing data should be overwritten"""
        
        # Never overwrite if extracted value is empty/invalid
        if pd.isna(extracted_value) or extracted_value == "":
            return False, "extracted_empty"
        
        # Always fill if existing is empty
        if pd.isna(existing_value):
            return True, "fill_empty"
        
        # Assess data quality
        source_reliability = self.assess_source_reliability(source_url)
        existing_quality = self.assess_existing_data_quality(existing_value, field_type)
        
        # Calculate combined confidence for extracted data
        combined_confidence = extraction_confidence * source_reliability
        
        # Get threshold for this field type
        threshold = self.overwrite_thresholds.get(field_type, 0.80)
        
        # Decision logic
        if combined_confidence >= threshold and combined_confidence > existing_quality + 0.2:
            return True, f"higher_confidence_{combined_confidence:.2f}_vs_{existing_quality:.2f}"
        elif existing_quality < 0.3 and combined_confidence > 0.6:
            return True, f"poor_existing_quality_{existing_quality:.2f}"
        else:
            return False, f"keep_existing_{existing_quality:.2f}_vs_{combined_confidence:.2f}"
    
    def validate_cannabinoid_consistency(self, thc_min: float, thc_max: float, 
                                       cbd_min: float, cbd_max: float) -> bool:
        """Validate cannabinoid ranges for consistency"""
        try:
            # Check THC range
            if thc_min is not None and thc_max is not None:
                if thc_min > thc_max or thc_min < 0 or thc_max > 40:
                    return False
            
            # Check CBD range  
            if cbd_min is not None and cbd_max is not None:
                if cbd_min > cbd_max or cbd_min < 0 or cbd_max > 30:
                    return False
            
            # Check THC+CBD doesn't exceed reasonable total
            total_max = (thc_max or 0) + (cbd_max or 0)
            if total_max > 45:  # Unreasonably high total
                return False
                
            return True
        except:
            return False

# Add this method to the StrainEnhancer class
def enhance_strain_record_intelligent(self, original_row: pd.Series, extracted_data: Dict) -> Tuple[pd.Series, Dict]:
    """Enhanced version with intelligent overwriting"""
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
    
    # 5. Add overwrite metadata
    enhanced_row['data_corrections'] = len(overwrite_log)
    enhanced_row['correction_log'] = str(overwrite_log) if overwrite_log else ""
    
    return enhanced_row, overwrite_log
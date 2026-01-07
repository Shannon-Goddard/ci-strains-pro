# Phase 3: Enhanced Analysis Pipeline - HTML to CSV Enhancement

**Date**: January 5, 2026  
**Architect**: Amazon Q  
**Technical Partner**: Shannon Goddard  
**Status**: Ready for Implementation  
**Target Dataset**: `revert_manual_review_cleaning.csv` (39 columns)

---

## Mission Statement
Transform 14,075 collected HTML files into structured data enhancements, filling gaps in your comprehensive 39-column cannabis strain dataset through intelligent parsing and AI analysis.

---

## Current Dataset Analysis

### Your Existing Schema (39 columns):
```
strain_id, source_of_truth, source_url, strain_name, primary_generation, breeding_method, 
phenotype, lineage, breeder_name, bank_name, seed_gender, flowering_behavior, 
sativa_percentage, indica_percentage, ruderalis_percentage, thc_min, thc_max, thc, 
cbd_min, cbd_max, cbd, seed_to_harvest_day_min, seed_to_harvest_day_max, 
flowering_day_min, flowering_day_max, height_indoor_description, height_indoor_min_cm, 
height_indoor_max_cm, height_outdoor_description, height_outdoor_min_cm, 
height_outdoor_max_cm, yield_decription, indoor_yield_min_g_per_m, 
indoor_yield_max_g_per_m, outdoor_yield_min_g_per_plant, outdoor_yield_max_g_per_plant, 
effects, flavors, terpenes, grow_difficulty, scraped_at
```

### Enhancement Strategy
**Focus**: Fill gaps and enhance existing columns rather than adding many new ones

---

## Phase 3A: Gap Analysis and Enhancement Targets

### Priority Enhancement Areas

#### 1. Cannabinoid Profile Enhancement
**Target Columns**: `thc_min`, `thc_max`, `cbd_min`, `cbd_max`
- Fill missing THC/CBD ranges from HTML
- Add minor cannabinoids (CBG, CBN) to `terpenes` column
- Validate existing ranges against HTML sources

#### 2. Terpene Profile Expansion  
**Target Column**: `terpenes`
- Extract detailed terpene profiles from HTML
- Structure as: "Myrcene: 0.8%, Limonene: 0.6%, Pinene: 0.4%"
- Enhance existing sparse terpene data

#### 3. Effects and Flavors Enhancement
**Target Columns**: `effects`, `flavors`
- Standardize and expand existing descriptions
- Extract detailed effects from product descriptions
- Normalize flavor terminology across sources

#### 4. Growing Information Completion
**Target Columns**: `flowering_day_min/max`, `height_*`, `yield_*`, `grow_difficulty`
- Fill missing flowering times from HTML
- Extract height and yield ranges
- Standardize difficulty levels (Easy/Medium/Hard)

#### 5. Genetics and Breeding Enhancement
**Target Columns**: `lineage`, `breeder_name`, `primary_generation`
- Extract detailed lineage information
- Validate and enhance breeder attributions
- Identify generation markers (F1, S1, BX, etc.)

---

## Phase 3B: HTML Processing Architecture

### Content Extraction Engine
```python
class StrainHTMLProcessor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        
    def process_strain_html(self, strain_row):
        """Process HTML for a single strain record"""
        if not strain_row['source_of_truth']:
            return None
            
        # Get HTML from S3 using source_url hash
        html_content = self.get_html_by_url(strain_row['source_url'])
        
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
```

### Pattern Recognition Patterns
```python
# Enhanced patterns for your specific data needs
EXTRACTION_PATTERNS = {
    # Cannabinoids - fill missing thc_min/max, cbd_min/max
    'thc_range': r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
    'cbd_range': r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
    'cbg_single': r'CBG[:\s]*(\d+(?:\.\d+)?)%',
    'cbn_single': r'CBN[:\s]*(\d+(?:\.\d+)?)%',
    
    # Flowering times - enhance flowering_day_min/max
    'flowering_days': r'[Ff]lowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*days?',
    'flowering_weeks': r'[Ff]lowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?',
    
    # Heights - enhance height_indoor/outdoor columns
    'height_cm': r'[Hh]eight[:\s]*(\d+)\s*[-–]\s*(\d+)\s*cm',
    'height_indoor': r'[Ii]ndoor[:\s]*height[:\s]*(\d+)\s*[-–]\s*(\d+)',
    
    # Yields - enhance yield columns
    'yield_grams': r'[Yy]ield[:\s]*(\d+)\s*[-–]\s*(\d+)\s*g',
    'yield_per_m2': r'(\d+)\s*[-–]\s*(\d+)\s*g/m²',
    
    # Genetics - enhance lineage column
    'cross_pattern': r'([A-Za-z\s]+)\s*[x×]\s*([A-Za-z\s]+)',
    'parent_pattern': r'[Pp]arents?[:\s]*([^.]+)',
    
    # Difficulty - standardize grow_difficulty
    'difficulty': r'[Dd]ifficulty[:\s]*(easy|medium|hard|beginner|intermediate|advanced|expert)'
}
```

---

## Phase 3C: Enhancement Implementation

### Data Enhancement Process
```python
def enhance_strain_record(original_row, extracted_data):
    """Enhance a single strain record with HTML data"""
    enhanced_row = original_row.copy()
    
    # 1. Enhance cannabinoids
    if extracted_data['cannabinoids']:
        if pd.isna(enhanced_row['thc_min']) and 'thc_min' in extracted_data['cannabinoids']:
            enhanced_row['thc_min'] = extracted_data['cannabinoids']['thc_min']
            enhanced_row['thc_max'] = extracted_data['cannabinoids']['thc_max']
        
        if pd.isna(enhanced_row['cbd_min']) and 'cbd_min' in extracted_data['cannabinoids']:
            enhanced_row['cbd_min'] = extracted_data['cannabinoids']['cbd_min']
            enhanced_row['cbd_max'] = extracted_data['cannabinoids']['cbd_max']
    
    # 2. Enhance terpenes column
    if extracted_data['terpenes'] and pd.isna(enhanced_row['terpenes']):
        terpene_string = format_terpene_profile(extracted_data['terpenes'])
        enhanced_row['terpenes'] = terpene_string
    
    # 3. Enhance effects and flavors
    if extracted_data['effects'] and pd.isna(enhanced_row['effects']):
        enhanced_row['effects'] = ', '.join(extracted_data['effects'])
    
    if extracted_data['flavors'] and pd.isna(enhanced_row['flavors']):
        enhanced_row['flavors'] = ', '.join(extracted_data['flavors'])
    
    # 4. Enhance growing information
    growing = extracted_data['growing_info']
    if growing:
        if pd.isna(enhanced_row['flowering_day_min']) and 'flowering_min' in growing:
            enhanced_row['flowering_day_min'] = growing['flowering_min']
            enhanced_row['flowering_day_max'] = growing['flowering_max']
        
        if pd.isna(enhanced_row['grow_difficulty']) and 'difficulty' in growing:
            enhanced_row['grow_difficulty'] = standardize_difficulty(growing['difficulty'])
    
    # 5. Add enhancement metadata
    enhanced_row['html_enhanced'] = True
    enhanced_row['enhancement_confidence'] = calculate_confidence_score(extracted_data)
    enhanced_row['enhancement_timestamp'] = pd.Timestamp.now()
    
    return enhanced_row
```

### Quality Assurance and Validation
```python
def validate_enhancement(original_value, extracted_value, field_type):
    """Validate extracted data against existing values"""
    
    if field_type == 'cannabinoid_range':
        # Check if extracted THC/CBD is reasonable
        if extracted_value < 0 or extracted_value > 40:
            return False, 0.0
        
        # If original exists, check similarity
        if not pd.isna(original_value):
            similarity = calculate_similarity(original_value, extracted_value)
            return similarity > 0.7, similarity
    
    elif field_type == 'flowering_time':
        # Validate flowering time ranges
        if extracted_value < 30 or extracted_value > 120:
            return False, 0.0
    
    elif field_type == 'text_field':
        # Validate text fields (effects, flavors)
        if len(extracted_value) < 3 or len(extracted_value) > 200:
            return False, 0.0
    
    return True, 0.8  # Default confidence
```

---

## Phase 3D: Implementation Pipeline

### Main Enhancement Script
```python
def enhance_complete_dataset():
    """Main pipeline to enhance the complete dataset"""
    
    # Load your current dataset
    df = pd.read_csv('revert_manual_review_cleaning.csv')
    print(f"Loaded {len(df)} strain records with {len(df.columns)} columns")
    
    # Initialize processors
    html_processor = StrainHTMLProcessor()
    enhanced_records = []
    
    # Process each strain
    for idx, row in df.iterrows():
        if row['source_of_truth']:  # Only enhance strains with HTML
            try:
                # Extract data from HTML
                extracted_data = html_processor.process_strain_html(row)
                
                # Enhance the record
                enhanced_row = enhance_strain_record(row, extracted_data)
                enhanced_records.append(enhanced_row)
                
                if idx % 100 == 0:
                    print(f"Processed {idx}/{len(df)} strains...")
                    
            except Exception as e:
                print(f"Error processing strain {row['strain_id']}: {e}")
                enhanced_records.append(row)  # Keep original on error
        else:
            # No HTML source - keep original
            enhanced_records.append(row)
    
    # Create enhanced dataset
    enhanced_df = pd.DataFrame(enhanced_records)
    
    # Add new metadata columns
    enhanced_df['html_enhanced'] = enhanced_df['source_of_truth']
    enhanced_df['data_completeness_score'] = enhanced_df.apply(calculate_completeness, axis=1)
    
    # Save enhanced dataset
    enhanced_df.to_csv('Cannabis_Database_Enhanced_Complete.csv', index=False)
    
    # Generate enhancement report
    generate_enhancement_report(df, enhanced_df)
    
    return enhanced_df
```

---

## Expected Enhancement Results

### Data Completeness Improvements
- **THC/CBD Ranges**: Fill 70%+ of missing cannabinoid data
- **Terpene Profiles**: Add detailed terpenes for 60%+ of strains
- **Effects/Flavors**: Enhance and standardize 80%+ of descriptions  
- **Growing Info**: Complete flowering times for 75%+ of missing data
- **Overall Completeness**: Increase from ~65% to >85% per strain

### Quality Metrics
- **Enhancement Coverage**: 14,075 strains with HTML sources (90.8%)
- **Confidence Threshold**: >0.8 average confidence for extracted data
- **Validation Accuracy**: >90% agreement with existing data where overlap exists
- **New Data Points**: 5,000+ new terpene profiles, 3,000+ missing cannabinoid ranges

---

## Deliverables

1. **Enhanced Dataset**: `Cannabis_Database_Enhanced_Complete.csv` (42+ columns)
2. **Enhancement Report**: Detailed before/after analysis and metrics
3. **Quality Assurance Report**: Confidence scores and validation results
4. **Gap Analysis**: Identification of remaining data gaps
5. **Methodology Documentation**: Complete enhancement process documentation

---

## Success Criteria
- [ ] Process 100% of strains with HTML sources (14,075 records)
- [ ] Achieve >85% overall data completeness per strain
- [ ] Fill >70% of missing THC/CBD ranges
- [ ] Add detailed terpene profiles for >60% of strains
- [ ] Maintain >0.8 average confidence score for enhancements
- [ ] Generate comprehensive enhancement analytics

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

**🌿 Ready to maximize the value of your comprehensive 39-column dataset using 14,075 HTML sources.**
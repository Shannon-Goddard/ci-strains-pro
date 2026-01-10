# Phase 3: Enhanced Analysis Pipeline - HTML to CSV Enhancement

**Date**: January 6, 2026  
**Architect**: Amazon Q  
**Technical Partner**: Shannon Goddard  
**Status**: Ready for Implementation  
**Target Dataset**: `revert_manual_review_cleaning.csv` (39 → 47 columns)

---

## QUICK START NOTES FOR NEW CHAT

### Context Summary
- **HTML Collection**: ✅ COMPLETE - 14,075/15,524 URLs collected (90.7% success)
- **Source of Truth**: ✅ COMPLETE - 14,333 strains flagged with verified HTML sources
- **Current Dataset**: 39 comprehensive columns in `revert_manual_review_cleaning.csv`
- **Mission**: Extract data from 14,075 HTML files to fill gaps + add 8 strategic columns

### Workflow Strategy (Agreed)
1. **Amazon Q**: Fill gaps + add 8 new columns from HTML analysis
2. **Gemini Flash**: Verify and validate all Amazon Q enhancements  
3. **Final AI Pass**: Generate comprehensive `strain_info` column using all structured data

### Key Files
- **HTML Storage**: S3 bucket `ci-strains-html-archive` (14,075 files)
- **Progress DB**: `pipeline/06_html_collection/data/scraping_progress.db`
- **Failed URLs**: `pipeline/07_source_of_truth/urls_no_source_of_truth_summary.csv`
- **Target CSV**: `revert_manual_review_cleaning.csv` (Shannon's manually cleaned dataset)

---

## Mission Statement
Transform 14,075 collected HTML files into structured data enhancements, creating a 47-column cannabis intelligence dataset - the most comprehensive in the industry.

---

## Current Dataset Schema (39 columns)
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

## NEW STRATEGIC COLUMNS TO ADD (8 total)

### 1. **`terpene_profile_structured`** (JSON Text)
**Purpose**: Structured terpene data for advanced analysis
**Format**: `{"myrcene": 0.8, "limonene": 0.6, "pinene": 0.4, "caryophyllene": 0.3}`
**Commercial Value**: Enables terpene-based recommendations and effects prediction

### 2. **`medical_applications`** (Text)
**Purpose**: Specific medical uses extracted from HTML
**Format**: `"Pain relief, Anxiety, Insomnia, Appetite stimulation"`
**Commercial Value**: Critical for medical cannabis market targeting

### 3. **`harvest_window_outdoor`** (Text)
**Purpose**: Outdoor harvest timing for cultivation planning
**Format**: `"Late September to Early October"`
**Commercial Value**: Essential for seasonal marketing and grow planning

### 4. **`clone_availability`** (Boolean)
**Purpose**: Whether strain is available as clones vs seeds only
**Format**: `True/False`
**Commercial Value**: Important product differentiation for growers

### 5. **`data_confidence_score`** (Float 0-1)
**Purpose**: Overall confidence in strain's data completeness and accuracy
**Format**: `0.85` (85% confidence)
**Commercial Value**: Enables tiered product offerings (Premium vs Standard)

### 6. **`dominant_terpene`** (Text)
**Purpose**: Single most prominent terpene for quick categorization
**Format**: `"Myrcene"` or `"Limonene"`
**Commercial Value**: Enables "Myrcene-dominant strains" filtering

### 7. **`cannabinoid_ratio`** (Text)
**Purpose**: Structured THC:CBD ratios for medical users
**Format**: `"20:1 THC:CBD"`, `"1:1 THC:CBD"`, `"High THC"`
**Commercial Value**: Critical for medical categorization

### 8. **`extraction_source_quality`** (Text)
**Purpose**: Rate HTML source quality based on data richness
**Format**: `"Premium"`, `"Standard"`, `"Basic"`
**Commercial Value**: Transparency for data reliability

---

## Phase 3A: HTML Processing Architecture

### S3 HTML Retrieval System
```python
class HTMLProcessor:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
        self.progress_db = 'pipeline/06_html_collection/data/scraping_progress.db'
    
    def get_html_for_strain(self, source_url):
        """Retrieve HTML content for a strain's source URL"""
        # Hash URL to find S3 object
        url_hash = hashlib.sha256(source_url.encode()).hexdigest()[:16]
        
        # Get HTML from S3
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket,
                Key=f'html/{url_hash}.html'
            )
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            return None
```

### Advanced Pattern Recognition
```python
EXTRACTION_PATTERNS = {
    # Enhanced cannabinoid extraction
    'thc_range': r'THC[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
    'cbd_range': r'CBD[:\s]*(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)%',
    'cannabinoid_ratio': r'(\d+):(\d+)\s*(?:THC:CBD|CBD:THC)',
    
    # Detailed terpene extraction
    'terpene_with_percent': r'([A-Za-z]+)[:\s]*(\d+(?:\.\d+)?)%',
    'terpene_dominant': r'[Dd]ominant[:\s]*([A-Za-z]+)',
    
    # Medical applications
    'medical_uses': r'(?:treats?|helps?|relieves?)[:\s]*([^.]+)',
    'conditions': r'(?:anxiety|depression|pain|insomnia|nausea|appetite|ptsd|adhd)',
    
    # Harvest and cultivation
    'harvest_outdoor': r'[Hh]arvest[:\s]*([^.]+(?:September|October|November))',
    'clone_available': r'(?:clone|cutting)s?\s*(?:available|offered)',
    
    # Growing information
    'flowering_weeks': r'[Ff]lowering[:\s]*(\d+)\s*[-–]\s*(\d+)\s*weeks?',
    'difficulty_level': r'[Dd]ifficulty[:\s]*(easy|medium|hard|beginner|intermediate|advanced)',
}
```

---

## Phase 3B: Data Enhancement Engine

### Gap Analysis and Enhancement
```python
class DataEnhancer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.html_processor = HTMLProcessor()
        
    def analyze_current_gaps(self):
        """Analyze missing data in current 39 columns"""
        gap_analysis = {
            'missing_thc_ranges': self.df['thc_min'].isna().sum(),
            'missing_cbd_ranges': self.df['cbd_min'].isna().sum(),
            'missing_effects': self.df['effects'].isna().sum(),
            'missing_flavors': self.df['flavors'].isna().sum(),
            'missing_terpenes': self.df['terpenes'].isna().sum(),
            'missing_flowering': self.df['flowering_day_min'].isna().sum(),
            'missing_yields': self.df['indoor_yield_min_g_per_m'].isna().sum(),
            'strains_with_html': self.df['source_of_truth'].sum(),
            'enhancement_potential': self.df['source_of_truth'].sum()
        }
        return gap_analysis
    
    def enhance_single_strain(self, strain_row):
        """Enhance a single strain with HTML data"""
        if not strain_row['source_of_truth']:
            return self.add_empty_new_columns(strain_row)
        
        # Get HTML content
        html_content = self.html_processor.get_html_for_strain(strain_row['source_url'])
        if not html_content:
            return self.add_empty_new_columns(strain_row)
        
        # Extract all data patterns
        extracted = self.extract_all_patterns(html_content)
        
        # Enhance existing columns
        enhanced_row = self.fill_existing_gaps(strain_row, extracted)
        
        # Add new strategic columns
        enhanced_row = self.add_new_columns(enhanced_row, extracted)
        
        return enhanced_row
```

### New Column Generation Logic
```python
def add_new_columns(self, strain_row, extracted_data):
    """Add the 8 new strategic columns"""
    
    # 1. Terpene Profile Structured
    if extracted_data.get('terpenes'):
        terpene_dict = self.structure_terpenes(extracted_data['terpenes'])
        strain_row['terpene_profile_structured'] = json.dumps(terpene_dict)
        
        # 6. Dominant Terpene
        if terpene_dict:
            strain_row['dominant_terpene'] = max(terpene_dict, key=terpene_dict.get)
    
    # 2. Medical Applications
    if extracted_data.get('medical_uses'):
        strain_row['medical_applications'] = ', '.join(extracted_data['medical_uses'])
    
    # 3. Harvest Window Outdoor
    if extracted_data.get('harvest_timing'):
        strain_row['harvest_window_outdoor'] = extracted_data['harvest_timing']
    
    # 4. Clone Availability
    strain_row['clone_availability'] = extracted_data.get('clone_available', False)
    
    # 7. Cannabinoid Ratio
    if extracted_data.get('thc') and extracted_data.get('cbd'):
        ratio = self.calculate_cannabinoid_ratio(
            extracted_data['thc'], extracted_data['cbd']
        )
        strain_row['cannabinoid_ratio'] = ratio
    
    # 8. Extraction Source Quality
    quality_score = self.assess_source_quality(extracted_data)
    strain_row['extraction_source_quality'] = quality_score
    
    # 5. Data Confidence Score
    confidence = self.calculate_confidence_score(strain_row, extracted_data)
    strain_row['data_confidence_score'] = confidence
    
    return strain_row
```

---

## Phase 3C: Quality Assurance System

### Confidence Scoring Algorithm
```python
def calculate_confidence_score(self, strain_row, extracted_data):
    """Calculate overall data confidence (0-1)"""
    
    confidence_factors = {
        'has_cannabinoids': 0.2 if extracted_data.get('thc') else 0,
        'has_terpenes': 0.15 if extracted_data.get('terpenes') else 0,
        'has_effects': 0.15 if extracted_data.get('effects') else 0,
        'has_growing_info': 0.15 if extracted_data.get('flowering') else 0,
        'source_quality': 0.1 if self.assess_source_quality(extracted_data) == 'Premium' else 0.05,
        'data_consistency': 0.15 if self.check_data_consistency(strain_row, extracted_data) else 0,
        'completeness': 0.1 * self.calculate_completeness_ratio(strain_row)
    }
    
    return sum(confidence_factors.values())

def assess_source_quality(self, extracted_data):
    """Rate HTML source quality"""
    data_points = len([v for v in extracted_data.values() if v])
    
    if data_points >= 8:
        return 'Premium'
    elif data_points >= 5:
        return 'Standard'
    else:
        return 'Basic'
```

---

## Phase 3D: Implementation Pipeline

### Main Enhancement Script
```python
def enhance_complete_dataset():
    """Main pipeline: 39 columns → 47 columns with enhanced data"""
    
    print("🌿 Starting Cannabis Intelligence Enhancement Pipeline")
    
    # Load current dataset
    enhancer = DataEnhancer('revert_manual_review_cleaning.csv')
    df = enhancer.df
    
    print(f"📊 Loaded {len(df)} strains with {len(df.columns)} columns")
    print(f"🎯 Target: {df['source_of_truth'].sum()} strains with HTML sources")
    
    # Analyze current gaps
    gaps = enhancer.analyze_current_gaps()
    print(f"📈 Enhancement potential: {gaps}")
    
    # Process each strain
    enhanced_records = []
    for idx, row in df.iterrows():
        try:
            enhanced_row = enhancer.enhance_single_strain(row)
            enhanced_records.append(enhanced_row)
            
            if idx % 500 == 0:
                print(f"⚡ Processed {idx}/{len(df)} strains...")
                
        except Exception as e:
            print(f"❌ Error processing strain {row['strain_id']}: {e}")
            enhanced_records.append(enhancer.add_empty_new_columns(row))
    
    # Create enhanced dataset
    enhanced_df = pd.DataFrame(enhanced_records)
    
    # Save results
    output_file = 'Cannabis_Database_Enhanced_47_Columns.csv'
    enhanced_df.to_csv(output_file, index=False)
    
    # Generate comprehensive report
    report = generate_enhancement_report(df, enhanced_df)
    
    print(f"✅ Enhancement complete: {output_file}")
    print(f"📊 Final dataset: {len(enhanced_df)} strains, {len(enhanced_df.columns)} columns")
    
    return enhanced_df, report
```

---

## Expected Results

### Data Completeness Improvements
- **THC/CBD Ranges**: Fill 80%+ of missing cannabinoid data
- **Terpene Profiles**: Add structured terpenes for 70%+ of strains with HTML
- **Medical Applications**: Extract medical uses for 60%+ of strains
- **Growing Information**: Complete cultivation details for 75%+ of gaps
- **Overall Completeness**: Increase from ~65% to >90% per strain

### New Intelligence Capabilities
- **Terpene-Based Recommendations**: Enable "Find similar terpene profiles"
- **Medical Targeting**: Precise medical application categorization
- **Cultivation Planning**: Seasonal harvest and growing guidance
- **Quality Tiers**: Premium/Standard/Basic data reliability levels
- **Advanced Filtering**: Cannabinoid ratios, dominant terpenes, clone availability

---

## Post-Enhancement Workflow

### Phase 4: Gemini Flash Validation (Next Step)
```python
# After Amazon Q enhancement, run Gemini validation
def prepare_for_gemini_validation(enhanced_df):
    """Prepare enhanced dataset for Gemini Flash validation"""
    
    # Create validation prompts for each new column
    validation_tasks = {
        'terpene_profile_structured': 'Validate terpene data accuracy',
        'medical_applications': 'Verify medical use claims',
        'cannabinoid_ratio': 'Confirm THC:CBD ratio calculations',
        'data_confidence_score': 'Assess confidence score accuracy'
    }
    
    # Generate Gemini validation dataset
    return create_gemini_validation_batch(enhanced_df, validation_tasks)
```

### Phase 5: Final Info Column Generation
```python
# After Gemini validation, generate comprehensive strain_info
def generate_strain_info_column(validated_df):
    """Create comprehensive strain_info using all 47 columns"""
    
    # Use all structured data to create rich strain descriptions
    # This will be the final step to create the ultimate dataset
    pass
```

---

## Success Criteria
- [ ] Process 100% of strains with HTML sources (14,333 records)
- [ ] Add 8 new strategic columns with >80% data coverage
- [ ] Achieve >90% overall data completeness per strain
- [ ] Generate >0.85 average confidence score
- [ ] Create most comprehensive cannabis dataset in industry
- [ ] Prepare clean handoff to Gemini Flash validation

---

## Deliverables
1. **Enhanced Dataset**: `Cannabis_Database_Enhanced_47_Columns.csv`
2. **Enhancement Report**: Detailed before/after analytics
3. **Quality Metrics**: Confidence scores and validation data
4. **Gemini Prep**: Validation-ready dataset for next phase
5. **Complete Documentation**: Methodology and process docs

---

**🎯 NEXT CHAT STARTUP COMMAND:**
```
"Start Phase 3 HTML enhancement pipeline on revert_manual_review_cleaning.csv - add 8 strategic columns and fill gaps using 14,075 HTML files from S3"
```

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

**🌿 Ready to create the most comprehensive cannabis intelligence dataset available - 47 columns of structured perfection.**
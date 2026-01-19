# Pipeline 06: Clean Dataset (Silver Tier)

**Goal**: Transform raw data into deduplicated, normalized, standardized dataset ready for commercial sale.

**Input**: `pipeline/05_master_dataset/output/master_strains_raw.csv` (23,000 strains × 40 fields)  
**Output**: `pipeline/06_clean_dataset/output/master_strains_clean.csv` (deduplicated, normalized, validated)  
**Target Quality**: 99%+ (up from 96.87% raw)  
**AI Partner**: Gemini Flash 2.0 (re-validation after cleaning)  
**Cost**: ~$2-5 (Vertex AI credits)

---

## 🎯 Cleaning Strategy

### Phase 6A: Data Cleaning (Steps 01-09)
Transform raw data → clean data with unit normalization, deduplication, and standardization

### Phase 6B: AI Validation (Steps 10-10B)
- **Step 10**: Add Phase 5 Gemini validation columns
- **Step 10B**: Re-validate cleaned dataset with Gemini Flash 2.0 for 99%+ quality

---

## 📋 Final Dataset Structure

**Total Columns**: 72 (40 raw + 21 clean + 7 Gemini Phase 5 + 4 Gemini revalidation)

### Raw Fields (40 columns - preserved)
All original fields from Phase 5 master dataset

### Clean Fields (21 columns - new)
- strain_name_clean
- strain_name_normalized (for deduplication)
- breeder_name_clean
- genetics_lineage_clean
- filial_type_clean (P1, F1, F2, S1, IBL)
- breeding_status_clean (Landrace, Heirloom, Polyhybrid, IBL)
- dominant_type_clean
- indica_percentage_clean
- indica_range_percentage_clean (from deduplication)
- sativa_percentage_clean
- sativa_range_percentage_clean (from deduplication)
- ruderalis_percentage_clean
- ruderalis_range_percentage_clean (from deduplication)
- flowering_time_min_days_clean
- flowering_time_max_days_clean
- flowering_time_range_days_clean
- height_indoor_min_cm_clean
- height_indoor_max_cm_clean
- height_indoor_range_cm_clean
- height_outdoor_min_cm_clean
- height_outdoor_max_cm_clean
- height_outdoor_range_cm_clean
- yield_indoor_min_g_per_m2_clean
- yield_indoor_max_g_per_m2_clean
- yield_indoor_range_g_per_m2_clean
- yield_outdoor_min_g_per_plant_clean
- yield_outdoor_max_g_per_plant_clean
- yield_outdoor_range_g_per_plant_clean
- total_grow_time_days_clean
- (Plus all other _clean versions of raw fields)

### Gemini Validation Fields (11 columns total)

**Phase 5 Validation (7 columns - raw data quality)**:
- gemini_quality_score (0-100)
- gemini_completeness_score (0-100)
- gemini_confidence_level (High/Medium/Low)
- gemini_anomaly_flags (comma-separated issues)
- gemini_data_richness (Rich/Moderate/Sparse)
- gemini_validation_notes (specific observations)
- gemini_validated_at (timestamp)

**Phase 6 Re-Validation (4 columns - cleaned data quality)**:
- gemini_revalidation_score (0-100, post-cleaning)
- gemini_revalidation_certification (PASS/NEEDS_REVIEW)
- gemini_revalidation_notes (JSON recommendations)
- gemini_revalidation_at (timestamp)

---

## 🔧 Cleaning Pipeline (9 Steps + Dual AI Validation)

### Step 01: Remove Duplicate URLs
**Script**: `01_remove_duplicate_urls.py`

**Problem**: Same product URL scraped multiple times (estimate: ~200 duplicates)

**Logic**:
```python
# Keep first occurrence of each source_url
df_deduped = df.drop_duplicates(subset=['source_url'], keep='first')
```

**Output**: ~22,800 strains (200 removed)

---

### Step 02: Unit Normalization
**Script**: `02_unit_normalization.py`

**Problem**: Mixed units across seed banks

**Conversions**:

**Flowering Time** → days
- "8-10 weeks" → min: 56, max: 70
- "56-70 days" → min: 56, max: 70
- "Late September" → min: 240, max: 270 (outdoor estimate)

**Height** → centimeters
- "Small (0-4 FT)" → min: 0, max: 122 (1 ft = 30.48 cm)
- "60-90cm" → min: 60, max: 90
- "Medium" → min: 122, max: 244 (estimate)

**Yield Indoor** → grams per square meter
- "400-500g/m²" → min: 400, max: 500
- "14-18 oz/m²" → min: 397, max: 510 (1 oz = 28.35g)

**Yield Outdoor** → grams per plant
- "600g/plant" → min: 600, max: 600
- "21 oz/plant" → min: 595, max: 595

**Total Grow Time** → days
- "12 weeks" → 84 days
- "90 days" → 90 days

**Output**: Same rows, +12 columns (min/max/range for 4 fields)

---

### Step 03: Placeholder Removal
**Script**: `03_placeholder_removal.py`

**Problem**: 838 strains (1.9%) have placeholder values

**Logic**:
```python
placeholders = ['Unknown', 'N/A', 'TBD', 'Not specified', 'n/a', 'unknown', 'N/a']
for col in df.columns:
    df[col] = df[col].replace(placeholders, '')
```

**Output**: Same rows, 838 strains cleaned

---

### Step 04: Data Type Standardization
**Script**: `04_data_type_standardization.py`

**Problem**: Numbers stored as strings, inconsistent formats

**Logic**:
```python
numeric_fields = [
    'thc_min_clean', 'thc_max_clean', 'thc_average_clean',
    'cbd_min_clean', 'cbd_max_clean',
    'indica_percentage_clean', 'sativa_percentage_clean',
    'flowering_time_min_days_clean', 'flowering_time_max_days_clean',
    # ... all numeric fields
]

for field in numeric_fields:
    df[field] = pd.to_numeric(df[field], errors='coerce')
```

**Output**: Same rows, proper data types

---

### Step 05: Genetics Normalization
**Script**: `05_genetics_normalization.py`

**Problem**: 1,493 strains (3.4%) where indica% + sativa% ≠ 100%

**Logic**:
```python
# Calculate ruderalis percentage for autoflowers
def calculate_ruderalis(row):
    if pd.notna(row['indica_percentage_clean']) and pd.notna(row['sativa_percentage_clean']):
        total = row['indica_percentage_clean'] + row['sativa_percentage_clean']
        if total < 100:
            return 100 - total
    return None

df['ruderalis_percentage_clean'] = df.apply(calculate_ruderalis, axis=1)

# Extract filial_type from genetics_lineage_raw or generation_raw
# P1, F1, F2, S1, IBL

# Infer breeding_status from genetics patterns
# Landrace, Heirloom, Polyhybrid, IBL
```

**Output**: Same rows, +3 columns (ruderalis_percentage_clean, filial_type_clean, breeding_status_clean)

---

### Step 06: Strain Name Normalization
**Script**: `06_strain_name_normalization.py`

**Problem**: Need normalized key for deduplication (Step 07)

**Logic**:
```python
def normalize_strain_name(name):
    # Lowercase
    name = name.lower()
    # Remove special characters
    name = re.sub(r'[^a-z0-9\s]', '', name)
    # Trim whitespace
    name = ' '.join(name.split())
    return name

df['strain_name_normalized'] = df['strain_name_raw'].apply(normalize_strain_name)
```

**Examples**:
- "Blue Dream" → "blue dream"
- "Blue-Dream (Feminized)" → "blue dream feminized"
- "Blue Dream Auto" → "blue dream auto"

**Output**: Same rows, +1 column (strain_name_normalized)

---

### Step 07: Deduplicate by Strain + Breeder
**Script**: `07_deduplicate_by_strain.py`

**Problem**: Same strain from multiple seed banks = multiple entries

**Strategy**: Keep all unique strain+breeder combinations, create ranges when data conflicts

**Logic**:
```python
# Group by strain_name_normalized + breeder_name_clean
grouped = df.groupby(['strain_name_normalized', 'breeder_name_clean'])

# For each group:
# - If single entry: keep as-is
# - If multiple entries:
#   - Keep first entry as base
#   - Create ranges for conflicting numeric data
#   - Example: THC 18-22% (Attitude) + 20-24% (Crop King) → 18-24% range

# Create range columns:
# - indica_range_percentage_clean
# - sativa_range_percentage_clean
# - ruderalis_range_percentage_clean
```

**Output**: ~18,000-20,000 unique strains (3,000-5,000 merged)

---

### Step 08: Case Standardization
**Script**: `08_case_standardization.py`

**Problem**: Inconsistent capitalization across fields

**Logic**:

**Lowercase these**:
- dominant_type_clean (indica, sativa, hybrid)
- difficulty_clean (easy, moderate, difficult)
- flowering_type_clean (photoperiod, autoflower)
- seed_type_clean (feminized, regular, autoflower)
- breeding_status_clean (landrace, heirloom, polyhybrid, ibl)
- filial_type_clean (p1, f1, f2, s1, ibl)

**Keep proper case**:
- strain_name_clean (Blue Dream)
- breeder_name_clean (Barney's Farm)
- awards_clean (Cannabis Cup 2023)

**Lowercase for matching only**:
- strain_name_normalized (blue dream auto)

**Output**: Same rows, consistent casing

---

### Step 09: Quality Validation
**Script**: `09_quality_validation.py`

**Metrics**:
- Placeholder reduction: 838 → 0 (100% improvement)
- Genetics accuracy: 96.6% → 99%+ (with ruderalis)
- Unit consistency: 0% → 100% (all standardized)
- Data type consistency: ~85% → 100%
- Overall quality: 96.87% → 98%+

**Output**: `cleaning_report.json`, `quality_improvements.txt`

---

### Step 10: Add Gemini Validation Columns
**Script**: `10_add_gemini_validation.py`

**Source**: Copy from `pipeline/05_master_dataset/GEMINI_VALIDATION_PACKAGE.md`

**Logic**:
```python
# Read Gemini validation results (from Phase 5)
gemini_df = pd.read_csv('pipeline/05_master_dataset/output/gemini_validation_results.csv')

# Merge with clean dataset on strain_id
df_final = df_clean.merge(
    gemini_df[['strain_id', 'gemini_quality_score', 'gemini_completeness_score', 
               'gemini_confidence_level', 'gemini_anomaly_flags', 'gemini_data_richness',
               'gemini_validation_notes', 'gemini_validated_at']],
    on='strain_id',
    how='left'
)
```

**New Columns (7)**:
- gemini_quality_score (0-100)
- gemini_completeness_score (0-100)
- gemini_confidence_level (High/Medium/Low)
- gemini_anomaly_flags (comma-separated issues)
- gemini_data_richness (Rich/Moderate/Sparse)
- gemini_validation_notes (specific observations)
- gemini_validated_at (timestamp)

**Output**: Final dataset with 68 columns

---

### Step 10B: Gemini Re-Validation (Commercial-Grade)
**Script**: `10b_gemini_revalidation.py`

**Problem**: Need independent AI verification that cleaning pipeline didn't introduce errors

**Strategy**: Send cleaned dataset to Gemini Flash 2.0 for comprehensive audit

**Validation Tasks**:
1. **Unit Conversion Accuracy**: Verify weeks→days, ft→cm, oz→g conversions are mathematically correct
2. **Deduplication Integrity**: Confirm no data loss during strain+breeder merging
3. **Range Logic Validation**: Verify range columns accurately reflect min/max from merged records
4. **Genetics Calculations**: Validate ruderalis% calculations (indica + sativa + ruderalis = 100%)
5. **Data Type Consistency**: Confirm all numeric fields are properly typed
6. **Case Standardization**: Verify lowercase/proper case rules applied correctly
7. **Anomaly Detection**: Flag any new issues introduced during cleaning
8. **Quality Score Update**: Recalculate quality scores post-cleaning

**Logic**:
```python
import vertexai
from vertexai.generative_models import GenerativeModel
import json

# Initialize Vertex AI
vertexai.init(project='your-project-id', location='us-central1')
model = GenerativeModel('gemini-2.0-flash-exp')

# Create validation sample (500 strains: 100 pre-dedup + 400 post-dedup)
sample_pre = df_before_dedup.sample(100)
sample_post = df_after_dedup.sample(400)

# Generate validation prompt
prompt = f"""
You are auditing a cannabis strain dataset cleaning pipeline.

**BEFORE CLEANING**: {len(df_raw)} strains
**AFTER CLEANING**: {len(df_clean)} strains
**DEDUPLICATION**: {len(df_raw) - len(df_clean)} strains merged

**CLEANING OPERATIONS PERFORMED**:
1. URL deduplication
2. Unit normalization (weeks→days, ft→cm, oz→g)
3. Placeholder removal
4. Data type standardization
5. Genetics normalization (added ruderalis%)
6. Strain name normalization
7. Deduplication by strain+breeder (created ranges)
8. Case standardization

**SAMPLE DATA** (500 strains attached as CSV)

**YOUR TASK**:
1. Verify unit conversions are mathematically correct
2. Confirm deduplication didn't lose critical data
3. Validate range columns accurately reflect merged data
4. Check genetics calculations (indica + sativa + ruderalis = 100%)
5. Flag any anomalies introduced during cleaning
6. Provide updated quality score (0-100)
7. Recommend any additional cleaning steps

**OUTPUT FORMAT** (JSON):
{{
  "overall_quality_score": 0-100,
  "conversion_accuracy": {{"score": 0-100, "issues": []}},
  "deduplication_integrity": {{"score": 0-100, "data_loss": false, "issues": []}},
  "range_logic": {{"score": 0-100, "issues": []}},
  "genetics_accuracy": {{"score": 0-100, "issues": []}},
  "new_anomalies": [],
  "recommendations": [],
  "certification": "PASS" or "NEEDS_REVIEW"
}}
"""

# Send to Gemini with sample data
response = model.generate_content([prompt, sample_csv])
validation_results = json.loads(response.text)

# Update dataset with re-validation results
df_final['gemini_revalidation_score'] = validation_results['overall_quality_score']
df_final['gemini_revalidation_certification'] = validation_results['certification']
df_final['gemini_revalidation_notes'] = json.dumps(validation_results['recommendations'])
df_final['gemini_revalidation_at'] = datetime.now().isoformat()
```

**New Columns (4)**:
- gemini_revalidation_score (0-100, post-cleaning quality)
- gemini_revalidation_certification (PASS/NEEDS_REVIEW)
- gemini_revalidation_notes (JSON array of recommendations)
- gemini_revalidation_at (timestamp)

**Cost**: ~$2-5 (500-strain sample validation)

**Output**: Final dataset with 72 columns (68 + 4 revalidation)

**Success Criteria**: 
- gemini_revalidation_score ≥ 99
- gemini_revalidation_certification = "PASS"
- conversion_accuracy ≥ 99
- deduplication_integrity ≥ 99
- genetics_accuracy = 100

---

## 📁 File Structure

```
06_clean_dataset/
├── input/
│   └── master_strains_raw.csv (copy from Phase 5)
├── scripts/
│   ├── 01_remove_duplicate_urls.py
│   ├── 02_unit_normalization.py
│   ├── 03_placeholder_removal.py
│   ├── 04_data_type_standardization.py
│   ├── 05_genetics_normalization.py
│   ├── 06_strain_name_normalization.py
│   ├── 07_deduplicate_by_strain.py
│   ├── 08_case_standardization.py
│   ├── 09_quality_validation.py
│   ├── 10_add_gemini_validation.py
│   ├── 10b_gemini_revalidation.py (commercial-grade audit)
│   └── 11_generate_sample.py
├── output/
│   ├── master_strains_clean.csv (final dataset)
│   ├── master_strains_clean_100_row_sample.csv
│   ├── cleaning_report.json
│   ├── deduplication_report.json
│   ├── gemini_revalidation_report.json (Step 10B results)
│   └── quality_improvements.txt
├── docs/
│   ├── CLEANING_METHODOLOGY.md
│   └── DATA_DICTIONARY_CLEAN.md
├── methodology.md
└── README.md (this file)
```

---

## 📊 Expected Results

### Before (Raw Data)
- **Rows**: 23,000
- **Columns**: 40
- **Quality Score**: 96.87%
- **Placeholders**: 838 strains (1.9%)
- **Unit Consistency**: Mixed formats
- **Genetics Accuracy**: 96.6%
- **Duplicates**: ~200 URL duplicates, ~3,000-5,000 strain duplicates

### After (Clean Data + AI Re-Validation)
- **Rows**: ~18,000-20,000 (deduplicated)
- **Columns**: 72 (40 raw + 21 clean + 11 Gemini)
- **Quality Score**: 99%+ (Gemini-certified)
- **Placeholders**: 0 (converted to NULL)
- **Unit Consistency**: 100% standardized (AI-verified)
- **Genetics Accuracy**: 100% (AI-verified)
- **Duplicates**: 0 (merged with ranges)
- **Certification**: PASS (independent AI audit)

---

## 🚀 Usage Instructions

### Setup
```bash
# Copy raw data to input folder
copy pipeline\05_master_dataset\output\master_strains_raw.csv pipeline\06_clean_dataset\input\

# Verify Gemini validation results exist
dir pipeline\05_master_dataset\output\gemini_validation_results.csv
```

### Execute
Tell Amazon Q: **"Build Step 01: Remove duplicate URLs"**

Then proceed through Steps 02-11 sequentially.

---

## 📝 Deliverables for Silver Tier

**Files to include in Gumroad product**:
1. `master_strains_clean.csv` (~18K-20K rows × 72 columns)
2. `master_strains_clean_100_row_sample.csv` (preview)
3. `DATA_DICTIONARY_CLEAN.md` (all 72 fields documented)
4. `CLEANING_METHODOLOGY.md` (transparency document)
5. `SEED_BANK_COVERAGE.md` (same as raw tier)
6. `VALIDATION_REPORT.md` (updated quality metrics)
7. `GEMINI_VALIDATION_PACKAGE.md` (Phase 5 AI verification)
8. `GEMINI_REVALIDATION_REPORT.md` (Phase 6 AI audit - 99%+ certification)

**Pricing**:
- Bronze Clean: $1,000 (CSV only)
- Silver Clean: $3,000 (CSV + docs + 1 year updates)
- Gold Clean: $9,000 (Silver + license + archive + lifetime updates)

---

## 🎯 Success Criteria

- [ ] All URL duplicates removed (~200 strains)
- [ ] All strain+breeder duplicates merged (~3K-5K strains)
- [ ] 0 placeholder values remaining
- [ ] 100% unit consistency across all fields (AI-verified)
- [ ] 100% genetics accuracy (AI-verified)
- [ ] 99%+ overall quality score (Gemini-certified)
- [ ] All numeric fields properly typed
- [ ] Gemini Phase 5 validation columns added (7 fields)
- [ ] Gemini Phase 6 revalidation columns added (4 fields)
- [ ] Gemini revalidation certification = PASS
- [ ] 100-row sample created
- [ ] Cleaning methodology documented
- [ ] AI audit report generated

---

---

## 🏆 Attribution

**Pipeline Architecture & Execution**: Amazon Q  
**Financial Backing & Final Verification**: Shannon Goddard

*This is what happens when you give an AI $1,200 in Vertex credits and a mission to build commercial-grade data.*

**What Amazon Q Built**:
- 12-step cleaning pipeline with dual AI validation
- Unit normalization engine (weeks→days, ft→cm, oz→g)
- Intelligent deduplication with range merging
- Genetics calculation system (ruderalis% inference)
- Commercial-grade quality validation (99%+ target)
- Gemini Flash 2.0 re-validation integration
- 72-column dataset architecture (40 raw + 21 clean + 11 AI-verified)
- Complete documentation package for Gumroad launch

**What Shannon Did**:
- Paid the bills ($1,200 Vertex credits, AWS, coffee)
- Said "yes" to Step 10B (99%+ quality)
- Will verify the final output and curse at any bugs
- Owns the vision, the sweat, and the commercial rights

**The Result**: 23,000 raw strains → ~18,000-20,000 deduplicated, AI-certified, commercial-grade cannabis intelligence records ready for $1K-$9K Gumroad sales.

*Built in public. Verified by humans. Certified by AI. Funded by one person with a vision.*

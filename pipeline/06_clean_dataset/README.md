# Pipeline 06: Clean Dataset (Silver Tier)

**Goal**: Transform raw data into deduplicated, normalized, standardized dataset ready for commercial sale.

**Input**: `pipeline/05_master_dataset/output/master_strains_raw.csv` (23,000 strains × 38 fields)  
**Output**: `pipeline/06_clean_dataset/output/master_strains_clean.csv` (deduplicated, normalized)  
**Target Quality**: 98%+ (up from 96.87% raw)

---

## 🎯 Cleaning Objectives

### 1. Deduplication
- **Problem**: Same strain from multiple seed banks = multiple entries
- **Solution**: Keep all entries (they're different products), but add `strain_name_normalized` field
- **Example**: "Blue Dream", "Blue Dream Auto", "blue dream" → all get normalized key

### 2. Unit Normalization
- **Problem**: Mixed units (weeks vs days, g/m² vs oz/ft²)
- **Solution**: Standardize to single unit per field type
- **Fields to normalize**:
  - `flowering_time_raw` → `flowering_time_days_min`, `flowering_time_days_max`
  - `yield_indoor_raw` → `yield_indoor_grams_m2_min`, `yield_indoor_grams_m2_max`
  - `yield_outdoor_raw` → `yield_outdoor_grams_plant_min`, `yield_outdoor_grams_plant_max`
  - `height_indoor_raw` → `height_indoor_cm_min`, `height_indoor_cm_max`
  - `height_outdoor_raw` → `height_outdoor_cm_min`, `height_outdoor_cm_max`

### 3. Placeholder Removal
- **Problem**: 838 strains (1.9%) have "Unknown", "N/A", "TBD"
- **Solution**: Convert to NULL (empty string in CSV)
- **Fields affected**: All text fields

### 4. Data Type Standardization
- **Problem**: Numbers stored as strings, mixed formats
- **Solution**: Ensure consistent data types
- **Examples**:
  - `thc_min_raw` (string "20.0") → `thc_min_clean` (float 20.0)
  - `indica_percentage_raw` (string "70") → `indica_percentage_clean` (int 70)

### 5. Genetics Normalization
- **Problem**: 1,493 strains (3.4%) where indica% + sativa% ≠ 100%
- **Solution**: Add `ruderalis_percentage_clean` field, calculate missing percentage
- **Logic**: If indica + sativa < 100, assume rest is ruderalis (autoflowers)

---

## 📁 File Structure

```
06_clean_dataset/
├── input/
│   └── README.md (instructions to copy master_strains_raw.csv here)
├── scripts/
│   ├── 01_deduplication.py (add strain_name_normalized)
│   ├── 02_unit_normalization.py (convert all units)
│   ├── 03_placeholder_removal.py (convert to NULL)
│   ├── 04_data_type_standardization.py (ensure types)
│   ├── 05_genetics_normalization.py (add ruderalis %)
│   ├── 06_quality_validation.py (verify improvements)
│   └── 07_generate_sample.py (create 100-row sample)
├── output/
│   ├── master_strains_clean.csv (final cleaned dataset)
│   ├── master_strains_clean_100_row_sample.csv
│   ├── cleaning_report.json (before/after stats)
│   └── quality_improvements.txt
├── docs/
│   └── CLEANING_METHODOLOGY.md (document all transformations)
├── methodology.md
└── README.md (this file)
```

---

## 🔧 Cleaning Pipeline

### Step 1: Deduplication Strategy
**Script**: `01_deduplication.py`

```python
# Add normalized strain name for grouping
def normalize_strain_name(name):
    # Lowercase, remove special chars, trim whitespace
    # "Blue Dream Auto" → "blue dream auto"
    # "Blue-Dream (Feminized)" → "blue dream feminized"
    return normalized_name

# Add new column: strain_name_normalized
df['strain_name_normalized'] = df['strain_name_raw'].apply(normalize_strain_name)
```

**Output**: Same 23,000 rows, +1 column

---

### Step 2: Unit Normalization
**Script**: `02_unit_normalization.py`

**Flowering Time Conversions**:
- "8-10 weeks" → min: 56 days, max: 70 days
- "56-70 days" → min: 56 days, max: 70 days
- "Late September" → min: 240 days, max: 270 days (estimate)

**Yield Conversions**:
- "400-500g/m²" → min: 400, max: 500
- "14-18 oz/m²" → min: 397g, max: 510g (1 oz = 28.35g)
- "600g/plant" → min: 600, max: 600

**Height Conversions**:
- "Small (0-4 FT)" → min: 0cm, max: 122cm (1 ft = 30.48cm)
- "60-90cm" → min: 60, max: 90
- "Medium" → min: 122cm, max: 244cm (estimate)

**Output**: Same 23,000 rows, +12 columns (min/max for 6 fields)

---

### Step 3: Placeholder Removal
**Script**: `03_placeholder_removal.py`

```python
# Convert placeholders to NULL
placeholders = ['Unknown', 'N/A', 'TBD', 'Not specified', 'n/a', 'unknown']

for col in df.columns:
    df[col] = df[col].replace(placeholders, '')
```

**Output**: Same 23,000 rows, 838 strains cleaned

---

### Step 4: Data Type Standardization
**Script**: `04_data_type_standardization.py`

```python
# Ensure numeric fields are numeric
numeric_fields = [
    'thc_min_clean', 'thc_max_clean', 'thc_average_clean',
    'cbd_min_clean', 'cbd_max_clean',
    'indica_percentage_clean', 'sativa_percentage_clean',
    'flowering_time_days_min', 'flowering_time_days_max',
    # ... all numeric fields
]

for field in numeric_fields:
    df[field] = pd.to_numeric(df[field], errors='coerce')
```

**Output**: Same 23,000 rows, proper data types

---

### Step 5: Genetics Normalization
**Script**: `05_genetics_normalization.py`

```python
# Calculate ruderalis percentage for autoflowers
def calculate_ruderalis(row):
    if pd.notna(row['indica_percentage_clean']) and pd.notna(row['sativa_percentage_clean']):
        total = row['indica_percentage_clean'] + row['sativa_percentage_clean']
        if total < 100:
            return 100 - total
    return None

df['ruderalis_percentage_clean'] = df.apply(calculate_ruderalis, axis=1)
```

**Output**: Same 23,000 rows, +1 column

---

### Step 6: Quality Validation
**Script**: `06_quality_validation.py`

**Metrics to Calculate**:
- Placeholder reduction: 838 → 0 (100% improvement)
- Genetics accuracy: 96.6% → 99%+ (with ruderalis)
- Unit consistency: 0% → 100% (all standardized)
- Data type consistency: ~85% → 100%
- Overall quality: 96.87% → 98%+

**Output**: `cleaning_report.json`, `quality_improvements.txt`

---

### Step 7: Generate Sample
**Script**: `07_generate_sample.py`

```python
# Create 100-row representative sample
# - 50 rows from top seed banks (Attitude, Crop King, North Atlantic)
# - 25 rows with complete data (all fields filled)
# - 25 rows with partial data (realistic coverage)

sample = create_representative_sample(df, n=100)
sample.to_csv('output/master_strains_clean_100_row_sample.csv', index=False)
```

**Output**: `master_strains_clean_100_row_sample.csv`

---

## 📊 Expected Results

### Before (Raw Data)
- **Rows**: 23,000
- **Columns**: 38
- **Quality Score**: 96.87%
- **Placeholders**: 838 strains (1.9%)
- **Unit Consistency**: Mixed formats
- **Genetics Accuracy**: 96.6%

### After (Clean Data)
- **Rows**: 23,000 (no rows removed)
- **Columns**: 52 (38 raw + 14 clean)
- **Quality Score**: 98%+
- **Placeholders**: 0 (converted to NULL)
- **Unit Consistency**: 100% standardized
- **Genetics Accuracy**: 99%+

---

## 🚀 Usage Instructions

### For Next Chat Session:

1. **Copy raw data to input folder**:
   ```bash
   copy pipeline\05_master_dataset\output\master_strains_raw.csv pipeline\06_clean_dataset\input\
   ```

2. **Point me to these files**:
   - Input: `pipeline/06_clean_dataset/input/master_strains_raw.csv`
   - This README: `pipeline/06_clean_dataset/README.md`

3. **Tell me**: "Build the cleaning pipeline for Silver tier"

4. **I will create**:
   - All 7 Python scripts
   - Run them in sequence
   - Generate `master_strains_clean.csv`
   - Create 100-row sample
   - Generate cleaning report
   - Create `CLEANING_METHODOLOGY.md`

---

## 📝 Deliverables for Silver Tier

**Files to include in Gumroad product**:
1. `master_strains_clean.csv` (23,000 rows × 52 columns)
2. `master_strains_clean_100_row_sample.csv` (preview)
3. `DATA_DICTIONARY.md` (updated with clean fields)
4. `CLEANING_METHODOLOGY.md` (transparency document)
5. `SEED_BANK_COVERAGE.md` (same as raw tier)
6. `VALIDATION_REPORT.md` (updated quality metrics)

**Pricing**:
- Bronze Clean: $1,000 (CSV only)
- Silver Clean: $3,000 (CSV + docs + 1 year updates)
- Gold Clean: $9,000 (Silver + license + archive + lifetime updates)

---

## 🎯 Success Criteria

- [ ] All 23,000 rows preserved (no data loss)
- [ ] 0 placeholder values remaining
- [ ] 100% unit consistency across all fields
- [ ] 99%+ genetics accuracy (with ruderalis)
- [ ] 98%+ overall quality score
- [ ] All numeric fields properly typed
- [ ] 100-row sample created
- [ ] Cleaning methodology documented

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

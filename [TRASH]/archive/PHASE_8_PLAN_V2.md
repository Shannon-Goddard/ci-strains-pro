# Phase 8: Strain Name Extraction (Per-Seed-Bank Approach)

**Status**: 🚧 IN PROGRESS  
**Goal**: Extract clean strain names from URLs using seed-bank-specific logic  
**Approach**: One script per seed bank (same as Phase 6 breeders)  
**Estimated Time**: 3-4 hours  

---

## Why Per-Seed-Bank Scripts?

**Lesson from Phase 6**: Each seed bank has unique URL patterns. A unified script with if/else logic becomes unmaintainable.

**Benefits**:
- ✅ Clean, focused logic per seed bank
- ✅ Easy to test and debug individually
- ✅ Can run in parallel
- ✅ Easy to add new seed banks later
- ✅ Clear documentation of each bank's pattern

---

## Seed Bank URL Patterns (Discovered)

### Attitude (7,673 strains)
**Pattern**: `{breeder}-{seeds|genetics|seedbank|farm}-{strain-name}/prod_####`  
**Example**: `auto-seeds-auto-1/prod_1705` → "Auto 1"  
**Logic**: Split on separator, take everything after it

### North Atlantic (2,726 strains)
**Pattern**: `/product/{strain-name}-{auto|fem}/`  
**Example**: `auto-1-auto` → "Auto 1"  
**Logic**: Remove seed type suffix at END only

### Amsterdam (163 strains)
**Pattern**: `/{strain-name}-{autoflower|feminized}-seeds/`  
**Example**: `green-crack-autoflower-seeds` → "Green Crack"  
**Logic**: Remove seed type keywords

### Other Banks (TBD)
- Crop King (3,336)
- Gorilla (2,000)
- Neptune (1,995)
- Seedsman JS (866)
- Herbies (753)
- Sensi Seeds (620)
- Multiverse Beans (528)
- Seed Supreme (350)
- Mephisto Genetics (245)
- Exotic Genetix (227)
- ILGM JS (133)
- Dutch Passion (119)
- Barney's Farm (88)
- Royal Queen Seeds (67)
- Seeds Here Now (39)
- Great Lakes (16)

---

## Workflow

### Step 1: Shannon Documents URL Patterns
**File**: `docs/URL_PATTERNS.md`  
**Task**: For each seed bank, document:
- 3-5 sample URLs
- URL structure pattern
- Expected strain name extraction

### Step 2: Amazon Q Builds Extraction Scripts
**Files**: `scripts/extract_{seedbank}.py` (19 scripts)  
**Each script**:
- Reads Phase 7 output CSV
- Filters to specific seed bank
- Extracts strain name from URL using bank-specific logic
- Removes breeder names (using Phase 6 variations list)
- Extracts metadata (generation, phenotype)
- Creates base name for deduplication
- Outputs: `output/{seedbank}_strain_names.csv`

### Step 3: Merge All Extractions
**File**: `scripts/merge_all_strains.py`  
**Output**: `output/all_strain_names_extracted.csv`

### Step 4: Standardization
**File**: `scripts/standardize_strain_names.py`  
**Output**: `output/all_strain_names_cleaned.csv`

### Step 5: Generate Lists
**File**: `scripts/generate_strain_list.py`  
**Outputs**: 
- `STRAIN_LIST.md` (A-Z, raw)
- `STRAIN_LIST_CLEANED.md` (A-Z, standardized)

---

## Output Columns

Each extraction script produces:
- `strain_id` (from input)
- `seed_bank` (from input)
- `source_url_raw` (from input)
- `url_slug` (extracted slug)
- `strain_name_extracted` (clean name from URL)
- `strain_name_base` (for deduplication)
- `generation_extracted` (F1, BX, S1, etc.)
- `phenotype_marker_extracted` (#4, Cut A, etc.)

---

## Success Criteria

- ✅ 100% extraction rate per seed bank
- ✅ No breeder names in extracted names
- ✅ No seed type keywords in extracted names
- ✅ Generation markers preserved
- ✅ Phenotype markers preserved
- ✅ "Auto" preserved when part of strain name (Auto 1, Auto Blueberry)
- ✅ Famous numbered strains intact (GG#4, Gelato #33)

---

## Next Steps

1. **Shannon**: Complete `docs/URL_PATTERNS.md` with all 19 seed banks
2. **Amazon Q**: Build extraction scripts based on patterns
3. **Both**: Test each script individually (100% success rate)
4. **Amazon Q**: Merge, standardize, generate lists
5. **Shannon**: Manual review of A-Z list

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

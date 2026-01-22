# Phase 1 Extended Cleaning Results (Steps 10E-10F)

**Date:** January 18, 2026  
**Logic designed by Amazon Q, verified by Shannon Goddard.**

## Overview
Extended Phase 1 cleaning based on Shannon's breeder extraction QA findings. Standardizes breeder names and removes non-cannabis products.

---

## Step 10E: Breeder Name Standardization

**Input:** 21,360 rows  
**Output:** 21,360 rows  
**Operations:** 13,365 breeder names standardized

### Standardization Categories

#### 1. Suffix Removals (11 breeders)
- "G13 Labs Seeds" → "G13 Labs"
- "Rare Dankness Seeds" → "Rare Dankness"
- "TH Seeds Seeds" → "TH Seeds" (duplicate "Seeds")
- "Feminised Seeds Company" → "Feminised Seeds"
- "Green Bodhi Seeds" → "Green Bodhi"
- "LIT Farms Seeds" → "LIT Farms"
- "Lovin' In Her Eyes Seeds" → "Lovin' In Her Eyes"
- "Massive Creations Seeds" → "Massive Creations"
- "Offensive Selections Seeds" → "Offensive Selections"
- "Seedsman Seeds" → "Seedsman"
- "SuperCBDx Seeds" → "SuperCBDx"

#### 2. Suffix Additions (2 breeders)
- "Geist Grow" → "Geist Grow Genetics"
- "Grandiflora" → "Grandiflora Genetics"

#### 3. Name Variations (20 breeders)
- "Greenhouse - Strain Hunters" → "Greenhouse Seed Co."
- "GrowersChoice" → "Growers Choice Seeds"
- "Haute Genetics" → "Haute Genetique"
- "Humboldt" → "Humboldt Seed Organization"
- "Humboldt Seed Co." → "Humboldt Seed Co"
- "Humboldt Seed Company" → "Humboldt Seed Co"
- "Humboldt Seeds REGULAR" → "Humboldt Seeds"
- "Jaws Gear" → "Jaws Genetics"
- "Katsu Seeds" → "Katsu Bluebird Seeds"
- "Lit Farms" → "LIT Farms" (capitalization)
- "Lovin In Her Eyes" → "Lovin' In Her Eyes" (apostrophe)
- "Mephisto Genetics Autos" → "Mephisto Genetics"
- "Mosca Negra" → "Mosca Seeds"
- "Oni Seed Co." → "Oni Seed Co"
- "SinCity Seeds" → "Sin City Seeds"
- "Strain Hunters Seedbank" → "Strain Hunters Seeds"
- "Strayfox Gardenz" → "Stray Fox Gardenz"
- "SubCools The Dank Seeds" → "Subcool Seeds"
- "Taste Budz Seeds" / "Taste-Budz Seeds" → "Tastebudz"
- "Thug Pug Genetics" → "Thug Pug"
- "Tony Green's" → "Tonygreens Tortured Beans"
- "Twenty 20 Genetics" → "Twenty20 Mendocino"

#### 4. Leading Character Fixes (2 breeders)
- "z710 Genetics" → "710 Genetics"
- "zAce Seeds" → "Ace Seeds"

#### 5. Multi-Breeder Collaborations (1 case)
- "Brother's Grimm Seeds - Trailer Park Boys / Hemptown Collab" → "Brothers Grimm Seeds, Trailer Park Boys, Hemptown Collab"

### New Column
- **breeder_name_clean**: Standardized breeder names (proper case, consistent suffixes)

---

## Step 10F: Non-Cannabis Product Removal

**Input:** 21,360 rows  
**Output:** 21,352 rows  
**Removed:** 8 rows

### Removal Categories

#### 1. Variety Packs (2 rows)
- https://www.gorilla-cannabis-seeds.co.uk/bulkseeds/feminized/bulk-cannabis-seeds.html
- https://www.northatlanticseed.com/product/early-girls-multipack-f/

#### 2. Puffco Vape Products (6 rows)
- https://neptuneseedbank.com/product/puffco-proxy-droplet/
- https://neptuneseedbank.com/product/puffco-proxy-travel-pack/
- https://www.northatlanticseed.com/product/proxy-kit/
- https://www.northatlanticseed.com/product/plus/
- https://www.northatlanticseed.com/product/hot-knife/
- https://www.northatlanticseed.com/product/peak-pro/

### Removal Logic
1. **URL-based removal**: Exact URL match for known non-cannabis products
2. **Breeder-based removal**: All products with breeder_name_clean = "Puffco" (0 additional rows found)

---

## Combined Impact

**Total Operations:** 13,365 standardizations + 8 deletions = 13,373 operations  
**Final Dataset:** 21,352 rows  
**Data Quality Impact:**
- Breeder name consistency: 13,365 names now follow standard format
- Non-cannabis contamination: 100% removed (8 products)
- Ready for deduplication: Breeder names now suitable as deduplication key

---

## Known Issues Remaining

### Empty Breeder Names (3 seed banks)
- **Multiverse**: 799 strains (needs Brand tag extraction)
- **Seed Supreme**: 349 strains (SKU in breeder field, needs Seedbank value)
- **Seedsman JS**: 866 strains (needs custom extraction logic)

**Total Empty:** ~2,014 strains (9.4% of dataset)

### Contaminated Breeder Names
- **Estimated:** ~6,337 strains still have product names/descriptions in breeder_name_raw
- **Solution:** Re-extract from S3 HTML using seed-bank-specific patterns

---

## Files Generated

### Scripts
- `10e_breeder_standardization.py` - Applies 50+ standardization rules
- `10f_non_cannabis_removal.py` - Removes vape products and variety packs

### Data Files
- `../../cleaning_csv/10e_breeder_standardized.csv` - 21,360 rows with breeder_name_clean
- `../../cleaning_csv/10f_non_cannabis_removed.csv` - 21,352 rows (final Phase 1 Extended output)
- `output/10e_breeder_standardized_sample.csv` - 100-row sample
- `output/10f_non_cannabis_removed_sample.csv` - 100-row sample

---

## Next Steps

1. **Shannon documents HTML patterns** for Multiverse, Seed Supreme, Seedsman JS
2. **Amazon Q builds extraction scripts** for 20 seed banks
3. **Re-extract breeder names** from S3 HTML archive
4. **Merge with current dataset** (replace breeder_name_raw)
5. **Re-run Step 10E** to standardize newly extracted names
6. **Verify 100% coverage** (target: <1% NULL breeder names)

---

**Documented by:** Shannon Goddard  
**Scripts by:** Amazon Q

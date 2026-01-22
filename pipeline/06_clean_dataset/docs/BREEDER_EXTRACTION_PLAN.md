# Breeder Name Extraction Project Plan

**Status**: IN PROGRESS  
**Priority**: CRITICAL (Required for deduplication)  
**Started**: January 20, 2026  
**Owner**: Shannon Goddard (pattern documentation) + Amazon Q (extraction scripts)

---

## Problem Statement

**Current State**:
- Dataset: `cleaning_csv/10d_categorical_standardized.csv` (21,360 strains)
- `breeder_name_raw` column: 61% NULL (13,009 strains), 39% contaminated (8,351 strains)
- Contamination examples: "Widow Bomb Cannabis Seeds" (product name), "New York City Sativa Dominant Hybrid" (description)

**Impact**:
- Deduplication key = `strain_name + breeder_name`
- Without accurate breeder names, deduplication will fail
- Cannot proceed to Step 11 (The Big Deduplication) without fixing this

**Root Cause**:
- Original extraction scripts didn't properly extract breeder names from HTML
- Breeder location varies by seed bank (breadcrumbs, metadata, product details, etc.)

---

## Solution: Re-Extract from Source HTML

**Approach**: Option A - Go back to source HTML (best quality, fully reproducible)

**Why this approach**:
- ✅ 100% reproducible (no manual fixes)
- ✅ Best quality (extract from authoritative source)
- ✅ Complete coverage (all 21,360 strains)
- ✅ Maintains data integrity and audit trail
- ✅ Aligns with project transparency requirements

**Data Sources**:
- S3 HTML archive: 21,360 HTML files
- S3 metadata: URL-to-hash mappings
- Current dataset: `cleaning_csv/10d_categorical_standardized.csv`

---

## Project Phases

### Phase 1: Pattern Documentation (Shannon) - IN PROGRESS

**File**: `pipeline/06_clean_dataset/docs/BREEDER_EXTRACTION_PATTERNS.md`

**Task**: Document HTML extraction patterns for all 20 seed banks

**Deliverables**:
For each seed bank, document:
1. Sample URLs (1-3 examples)
2. HTML location of breeder name (CSS selector, class, pattern)
3. Example HTML snippet
4. Edge cases or variations

**Priority Order** (by strain count):
1. ✅ Attitude Seed Bank (7,673) - COMPLETE
2. ✅ Amsterdam (163) - COMPLETE (bank = breeder)
3. Crop King (3,336)
4. North Atlantic (2,727)
5. Gorilla Seed Bank (2,000)
6. Neptune (1,995)
7. Seedsman JS (866)
8. Herbies (753)
9. Sensi Seeds (620)
10. Multiverse Beans (528)
11. Seed Supreme (353)
12. Mephisto Genetics (245)
13. Exotic Genetix (227)
14. ILGM JS (169)
15. Dutch Passion (119)
16. Barney's Farm (88)
17. Royal Queen Seeds (67)
18. Seeds Here Now (43)
19. Great Lakes Genetics (16)
20. Compound Genetics (1)

**Success Criteria**: All 20 seed banks documented with clear extraction patterns

---

### Phase 2: Build Extraction Scripts (Amazon Q) - PENDING

**Scripts to Build**:

**Step 10E: Breeder Name Extraction from S3 HTML**
- Input: S3 HTML files (21,360 files)
- Logic: Seed-bank-specific extraction based on Shannon's patterns
- Output: `breeder_names_extracted.csv` (strain_id, breeder_name_extracted)

**Step 10F: Merge Breeder Names with Dataset**
- Input: `10d_categorical_standardized.csv` + `breeder_names_extracted.csv`
- Logic: Merge on strain_id, create `breeder_name_clean` column
- Output: `10f_breeder_names_merged.csv` (21,360 rows with breeder names)

**Technical Requirements**:
- Read HTML from S3 using boto3
- Parse HTML with BeautifulSoup4
- Apply seed-bank-specific extraction logic
- Handle encoding issues (UTF-8, latin-1)
- Log extraction success/failure rates
- Generate detailed extraction report

**Success Criteria**:
- 95%+ extraction success rate
- All 21,360 strains processed
- Clear logging of failures for manual review

---

### Phase 3: Validation & QA (Shannon) - PENDING

**Tasks**:
1. Review extraction report
2. Spot-check 100-200 random strains
3. Verify top 50 most common breeders
4. Document any issues in `02_MANUAL_QA_REVIEW_GUIDE.md`

**Success Criteria**:
- 95%+ accuracy on spot-check
- No systematic extraction errors
- Ready for case standardization (Step 10G)

---

### Phase 4: Breeder Name Standardization (Amazon Q) - PENDING

**Step 10G: Breeder Name Case Standardization**
- Input: `10f_breeder_names_merged.csv`
- Logic: Apply Shannon's QA findings (proper case, punctuation)
- Output: `10g_breeder_names_standardized.csv`

**Standardization Rules** (from Shannon's QA):
- Proper case: "Barney's Farm" not "barneys farm"
- Consistent punctuation: "Barney's Farm" not "Barneys Farm"
- Remove suffixes: "Barney's Farm Seeds" → "Barney's Farm"

---

## File Structure

```
06_clean_dataset/
├── docs/
│   ├── BREEDER_EXTRACTION_PATTERNS.md (Shannon's pattern documentation)
│   ├── BREEDER_EXTRACTION_PLAN.md (this file)
│   └── 02_MANUAL_QA_REVIEW_GUIDE.md (Phase 3 validation)
├── scripts/
│   ├── 10e_extract_breeders_from_s3.py (Amazon Q - Phase 2)
│   ├── 10f_merge_breeder_names.py (Amazon Q - Phase 2)
│   └── 10g_standardize_breeder_names.py (Amazon Q - Phase 4)
├── output/
│   ├── 10e_breeder_names_extracted.csv
│   ├── 10e_extraction_report.txt
│   ├── 10f_breeder_names_merged.csv
│   ├── 10g_breeder_names_standardized.csv
│   └── 10g_standardization_report.txt
└── cleaning_csv/
    └── 10d_categorical_standardized.csv (current dataset)
```

---

## Data Flow

```
S3 HTML Files (21,360)
    ↓
[Step 10E: Extract Breeders]
    ↓
breeder_names_extracted.csv (strain_id, breeder_name_extracted)
    ↓
[Step 10F: Merge with Dataset]
    ↓
10f_breeder_names_merged.csv (21,360 rows, breeder_name_clean added)
    ↓
[Shannon QA Review]
    ↓
[Step 10G: Standardize Cases]
    ↓
10g_breeder_names_standardized.csv (FINAL - ready for deduplication)
```

---

## Success Metrics

**Coverage**:
- Target: 95%+ of strains have breeder names
- Current: 39% (8,351 strains)
- Gap: 13,009 strains need extraction

**Accuracy**:
- Target: 95%+ correct breeder names (validated by Shannon)
- Method: Spot-check 100-200 random strains

**Quality**:
- No product names in breeder field
- No descriptions in breeder field
- Consistent case and punctuation
- Ready for deduplication

---

## Dependencies

**AWS Resources**:
- S3 bucket: `ci-strains-html-archive` (or equivalent)
- S3 path: `s3://bucket/seed_bank_name/hash.html`
- Metadata: URL-to-hash mappings

**Python Libraries**:
- boto3 (S3 access)
- BeautifulSoup4 (HTML parsing)
- pandas (data manipulation)
- re (regex for pattern matching)

**Data Files**:
- Current dataset: `cleaning_csv/10d_categorical_standardized.csv`
- Pattern documentation: `docs/BREEDER_EXTRACTION_PATTERNS.md`
- S3 inventory: `pipeline/03_s3_inventory/s3_html_inventory.csv`

---

## Risk Mitigation

**Risk 1: Some seed banks don't have breeder info**
- Mitigation: Document in patterns, use seed bank name as fallback
- Example: Amsterdam = "Amsterdam Marijuana Seeds"

**Risk 2: Extraction patterns change over time**
- Mitigation: HTML is archived, patterns are stable
- Fallback: Manual review of failures

**Risk 3: Encoding issues in HTML**
- Mitigation: Try UTF-8, fallback to latin-1, log issues
- Handle mojibake (Ã£Â¢Ã¢Â€Ã¢Â")

**Risk 4: Missing HTML files in S3**
- Mitigation: Log missing files, report coverage
- Cross-reference with S3 inventory

---

## Timeline Estimate

**Phase 1: Pattern Documentation** (Shannon)
- Time: 4-8 hours (20 seed banks × 15-20 min each)
- Status: 2/20 complete (Attitude, Amsterdam)

**Phase 2: Build Extraction Scripts** (Amazon Q)
- Time: 2-3 hours (script development + testing)
- Status: Pending Phase 1 completion

**Phase 3: Validation & QA** (Shannon)
- Time: 2-4 hours (spot-checking + documentation)
- Status: Pending Phase 2 completion

**Phase 4: Standardization** (Amazon Q)
- Time: 1 hour (script + execution)
- Status: Pending Phase 3 completion

**Total Estimated Time**: 9-16 hours across 2-3 days

---

## Next Steps

**Immediate** (Shannon):
1. Continue documenting patterns in `BREEDER_EXTRACTION_PATTERNS.md`
2. Focus on top 5 seed banks first (covers 83% of dataset)
3. Notify Amazon Q when patterns are ready

**After Pattern Documentation** (Amazon Q):
1. Build Step 10E extraction script
2. Test on 100-strain sample
3. Run full extraction on 21,360 strains
4. Generate extraction report

**After Extraction** (Shannon):
1. Review extraction report
2. Spot-check accuracy
3. Document findings for standardization

**Final Step** (Amazon Q):
1. Build Step 10G standardization script
2. Apply Shannon's QA findings
3. Generate final dataset ready for deduplication

---

## Communication Protocol

**When Shannon completes patterns**:
- Update `BREEDER_EXTRACTION_PATTERNS.md` with "Ready for extraction: Yes"
- Start new chat with Amazon Q
- Reference this plan document

**When Amazon Q completes extraction**:
- Generate detailed report
- Notify Shannon for QA review
- Provide sample of extracted breeders

**When Shannon completes QA**:
- Update `02_MANUAL_QA_REVIEW_GUIDE.md`
- Notify Amazon Q for standardization
- Provide case/punctuation rules

---

## Related Documents

- **Pattern Documentation**: `pipeline/06_clean_dataset/docs/BREEDER_EXTRACTION_PATTERNS.md`
- **Current Dataset**: `cleaning_csv/10d_categorical_standardized.csv`
- **Phase 1 Results**: `pipeline/06_clean_dataset/docs/PHASE_1_CLEANING_RESULTS.md`
- **Manual QA Guide**: `pipeline/06_clean_dataset/docs/01_MANUAL_QA_REVIEW_GUIDE.md`
- **S3 Inventory**: `pipeline/03_s3_inventory/s3_html_inventory.csv`

---

## Attribution

**Pattern Documentation**: Shannon Goddard (19 years cannabis industry expertise)  
**Extraction Scripts**: Amazon Q (automation + AWS integration)  
**QA Validation**: Shannon Goddard (domain knowledge + quality gate)  
**Methodology**: Collaborative human-AI partnership

**Philosophy**: Best quality, fully reproducible, no manual fixes, complete transparency.

---

**Last Updated**: January 20, 2026  
**Status**: Phase 1 in progress (2/20 seed banks documented)  
**Next Milestone**: Complete pattern documentation for top 5 seed banks

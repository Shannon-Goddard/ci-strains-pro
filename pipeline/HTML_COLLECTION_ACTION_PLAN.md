# Cannabis Intelligence Database - HTML Collection & Enhanced Analysis Action Plan

**Date**: January 2, 2026  
**Architect**: Shannon Goddard  
**Technical Partner**: Amazon Q  
**Status**: Planning Phase  

---

## Overview
Comprehensive quality assurance initiative to maximize data completeness through full HTML collection and dual AI analysis of all 15,768 strain records.

## Objectives
- Collect complete HTML source for all strain URLs
- Identify missed data points in current extraction
- Enhance dataset with Amazon Q + Gemini dual validation
- Create most comprehensive Cannabis Intelligence Database possible

---

## Phase 1: Current Manual Review (In Progress)
**Status**: 50% Complete (96/193 URLs fixed)

### Tasks
- [x] Identify 193 failed scrapes (`scrape_success = FALSE`)
- [🔄] Fix broken URLs using Excel Find & Replace
  - [x] Fixed 86 URLs: "AK " → "ak-" 
  - [🔄] Manually verify remaining 107 URLs
- [ ] Create `failed_scrapes_fixed_187.csv`
- [ ] Run through `pipeline/04_full_dataset_validation`
- [ ] Merge results into main dataset

---

## Phase 2: HTML Collection Pipeline
**Target**: `pipeline/06_html_collection/`

### Infrastructure Setup
- **Storage**: Google Cloud Storage (free credits)
- **Structure**: `strain_html/{strain_id}.html`
- **API**: Bright Data for full HTML scraping
- **Index**: CSV mapping strain_id → GCS path

### Deliverables
- [ ] HTML collection script
- [ ] GCS bucket configuration
- [ ] Index CSV with strain_id mappings
- [ ] Complete HTML archive (15,768 files)
- [ ] `HTML_COLLECTION.md` methodology

---

## Phase 3: Enhanced Analysis Pipeline
**Target**: `pipeline/07_enhanced_extraction/`

### Dual AI Analysis Workflow

#### Step 1: Amazon Q Analysis
**Method**: Direct HTML parsing and pattern recognition
- [ ] Analyze all 15,768 HTML files
- [ ] Identify systematic extraction gaps
- [ ] Generate enhanced dataset with missed data points
- [ ] Create gap analysis report

**Focus Areas**:
- Missing THC/CBD ranges
- Unreported effects and flavors  
- Terpene profiles
- Cultivation details
- Breeder information

#### Step 2: Gemini Validation
**Method**: Natural language processing validation
- [ ] Cross-validate Amazon Q findings
- [ ] Process enhanced dataset through Gemini
- [ ] Final quality check on new extractions
- [ ] Generate confidence scores

### Deliverables
- [ ] Enhanced extraction script (Amazon Q)
- [ ] Gemini validation script
- [ ] Gap analysis report
- [ ] Enhanced Cannabis Database (final)
- [ ] `ENHANCED_EXTRACTION.md` methodology

---

## Expected Outcomes

### Data Completeness Improvements
- **Current**: 99.17% scrape success (15,575/15,768)
- **Target**: 100% with enhanced data extraction
- **New Fields**: Terpenes, detailed effects, cultivation notes

### Quality Metrics
- Dual AI validation for maximum accuracy
- Complete source HTML backup for future analysis
- Comprehensive audit trail of all enhancements

### Commercial Value
- Most complete cannabis strain database available
- Enhanced data points increase commercial licensing value
- Future-proof architecture for ongoing updates

---

## Resource Requirements

### Technical
- Google Cloud Storage: ~500MB HTML files
- Bright Data API: ~$30-50 for full collection
- Processing time: 2-3 days for complete pipeline

### Human
- Shannon: Manual URL fixes, pipeline oversight
- Amazon Q: HTML analysis, script development
- Gemini: Final validation processing

---

## Risk Mitigation
- **Backup Strategy**: All original data preserved
- **Version Control**: Each phase creates new dataset version
- **Quality Gates**: Manual review at each pipeline stage
- **Cost Control**: Targeted API usage, free GCS credits

---

## Success Criteria
- [ ] 100% URL success rate (0 failed scrapes)
- [ ] 25%+ increase in data completeness per strain
- [ ] Dual AI validation confidence >95%
- [ ] Complete HTML archive for future analysis
- [ ] Enhanced dataset ready for Phase 2 monetization

---

## Timeline
- **Week 1**: Complete manual review, HTML collection setup
- **Week 2**: Full HTML scraping, Amazon Q analysis
- **Week 3**: Gemini validation, final dataset generation
- **Week 4**: Quality assurance, documentation, deployment

---

## Methodology Attribution
**Logic designed by Amazon Q, verified by Shannon Goddard.**

**Next Action**: Complete manual URL fixes → Create failed_scrapes_fixed_193.csv

---

**🌿 Cannabis Intelligence Database - Maximizing data completeness through Human-AI partnership.**
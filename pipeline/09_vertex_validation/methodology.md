# Phase 9: Vertex AI Validation - Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Overview

Validate and correct 21,361 extracted strain names and breeder names using Google Vertex AI (Gemini 2.0 Flash). AI reviews each extraction for accuracy, removes remaining breeder names from strain fields, identifies correct breeders, and flags low-confidence items for manual review.

---

## Approach

### 1. Why AI Validation?

**Limitations of Rule-Based Extraction:**
- Cannot distinguish "Barney's Farm" (breeder) from "Barney Rubble OG" (strain)
- Misses context-dependent patterns (e.g., when "Auto" is part of strain name)
- Requires manual breeder list maintenance (140+ breeders across 19 seed banks)
- Edge cases require human judgment

**AI Advantages:**
- Understands context from URL structure
- Learns patterns across 21K examples
- Handles ambiguous cases with confidence scoring
- Identifies breeders without pre-defined lists

### 2. Model Selection: Gemini 2.0 Flash

**Why Gemini Flash:**
- **Cost**: $0.00001 per 1K input tokens (cheapest available)
- **Speed**: Fast inference for batch processing
- **Quality**: Sufficient for structured validation tasks
- **Availability**: Already integrated via Google Cloud credits

**Alternatives Considered:**
- GPT-4: 10x more expensive, overkill for this task
- Claude: Similar cost, but less integrated with our stack
- Gemini Pro: 5x more expensive, unnecessary for validation

### 3. Validation Strategy

**Batch Processing:**
- 50 strains per API call (balance speed/cost)
- 1 second delay between batches (rate limiting)
- ~428 batches total = 7-8 minutes runtime

**Input Data per Strain:**
- URL (for context on naming patterns)
- Seed bank (for breeder identification)
- Extracted strain name (to validate)
- Extracted breeder (to validate)

**Output Data per Strain:**
- Corrected strain name (or "CORRECT")
- Corrected breeder (or "CORRECT")
- Confidence score (0-100)
- Reasoning (brief explanation)

### 4. Validation Rules

**Implemented in AI Prompt:**
1. Remove breeder names from strain field
2. Preserve strain numbers (e.g., "Project 4516")
3. Remove "Auto" suffix unless at start of name
4. Standardize breeder names (proper capitalization)
5. Flag unknown breeders as "Unknown"

**Confidence Scoring:**
- 95-100%: High confidence, no review needed
- 90-94%: Good confidence, spot-check recommended
- 80-89%: Medium confidence, review recommended
- <80%: Low confidence, manual review required

### 5. Quality Assurance

**Automated Checks:**
- All 21,361 strains processed (100% completeness)
- Confidence distribution analysis
- Correction rate tracking (expected: 2-5%)
- Flagged rate tracking (expected: 2-7%)

**Manual Review:**
- Review all items with confidence < 90%
- Spot-check 50-100 random high-confidence items
- Validate breeder identification accuracy
- Update extraction rules if systematic errors found

---

## Execution

### Prerequisites
1. AWS CLI configured with Secrets Manager access
2. Google Cloud credentials in AWS Secrets Manager (`cannabis_google_cloud_api`)
3. Python 3.8+ with dependencies: `pandas`, `boto3`, `google-cloud-aiplatform`

### Run Validation
```bash
cd pipeline/09_vertex_validation/scripts
python validate_with_vertex.py
```

### Configuration
- **Batch size**: 50 strains per API call
- **Confidence threshold**: 90% (flag below for review)
- **Rate limit**: 1 second delay between batches

---

## Output Format

### Main Output: `all_strains_validated.csv`
**New Columns:**
- `strain_name_validated` - AI-corrected strain name
- `breeder_validated` - AI-corrected breeder name
- `validation_confidence` - Confidence score (0-100)
- `validation_reasoning` - AI explanation for changes
- `validation_changes` - Summary of corrections made
- `flagged_for_review` - Boolean (True if confidence < 90%)

### Flagged Items: `all_strains_validated_flagged.csv`
Subset of strains requiring manual review (confidence < 90%)

### Report: `all_strains_validated_report.txt`
Summary statistics:
- Total corrections made
- Confidence distribution
- Corrections by seed bank
- Estimated API cost

---

## Cost Analysis

### Gemini 2.0 Flash Pricing
- **Input**: $0.00001 per 1,000 tokens
- **Output**: $0.00003 per 1,000 tokens

### Estimated Usage
- **~200 tokens per strain** (input + output)
- **21,361 strains** × 200 tokens = 4,272,200 tokens
- **Cost**: (4,272,200 ÷ 1,000) × $0.00002 = **$0.85**

### Budget
- **Available**: $1,200 Google Cloud credits
- **This phase**: ~$1
- **Remaining**: $1,199 for future phases (lineage extraction, AI enhancement)

---

## Expected Results

### Corrections
- **2-5% correction rate** = 400-1,000 strains corrected
- **Primary corrections**: Breeder identification, "Auto" suffix removal
- **Secondary corrections**: Capitalization, number preservation

### Flagged Items
- **2-7% flagged rate** = 400-1,500 strains flagged
- **Reasons**: Ambiguous URLs, unusual patterns, conflicting information
- **Manual review**: 5-10 hours estimated

### Accuracy Target
- **99%+ accuracy** on strain names (post-review)
- **95%+ accuracy** on breeder names
- **100% completeness** (all strains processed)

---

## Next Steps

### After Validation
1. **Review flagged items** (confidence < 90%)
2. **Spot-check corrections** (sample 50-100 random strains)
3. **Update extraction rules** if systematic errors found
4. **Proceed to Phase 10**: Lineage extraction from HTML

### Manual Review Process
1. Open `all_strains_validated_flagged.csv`
2. Review `validation_reasoning` column
3. Check original URL for context
4. Accept or override AI suggestion
5. Update `strain_name_validated` and `breeder_validated` as needed

---

## Success Metrics

**Target Outcomes:**
- ✅ 21,361 strains validated (100% completeness)
- ✅ 99%+ accuracy on strain names
- ✅ 95%+ accuracy on breeder names
- ✅ <$2 total API cost
- ✅ <10 hours manual review time

**Deliverables:**
- Validated dataset with confidence scores
- Flagged items for manual review
- Validation report with statistics
- Updated extraction rules (if needed)

---

**Total Strains**: 21,361  
**Estimated Cost**: $0.50-$1.00  
**Estimated Runtime**: 7-8 minutes  
**Manual Review**: 5-10 hours (flagged items only)

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

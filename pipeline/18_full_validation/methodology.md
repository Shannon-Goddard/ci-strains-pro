# Pipeline 18: Full Validation Analysis

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Objective

Parse Pipeline 17 validation results and generate actionable correction recommendations.

---

## Process

1. **Load Results** - Parse JSON validation output from Pipeline 17
2. **Categorize Corrections** - Group by confidence level
3. **Generate Reports** - Create CSV files for review and application
4. **Field Analysis** - Breakdown corrections by data field

---

## Output Files

### 1. `high_confidence_corrections.csv`
- Status: `incorrect` or `missing`
- Confidence: `high`
- **Action:** Auto-apply after Shannon's review

### 2. `manual_review_needed.csv`
- Status: `incorrect` or `missing`
- Confidence: `low` or `medium`
- **Action:** Manual review required

### 3. `all_corrections.csv`
- Complete list of all corrections
- **Action:** Reference file

### 4. `validation_errors.csv`
- Strains that failed validation
- **Action:** Investigate and retry

---

## Correction Categories

**Status Values:**
- `incorrect` - Current value differs from source
- `missing` - No current value, but found on source
- `correct` - Current value matches source (no action)
- `not_found` - Not present on source page (no action)

**Confidence Levels:**
- `high` - Clear, unambiguous data on source page
- `medium` - Data present but requires interpretation
- `low` - Unclear or conflicting data on source page

---

## Next Steps

1. Shannon reviews `high_confidence_corrections.csv`
2. Shannon reviews `manual_review_needed.csv`
3. Apply approved corrections to dataset
4. Generate final cleaned dataset

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

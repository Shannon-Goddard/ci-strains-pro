# Pipeline 17 & 18: Validation Attempts Log

## Attempt 1: URL Grounding with JSON Response (FAILED)
- **Approach:** Batched URL grounding with `response_mime_type="application/json"`
- **Issue:** Gemini doesn't support controlled generation with URL Context tool
- **Result:** 21,210 errors (400 INVALID_ARGUMENT)
- **Files Deleted:** `full_validation_results.json` (21,210 error records)

## Attempt 2: URL Grounding without JSON Control (FAILED)
- **Approach:** Batched URL grounding, manual JSON parsing
- **Issue:** 99.9% JSON parsing failures (21,190/21,205 errors)
- **Runtime:** 13+ hours for 21,205 strains
- **Result:** Only 15 successful validations
- **Files Deleted:** `full_validation_results.json` (mostly errors), all checkpoints

## Attempt 3: S3 HTML Validation (SUCCESS)
- **Approach:** Use archived S3 HTML, controlled JSON response
- **Result:** 91.8% success rate (19,475/21,210)
- **Corrections:** 1,303 total (691 high confidence, 225 medium, 387 low)
- **Status:** Gold-platinum data quality achieved

---

**Lesson Learned:** URL grounding is unreliable for batch processing. Use archived HTML sources when available.

**Logic designed by Amazon Q, verified by Shannon Goddard.**

import os
import json

# --- CONFIGURATION ---
PIPELINE_17 = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\17_gemini_revalidation"
PIPELINE_18 = r"c:\Users\uthin\OneDrive\Desktop\ci-strains-pro\pipeline\18_full_validation"

print("Cleaning up failed attempts...\n")

# Document what we tried
attempts_log = """# Pipeline 17 & 18: Validation Attempts Log

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
"""

# Write attempts log
log_file = os.path.join(PIPELINE_17, "ATTEMPTS_LOG.md")
with open(log_file, 'w', encoding='utf-8') as f:
    f.write(attempts_log)
print(f"Created: {log_file}")

# Delete large JSON files from failed attempts
files_to_delete = [
    os.path.join(PIPELINE_17, "output", "full_validation_results.json")
]

deleted_count = 0
for file_path in files_to_delete:
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {os.path.basename(file_path)}")
        deleted_count += 1

# Delete checkpoint files
for pipeline_dir in [PIPELINE_17, PIPELINE_18]:
    output_dir = os.path.join(pipeline_dir, "output")
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            if "checkpoint" in file.lower():
                file_path = os.path.join(output_dir, file)
                os.remove(file_path)
                print(f"Deleted checkpoint: {file}")
                deleted_count += 1

print(f"\nCleanup complete!")
print(f"Deleted {deleted_count} files")
print(f"Documented attempts in ATTEMPTS_LOG.md")
print(f"\nKeeping: s3_validation_results.json (successful validation)")
print(f"Keeping: All CSV review files in pipeline 18")

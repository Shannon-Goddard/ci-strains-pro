# Pipeline 05: Manual Review Cleaning - Data Mix-up Documentation

## ⚠️ **CRITICAL ISSUE DISCOVERED**

**Date**: January 2026  
**Issue**: Data integrity compromised during manual review process  
**Resolution**: Reverted to previous validated dataset  
**Status**: DEPRECATED - Use Pipeline 08 instead

---

## What Happened

During the manual review and cleaning process in this pipeline, the dataset became corrupted due to:

1. **Column Misalignment**: Manual edits caused column shifts
2. **Data Type Corruption**: Mixed data types in critical columns
3. **Row Integrity Loss**: Some strain records became fragmented
4. **Validation Failures**: Quality checks revealed inconsistencies

## Files Affected

- `failed_scrapes_fixed_187.csv` - Corrupted during manual editing
- `failed_scrapes_validated_187.csv` - Validation attempts failed
- `manual_review_progress.db` - Progress tracking became unreliable

## Resolution Action

**REVERTED** to the clean dataset from Pipeline 04:
- Source: `pipeline/04_full_dataset_validation/full_dataset_validated.csv`
- Destination: `revert_manual_review_cleaning.csv` (root directory)
- Action: Complete rollback to last known good state

## Lessons Learned

1. **Never edit raw CSV files manually** - Use programmatic cleaning only
2. **Always backup before manual intervention** - Maintain data integrity
3. **Validate after every manual step** - Catch issues immediately
4. **Use version control for datasets** - Track all changes

## Current Status

- ❌ **Pipeline 05**: DEPRECATED - Do not use
- ✅ **Pipeline 08**: Active manual cleaning with proper controls
- ✅ **Root CSV**: `revert_manual_review_cleaning.csv` is the clean baseline

---

**Next Steps**: All future manual cleaning moved to Pipeline 08 with proper safeguards.

*Logic designed by Amazon Q, verified by Shannon Goddard.*
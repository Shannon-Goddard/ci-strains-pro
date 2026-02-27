# Conflict Review Instructions

## Your Workflow

1. **Open:** `conflicts_flagged.csv` in Excel/Google Sheets
2. **Review:** Each row shows old_value vs new_value
3. **Decide:** Fill in `final_value` column with your choice:
   - Leave blank = keep current_value (NEW data)
   - Enter old_value = use OLD data
   - Enter new_value = confirm NEW data
   - Enter custom value = manual override
4. **Save:** Save the CSV
5. **Apply:** Run `python apply_overrides.py`

---

## Columns in conflicts_flagged.csv

| Column | Description |
|--------|-------------|
| strain_id | Unique identifier |
| strain_name_display | Strain name for reference |
| seed_bank_display | Seed bank for reference |
| column | Which botanical field has conflict |
| old_value | Value from Pipeline 11 (old scrape) |
| new_value | Value from Pipeline 13 (new scrape) |
| current_value | What's currently in dataset (defaults to new_value) |
| difference | Absolute difference between old and new |
| final_value | **YOUR DECISION** - fill this in |

---

## Review Priority

### High Priority (1,538 conflicts)
- **thc_avg** (671 conflicts) - Critical for buyers
- **thc_min** (345 conflicts) - Price tier decisions
- **thc_max** (522 conflicts) - Marketing claims

### Medium Priority (1,178 conflicts)
- **flowering_days_avg** (1,178 conflicts) - Growers need accurate timing

### Low Priority (10,183 conflicts)
- **height_indoor_cm_min** (3,366) - Unit conversion issues, trust NEW
- **height_outdoor_cm_min** (3,111) - Unit conversion issues, trust NEW
- **yield_indoor_g_m2_min** (2,608) - Different methods, trust NEW
- **yield_outdoor_g_plant_min** (839) - Different methods, trust NEW
- **cbd_avg/min/max** (259) - Low user demand, trust NEW

---

## Quick Review Tips

### Sort by difference (descending)
Focus on biggest conflicts first - small differences (<5%) probably don't matter

### Filter by seed bank
Review one seed bank at a time - patterns emerge (e.g., "ILGM always has better NEW data")

### Spot check with source lookup
Use strains.loyal9.app to verify against original HTML when unsure

### Batch decisions
If you see a pattern (e.g., "OLD data for Neptune is always better"), apply to all

---

## Example Decisions

**Scenario 1: NEW data looks correct**
- old_value: 150 (clearly wrong)
- new_value: 15 (makes sense for THC%)
- final_value: `15` or leave blank

**Scenario 2: OLD data looks correct**
- old_value: 22 (reasonable THC%)
- new_value: 220 (decimal error)
- final_value: `22`

**Scenario 3: Both wrong, manual override**
- old_value: 8 (too low)
- new_value: 80 (decimal shift)
- Check source → actual is 18%
- final_value: `18`

**Scenario 4: Can't decide**
- Leave final_value blank = defaults to NEW
- Add note in separate column if needed

---

## After Review

Run: `python apply_overrides.py`

This will:
1. Read your final_value decisions
2. Apply them to pipeline_15_consolidated.csv
3. Save as pipeline_15_consolidated_reviewed.csv

Then you can compare before/after coverage and move to Pipeline 16.

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

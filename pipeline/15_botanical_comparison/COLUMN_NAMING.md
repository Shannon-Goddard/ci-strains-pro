# CRITICAL: Column Naming Pattern

## How to Distinguish Old vs New Columns

### OLD Columns (from Pipeline 11)
**Pattern:** Ends with `_raw` or `_clean`

**Examples:**
- `thc_min_raw`, `thc_max_raw`, `thc_content_raw`
- `cbd_min_raw`, `cbd_max_raw`, `cbd_content_raw`
- `flowering_time_days_clean`
- `height_indoor_cm_clean`, `height_outdoor_cm_clean`
- `yield_indoor_g_m2_clean`, `yield_outdoor_g_plant_clean`

### NEW Columns (from Pipeline 13)
**Pattern:** NO `_raw` or `_clean` suffix, just `_min`, `_max`, `_avg`

**Examples:**
- `thc_min`, `thc_max`, `thc_avg`
- `cbd_min`, `cbd_max`, `cbd_avg`
- `flowering_days_min`, `flowering_days_max`, `flowering_days_avg`
- `height_indoor_cm_min`, `height_indoor_cm_max`
- `yield_indoor_g_m2_min`, `yield_indoor_g_m2_max`

## Programmatic Detection

```python
# Identify OLD columns
old_cols = [col for col in df.columns if col.endswith('_raw') or col.endswith('_clean')]

# Identify NEW columns (botanical only, not all columns)
new_cols = [col for col in df.columns if any(x in col for x in ['thc_', 'cbd_', 'flowering_days_', 'height_', 'yield_']) and not (col.endswith('_raw') or col.endswith('_clean'))]
```

## Column Pairs for Consolidation

| OLD (Pipeline 11) | NEW (Pipeline 13) | Final Column |
|-------------------|-------------------|--------------|
| `thc_content_raw` | `thc_avg` | `thc_avg_final` |
| `cbd_content_raw` | `cbd_avg` | `cbd_avg_final` |
| `flowering_time_days_clean` | `flowering_days_avg` | `flowering_days_avg_final` |
| `height_indoor_cm_clean` | `height_indoor_cm_min` | `height_indoor_cm_min_final` |
| `yield_indoor_g_m2_clean` | `yield_indoor_g_m2_min` | `yield_indoor_g_m2_min_final` |

**This naming pattern makes old vs new columns easy to distinguish!**

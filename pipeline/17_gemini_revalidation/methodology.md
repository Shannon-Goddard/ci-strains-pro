# Pipeline 17: Gemini Re-Validation Methodology

**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Objective

Validate and correct ALL botanical data columns using Gemini 2.0 Flash with URL grounding to access live source pages.

---

## Approach

### URL Grounding (Correct Method)
- Uses `genai.Client` with `vertexai=True`
- Configures `Tool(url_context=UrlContext())` for live URL access
- Gemini accesses full webpage content (no truncation)
- No manual HTML fetching required

### Previous Broken Approach (Fixed)
- ❌ Used old `vertexai.generative_models.GenerativeModel`
- ❌ Manually fetched HTML from S3 (truncated to 15K chars)
- ❌ No URL context tool configured
- ❌ Wrong model name (`gemini-2.5-flash`)

---

## Column Groups Validated

1. **Cannabinoids** (6 fields)
   - thc_min, thc_max, thc_avg
   - cbd_min, cbd_max, cbd_avg

2. **Genetics** (3 fields)
   - indica_percentage, sativa_percentage
   - genetics_type

3. **Flowering Time** (3 fields)
   - flowering_days_min, flowering_days_max, flowering_days_avg

4. **Height Indoor** (2 fields)
   - height_indoor_cm_min, height_indoor_cm_max

5. **Height Outdoor** (2 fields)
   - height_outdoor_cm_min, height_outdoor_cm_max

6. **Yield Indoor** (2 fields)
   - yield_indoor_g_m2_min, yield_indoor_g_m2_max

7. **Yield Outdoor** (2 fields)
   - yield_outdoor_g_plant_min, yield_outdoor_g_plant_max

**Total: 20 botanical data columns**

---

## Validation Logic

For each strain:
1. Access live source URL via Gemini URL grounding
2. Extract all botanical data present on page
3. Compare with current database values
4. Return validation status for each field:
   - `correct`: Current value matches source
   - `incorrect`: Current value differs from source
   - `missing`: No current value, but found on source
   - `not_found`: Not present on source page

---

## Output Format

```json
{
  "strain_id": "uuid",
  "strain_name": "Strain Name",
  "source_url": "https://...",
  "validation": {
    "cannabinoids": {
      "thc_min": {
        "current": 20.0,
        "extracted": 22.0,
        "status": "incorrect",
        "confidence": "high",
        "note": "Page shows 22-24% THC"
      }
    },
    "genetics": { ... },
    "flowering": { ... },
    ...
  },
  "status": "success"
}
```

---

## Processing

- **Batch Size:** 10 strains per API call (reduces 21,220 calls to ~2,122 calls)
- **Checkpoint Interval:** Every 100 strains
- **Rate Limiting:** 0.5s delay between batches
- **Error Handling:** Captures and logs all failures
- **Encoding:** UTF-8 with latin-1 CSV read
- **Estimated Runtime:** ~18 minutes (vs 30 hours unbatched)

---

## Next Steps (Pipeline 18)

1. Parse validation results
2. Identify corrections needed
3. Flag high-confidence changes
4. Generate human review list for low-confidence items
5. Apply approved corrections to dataset

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

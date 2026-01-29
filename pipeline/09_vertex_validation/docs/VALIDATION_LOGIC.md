# Vertex AI Validation Logic

## Overview
This document details the AI prompt structure, validation rules, and expected outputs for Gemini 2.0 Flash validation of strain names and breeders.

## Prompt Engineering

### Base Prompt Template
```
You are a cannabis strain name validator. Review each strain's extracted name and breeder.

RULES:
1. Strain names should NOT contain breeder names, seed types (feminized/auto), or pack sizes
2. Preserve strain numbers (e.g., "Project 4516", "Haze 13")
3. Remove "Auto" suffix unless it's at the start (preserve "Auto 1", "Auto Moonrocks")
4. Breeder names should be clean company names (e.g., "Barney's Farm", "Mephisto Genetics")
5. If breeder is unknown/unclear, return "Unknown"

For each strain, provide:
- corrected_strain_name (or "CORRECT" if no changes needed)
- corrected_breeder (or "CORRECT" if no changes needed)
- confidence (0-100)
- reasoning (brief explanation)
```

### Input Data Format
```
INPUT DATA:

0. URL: https://www.cannabis-seeds-bank.co.uk/barney-s-farm-blue-gelato-41-feminised-seeds/prod_6789.html
   Seed Bank: attitude_seed_bank
   Extracted Strain: Blue Gelato 41
   Extracted Breeder: N/A

1. URL: https://www.mephistogenetics.com/illuminauto-29
   Seed Bank: mephisto_genetics
   Extracted Strain: Illuminauto 29
   Extracted Breeder: Mephisto Genetics

[... up to 50 strains per batch ...]
```

### Expected Output Format
```json
{
  "validations": [
    {
      "index": 0,
      "corrected_strain_name": "CORRECT",
      "corrected_breeder": "Barney's Farm",
      "confidence": 98,
      "reasoning": "Breeder identified from URL prefix 'barney-s-farm'"
    },
    {
      "index": 1,
      "corrected_strain_name": "CORRECT",
      "corrected_breeder": "CORRECT",
      "confidence": 100,
      "reasoning": "Extraction is accurate, Illuminauto is Mephisto's series name"
    }
  ]
}
```

## Validation Rules (Detailed)

### Rule 1: Remove Breeder Names from Strain Field
**Problem**: Breeder names sometimes leak into strain names during extraction

**Examples:**
- ❌ "Barney's Farm Blue Gelato 41" → ✅ "Blue Gelato 41"
- ❌ "Mephisto Genetics Sour Stomper" → ✅ "Sour Stomper"
- ❌ "FastBuds Gorilla Glue" → ✅ "Gorilla Glue"

**AI Detection:**
- Check if extracted strain name contains known breeder names
- Cross-reference URL for breeder identification
- Remove breeder prefix/suffix from strain name

### Rule 2: Preserve Strain Numbers
**Problem**: Numbers are often part of the official strain name

**Examples:**
- ✅ "Project 4516" (keep number)
- ✅ "Haze 13" (keep number)
- ✅ "Cherry Nova 6" (keep number)
- ✅ "Illuminauto 29" (keep number)
- ✅ "Blue Gelato 41" (keep number)

**AI Detection:**
- If number appears in URL slug, it's likely part of strain name
- If number is 1-4 digits and integrated with name, preserve it
- If number is 5+ digits or separated, it might be product code (flag for review)

### Rule 3: Handle "Auto" Suffix Intelligently
**Problem**: "Auto" can be metadata (autoflowering type) or part of strain name

**Remove "Auto" when:**
- ❌ "Blue Dream Auto" → ✅ "Blue Dream"
- ❌ "Wedding Cake Auto" → ✅ "Wedding Cake"
- ❌ "Gorilla Glue Auto" → ✅ "Gorilla Glue"

**Preserve "Auto" when:**
- ✅ "Auto 1" (starts with Auto)
- ✅ "Auto Moonrocks" (starts with Auto)
- ✅ "Illuminauto 29" (part of series name)
- ✅ "Autoflower Mix" (descriptive strain name)

**AI Detection:**
- If "Auto" is at the end and URL contains "auto" or "autoflower" → remove
- If "Auto" is at the start → preserve
- If "Auto" is embedded in compound word → preserve

### Rule 4: Clean Breeder Names
**Problem**: Breeder names need standardization

**Examples:**
- "barney-s-farm" → "Barney's Farm"
- "mephisto" → "Mephisto Genetics"
- "fastbuds" → "FastBuds"
- "exotic-genetix" → "Exotic Genetix"

**AI Detection:**
- Extract breeder from URL prefix/suffix
- Standardize capitalization and punctuation
- Use full company name (not abbreviations)

### Rule 5: Flag Unknown Breeders
**Problem**: Not all strains have identifiable breeders

**When to flag "Unknown":**
- No breeder information in URL
- Seed bank is reseller (not original breeder)
- Multiple breeders possible (white-label strains)

**AI Detection:**
- If URL has no breeder prefix/suffix → "Unknown"
- If seed bank is marketplace (Attitude, Seedsman) → extract from URL
- If seed bank is direct breeder (Mephisto, Exotic) → use seed bank as breeder

## Confidence Scoring Guidelines

### 95-100%: High Confidence
- Clear URL structure with obvious breeder/strain separation
- Extraction matches expected patterns
- No ambiguity in naming

**Example:**
```
URL: mephistogenetics.com/sour-stomper
Extracted: Sour Stomper
Breeder: Mephisto Genetics
Confidence: 100
```

### 90-94%: Good Confidence
- Minor corrections needed (capitalization, breeder identification)
- Strain name is clear, but breeder required inference

**Example:**
```
URL: attitude.com/fastbuds-gorilla-glue-auto
Extracted: Gorilla Glue
Breeder: Unknown
Corrected Breeder: FastBuds
Confidence: 92
```

### 80-89%: Medium Confidence
- Ambiguous URL structure
- Strain numbers that could be product codes
- Multiple possible interpretations

**Example:**
```
URL: seedsherenow.com/exotic-genetix-project-4516-regs
Extracted: Project 4516
Breeder: Exotic Genetix
Confidence: 85
Reasoning: "Strain number preserved, but could be product code"
```

### <80%: Low Confidence
- Highly ambiguous naming
- Conflicting information in URL vs extracted name
- Unusual patterns not covered by rules

**Example:**
```
URL: seedbank.com/strain-12345-special-edition
Extracted: Strain 12345
Breeder: Unknown
Confidence: 70
Reasoning: "Unclear if '12345' is strain name or product code"
```

## Edge Cases

### Case 1: Aka Names (Gorilla Seed Bank)
**Input:** "Blue Dream (aka Azure Fantasy)"
**Output:** "Blue Dream (aka Azure Fantasy)" (preserve full name)
**Confidence:** 95+

### Case 2: Series Names (Mephisto)
**Input:** "Illuminauto 29"
**Output:** "Illuminauto 29" (preserve series + number)
**Confidence:** 100

### Case 3: Multi-Word Breeders
**Input:** "Royal Queen Seeds Northern Light"
**Output:** Strain: "Northern Light", Breeder: "Royal Queen Seeds"
**Confidence:** 95+

### Case 4: Breeder in Strain Name
**Input:** "Barney Rubble OG"
**Output:** "Barney Rubble OG" (Barney is part of strain, not breeder)
**Confidence:** 90+ (requires context from URL)

### Case 5: Numbered Generations
**Input:** "Blue Dream F3"
**Output:** "Blue Dream" (remove generation marker)
**Confidence:** 92

## Batch Processing Strategy

### Batch Size: 50 Strains
- Balances API token limits with processing speed
- Allows AI to see patterns across multiple strains
- Reduces per-strain cost through batching

### Rate Limiting
- 1 second delay between batches
- Prevents API throttling
- Total runtime: ~7-8 minutes for 21,361 strains

### Error Handling
- Retry failed batches up to 3 times
- Log malformed JSON responses
- Continue processing even if individual batches fail

## Cost Optimization

### Token Efficiency
- Concise prompts (avoid verbose instructions)
- Batch processing (50 strains per call)
- JSON output format (structured, parseable)

### Estimated Token Usage
- **Prompt**: ~500 tokens (base rules + format)
- **Input per strain**: ~100 tokens (URL + extracted data)
- **Output per strain**: ~100 tokens (validation result)
- **Total per batch**: ~500 + (50 × 200) = 10,500 tokens
- **Cost per batch**: ~$0.0002

### Total Cost Estimate
- **428 batches** × $0.0002 = **$0.086**
- **Safety margin**: 10x = **$0.86**
- **Actual expected**: **$0.50-$1.00**

## Quality Assurance

### Post-Validation Checks
1. **Completeness**: All 21,361 strains processed
2. **Confidence distribution**: 90%+ should be high confidence (95+)
3. **Correction rate**: 2-5% corrections expected
4. **Flagged rate**: 2-7% flagged for review expected

### Manual Review Triggers
- Confidence < 90%
- Unusual correction patterns (e.g., AI removes numbers)
- Breeder = "Unknown" for direct breeder seed banks

### Validation Success Criteria
- 99%+ accuracy on strain names (post-review)
- 95%+ accuracy on breeder names
- <5% flagged for manual review
- <$2 total API cost

---

**Logic designed by Amazon Q, verified by Shannon Goddard.**

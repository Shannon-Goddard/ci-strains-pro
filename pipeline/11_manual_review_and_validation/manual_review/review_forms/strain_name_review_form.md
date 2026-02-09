# Strain Name Manual Review Form

**Reviewer:** Shannon Goddard  
**Date Started:** 02/04/2026  
**Total Strains:** 21,361  
**Sample Size Reviewed:** [NUMBER]

---

## Standardization Rules

### 1. Suffixes to Remove
List all suffixes that should be stripped from strain names:

| Suffix Pattern | Example | Cleaned Result |
|----------------|---------|----------------|
| Feminized | "Zkittlez Feminized" | "Zkittlez" |
| Auto | "Northern Lights Auto" | "Northern Lights" |
| Autoflower | "Gorilla Glue Autoflower" | "Gorilla Glue" |
| Regular | | |
| Seeds | | |
| [Add more] | | |

### 2. Prefixes to Remove
List prefixes that should be stripped (usually breeder names when redundant):

| Prefix Pattern | When to Remove | Example | Cleaned Result |
|----------------|----------------|---------|----------------|
| DNA | If breeder = "DNA Genetics" | "DNA Lemon Skunk" | "Lemon Skunk" |
| Barney's | If breeder = "Barney's Farm" | | |
| [Add more] | | | |

### 3. Pack Size Patterns to Remove
List pack size indicators to strip:

| Pattern | Example | Cleaned Result |
|---------|---------|----------------|
| [5pk] | "Zkittlez [5pk]" | "Zkittlez" |
| 3 pack | "OG Kush 3 pack" | "OG Kush" |
| (10 seeds) | | |
| [Add more] | | |

### 4. Code/ID Patterns to Remove
List strain codes or IDs to strip:

| Pattern | Example | Cleaned Result |
|---------|---------|----------------|
| BFS-XXX | "Blue Dream BFS-123" | "Blue Dream" |
| [Add more] | | |

### 5. Capitalization Rules

| Rule | Example | Standardized |
|------|---------|--------------|
| Title Case | "gorilla glue" | "Gorilla Glue" |
| Preserve # | "gorilla glue #4" | "Gorilla Glue #4" |
| Preserve ALL CAPS acronyms | "og kush" | "OG Kush" |
| [Add more] | | |

### 6. Special Character Rules

| Character | Action | Example | Result |
|-----------|--------|---------|--------|
| # | Keep | "Gorilla Glue #4" | "Gorilla Glue #4" |
| - (hyphen) | Keep | "Super-Skunk" | "Super-Skunk" |
| ' (apostrophe) | Keep | "Barney's Cookies" | "Barney's Cookies" |
| Multiple spaces | Replace with single | "Blue  Dream" | "Blue Dream" |
| [Add more] | | | |

### 7. Seed Bank Specific Patterns

| Seed Bank | Pattern | Action | Example | Result |
|-----------|---------|--------|---------|--------|
| Attitude | | | | |
| Crop King | | | | |
| ILGM | | | | |
| [Add more] | | | | |

### 8. Edge Cases & Exceptions

| Issue | Rule | Example | Standardized |
|-------|------|---------|--------------|
| Strain name = breeder name | Keep as-is | "Mephisto" by Mephisto | "Mephisto" |
| Numbers at start | Keep | "24K Gold" | "24K Gold" |
| [Add more] | | | |

---

## Validation Criteria

### High Confidence (0.95-1.0)
- [ ] No suffixes remaining
- [ ] No pack sizes remaining
- [ ] Proper capitalization
- [ ] No extra spaces
- [ ] Valid strain name format

### Medium Confidence (0.85-0.94)
- [ ] Minor capitalization issues
- [ ] Unusual but valid characters
- [ ] Very short names (1-2 words)

### Low Confidence (<0.85) - Flag for Review
- [ ] Contains numbers/codes that might be valid
- [ ] Unusual format
- [ ] Possible breeder prefix remaining
- [ ] Contains special characters not in rules

---

## Sample Findings

Document 10-20 examples you reviewed manually:

| Original Strain Name | Seed Bank | Issue Found | Standardized Name | Notes |
|---------------------|-----------|-------------|-------------------|-------|
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |

---

## Implementation Notes

**Priority Order for Cleaning:**
1. [First step - e.g., "Remove pack sizes"]
2. [Second step - e.g., "Remove suffixes"]
3. [Third step - e.g., "Remove breeder prefixes"]
4. [Fourth step - e.g., "Standardize capitalization"]
5. [Fifth step - e.g., "Clean special characters"]
6. [Final step - e.g., "Trim extra spaces"]

**Special Instructions for Amazon Q:**
- [Any specific logic or conditions]
- [Edge cases to handle carefully]
- [When to flag for manual review]

---

**Status:** [ ] In Progress  |  [ ] Complete  
**Ready for Standardization Script:** [ ] Yes  |  [ ] No

# Breeder Extraction - Seed Bank by Seed Bank Approach

**Date:** January 21, 2026  
**Strategy:** Individual extraction scripts per seed bank for maximum control and clarity

## Approach

Instead of one complex script handling all 19 seed banks, we'll create:
- One script per seed bank
- Each script extracts breeders for that seed bank only
- Shannon verifies each seed bank's results before moving to next
- Final merge script combines all verified extractions

## Seed Banks (Priority Order)

1. **Attitude** (7,673) - Breadcrumb extraction
2. **Crop King** (3,336) - Self-branded
3. **North Atlantic** (2,727) - Breeder link
4. **Gorilla** (2,000) - Product manufacturer
5. **Neptune** (1,995) - Breeder link
6. **Seedsman JS** (866) - Brand div
7. **Herbies** (753) - Strain brand link
8. **Multiverse** (528) - Brand tag
9. **Seed Supreme** (353) - Seedbank table
10. **Mephisto** (245) - Self-branded
11. **Exotic** (227) - Self-branded
12. **ILGM** (169) - JS-rendered span
13. **Amsterdam** (163) - Self-branded
14. **Sensi** (620) - Self-branded
15. **Barney's Farm** (88) - Self-branded
16. **Royal Queen** (67) - Self-branded
17. **Dutch Passion** (54) - Self-branded
18. **Seeds Here Now** (43) - Breadcrumb with dash
19. **Great Lakes** (16) - H3 with dash

## Files

- `extract_attitude.py` - Attitude Seed Bank extraction
- `extract_crop_king.py` - Crop King extraction
- `extract_north_atlantic.py` - North Atlantic extraction
- ... (one per seed bank)
- `merge_all_breeders.py` - Final merge script

## Workflow

1. Shannon: "Extract Attitude"
2. Amazon Q: Runs `extract_attitude.py`
3. Shannon: Reviews results, approves or requests fixes
4. Repeat for each seed bank
5. Final merge once all approved

**This approach trades efficiency for accuracy and control.**

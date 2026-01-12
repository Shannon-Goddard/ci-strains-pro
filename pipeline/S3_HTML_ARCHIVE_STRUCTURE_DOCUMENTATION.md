# CI-Strains-Pro S3 HTML Archive Structure Documentation

**Logic designed by Amazon Q, verified by Shannon Goddard.**

## 🎯 S3 Bucket Structure: `ci-strains-html-archive`

### **CRITICAL UNDERSTANDING:**
The S3 archive contains **15,778+ HTML files** with **corresponding metadata** - this is our **source of truth** for commercial CSV generation.

## 📁 Directory Structure

```
ci-strains-html-archive/
├── html/
│   ├── {url_hash}.html          # Actual HTML content (15,778+ files)
│   ├── ece6b937138e817a.html    # Example: Neptune strain page
│   ├── ef346f56027815d1.html    # Example: Large HTML file (995KB)
│   └── ...                      # All strain HTML files
└── metadata/
    ├── {url_hash}.json          # Metadata for each HTML file
    ├── ece6b937138e817a.json    # Example metadata
    └── ...                      # Corresponding metadata files
```

## 🔍 File Relationship

### HTML Files (`html/{hash}.html`)
- **Content**: Full HTML source of strain pages
- **Size Range**: 150KB - 1.1MB per file
- **Total Count**: 15,778+ files
- **Encoding**: UTF-8
- **Purpose**: Source data for strain extraction

### Metadata Files (`metadata/{hash}.json`)
- **Content**: Processing metadata and strain IDs
- **Size**: ~500-600 bytes per file
- **Purpose**: Mapping and validation data

### Example Metadata Structure:
```json
{
  "url": "https://neptuneseedbank.com/product/ab-seeds-rainbow-monk/",
  "url_hash": "ece6b937138e817a",
  "strain_ids": [11587],
  "collection_date": "2026-01-03T08:41:19.088892",
  "scrape_method": "direct",
  "validation_score": 0.75,
  "validation_checks": {
    "min_size": true,
    "has_title": true,
    "has_cannabis_content": true,
    "not_blocked": false,
    "not_error": false,
    "has_structure": true,
    "reasonable_size": true,
    "has_content": true
  },
  "html_size": 258638
}
```

## 🚀 Processing Strategy

### **CORRECT APPROACH:**
1. **Read metadata** to get URL and hash mapping
2. **Fetch HTML** from `html/{hash}.html`
3. **Apply 4-method extraction** on HTML content
4. **Generate CSV** with extracted strain data

### **WRONG APPROACH (What We Were Doing):**
- Looking for seed bank folders (dutch-passion/, mephisto/, etc.)
- These folders **DO NOT EXIST** in S3 archive
- HTML files are stored by **hash**, not seed bank name

## 📊 Data Volume

### HTML Files Available:
- **Total Files**: 15,778+ HTML files
- **File Sizes**: 150KB - 1.1MB each
- **Total Data**: ~2.5GB of HTML content
- **Coverage**: All major seed banks included

### Seed Bank Distribution (Estimated):
Based on original extractions:
- **Attitude Seedbank**: ~7,734 HTML files
- **North Atlantic**: ~2,934 HTML files  
- **Neptune**: ~2,048 HTML files
- **Multiverse Beans**: ~1,227 HTML files
- **Seedsman**: ~984 HTML files
- **Others**: ~1,000+ HTML files

## 🛠 Implementation Pattern

### Step 1: Create Metadata Processor
```python
# Read all metadata files to map URLs to hashes
metadata_files = s3_client.list_objects_v2(Bucket='ci-strains-html-archive', Prefix='metadata/')
```

### Step 2: Filter by Seed Bank
```python
# Filter metadata for specific seed bank URLs
neptune_files = [f for f in metadata if 'neptuneseedbank.com' in f['url']]
```

### Step 3: Process HTML Files
```python
# Fetch HTML using hash from metadata
html_content = s3_client.get_object(Bucket='ci-strains-html-archive', Key=f'html/{url_hash}.html')
```

### Step 4: Apply 4-Method Extraction
```python
# Use proven extraction patterns on HTML content
strain_data = apply_4_methods(html_content, url)
```

## 🎯 NEXT STEPS

### **IMMEDIATE ACTION:**
1. **Create universal S3 processor** that reads metadata first
2. **Filter by seed bank** from URL patterns
3. **Process HTML files** using proven 4-method extraction
4. **Generate commercial CSVs** for each seed bank

### **Expected Results:**
- **15,778 strain CSVs** ready for commercial sale
- **Source of truth preserved** (HTML files in S3)
- **Complete data coverage** across all seed banks

## 🚨 **CRITICAL REMINDER FOR FUTURE SESSIONS:**

**THE HTML FILES ARE IN S3 UNDER `html/{hash}.html`**
**NOT IN SEED BANK FOLDERS**
**USE METADATA TO MAP URLS TO HASHES**

This documentation should prevent the "wall we hit every session" by clearly explaining the S3 structure and correct processing approach.

## 🌿 Ready to Process!

With **15,778+ HTML files** in S3, we have the **complete source data** needed to generate comprehensive CSVs for commercial sale. The 4-method extraction approach will work perfectly on this data.

**Let's build the universal S3 processor and extract ALL the strain data!** 🚀
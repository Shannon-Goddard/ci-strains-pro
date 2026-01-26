# Breeder Name Extraction Patterns

**Purpose**: Document Failures In Breeder Extraction  
**Reviewer**: Shannon Goddard  
**Date**: January 22, 2026

---

## Instructions
pipeline\06_clean_dataset\output\11_breeder_extracted.csv  
For each seed breeder missing or typo:
1. Notate discrepancy


---

## Seed Breeders Extraction Failures

### Exotic Genetics  
**Note**:
```
All https://exoticgenetix.com/ breeder_name_extracted should be "Exotic Genetics"
- Printed as: long description of strain
- Should be: Exotic Genetics
```
### Barney's Farm  
**Note**:
```
All breeder_name_extracted from https://seedsherenow.com/
- Printed as: Barneyâ€™s Farm
- Should be: Barney's Farm

All breeder_name_extracted from https://www.cannabis-seeds-bank.co.uk/
- Printed as: Barneys Farm Seeds
- Should be: Barney's Farm
```

### Cali Connection  
**Note**:
```
https://www.cannabis-seeds-bank.co.uk/
- Printed as: Cali Connection Seeds
- Should be: Cali Connection

All breeder_name_extracted from https://www.cannabis-seeds-bank.co.uk/
- Printed as: Barneys Farm Seeds
- Should be: Barney's Farm
```
### Crop King 
**Note**:
```
All https://exoticgenetix.com/ breeder_name_extracted should be "Crop King"

```
### Crop King 
**Note**:
```
All https://www.cropkingseeds.com breeder_name_extracted should be "Crop King"

```
---

https://www.cropkingseeds.com may have more data filled in, but breeder_name_clean was better.
example: Twenty20 Mendocino	became Home/Seeds/Â Twenty 20 Genetics â€“ Glue Sniffer V2 (F) (6)


**Total seed bank's breeders**:   
**Failures documented**:  
**Ready for extraction**: 

---

**Next Steps**:
1. Shannon completes failure documentation
2. Amazon Q builds new seed-bank-specific extraction scripts
3. Re-extract breeder names from S3 HTML files
4. Merge with existing dataset
5. Verify 100% coverage

---

**Documented by**: Shannon Goddard  
**Scripts by**: Amazon Q

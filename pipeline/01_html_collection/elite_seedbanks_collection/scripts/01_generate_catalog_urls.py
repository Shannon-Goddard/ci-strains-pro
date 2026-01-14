#!/usr/bin/env python3
"""
Pipeline 06: Elite Seedbanks URL Generator
Generate all URLs based on known pagination patterns from chat.txt

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

def generate_elite_urls():
    """Generate all URLs based on chat.txt research"""
    
    urls = []
    
    # Herbies Head Shop - 21 pages feminized + 1 page regular
    print("Generating Herbies URLs...")
    for page in range(1, 22):
        urls.append({
            'url': f'https://herbiesheadshop.com/collections/feminized-seeds/page/{page}',
            'seedbank': 'Herbies Head Shop',
            'category': 'feminized'
        })
    urls.append({
        'url': 'https://herbiesheadshop.com/collections/regular-cannabis-seeds',
        'seedbank': 'Herbies Head Shop',
        'category': 'regular'
    })
    
    # Amsterdam Marijuana Seeds - 14 pages
    print("Generating Amsterdam URLs...")
    for page in range(1, 15):
        urls.append({
            'url': f'https://amsterdammarijuanaseeds.com/all-seeds/page/{page}/',
            'seedbank': 'Amsterdam Marijuana Seeds',
            'category': 'all'
        })
    
    # Gorilla Seeds Bank - 93 pages feminized + 33 pages auto
    print("Generating Gorilla URLs...")
    for page in range(1, 94):
        urls.append({
            'url': f'https://www.gorilla-cannabis-seeds.co.uk/feminized-seeds?page={page}',
            'seedbank': 'Gorilla Seeds Bank',
            'category': 'feminized'
        })
    for page in range(1, 34):
        urls.append({
            'url': f'https://www.gorilla-cannabis-seeds.co.uk/autoflowering-seeds?page={page}',
            'seedbank': 'Gorilla Seeds Bank',
            'category': 'autoflower'
        })
    
    # Zamnesia - 6 pages feminized + 4 pages auto
    print("Generating Zamnesia URLs...")
    for page in range(1, 7):
        urls.append({
            'url': f'https://www.zamnesia.com/us/295-feminized-seeds?p={page}',
            'seedbank': 'Zamnesia',
            'category': 'feminized'
        })
    for page in range(1, 5):
        urls.append({
            'url': f'https://www.zamnesia.com/us/294-autoflower-seeds?p={page}',
            'seedbank': 'Zamnesia',
            'category': 'autoflower'
        })
    
    # Exotic Genetix - 22 pages
    print("Generating Exotic Genetix URLs...")
    for page in range(1, 23):
        urls.append({
            'url': f'https://exoticgenetix.com/shop/page/{page}/',
            'seedbank': 'Exotic Genetix',
            'category': 'all'
        })
    
    # Original Seeds Store - 2 single pages
    print("Generating Original Seeds Store URLs...")
    urls.append({
        'url': 'https://www.originalseedsstore.com/feminized-cannabis-seeds',
        'seedbank': 'Original Seeds Store',
        'category': 'feminized'
    })
    urls.append({
        'url': 'https://www.originalseedsstore.com/regular-seeds',
        'seedbank': 'Original Seeds Store',
        'category': 'regular'
    })
    
    # Tiki Madman - 1 page
    print("Generating Tiki Madman URLs...")
    urls.append({
        'url': 'https://tikimadman.com/strains/',
        'seedbank': 'Tiki Madman',
        'category': 'all'
    })
    
    # Compound Genetics - 4 collections
    print("Generating Compound Genetics URLs...")
    collections = [
        'grape-gasoline',
        'eye-candy',
        'jokerz-volume-2',
        'jokerz-vol-1'
    ]
    for collection in collections:
        urls.append({
            'url': f'https://seeds.compound-genetics.com/collections/{collection}',
            'seedbank': 'Compound Genetics',
            'category': collection
        })
    
    return urls

def save_to_database(urls, db_path):
    """Save URLs to database"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS elite_urls (
            url_hash TEXT PRIMARY KEY,
            original_url TEXT NOT NULL,
            seedbank TEXT NOT NULL,
            category TEXT,
            discovered_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            attempts INTEGER DEFAULT 0
        )
    ''')
    
    # Insert URLs
    added = 0
    for url_data in urls:
        url_hash = hashlib.sha256(url_data['url'].encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT OR IGNORE INTO elite_urls 
            (url_hash, original_url, seedbank, category)
            VALUES (?, ?, ?, ?)
        ''', (url_hash, url_data['url'], url_data['seedbank'], url_data['category']))
        
        if cursor.rowcount > 0:
            added += 1
    
    conn.commit()
    conn.close()
    
    return added

def generate_report(urls, db_path):
    """Generate discovery report"""
    
    # Count by seedbank
    seedbank_counts = {}
    for url_data in urls:
        seedbank = url_data['seedbank']
        seedbank_counts[seedbank] = seedbank_counts.get(seedbank, 0) + 1
    
    report = f"""
# Pipeline 06: Elite Seedbanks URL Generation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## URL Generation Summary
- **Total Catalog Pages Generated**: {len(urls):,}
- **Method**: Direct generation from known pagination patterns

## Breakdown by Seedbank
"""
    
    for seedbank, count in sorted(seedbank_counts.items(), key=lambda x: x[1], reverse=True):
        report += f"- **{seedbank}**: {count:,} catalog pages\n"
    
    report += f"""
## Next Steps
1. Run bulletproof HTML collection on ALL {len(urls):,} catalog pages
2. Extract individual product URLs from each catalog page
3. Collect HTML for all individual product pages
4. Extract maximum value using Dutch Passion methodology
5. **BREAK 20,000 STRAINS!**

## Expected Results
- Herbies: ~440 strains
- Amsterdam: ~168 strains
- Gorilla: ~1,260 strains
- Zamnesia: ~759 strains
- Exotic: ~330 strains
- Original: ~56 strains
- Tiki: ~41 strains
- Compound: ~29 strains

**Total Expected: ~3,083 strains**
**New Database Total: 20,326 strains**

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
    
    report_path = Path(db_path).parent / 'elite_url_generation_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport saved: {report_path}")
    
    # Also save flat URL list
    urls_file = Path(db_path).parent / 'elite_catalog_urls.txt'
    with open(urls_file, 'w') as f:
        for url_data in urls:
            f.write(url_data['url'] + '\n')
    
    print(f"URL list saved: {urls_file}")

def main():
    """Main execution"""
    
    print("="*60)
    print("PIPELINE 06: ELITE SEEDBANKS URL GENERATION")
    print("="*60)
    
    # Generate URLs
    urls = generate_elite_urls()
    
    print(f"\nGenerated {len(urls):,} catalog page URLs")
    
    # Save to database
    db_path = "../data/elite_catalog_urls.db"
    Path(db_path).parent.mkdir(exist_ok=True)
    
    added = save_to_database(urls, db_path)
    print(f"Saved {added:,} URLs to database")
    
    # Generate report
    generate_report(urls, db_path)
    
    print("\n" + "="*60)
    print("URL GENERATION COMPLETE!")
    print("="*60)
    print(f"Total catalog pages: {len(urls):,}")
    print("Ready for bulletproof HTML collection!")
    print("="*60)

if __name__ == "__main__":
    main()

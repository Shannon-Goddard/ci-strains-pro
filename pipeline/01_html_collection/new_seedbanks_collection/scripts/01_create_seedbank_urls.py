#!/usr/bin/env python3
"""
Cannabis Intelligence Database - New Seedbanks URL Discovery
Creates database of strain URLs from 5 premium seedbanks

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import configuration
import sys
sys.path.append('../config')
try:
    from scraper_config import SEEDBANKS
except ImportError:
    # Fallback if import fails
    SEEDBANKS = {
        "sensi_seeds": {
            "name": "Sensi Seeds",
            "category_url": "https://sensiseeds.us/cannabis-seeds/",
            "domain": "sensiseeds.us",
            "product_example": "https://sensiseeds.com/en/feminized-seeds/sensi-seeds/big-bud-feminized"
        },
        "humboldt": {
            "name": "Humboldt Seed Company", 
            "category_url": "https://californiahempseeds.com/shop-all/",
            "domain": "californiahempseeds.com",
            "product_example": "https://humboldtseedcompany.com/appleblossom/"
        },
        "crop_king": {
            "name": "Crop King",
            "category_url": "https://www.cropkingseeds.com/?s=seeds&post_type=product&dgwt_wcas=1",
            "domain": "cropkingseeds.com", 
            "product_example": "https://www.cropkingseeds.com/feminized-seeds/permanent-marker-strain-feminized-marijuana-seeds/"
        },
        "barneys_farm": {
            "name": "Barney's Farm",
            "category_url": "https://www.barneysfarm.com/us/",
            "domain": "barneysfarm.com",
            "product_example": "https://www.barneysfarm.com/us/pineapple-express-auto-autoflower-strain-37"
        },
        "ilgm": {
            "name": "ILGM",
            "category_url": "https://ilgm.com/categories/cannabis-seeds", 
            "domain": "ilgm.com",
            "product_example": "https://ilgm.com/products/blue-dream-autoflower-seeds?variant=UHJvZHVjdFZhcmlhbnQ6NzI="
        }
    }

class SeedbankURLDatabase:
    """Create URL database for new seedbanks collection"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_database()
    
    def create_database(self):
        """Create SQLite database with same structure as pipeline/01"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Same table structure as pipeline/01
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_progress (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                strain_ids TEXT NOT NULL,
                seedbank TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                html_size INTEGER,
                validation_score REAL,
                s3_path TEXT,
                error_message TEXT,
                scrape_method TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database created: {self.db_path}")
    
    def generate_url_hash(self, url: str) -> str:
        """Generate 16-character hash for URL (same method as pipeline/01)"""
        return hashlib.sha256(url.encode()).hexdigest()[:16]
    
    def add_manual_urls(self):
        """Add the provided example URLs as starting points"""
        
        manual_urls = [
            ("sensi_seeds", "https://sensiseeds.com/en/feminized-seeds/sensi-seeds/big-bud-feminized"),
            ("humboldt", "https://humboldtseedcompany.com/appleblossom/"),
            ("crop_king", "https://www.cropkingseeds.com/feminized-seeds/permanent-marker-strain-feminized-marijuana-seeds/"),
            ("barneys_farm", "https://www.barneysfarm.com/us/pineapple-express-auto-autoflower-strain-37"),
            ("ilgm", "https://ilgm.com/products/blue-dream-autoflower-seeds?variant=UHJvZHVjdFZhcmlhbnQ6NzI=")
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for seedbank_key, url in manual_urls:
            url_hash = self.generate_url_hash(url)
            seedbank_name = SEEDBANKS[seedbank_key]["name"]
            
            # Create strain_ids as JSON array (single ID for manual URLs)
            strain_ids = json.dumps([f"manual_{seedbank_key}_001"])
            
            cursor.execute('''
                INSERT OR IGNORE INTO scraping_progress 
                (url_hash, original_url, strain_ids, seedbank, status)
                VALUES (?, ?, ?, ?, 'pending')
            ''', (url_hash, url, strain_ids, seedbank_name))
            
            logger.info(f"Added manual URL: {seedbank_name} - {url}")
        
        conn.commit()
        
        # Get count
        cursor.execute('SELECT COUNT(*) FROM scraping_progress')
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"Manual URLs added. Total URLs in database: {total_count}")
        return total_count
    
    def generate_report(self):
        """Generate URL discovery report"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get statistics by seedbank
        cursor.execute('''
            SELECT seedbank, COUNT(*) as url_count
            FROM scraping_progress 
            GROUP BY seedbank
            ORDER BY url_count DESC
        ''')
        
        seedbank_stats = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) FROM scraping_progress')
        total_urls = cursor.fetchone()[0]
        
        conn.close()
        
        # Generate report
        report = f"""
# Cannabis Intelligence Database - New Seedbanks URL Discovery Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## URL Discovery Summary
- **Total URLs**: {total_urls:,}

## Seedbank Breakdown
"""
        
        for seedbank, count in seedbank_stats:
            report += f"- **{seedbank}**: {count:,} URLs\n"
        
        report += """
## Next Steps
1. Run `02_bulletproof_scraper.py` to collect HTML
2. Monitor progress with `03_progress_monitor.py --watch`
3. URLs will be added to existing S3 archive seamlessly

## Integration Notes
- Same S3 bucket: ci-strains-html-archive
- Same validation thresholds: 75%
- Same retry logic: 6 attempts max
- Same encryption: AES-256

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = Path(self.db_path).parent / 'url_discovery_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Report saved: {report_path}")

def main():
    """Main execution function"""
    
    # Configuration
    db_path = "../data/new_seedbanks_progress.db"
    
    # Ensure data directory exists
    Path(db_path).parent.mkdir(exist_ok=True)
    
    # Create database
    url_db = SeedbankURLDatabase(db_path)
    
    # Add manual URLs as starting points
    total_urls = url_db.add_manual_urls()
    
    # Generate report
    url_db.generate_report()
    
    print("\n" + "="*60)
    print("NEW SEEDBANKS URL DISCOVERY COMPLETE")
    print("="*60)
    print(f"Database created: {db_path}")
    print(f"Total URLs ready: {total_urls}")
    print("Ready for HTML collection!")
    print("\nNext steps:")
    print("1. python scripts/02_bulletproof_scraper.py")
    print("2. python scripts/03_progress_monitor.py --watch")
    print("="*60)

if __name__ == "__main__":
    main()
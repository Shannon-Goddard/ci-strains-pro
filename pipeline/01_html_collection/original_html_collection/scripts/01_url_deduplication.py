#!/usr/bin/env python3
"""
Cannabis Intelligence Database - URL Deduplication Script
Processes 15,778 strain records to identify unique URLs for HTML collection

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import pandas as pd
import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/url_deduplication.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class URLDeduplicator:
    def __init__(self, csv_path, output_dir):
        self.csv_path = csv_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def load_strain_data(self):
        """Load and validate strain data from CSV"""
        logger.info(f"Loading strain data from {self.csv_path}")
        
        try:
            df = pd.read_csv(self.csv_path, encoding='latin-1')
            logger.info(f"Loaded {len(df)} strain records")
            
            # Validate required columns
            required_cols = ['source_url', 'strain_id', 'strain_name', 'scraped_at']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
                
            return df
            
        except Exception as e:
            logger.error(f"Error loading CSV: {e}")
            raise
    
    def clean_urls(self, df):
        """Clean and validate URLs"""
        logger.info("Cleaning and validating URLs")
        
        # Remove rows with null URLs
        initial_count = len(df)
        df = df.dropna(subset=['source_url'])
        logger.info(f"Removed {initial_count - len(df)} records with null URLs")
        
        # Strip whitespace
        df['source_url'] = df['source_url'].str.strip()
        
        # Remove empty URLs
        df = df[df['source_url'] != '']
        logger.info(f"Final URL count: {len(df)}")
        
        return df
    
    def deduplicate_urls(self, df):
        """
        Deduplicate URLs and create mapping structure
        Returns: {url_hash: {url, strain_ids[], first_seen, metadata}}
        """
        logger.info("Starting URL deduplication process")
        
        url_map = {}
        duplicate_count = 0
        
        for idx, row in df.iterrows():
            url = row['source_url']
            strain_id = row['strain_id']
            strain_name = row['strain_name']
            scraped_at = row['scraped_at']
            
            # Create consistent hash
            url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:16]
            
            if url_hash not in url_map:
                # First occurrence of this URL
                url_map[url_hash] = {
                    'url': url,
                    'strain_ids': [strain_id],
                    'strain_names': [strain_name],
                    'first_seen': scraped_at,
                    'occurrence_count': 1,
                    'status': 'pending'
                }
            else:
                # Duplicate URL found
                url_map[url_hash]['strain_ids'].append(strain_id)
                url_map[url_hash]['strain_names'].append(strain_name)
                url_map[url_hash]['occurrence_count'] += 1
                duplicate_count += 1
        
        unique_urls = len(url_map)
        total_records = len(df)
        dedup_percentage = (duplicate_count / total_records) * 100
        
        logger.info(f"Deduplication Results:")
        logger.info(f"  Total records: {total_records:,}")
        logger.info(f"  Unique URLs: {unique_urls:,}")
        logger.info(f"  Duplicates removed: {duplicate_count:,}")
        logger.info(f"  Deduplication rate: {dedup_percentage:.1f}%")
        
        return url_map
    
    def create_progress_database(self, url_map):
        """Create SQLite database for progress tracking"""
        db_path = self.output_dir / 'scraping_progress.db'
        logger.info(f"Creating progress database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_progress (
                url_hash TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                strain_ids TEXT NOT NULL,
                strain_names TEXT NOT NULL,
                occurrence_count INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                html_size INTEGER,
                validation_score REAL,
                s3_path TEXT,
                error_message TEXT,
                scrape_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collection_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_urls INTEGER,
                completed INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                avg_html_size INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert URL data
        for url_hash, data in url_map.items():
            cursor.execute('''
                INSERT OR REPLACE INTO scraping_progress 
                (url_hash, original_url, strain_ids, strain_names, occurrence_count, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                url_hash,
                data['url'],
                json.dumps(data['strain_ids']),
                json.dumps(data['strain_names']),
                data['occurrence_count'],
                data['status']
            ))
        
        # Insert initial stats
        cursor.execute('''
            INSERT OR REPLACE INTO collection_stats (id, total_urls)
            VALUES (1, ?)
        ''', (len(url_map),))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database created with {len(url_map)} URLs")
        return db_path
    
    def save_url_mapping(self, url_map):
        """Save URL mapping to JSON and CSV files"""
        
        # Save as JSON for programmatic access
        json_path = self.output_dir / 'url_mapping.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(url_map, f, indent=2, ensure_ascii=False)
        logger.info(f"URL mapping saved to {json_path}")
        
        # Save as CSV for analysis
        csv_data = []
        for url_hash, data in url_map.items():
            csv_data.append({
                'url_hash': url_hash,
                'url': data['url'],
                'strain_count': len(data['strain_ids']),
                'strain_ids': ','.join(map(str, data['strain_ids'])),
                'first_seen': data['first_seen'],
                'status': data['status']
            })
        
        csv_path = self.output_dir / 'unique_urls.csv'
        pd.DataFrame(csv_data).to_csv(csv_path, index=False)
        logger.info(f"URL CSV saved to {csv_path}")
        
        return json_path, csv_path
    
    def generate_summary_report(self, url_map):
        """Generate deduplication summary report"""
        
        # Calculate statistics
        total_urls = len(url_map)
        single_strain_urls = sum(1 for data in url_map.values() if data['occurrence_count'] == 1)
        multi_strain_urls = total_urls - single_strain_urls
        max_strains_per_url = max(data['occurrence_count'] for data in url_map.values())
        
        # Domain analysis
        domain_counts = {}
        for data in url_map.values():
            try:
                from urllib.parse import urlparse
                domain = urlparse(data['url']).netloc
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
            except:
                domain_counts['invalid'] = domain_counts.get('invalid', 0) + 1
        
        top_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Generate report
        report = f"""
# Cannabis Intelligence Database - URL Deduplication Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary Statistics
- **Total Unique URLs**: {total_urls:,}
- **Single-strain URLs**: {single_strain_urls:,} ({single_strain_urls/total_urls*100:.1f}%)
- **Multi-strain URLs**: {multi_strain_urls:,} ({multi_strain_urls/total_urls*100:.1f}%)
- **Max strains per URL**: {max_strains_per_url}

## Top Domains
"""
        
        for domain, count in top_domains:
            percentage = (count / total_urls) * 100
            report += f"- **{domain}**: {count:,} URLs ({percentage:.1f}%)\n"
        
        report += f"""
## Collection Readiness
✅ URLs deduplicated and validated
✅ Progress database created
✅ Mapping files generated
✅ Ready for bulletproof scraping

## Next Steps
1. Run `02_bulletproof_scraper.py` to begin HTML collection
2. Monitor progress via `scraping_progress.db`
3. Handle failures with retry mechanisms
4. Validate collected HTML quality

---
*Logic designed by Amazon Q, verified by Shannon Goddard*
"""
        
        report_path = self.output_dir / 'deduplication_report.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"Summary report saved to {report_path}")
        return report_path
    
    def run(self):
        """Execute the complete deduplication process"""
        logger.info("Starting URL deduplication process")
        start_time = datetime.now()
        
        try:
            # Load and clean data
            df = self.load_strain_data()
            df = self.clean_urls(df)
            
            # Deduplicate URLs
            url_map = self.deduplicate_urls(df)
            
            # Create outputs
            db_path = self.create_progress_database(url_map)
            json_path, csv_path = self.save_url_mapping(url_map)
            report_path = self.generate_summary_report(url_map)
            
            # Final summary
            duration = datetime.now() - start_time
            logger.info(f"Deduplication completed in {duration}")
            logger.info(f"Ready to collect HTML for {len(url_map):,} unique URLs")
            
            return {
                'unique_urls': len(url_map),
                'database_path': str(db_path),
                'json_path': str(json_path),
                'csv_path': str(csv_path),
                'report_path': str(report_path)
            }
            
        except Exception as e:
            logger.error(f"Deduplication failed: {e}")
            raise

def main():
    """Main execution function"""
    
    # Configuration
    csv_path = "../../../Cannabis_Database_Validated_Complete.csv"
    output_dir = "../data"
    
    # Run deduplication
    deduplicator = URLDeduplicator(csv_path, output_dir)
    results = deduplicator.run()
    
    print("\n" + "="*60)
    print("CANNABIS INTELLIGENCE - URL DEDUPLICATION COMPLETE")
    print("="*60)
    print(f"Unique URLs identified: {results['unique_urls']:,}")
    print(f"Database created: {results['database_path']}")
    print(f"Report generated: {results['report_path']}")
    print("\nReady for bulletproof HTML collection!")
    print("="*60)

if __name__ == "__main__":
    main()
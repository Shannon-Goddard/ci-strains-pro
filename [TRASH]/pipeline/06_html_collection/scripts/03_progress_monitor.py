#!/usr/bin/env python3
"""
Cannabis Intelligence Database - Progress Monitor & Recovery
Real-time monitoring and recovery tools for HTML collection

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import sqlite3
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ProgressMonitor:
    """Monitor and manage HTML collection progress"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        
    def get_overall_stats(self):
        """Get overall collection statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN status = 'processing' THEN 1 ELSE 0 END) as processing,
                AVG(CASE WHEN status = 'success' THEN html_size ELSE NULL END) as avg_html_size,
                AVG(CASE WHEN status = 'success' THEN validation_score ELSE NULL END) as avg_validation_score
            FROM scraping_progress
        ''')
        
        stats = cursor.fetchone()
        conn.close()
        
        total, success, failed, pending, processing, avg_size, avg_score = stats
        
        return {
            'total': total,
            'success': success,
            'failed': failed,
            'pending': pending,
            'processing': processing,
            'success_rate': (success / total * 100) if total > 0 else 0,
            'avg_html_size': int(avg_size) if avg_size else 0,
            'avg_validation_score': round(avg_score, 3) if avg_score else 0
        }
    
    def get_method_stats(self):
        """Get statistics by scraping method"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                scrape_method,
                COUNT(*) as count,
                AVG(validation_score) as avg_score
            FROM scraping_progress 
            WHERE status = 'success' AND scrape_method IS NOT NULL
            GROUP BY scrape_method
            ORDER BY count DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'method': r[0], 'count': r[1], 'avg_score': round(r[2], 3)} for r in results]
    
    def get_domain_stats(self):
        """Get statistics by domain"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                CASE 
                    WHEN original_url LIKE '%seedsman.com%' THEN 'seedsman.com'
                    WHEN original_url LIKE '%attitude.co.uk%' THEN 'attitude.co.uk'
                    WHEN original_url LIKE '%northatlanticseed.com%' THEN 'northatlanticseed.com'
                    WHEN original_url LIKE '%neptuneseedbank.com%' THEN 'neptuneseedbank.com'
                    WHEN original_url LIKE '%multiversebeans.com%' THEN 'multiversebeans.com'
                    WHEN original_url LIKE '%seedsherenow.com%' THEN 'seedsherenow.com'
                    WHEN original_url LIKE '%mephistogenetics.com%' THEN 'mephistogenetics.com'
                    ELSE 'other'
                END as domain,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
            FROM scraping_progress
            GROUP BY domain
            ORDER BY total DESC
        ''')
        
        results = cursor.fetchall()
        
        return [{
            'domain': r[0], 
            'total': r[1], 
            'success': r[2], 
            'failed': r[3],
            'success_rate': round((r[2] / r[1] * 100), 1) if r[1] > 0 else 0
        } for r in results]
    
    def get_failed_urls(self, limit: int = 50):
        """Get failed URLs for manual review"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT url_hash, original_url, attempts, error_message, last_attempt
            FROM scraping_progress 
            WHERE status = 'failed'
            ORDER BY last_attempt DESC
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'url_hash': r[0],
            'url': r[1],
            'attempts': r[2],
            'error': r[3],
            'last_attempt': r[4]
        } for r in results]
    
    def reset_failed_urls(self, max_attempts: int = 3):
        """Reset failed URLs for retry (if attempts < max_attempts)"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scraping_progress 
            SET status = 'pending', error_message = NULL
            WHERE status = 'failed' AND attempts < ?
        ''', (max_attempts,))
        
        reset_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Reset {reset_count} failed URLs for retry")
        return reset_count
    
    def reset_processing_urls(self, timeout_minutes: int = 30):
        """Reset URLs stuck in 'processing' status"""
        
        timeout_time = datetime.now() - timedelta(minutes=timeout_minutes)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scraping_progress 
            SET status = 'pending'
            WHERE status = 'processing' AND last_attempt < ?
        ''', (timeout_time.isoformat(),))
        
        reset_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Reset {reset_count} stuck processing URLs")
        return reset_count
    
    def export_failed_urls(self, output_file: str):
        """Export failed URLs to CSV for manual review"""
        
        failed_urls = self.get_failed_urls(limit=1000)
        
        import pandas as pd
        df = pd.DataFrame(failed_urls)
        df.to_csv(output_file, index=False)
        
        logger.info(f"Exported {len(failed_urls)} failed URLs to {output_file}")
        return len(failed_urls)
    
    def display_dashboard(self):
        """Display real-time progress dashboard"""
        
        stats = self.get_overall_stats()
        method_stats = self.get_method_stats()
        domain_stats = self.get_domain_stats()
        
        print("\n" + "="*80)
        print("🌿 CANNABIS INTELLIGENCE - HTML COLLECTION DASHBOARD")
        print("="*80)
        
        # Overall Progress
        print(f"\n📊 OVERALL PROGRESS")
        print(f"   Total URLs: {stats['total']:,}")
        print(f"   ✅ Success: {stats['success']:,} ({stats['success_rate']:.1f}%)")
        print(f"   ❌ Failed: {stats['failed']:,}")
        print(f"   ⏳ Pending: {stats['pending']:,}")
        print(f"   🔄 Processing: {stats['processing']:,}")
        
        if stats['success'] > 0:
            print(f"\n📈 QUALITY METRICS")
            print(f"   Average HTML Size: {stats['avg_html_size']:,} bytes")
            print(f"   Average Validation Score: {stats['avg_validation_score']}")
        
        # Method Performance
        if method_stats:
            print(f"\n🔧 SCRAPING METHOD PERFORMANCE")
            for method in method_stats:
                print(f"   {method['method']}: {method['count']:,} URLs (score: {method['avg_score']})")
        
        # Domain Performance
        print(f"\n🌐 DOMAIN PERFORMANCE")
        for domain in domain_stats[:10]:  # Top 10 domains
            print(f"   {domain['domain']}: {domain['success']:,}/{domain['total']:,} ({domain['success_rate']:.1f}%)")
        
        # Progress Bar
        if stats['total'] > 0:
            progress = stats['success'] / stats['total']
            bar_length = 50
            filled_length = int(bar_length * progress)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            print(f"\n📊 Progress: [{bar}] {progress*100:.1f}%")
        
        print("\n" + "="*80)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)

def main():
    """Main CLI interface"""
    
    parser = argparse.ArgumentParser(description='Cannabis Intelligence HTML Collection Monitor')
    parser.add_argument('--db', default='../data/scraping_progress.db', help='Database path')
    parser.add_argument('--action', choices=['dashboard', 'reset-failed', 'reset-stuck', 'export-failed'], 
                       default='dashboard', help='Action to perform')
    parser.add_argument('--watch', action='store_true', help='Watch mode (refresh every 30 seconds)')
    parser.add_argument('--output', help='Output file for export-failed action')
    
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        logger.error(f"Database not found: {args.db}")
        return
    
    monitor = ProgressMonitor(args.db)
    
    if args.action == 'dashboard':
        if args.watch:
            try:
                while True:
                    monitor.display_dashboard()
                    time.sleep(30)
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
        else:
            monitor.display_dashboard()
    
    elif args.action == 'reset-failed':
        count = monitor.reset_failed_urls()
        print(f"Reset {count} failed URLs for retry")
    
    elif args.action == 'reset-stuck':
        count = monitor.reset_processing_urls()
        print(f"Reset {count} stuck processing URLs")
    
    elif args.action == 'export-failed':
        output_file = args.output or f"failed_urls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        count = monitor.export_failed_urls(output_file)
        print(f"Exported {count} failed URLs to {output_file}")

if __name__ == "__main__":
    main()
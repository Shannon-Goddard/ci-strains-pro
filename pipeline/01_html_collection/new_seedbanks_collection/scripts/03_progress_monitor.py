#!/usr/bin/env python3
"""
Cannabis Intelligence Database - New Seedbanks Progress Monitor
Real-time monitoring and recovery for HTML collection

Author: Amazon Q (Logic designed by Amazon Q, verified by Shannon Goddard)
Date: January 2026
"""

import sqlite3
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewSeedbanksProgressMonitor:
    """Progress monitoring and recovery for new seedbanks collection"""
    
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
                AVG(CASE WHEN status = 'success' THEN validation_score END) as avg_score,
                AVG(CASE WHEN status = 'success' THEN html_size END) as avg_size
            FROM scraping_progress
        ''')
        
        stats = cursor.fetchone()
        conn.close()
        
        return {
            'total': stats[0],
            'success': stats[1] or 0,
            'failed': stats[2] or 0,
            'pending': stats[3] or 0,
            'processing': stats[4] or 0,
            'avg_score': stats[5] or 0,
            'avg_size': stats[6] or 0
        }
    
    def get_seedbank_stats(self):
        """Get statistics by seedbank"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                seedbank,
                COUNT(*) as total,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM scraping_progress 
            GROUP BY seedbank
            ORDER BY success DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        return [{'seedbank': r[0], 'total': r[1], 'success': r[2], 'failed': r[3], 'pending': r[4]} for r in results]
    
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
        
        return [{'method': r[0], 'count': r[1], 'avg_score': r[2]} for r in results]
    
    def display_dashboard(self):
        """Display real-time dashboard"""
        
        stats = self.get_overall_stats()
        seedbank_stats = self.get_seedbank_stats()
        method_stats = self.get_method_stats()
        
        # Clear screen (Windows)
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("CANNABIS INTELLIGENCE - NEW SEEDBANKS COLLECTION DASHBOARD")
        print("=" * 80)
        print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Overall Progress
        if stats['total'] > 0:
            success_rate = (stats['success'] / stats['total']) * 100
            progress_bar = "#" * int(success_rate / 2) + "-" * (50 - int(success_rate / 2))
            
            print("OVERALL PROGRESS")
            print("-" * 40)
            print(f"Progress: [{progress_bar}] {success_rate:.1f}%")
            print(f"Total URLs: {stats['total']:,}")
            print(f"Success: {stats['success']:,} ({success_rate:.1f}%)")
            print(f"Failed: {stats['failed']:,}")
            print(f"Pending: {stats['pending']:,}")
            print(f"Processing: {stats['processing']:,}")
            
            if stats['avg_score'] > 0:
                print(f"Avg Quality Score: {stats['avg_score']:.3f}")
            if stats['avg_size'] > 0:
                print(f"Avg HTML Size: {int(stats['avg_size']):,} bytes")
        
        print()
        
        # Seedbank Performance
        if seedbank_stats:
            print("SEEDBANK PERFORMANCE")
            print("-" * 40)
            for sb in seedbank_stats:
                if sb['total'] > 0:
                    success_rate = (sb['success'] / sb['total']) * 100
                    print(f"{sb['seedbank']:<25} {sb['success']:>3}/{sb['total']:<3} ({success_rate:>5.1f}%)")
        
        print()
        
        # Method Performance
        if method_stats:
            print("SCRAPING METHOD PERFORMANCE")
            print("-" * 40)
            for method in method_stats:
                print(f"{method['method']:<15} {method['count']:>4} successes (score: {method['avg_score']:.3f})")
        
        print()
        print("=" * 80)
        print("Commands: --action dashboard | --action reset-failed | --action export-failed")
        print("=" * 80)
    
    def reset_failed_urls(self):
        """Reset failed URLs for retry (if attempts < max)"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE scraping_progress 
            SET status = 'pending', error_message = NULL
            WHERE status = 'failed' AND attempts < 6
        ''')
        
        reset_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Reset {reset_count} failed URLs for retry")
        return reset_count
    
    def reset_stuck_processing(self):
        """Reset stuck processing URLs (30min timeout)"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Reset URLs stuck in processing for more than 30 minutes
        timeout_time = (datetime.now() - timedelta(minutes=30)).isoformat()
        
        cursor.execute('''
            UPDATE scraping_progress 
            SET status = 'pending'
            WHERE status = 'processing' AND last_attempt < ?
        ''', (timeout_time,))
        
        reset_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        logger.info(f"Reset {reset_count} stuck processing URLs")
        return reset_count
    
    def export_failed_urls(self, output_file: str):
        """Export failed URLs for manual review"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT original_url, seedbank, attempts, error_message
            FROM scraping_progress 
            WHERE status = 'failed'
            ORDER BY seedbank, original_url
        ''')
        
        failed_urls = cursor.fetchall()
        conn.close()
        
        # Write CSV
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("url,seedbank,attempts,error_message\n")
            for url, seedbank, attempts, error in failed_urls:
                error_clean = (error or '').replace('"', '""')
                f.write(f'"{url}","{seedbank}",{attempts},"{error_clean}"\n')
        
        logger.info(f"Exported {len(failed_urls)} failed URLs to {output_file}")
        return len(failed_urls)
    
    def watch_progress(self, refresh_interval: int = 30):
        """Watch progress with auto-refresh"""
        
        logger.info(f"Starting progress monitor (refresh every {refresh_interval}s)")
        logger.info("Press Ctrl+C to stop")
        
        try:
            while True:
                self.display_dashboard()
                time.sleep(refresh_interval)
        except KeyboardInterrupt:
            logger.info("Progress monitoring stopped")

def main():
    """Main execution function"""
    
    parser = argparse.ArgumentParser(description='New Seedbanks Collection Progress Monitor')
    parser.add_argument('--action', choices=['dashboard', 'reset-failed', 'reset-stuck', 'export-failed', 'watch'], 
                       default='dashboard', help='Action to perform')
    parser.add_argument('--output', help='Output file for export-failed action')
    parser.add_argument('--refresh', type=int, default=30, help='Refresh interval for watch mode (seconds)')
    
    args = parser.parse_args()
    
    # Configuration
    db_path = "../data/new_seedbanks_progress.db"
    
    # Verify database exists
    if not Path(db_path).exists():
        logger.error(f"Database not found: {db_path}")
        logger.error("Please run 01_create_seedbank_urls.py first")
        return
    
    # Create monitor
    monitor = NewSeedbanksProgressMonitor(db_path)
    
    # Execute action
    if args.action == 'dashboard':
        monitor.display_dashboard()
    
    elif args.action == 'watch':
        monitor.watch_progress(args.refresh)
    
    elif args.action == 'reset-failed':
        count = monitor.reset_failed_urls()
        print(f"Reset {count} failed URLs for retry")
    
    elif args.action == 'reset-stuck':
        count = monitor.reset_stuck_processing()
        print(f"Reset {count} stuck processing URLs")
    
    elif args.action == 'export-failed':
        output_file = args.output or f"../data/failed_urls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        count = monitor.export_failed_urls(output_file)
        print(f"Exported {count} failed URLs to {output_file}")

if __name__ == "__main__":
    main()
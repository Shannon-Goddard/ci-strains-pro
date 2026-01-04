#!/usr/bin/env python3
"""
Comprehensive retry system for all failed URLs
"""
import sqlite3
import asyncio
import aiohttp
import random
import time
from pathlib import Path

class ComprehensiveRetrier:
    def __init__(self):
        self.db_path = '../data/scraping_progress.db'
        
    def get_all_failed_urls(self):
        """Get all failed URLs for retry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT url_hash, original_url, strain_names, attempts 
            FROM scraping_progress 
            WHERE status = "failed"
        ''')
        
        failed_urls = cursor.fetchall()
        conn.close()
        
        print(f"Found {len(failed_urls)} failed URLs to retry")
        return failed_urls
    
    def update_retry_status(self, url_hash, status, html_content=None, error_msg=None):
        """Update database with retry results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status == 'success':
            cursor.execute('''
                UPDATE scraping_progress 
                SET status = "completed", html_size = ?, validation_score = 0.8,
                    attempts = attempts + 1, last_attempt = datetime('now')
                WHERE url_hash = ?
            ''', (len(html_content), url_hash))
        else:
            cursor.execute('''
                UPDATE scraping_progress 
                SET attempts = attempts + 1, last_attempt = datetime('now'),
                    error_message = ?
                WHERE url_hash = ?
            ''', (error_msg, url_hash))
        
        conn.commit()
        conn.close()
    
    async def enhanced_retry_session(self, failed_urls):
        """Retry with enhanced strategies"""
        
        # Enhanced headers rotation
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        success_count = 0
        
        # Extended timeout configuration
        timeout = aiohttp.ClientTimeout(total=90, connect=45)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            for i, (url_hash, url, strain_names, prev_attempts) in enumerate(failed_urls):
                
                # Rotate user agent
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                print(f"Retry {i+1}/{len(failed_urls)}: {url}")
                
                try:
                    # Random delay between requests
                    await asyncio.sleep(random.uniform(3, 8))
                    
                    async with session.get(url, headers=headers, allow_redirects=True) as response:
                        if response.status == 200:
                            html = await response.text()
                            
                            # Basic validation
                            if len(html) > 1000 and '<html' in html.lower():
                                self.update_retry_status(url_hash, 'success', html)
                                success_count += 1
                                print(f"  ✅ SUCCESS: {len(html)} chars")
                            else:
                                self.update_retry_status(url_hash, 'failed', error_msg=f"Invalid HTML: {len(html)} chars")
                                print(f"  ❌ Invalid HTML: {len(html)} chars")
                        else:
                            self.update_retry_status(url_hash, 'failed', error_msg=f"HTTP {response.status}")
                            print(f"  ❌ HTTP {response.status}")
                            
                except asyncio.TimeoutError:
                    self.update_retry_status(url_hash, 'failed', error_msg="Timeout (90s)")
                    print(f"  ❌ Timeout")
                    
                except Exception as e:
                    self.update_retry_status(url_hash, 'failed', error_msg=str(e)[:100])
                    print(f"  ❌ Error: {str(e)[:50]}")
                
                # Progress update every 50 URLs
                if (i + 1) % 50 == 0:
                    print(f"\n--- Progress: {i+1}/{len(failed_urls)} | Recovered: {success_count} ---\n")
        
        return success_count

def main():
    retrier = ComprehensiveRetrier()
    
    print("=== COMPREHENSIVE RETRY SYSTEM ===")
    failed_urls = retrier.get_all_failed_urls()
    
    if not failed_urls:
        print("No failed URLs to retry!")
        return
    
    print(f"\nStarting comprehensive retry of {len(failed_urls)} URLs...")
    print("Enhanced strategies:")
    print("- Extended 90s timeouts")
    print("- Rotating user agents")
    print("- Random delays (3-8s)")
    print("- Enhanced headers")
    
    start_time = time.time()
    success_count = asyncio.run(retrier.enhanced_retry_session(failed_urls))
    duration = time.time() - start_time
    
    print(f"\n=== RETRY COMPLETE ===")
    print(f"Recovered: {success_count}/{len(failed_urls)} URLs")
    print(f"Duration: {duration/3600:.1f} hours")
    print(f"Recovery rate: {success_count/len(failed_urls)*100:.1f}%")

if __name__ == "__main__":
    main()
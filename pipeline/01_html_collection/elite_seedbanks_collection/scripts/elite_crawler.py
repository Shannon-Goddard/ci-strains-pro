"""
Pipeline 06: Elite Seedbanks URL Discovery Crawler
Target: 8 Premium Seedbanks | ~3,083 Strains | Breaking 20K Total

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/elite_crawler.log'),
        logging.StreamHandler()
    ]
)

class EliteSeedbankCrawler:
    def __init__(self):
        self.discovered_urls = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Seedbank configurations based on chat.txt research
        self.seedbanks = {
            'herbies': {
                'name': 'Herbies Head Shop',
                'base_urls': [
                    'https://herbiesheadshop.com/collections/feminized-seeds',
                    'https://herbiesheadshop.com/collections/regular-cannabis-seeds'
                ],
                'pagination': '/page/{page}',
                'max_pages': [21, 1],
                'selectors': ['a[href*="/seeds/"]', 'a.product-card__name', 'h3.product-item__title a']
            },
            'amsterdam': {
                'name': 'Amsterdam Marijuana Seeds',
                'base_urls': ['https://amsterdammarijuanaseeds.com/all-seeds/'],
                'pagination': 'page/{page}/',
                'max_pages': [14],
                'selectors': ['a.woocommerce-LoopProduct-link', 'a[href*="/product/"]', '.product a']
            },
            'gorilla': {
                'name': 'Gorilla Seeds Bank',
                'base_urls': [
                    'https://www.gorilla-cannabis-seeds.co.uk/feminized-seeds',
                    'https://www.gorilla-cannabis-seeds.co.uk/autoflowering-seeds'
                ],
                'pagination': '?page={page}',
                'max_pages': [93, 33],
                'selectors': ['a.product-item-link', 'a.product.photo', 'a[href*=".html"]']
            },
            'zamnesia': {
                'name': 'Zamnesia',
                'base_urls': [
                    'https://www.zamnesia.com/us/295-feminized-seeds',
                    'https://www.zamnesia.com/us/294-autoflower-seeds'
                ],
                'pagination': '?p={page}',
                'max_pages': [6, 4],
                'selectors': ['a.product-name', 'a[href*="/product/"]', '.product-item a']
            },
            'exotic': {
                'name': 'Exotic Genetix',
                'base_urls': ['https://exoticgenetix.com/shop/'],
                'pagination': 'page/{page}/',
                'max_pages': [22],
                'selectors': ['a.woocommerce-LoopProduct-link', 'a[href*="/product/"]', '.product a']
            },
            'original': {
                'name': 'Original Seeds Store',
                'base_urls': [
                    'https://www.originalseedsstore.com/feminized-cannabis-seeds',
                    'https://www.originalseedsstore.com/regular-seeds'
                ],
                'pagination': None,
                'max_pages': [1, 1],
                'selectors': ['a.product-item-link', 'a[href*="/product/"]', '.product a']
            },
            'tiki': {
                'name': 'Tiki Madman',
                'base_urls': ['https://tikimadman.com/strains/'],
                'pagination': None,
                'max_pages': [1],
                'selectors': ['a[href*="/strain/"]', '.strain-card a', 'a.strain-link']
            }
        }
    
    def crawl_seedbank(self, bank_key):
        """Crawl a specific seedbank for strain URLs"""
        config = self.seedbanks[bank_key]
        logging.info(f"Starting crawl: {config['name']}")
        
        bank_urls = []
        
        for idx, base_url in enumerate(config['base_urls']):
            max_page = config['max_pages'][idx]
            
            for page in range(1, max_page + 1):
                if config['pagination'] and page > 1:
                    url = base_url.rstrip('/') + '/' + config['pagination'].format(page=page)
                else:
                    url = base_url
                
                try:
                    logging.info(f"Crawling: {url}")
                    response = requests.get(url, headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Try multiple selectors
                        links = []
                        for selector in config['selectors']:
                            found = soup.select(selector)
                            if found:
                                links = found
                                logging.info(f"Using selector: {selector}")
                                break
                        
                        if not links:
                            # Fallback: find all links and filter by domain patterns
                            all_links = soup.find_all('a', href=True)
                            links = [l for l in all_links if any(pattern in l['href'] for pattern in ['/product/', '/seeds/', '/strain/', '.html'])]
                            logging.info(f"Using fallback pattern matching")
                        
                        for link in links:
                            href = link.get('href')
                            if href and not any(skip in href for skip in ['cart', 'account', 'login', 'category', 'collection']):
                                full_url = urljoin(url, href)
                                if full_url not in bank_urls and urlparse(full_url).netloc:
                                    bank_urls.append(full_url)
                        
                        logging.info(f"Found {len(links)} products on page {page}, {len(bank_urls)} unique URLs so far")
                        time.sleep(2)
                    else:
                        logging.warning(f"Failed to fetch {url}: {response.status_code}")
                    
                    if not config['pagination']:
                        break
                        
                except Exception as e:
                    logging.error(f"Error crawling {url}: {str(e)}")
                    continue
        
        logging.info(f"{config['name']}: Discovered {len(bank_urls)} URLs")
        return {
            'seedbank': config['name'],
            'key': bank_key,
            'urls': bank_urls,
            'count': len(bank_urls)
        }
    
    def crawl_all(self):
        """Crawl all elite seedbanks"""
        results = {}
        total_urls = 0
        
        for bank_key in self.seedbanks.keys():
            result = self.crawl_seedbank(bank_key)
            results[bank_key] = result
            total_urls += result['count']
            self.discovered_urls.extend(result['urls'])
        
        # Save results
        output = {
            'total_urls': total_urls,
            'seedbanks': results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('../data/elite_urls.json', 'w') as f:
            json.dump(output, f, indent=2)
        
        # Save flat URL list
        with open('../data/elite_urls_flat.txt', 'w') as f:
            for url in self.discovered_urls:
                f.write(url + '\n')
        
        logging.info(f"\nCRAWL COMPLETE!")
        logging.info(f"Total URLs discovered: {total_urls}")
        logging.info(f"Results saved to: ../data/elite_urls.json")
        
        return output

if __name__ == "__main__":
    crawler = EliteSeedbankCrawler()
    results = crawler.crawl_all()
    
    print("\n" + "="*60)
    print("PIPELINE 06: ELITE SEEDBANKS URL DISCOVERY")
    print("="*60)
    for bank_key, data in results['seedbanks'].items():
        print(f"{data['seedbank']}: {data['count']} URLs")
    print(f"\nTOTAL: {results['total_urls']} URLs discovered")
    print("="*60)

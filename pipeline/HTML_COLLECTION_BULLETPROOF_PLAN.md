# Cannabis Intelligence Database - Bulletproof HTML Collection Plan

**Date**: January 3, 2026  
**Architect**: Shannon Goddard  
**Technical Partner**: Amazon Q  
**Status**: ✅ COMPLETED - 90.7% Success Rate  
**Results**: 14,075/15,524 URLs collected

---

## ✅ COLLECTION COMPLETE - FINAL RESULTS

### Success Metrics
- **Total Unique URLs**: 15,524 (after deduplication from 15,778 strains)
- **Successfully Collected**: 14,075 URLs (90.7%)
- **Initial Collection**: 13,163 URLs (84.8%) - 6h 55m
- **Comprehensive Retry**: +912 URLs (38.6% recovery) - 3.9h
- **Final Failures**: 1,449 URLs (9.3%)

### Data Quality
- Average HTML size: 222,933 bytes
- Validation threshold: 75%
- Multi-layer fallback system: ✅ Deployed
- S3 storage with encryption: ✅ Active
- Progress tracking: ✅ Complete

---

## Phase 6: Source of Truth Flagging

### Implementation Required
Add `source_of_truth` column to main dataset:

```python
# Flag URLs without HTML collection
def flag_source_of_truth(df):
    """
    Add source_of_truth column based on HTML collection results
    """
    conn = sqlite3.connect('pipeline/06_html_collection/data/scraping_progress.db')
    
    # Get successful collections
    successful_urls = pd.read_sql('''
        SELECT original_url 
        FROM scraping_progress 
        WHERE status = "completed"
    ''', conn)
    
    successful_set = set(successful_urls['original_url'])
    
    # Add source_of_truth column
    df['source_of_truth'] = df['source_url'].isin(successful_set)
    
    conn.close()
    return df

# Usage
df = pd.read_csv('Cannabis_Database_Validated_Complete.csv')
df = flag_source_of_truth(df)
df.to_csv('Cannabis_Database_With_Source_Truth.csv', index=False)

print(f"Strains with source of truth: {df['source_of_truth'].sum()}")
print(f"Strains flagged 'no source': {(~df['source_of_truth']).sum()}")
```

### Business Logic
- `source_of_truth = True`: HTML successfully collected and verified
- `source_of_truth = False`: No HTML source available (1,449 URLs)
- Use for product listings, legal protection, customer transparency

---

## Architecture Overview

### Core Infrastructure
- **Primary Storage**: AWS S3 with server-side encryption
- **API Layer**: AWS Lambda + API Gateway
- **Frontend**: GitHub Pages with Next.js
- **Database**: SQLite for progress tracking + DynamoDB for metadata
- **CDN**: CloudFront for global access

### Data Flow
```
URLs → Deduplication → Bulletproof Scraper → S3 Storage → API Gateway → GitHub Pages Frontend
```

---

## Phase 1: Infrastructure Setup

### AWS S3 Configuration
```
Bucket: ci-strains-html-archive
Structure:
├── html/
│   ├── {url_hash}.html
│   └── metadata/
│       └── {url_hash}.json
├── index/
│   ├── url_mapping.csv
│   └── collection_stats.json
└── logs/
    └── scraping_logs/
```

### Security Settings
- Server-side encryption (AES-256)
- Private bucket with IAM-controlled access
- Cross-region replication to us-west-2
- Versioning enabled for data protection

### API Gateway Setup
- Rate limiting: 100 requests/minute per IP
- API key authentication for premium access
- CORS enabled for GitHub Pages integration
- CloudWatch logging for monitoring

---

## Phase 2: URL Deduplication Strategy

### Duplicate Handling Logic
```python
import hashlib
import pandas as pd

def deduplicate_urls(df):
    """
    Handle duplicate URLs from AKA name separation
    Returns: {url_hash: {url, strain_ids[], first_seen}}
    """
    url_map = {}
    
    for idx, row in df.iterrows():
        url = row['source_url'].strip()
        strain_id = row['strain_id']
        
        # Create consistent hash
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        
        if url_hash not in url_map:
            url_map[url_hash] = {
                'url': url,
                'strain_ids': [strain_id],
                'first_seen': row['scraped_at']
            }
        else:
            url_map[url_hash]['strain_ids'].append(strain_id)
    
    return url_map
```

### Expected Deduplication Results
- **Input**: 15,778 strain records
- **Estimated Unique URLs**: ~12,000-13,000
- **Duplicate Reduction**: ~20-25%
- **Storage Savings**: Significant (no duplicate HTML files)

---

## Phase 3: Bulletproof Scraping Engine

### Multi-Layer Retry Architecture

#### Layer 1: Bright Data Web Unlocker (Primary)
```python
BRIGHT_DATA_CONFIG = {
    'endpoint': 'brd-customer-hl_XXXXXXX-zone-web_unlocker',
    'timeout': 60,
    'retry_attempts': 3,
    'session_persistence': True
}
```

#### Layer 2: Fallback Chain
1. **Bright Data Residential Proxies**
2. **ScrapingBee API** (backup service)
3. **Direct Requests** (rotating user agents)
4. **Manual Queue** (human intervention)

### Retry Logic Implementation
```python
class BulletproofScraper:
    def __init__(self):
        self.retry_delays = [1, 3, 7, 15, 30, 60]  # Exponential backoff
        self.max_attempts = 6
        self.success_threshold = 0.995  # 99.5% target
    
    async def scrape_with_fallbacks(self, url):
        for attempt in range(self.max_attempts):
            try:
                # Try primary method
                html = await self.bright_data_scrape(url)
                if self.validate_html(html, url):
                    return html, 'bright_data_primary'
                
                # Try fallback methods
                for method in self.fallback_methods:
                    html = await method(url)
                    if self.validate_html(html, url):
                        return html, method.__name__
                        
            except Exception as e:
                await asyncio.sleep(self.retry_delays[attempt])
                continue
        
        return None, 'failed_all_methods'
```

### HTML Quality Validation
```python
def validate_html(self, html_content, url):
    """Comprehensive HTML quality checks"""
    checks = {
        'min_size': len(html_content) > 5000,
        'has_title': '<title>' in html_content,
        'has_cannabis_content': any(term in html_content.lower() 
                                  for term in ['strain', 'cannabis', 'thc', 'cbd']),
        'not_blocked': not any(term in html_content.lower() 
                             for term in ['blocked', 'captcha', 'access denied']),
        'not_error': not any(term in html_content 
                           for term in ['404', '403', '500']),
        'has_structure': all(tag in html_content 
                           for tag in ['<html', '<body', '</html>'])
    }
    
    score = sum(checks.values()) / len(checks)
    return score >= 0.8, score, checks
```

### Rate Limiting & Politeness
```python
DOMAIN_DELAYS = {
    'seedsman.com': 3,
    'leafly.com': 2,
    'allbud.com': 4,
    'default': 2
}

class PolitenessMixin:
    def __init__(self):
        self.last_request = {}
        self.request_counts = {}
    
    async def respectful_delay(self, url):
        domain = urlparse(url).netloc
        delay = DOMAIN_DELAYS.get(domain, DOMAIN_DELAYS['default'])
        
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)
        
        self.last_request[domain] = time.time()
```

---

## Phase 4: Progress Tracking & Recovery

### SQLite Progress Database
```sql
CREATE TABLE scraping_progress (
    url_hash TEXT PRIMARY KEY,
    original_url TEXT,
    strain_ids TEXT,  -- JSON array
    status TEXT,  -- pending, success, failed, manual_review
    attempts INTEGER DEFAULT 0,
    last_attempt TIMESTAMP,
    html_size INTEGER,
    validation_score REAL,
    s3_path TEXT,
    error_message TEXT,
    scrape_method TEXT
);

CREATE TABLE collection_stats (
    id INTEGER PRIMARY KEY,
    total_urls INTEGER,
    completed INTEGER,
    failed INTEGER,
    success_rate REAL,
    avg_html_size INTEGER,
    last_updated TIMESTAMP
);
```

### Checkpoint System
```python
class CheckpointManager:
    def __init__(self, checkpoint_interval=100):
        self.checkpoint_interval = checkpoint_interval
        self.processed_count = 0
    
    def save_checkpoint(self, progress_data):
        """Save progress every N URLs"""
        if self.processed_count % self.checkpoint_interval == 0:
            with open(f'checkpoint_{int(time.time())}.json', 'w') as f:
                json.dump(progress_data, f)
    
    def resume_from_checkpoint(self):
        """Resume from last successful checkpoint"""
        checkpoints = glob.glob('checkpoint_*.json')
        if checkpoints:
            latest = max(checkpoints, key=os.path.getctime)
            with open(latest, 'r') as f:
                return json.load(f)
        return None
```

---

## Phase 5: Secure Storage & Access

### S3 Storage Strategy
```python
class SecureHTMLStorage:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket = 'ci-strains-html-archive'
    
    def store_html(self, url_hash, html_content, metadata):
        """Store HTML with metadata and encryption"""
        
        # Store HTML file
        html_key = f'html/{url_hash}.html'
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=html_key,
            Body=html_content.encode('utf-8'),
            ServerSideEncryption='AES256',
            ContentType='text/html',
            Metadata={
                'collection-date': datetime.now().isoformat(),
                'validation-score': str(metadata['validation_score']),
                'original-url': metadata['url']
            }
        )
        
        # Store metadata JSON
        metadata_key = f'metadata/{url_hash}.json'
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=2),
            ServerSideEncryption='AES256',
            ContentType='application/json'
        )
        
        return html_key, metadata_key
```

### GitHub Pages API Frontend
```javascript
// Next.js API route: /api/get-html
export default async function handler(req, res) {
    const { url } = req.query;
    
    if (!url) {
        return res.status(400).json({ error: 'URL required' });
    }
    
    try {
        // Hash the URL
        const urlHash = crypto.createHash('sha256').update(url).digest('hex').substring(0, 16);
        
        // Call Lambda function to retrieve HTML
        const response = await fetch(`${process.env.API_GATEWAY_URL}/get-html/${urlHash}`, {
            headers: {
                'x-api-key': process.env.API_KEY
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            res.status(200).json(data);
        } else {
            res.status(404).json({ error: 'HTML not found' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Internal server error' });
    }
}
```

---

## Phase 6: Implementation Timeline

### Week 1: Infrastructure Setup
- [ ] AWS S3 bucket configuration
- [ ] API Gateway + Lambda setup
- [ ] GitHub Pages repository creation
- [ ] SQLite database schema
- [ ] AWS Secrets Manager integration

### Week 2: Scraper Development
- [ ] URL deduplication script
- [ ] Bulletproof scraper implementation
- [ ] Progress tracking system
- [ ] Quality validation pipeline
- [ ] Checkpoint/recovery system

### Week 3: Collection Execution
- [ ] Test run on 100 URLs
- [ ] Full collection launch (~12,000 unique URLs)
- [ ] Monitor progress and handle failures
- [ ] Manual review of failed URLs
- [ ] Quality assurance checks

### Week 4: Frontend & Documentation
- [ ] GitHub Pages frontend deployment
- [ ] API documentation
- [ ] Collection statistics dashboard
- [ ] Methodology documentation
- [ ] Success metrics analysis

---

## Success Metrics

### Primary Targets
- **Collection Rate**: 99.5%+ successful HTML captures
- **Data Quality**: 95%+ validation score average
- **Performance**: <2 seconds average response time
- **Reliability**: 99.9% API uptime

### Quality Assurance
- Manual review of failed URLs
- Random sampling of collected HTML
- Cross-validation with original scrape data
- User feedback integration

---

## Cost Estimates

### AWS Infrastructure
- **S3 Storage**: ~$5/month (500MB HTML + metadata)
- **Lambda**: ~$2/month (API calls)
- **API Gateway**: ~$3/month (requests)
- **CloudFront**: ~$1/month (CDN)
- **Total**: ~$11/month operational cost

### Collection Costs
- **Bright Data**: ~$30-50 (12,000 URLs)
- **ScrapingBee**: ~$20 (backup service)
- **One-time**: ~$50-70 total

---

## Risk Mitigation

### Technical Risks
- **API Rate Limits**: Multi-service fallback chain
- **Storage Failures**: Cross-region replication
- **Data Corruption**: Versioning + checksums
- **Access Issues**: Multiple authentication methods

### Business Risks
- **Cost Overruns**: Strict budget monitoring
- **Legal Issues**: Respectful scraping practices
- **Data Loss**: Multiple backup strategies
- **Performance**: CDN + caching layers

---

## Post-Collection Analysis

### Data Completeness Report
- URLs successfully collected vs. failed
- HTML size distribution analysis
- Content quality assessment
- Missing data identification

### Enhancement Opportunities
- Identify systematic extraction gaps
- Plan for Phase 3 enhanced analysis
- User feedback integration
- Continuous improvement roadmap

---

## Methodology Attribution
**Logic designed by Amazon Q, verified by Shannon Goddard.**

---

## Implementation Notes Section
*[To be filled during implementation]*

### What We Actually Did
- 

### What Worked Well
- 

### What We'd Do Differently
- 

### Lessons Learned
- 

### Next Time Improvements
- 

---

**🌿 Cannabis Intelligence Database - Creating an immutable source of truth through bulletproof data collection.**
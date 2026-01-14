# Pipeline 06: Elite Seedbanks Collection Configuration
# Logic designed by Amazon Q, verified by Shannon Goddard

# AWS Configuration (Same as pipeline/01 and 04)
AWS_REGION = "us-east-1"
S3_BUCKET = "ci-strains-html-archive"  # Same bucket for integration

# Secrets Manager Keys (Same credentials as Pipeline 01/04)
BRIGHT_DATA_SECRET = "cannabis_bright_data_api"
SCRAPINGBEE_SECRET = "cannabis_scrapingbee_api"

# Scraping Configuration (Proven settings)
MAX_CONCURRENT_REQUESTS = 10
BATCH_SIZE = 50
MAX_RETRY_ATTEMPTS = 6
SUCCESS_THRESHOLD = 0.995  # 99.5% target

# Elite Seedbanks Rate Limiting
DOMAIN_DELAYS = {
    "herbiesheadshop.com": 2,
    "amsterdammarijuanaseeds.com": 2,
    "gorilla-cannabis-seeds.co.uk": 2,
    "zamnesia.com": 2,
    "exoticgenetix.com": 3,  # Premium, be gentle
    "originalseedsstore.com": 2,
    "tikimadman.com": 3,  # Boutique, be gentle
    "compound-genetics.com": 3,  # Elite, be gentle
    "default": 2
}

# Target Elite Seedbanks
SEEDBANKS = {
    "herbies": {
        "name": "Herbies Head Shop",
        "domain": "herbiesheadshop.com",
        "expected": 440,
        "tier": "high_volume"
    },
    "amsterdam": {
        "name": "Amsterdam Marijuana Seeds",
        "domain": "amsterdammarijuanaseeds.com",
        "expected": 168,
        "tier": "medium_volume"
    },
    "gorilla": {
        "name": "Gorilla Seeds Bank",
        "domain": "gorilla-cannabis-seeds.co.uk",
        "expected": 1260,
        "tier": "high_volume"
    },
    "zamnesia": {
        "name": "Zamnesia",
        "domain": "zamnesia.com",
        "expected": 759,
        "tier": "high_volume"
    },
    "exotic": {
        "name": "Exotic Genetix",
        "domain": "exoticgenetix.com",
        "expected": 330,
        "tier": "premium"
    },
    "original": {
        "name": "Original Seeds Store",
        "domain": "originalseedsstore.com",
        "expected": 56,
        "tier": "boutique"
    },
    "tiki": {
        "name": "Tiki Madman",
        "domain": "tikimadman.com",
        "expected": 41,
        "tier": "boutique"
    },
    "compound": {
        "name": "Compound Genetics",
        "domain": "compound-genetics.com",
        "expected": 29,
        "tier": "elite"
    }
}

# HTML Validation (Same thresholds)
MIN_HTML_SIZE = 5000
MAX_HTML_SIZE = 5000000  # 5MB
VALIDATION_THRESHOLD = 0.75  # 75% of checks must pass

# Cannabis Keywords (Same as pipeline/01/04)
CANNABIS_KEYWORDS = [
    "strain", "cannabis", "thc", "cbd", "seed", "genetics", 
    "indica", "sativa", "hybrid", "flowering", "yield", 
    "terpene", "cannabinoid", "cultivation", "grow",
    "feminized", "autoflower", "regular"
]

# Error Keywords (Same as pipeline/01/04)
ERROR_KEYWORDS = [
    "blocked", "captcha", "access denied", "forbidden",
    "rate limit", "too many requests", "503", "502",
    "bot detected", "security check"
]

# User Agents (Same rotation)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# S3 Storage (Same structure for integration)
S3_PATHS = {
    "html": "pipeline06/html/",
    "metadata": "pipeline06/metadata/", 
    "index": "pipeline06/index/",
    "logs": "logs/pipeline06/"
}

# Database Configuration (Same settings)
DB_TIMEOUT = 30
CHECKPOINT_INTERVAL = 100
PROGRESS_LOG_INTERVAL = 50

# The 20K Milestone
CURRENT_DATABASE_SIZE = 17243
TARGET_NEW_STRAINS = 3083
TARGET_TOTAL = 20326

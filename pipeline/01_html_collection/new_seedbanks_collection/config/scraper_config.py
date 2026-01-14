# Cannabis Intelligence Database - New Seedbanks Collection Configuration
# Logic designed by Amazon Q, verified by Shannon Goddard

# AWS Configuration (Same as pipeline/01)
AWS_REGION = "us-east-1"
S3_BUCKET = "ci-strains-html-archive"  # Same bucket for integration

# Secrets Manager Keys (Same credentials)
BRIGHT_DATA_SECRET = "cannabis_bright_data_api"
SCRAPINGBEE_SECRET = "cannabis_scrapingbee_api"

# Scraping Configuration (Same settings)
MAX_CONCURRENT_REQUESTS = 10
BATCH_SIZE = 50
MAX_RETRY_ATTEMPTS = 6
SUCCESS_THRESHOLD = 0.995  # 99.5% target

# New Seedbanks Rate Limiting
DOMAIN_DELAYS = {
    "sensiseeds.us": 2,
    "sensiseeds.com": 2,
    "californiahempseeds.com": 2,
    "humboldtseedcompany.com": 2,
    "cropkingseeds.com": 2,
    "barneysfarm.com": 2,
    "ilgm.com": 2,
    "default": 2
}

# Target Seedbanks
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

# HTML Validation (Same thresholds)
MIN_HTML_SIZE = 5000
MAX_HTML_SIZE = 5000000  # 5MB
VALIDATION_THRESHOLD = 0.75  # 75% of checks must pass

# Cannabis Keywords (Same as pipeline/01)
CANNABIS_KEYWORDS = [
    "strain", "cannabis", "thc", "cbd", "seed", "genetics", 
    "indica", "sativa", "hybrid", "flowering", "yield", 
    "terpene", "cannabinoid", "cultivation", "grow"
]

# Error Keywords (Same as pipeline/01)
ERROR_KEYWORDS = [
    "blocked", "captcha", "access denied", "forbidden",
    "rate limit", "too many requests", "503", "502"
]

# User Agents (Same rotation)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# S3 Storage (Same structure for integration)
S3_PATHS = {
    "html": "html/",
    "metadata": "metadata/", 
    "index": "index/",
    "logs": "logs/scraping_logs/"
}

# Database Configuration (Same settings)
DB_TIMEOUT = 30
CHECKPOINT_INTERVAL = 100
PROGRESS_LOG_INTERVAL = 50
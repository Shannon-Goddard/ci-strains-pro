# Cannabis Intelligence Database - HTML Collection Configuration
# Logic designed by Amazon Q, verified by Shannon Goddard

# AWS Configuration
AWS_REGION = "us-east-1"
S3_BUCKET = "ci-strains-html-archive"

# Secrets Manager Keys
BRIGHT_DATA_SECRET = "cannabis_bright_data_api"
SCRAPINGBEE_SECRET = "cannabis_scrapingbee_api"
GOOGLE_CLOUD_SECRET = "cannabis_google_cloud_api"

# Scraping Configuration
MAX_CONCURRENT_REQUESTS = 10
BATCH_SIZE = 50
MAX_RETRY_ATTEMPTS = 6
SUCCESS_THRESHOLD = 0.995  # 99.5% target

# Rate Limiting (seconds between requests per domain)
DOMAIN_DELAYS = {
    "seedsman.com": 3,
    "leafly.com": 2,
    "allbud.com": 4,
    "attitude.co.uk": 2,
    "northatlanticseed.com": 2,
    "neptuneseedbank.com": 2,
    "multiversebeans.com": 2,
    "seedsherenow.com": 3,
    "mephistogenetics.com": 3,
    "default": 2
}

# HTML Validation Thresholds
MIN_HTML_SIZE = 5000
MAX_HTML_SIZE = 5000000  # 5MB
VALIDATION_THRESHOLD = 0.75  # 75% of checks must pass

# Cannabis-specific keywords for validation
CANNABIS_KEYWORDS = [
    "strain", "cannabis", "thc", "cbd", "seed", "genetics", 
    "indica", "sativa", "hybrid", "flowering", "yield", 
    "terpene", "cannabinoid", "cultivation", "grow"
]

# Error keywords that indicate blocked/failed requests
ERROR_KEYWORDS = [
    "blocked", "captcha", "access denied", "forbidden",
    "rate limit", "too many requests", "503", "502"
]

# User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# Checkpoint Configuration
CHECKPOINT_INTERVAL = 100  # Save progress every N URLs
PROGRESS_LOG_INTERVAL = 50  # Log progress every N URLs

# S3 Storage Structure
S3_PATHS = {
    "html": "html/",
    "metadata": "metadata/",
    "index": "index/",
    "logs": "logs/scraping_logs/"
}

# Database Configuration
DB_TIMEOUT = 30  # SQLite timeout in seconds
DB_CHECKPOINT_WAL = True  # Enable WAL mode for better concurrency
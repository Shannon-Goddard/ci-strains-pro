#!/usr/bin/env python3
"""
Configuration for Phase 3 HTML Enhancement Pipeline
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

# AWS S3 Configuration
S3_CONFIG = {
    'bucket_name': 'ci-strains-html-archive',
    'html_prefix': 'html_files/',
    'region': 'us-east-1'
}

# Data Processing Configuration
PROCESSING_CONFIG = {
    'batch_size': 100,  # Progress logging interval
    'max_retries': 3,   # S3 retrieval retries
    'timeout_seconds': 30,  # S3 operation timeout
    'encoding': 'utf-8'  # Output file encoding
}

# Data Validation Thresholds
VALIDATION_THRESHOLDS = {
    'thc_min': 0.0,
    'thc_max': 40.0,
    'cbd_min': 0.0,
    'cbd_max': 30.0,
    'flowering_min_days': 30,
    'flowering_max_days': 120,
    'text_min_length': 3,
    'text_max_length': 200,
    'confidence_threshold': 0.8
}

# Enhancement Priorities (weights for confidence scoring)
ENHANCEMENT_WEIGHTS = {
    'cannabinoids': 0.9,
    'terpenes': 0.8,
    'growing_info': 0.8,
    'effects': 0.7,
    'flavors': 0.7,
    'genetics': 0.6
}

# Key fields for completeness scoring
COMPLETENESS_FIELDS = [
    'thc_min', 'thc_max', 'cbd_min', 'cbd_max', 'terpenes',
    'effects', 'flavors', 'flowering_day_min', 'flowering_day_max',
    'grow_difficulty', 'lineage'
]

# Standardization mappings
DIFFICULTY_MAPPING = {
    'easy': 'Easy',
    'beginner': 'Easy',
    'novice': 'Easy',
    'medium': 'Medium',
    'intermediate': 'Medium',
    'moderate': 'Medium',
    'hard': 'Hard',
    'advanced': 'Hard',
    'expert': 'Hard',
    'difficult': 'Hard'
}

# Common terpenes for validation
KNOWN_TERPENES = [
    'myrcene', 'limonene', 'pinene', 'linalool', 'caryophyllene',
    'humulene', 'terpinolene', 'ocimene', 'bisabolol', 'camphene'
]

# Output file configuration
OUTPUT_CONFIG = {
    'enhanced_dataset': 'cannabis_database_phase3_enhanced.csv',
    'enhancement_report': 'phase3_enhancement_report.md',
    'processing_log': 'phase3_enhancement.log'
}
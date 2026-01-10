#!/usr/bin/env python3
"""
Intelligent Overwrite Configuration
Controls when existing data should be corrected with HTML sources

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

# INTELLIGENT OVERWRITE SETTINGS
INTELLIGENT_OVERWRITE = {
    'enabled': True,  # Set to False for gap-filling only mode
    
    # Confidence thresholds for overwriting existing data
    'overwrite_thresholds': {
        'cannabinoids': 0.85,  # High confidence needed for THC/CBD
        'terpenes': 0.80,      # Medium-high for terpenes  
        'effects': 0.75,       # Medium for effects/flavors
        'flavors': 0.75,
        'growing_info': 0.80,  # High for growing data
        'genetics': 0.70       # Lower for genetics (often subjective)
    },
    
    # High-quality sources that get higher reliability scores
    'trusted_sources': [
        'mephistogenetics.com',     # Mephisto Genetics (breeder)
        'royalqueenseeds.com',      # Royal Queen Seeds (breeder)
        'barneysfarm.com',          # Barney's Farm (breeder)
        'greenhouseseeds.nl',       # Greenhouse Seeds (breeder)
        'sweetseeds.es',            # Sweet Seeds (breeder)
        'dinafem.org',              # Dinafem (breeder)
        'fastbuds.com',             # Fast Buds (breeder)
        'dutchpassion.com'          # Dutch Passion (breeder)
    ],
    
    # Patterns that indicate low-quality existing data
    'suspect_data_patterns': [
        r'^\d+$',                   # Just a number
        r'^[a-z]+$',               # All lowercase single word
        r'unknown|n/a|tbd|coming soon|placeholder',  # Placeholder text
        r'^\s*$',                  # Empty/whitespace
        r'^test|sample|example',    # Test data
        r'^[0-9]+\.[0-9]+\.[0-9]+' # Version numbers mistaken for data
    ],
    
    # Minimum confidence difference to overwrite
    'min_confidence_gap': 0.2,  # New data must be 0.2 points higher
    
    # Fields that should NEVER be overwritten (too subjective/risky)
    'protected_fields': [
        'strain_name',
        'breeder_name', 
        'bank_name',
        'strain_id'
    ]
}

# CORRECTION LOGGING
CORRECTION_LOGGING = {
    'log_all_corrections': True,
    'log_file': 'data_corrections.log',
    'include_before_after': True,
    'correction_reasons': {
        'fill_empty': 'Filled missing data',
        'higher_confidence': 'HTML source more reliable',
        'poor_existing_quality': 'Existing data appears low quality',
        'trusted_source': 'Data from trusted breeder source'
    }
}

# VALIDATION RULES
VALIDATION_RULES = {
    'cannabinoids': {
        'thc_max_reasonable': 40.0,
        'cbd_max_reasonable': 30.0,
        'total_max_reasonable': 45.0,
        'min_value': 0.0
    },
    'flowering_time': {
        'min_days': 30,
        'max_days': 120
    },
    'text_fields': {
        'min_length': 3,
        'max_length': 500
    }
}
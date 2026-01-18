# Master Dataset Core Schema
# Botanical and cultivation data only - no commercial/pricing data

CORE_SCHEMA = {
    # Identity
    'strain_id': 'UUID generated',
    'strain_name': 'Primary strain name',
    'seed_bank': 'Source attribution only',
    'source_url': 'Original URL for verification',
    's3_html_key': 'Archive reference',
    'scraped_at': 'Collection timestamp',
    
    # Genetics (Raw)
    'genetics_lineage_raw': 'Parent strains, crosses',
    'sativa_percentage_raw': 'Sativa %',
    'indica_percentage_raw': 'Indica %',
    'dominant_type_raw': 'Sativa/Indica/Hybrid',
    'breeder_name_raw': 'Original breeder',
    'generation_raw': 'F1, F2, etc.',
    
    # Cannabinoids (Raw)
    'thc_content_raw': 'THC as scraped',
    'thc_min_raw': 'THC minimum %',
    'thc_max_raw': 'THC maximum %',
    'cbd_content_raw': 'CBD as scraped',
    'cbd_min_raw': 'CBD minimum %',
    'cbd_max_raw': 'CBD maximum %',
    
    # Terpenes (Raw)
    'terpenes_raw': 'Terpene profile',
    'dominant_terpene_raw': 'Primary terpene',
    
    # Effects (Raw)
    'effects_all_raw': 'All effects listed',
    'primary_effect_raw': 'Main effect',
    'effects_mental_raw': 'Mental effects',
    'effects_physical_raw': 'Physical effects',
    
    # Flavors/Aromas (Raw)
    'flavors_all_raw': 'All flavors',
    'primary_flavor_raw': 'Dominant flavor',
    'aroma_raw': 'Aroma description',
    
    # Cultivation (Raw)
    'flowering_time_raw': 'Flowering period',
    'flowering_min_raw': 'Min days',
    'flowering_max_raw': 'Max days',
    'yield_indoor_raw': 'Indoor yield',
    'yield_outdoor_raw': 'Outdoor yield',
    'height_indoor_raw': 'Indoor height',
    'height_outdoor_raw': 'Outdoor height',
    'difficulty_raw': 'Grow difficulty',
    'climate_raw': 'Suitable climates',
    
    # Seed Type (Raw)
    'seed_type_raw': 'Feminized/Regular/Auto',
    'flowering_type_raw': 'Photoperiod/Autoflower',
    
    # Awards (Raw)
    'awards_raw': 'Cannabis Cup wins, etc.',
    'award_count_raw': 'Number of awards',
    
    # Quality Metadata
    'data_completeness_score': '0-100',
    'extraction_version': 'Script version',
    'extraction_methods_used': 'Methods applied',
}

# Columns to EXCLUDE (commercial data)
EXCLUDED_COLUMNS = [
    'price', 'prices_usd', 'prices_gbp', 'min_price', 'max_price', 'avg_price',
    'package_size', 'pack_size', 'min_package_size', 'max_package_size',
    'sku', 'product_id', 'availability', 'in_stock', 'discount',
    'shipping', 'payment', 'currency',
]

# Column mapping keywords (if keyword in column_name → map to unified)
COLUMN_MAPPINGS = {
    'strain_name_raw': ['strain_name'],
    'source_url_raw': ['source_url'],
    's3_html_key_raw': ['s3_html_key', 's3_key'],
    'scraped_at_raw': ['scraped_at'],
    'genetics_lineage_raw': ['genetics', 'lineage', 'parent', 'cross'],
    'sativa_percentage_raw': ['sativa_percentage', 'sativa'],
    'indica_percentage_raw': ['indica_percentage', 'indica'],
    'dominant_type_raw': ['dominant_type', 'strain_type', 'cannabis_type'],
    'breeder_name_raw': ['breeder'],
    'thc_content_raw': ['thc_content', 'thc_level', 'thc_percentage', 'spec_thc'],
    'thc_min_raw': ['thc_min'],
    'thc_max_raw': ['thc_max'],
    'thc_range_raw': ['thc_range'],
    'thc_average_raw': ['thc_average', 'thc_avg'],
    'cbd_content_raw': ['cbd_content', 'cbd_level', 'cbd_percentage', 'spec_cbd'],
    'cbd_min_raw': ['cbd_min'],
    'cbd_max_raw': ['cbd_max'],
    'cbd_range_raw': ['cbd_range'],
    'terpenes_raw': ['terpene'],
    'dominant_terpene_raw': ['dominant_terpene'],
    'effects_all_raw': ['effects_all', 'effect'],
    'primary_effect_raw': ['primary_effect'],
    'effects_mental_raw': ['effects_mental', 'mental'],
    'effects_physical_raw': ['effects_physical', 'physical'],
    'flavors_all_raw': ['flavors_all', 'flavor', 'taste', 'aroma'],
    'primary_flavor_raw': ['primary_flavor'],
    'flowering_time_raw': ['flowering_time', 'flowering'],
    'flowering_min_raw': ['flowering_min', 'flowering_time_min'],
    'flowering_max_raw': ['flowering_max', 'flowering_time_max'],
    'yield_indoor_raw': ['yield_indoor', 'indoor_yield'],
    'yield_outdoor_raw': ['yield_outdoor', 'outdoor_yield'],
    'height_indoor_raw': ['height_indoor', 'indoor_height'],
    'height_outdoor_raw': ['height_outdoor', 'outdoor_height'],
    'height_raw': ['height_amount', 'height_max', 'height_min', 'height_range', 'height_unit', 'plant_height'],
    'generation_raw': ['generation'],
    'is_hybrid_raw': ['is_hybrid'],
    'description_raw': ['description'],
    'cbn_content_raw': ['cbn'],
    'total_grow_time_raw': ['seed_to_harvest', 'from_seed_to_harvest'],
    'suitable_environments_raw': ['suitable_for_growing', 'suitable_environment'],
    'difficulty_raw': ['difficulty', 'grow_difficulty'],
    'climate_raw': ['climate', 'suitable_climate'],
    'seed_type_raw': ['seed_type', 'variety'],
    'flowering_type_raw': ['flowering_type', 'autoflower'],
    'awards_raw': ['award'],
}

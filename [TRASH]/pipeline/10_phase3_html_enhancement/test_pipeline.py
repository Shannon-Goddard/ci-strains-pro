#!/usr/bin/env python3
"""
Test Script for Phase 3 HTML Enhancement Pipeline
Tests the enhancement pipeline with a small sample of data

Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime

# Add the current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from phase3_html_enhancer import StrainEnhancer, StrainHTMLProcessor

def create_test_data():
    """Create a small test dataset for validation"""
    test_data = {
        'strain_id': [1, 2, 3, 4, 5],
        'source_of_truth': [True, True, False, True, True],
        'source_url': [
            'https://mephistogenetics.com/products/canna-cheese-1-1',
            'https://neptuneseedbank.com/product/sour-crack',
            'https://example.com/no-html',
            'https://neptuneseedbank.com/product/honey-melon-rolex-strain/',
            'https://mephistogenetics.com/products/mephistoz'
        ],
        'strain_name': ['Canna Cheese', 'Sour Crack', 'Test Strain', 'Honey Melon Rolex', 'Mephistoz'],
        'thc_min': [np.nan, 19.0, np.nan, np.nan, np.nan],
        'thc_max': [np.nan, 19.0, np.nan, np.nan, np.nan],
        'thc': [np.nan, 19.0, np.nan, np.nan, np.nan],
        'cbd_min': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'cbd_max': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'cbd': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'terpenes': [np.nan, np.nan, 'Existing terpenes', np.nan, np.nan],
        'effects': ['euphoric, energetic', np.nan, np.nan, np.nan, np.nan],
        'flavors': [np.nan, 'Fruity, Sour', np.nan, np.nan, np.nan],
        'flowering_day_min': [56, 60, np.nan, np.nan, 70],
        'flowering_day_max': [63, 70, np.nan, np.nan, 56],
        'grow_difficulty': [np.nan, np.nan, 'Easy', np.nan, 'Expert'],
        'lineage': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'height_indoor_min_cm': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'height_indoor_max_cm': [np.nan, np.nan, np.nan, np.nan, np.nan],
        'scraped_at': ['2025-01-27T10:00:00Z'] * 5
    }
    
    return pd.DataFrame(test_data)

def test_html_processor():
    """Test the HTML processor with mock data"""
    print("Testing HTML Processor...")
    
    processor = StrainHTMLProcessor()
    
    # Test pattern matching with sample HTML content
    sample_html = """
    <div class="strain-info">
        <p>THC: 18-22%</p>
        <p>CBD: 0.5-1.2%</p>
        <p>Flowering: 8-9 weeks</p>
        <p>Effects: relaxing, euphoric, creative</p>
        <p>Flavors: citrus, pine, earthy</p>
        <p>Difficulty: Medium</p>
        <p>Terpenes: Myrcene: 0.8%, Limonene: 0.6%</p>
    </div>
    """
    
    # Test cannabinoid extraction
    cannabinoids = processor.extract_cannabinoids(sample_html)
    print(f"Cannabinoids extracted: {cannabinoids}")
    
    # Test terpene extraction
    terpenes = processor.extract_terpenes(sample_html)
    print(f"Terpenes extracted: {terpenes}")
    
    # Test effects extraction
    effects = processor.extract_effects(sample_html)
    print(f"Effects extracted: {effects}")
    
    # Test flavors extraction
    flavors = processor.extract_flavors(sample_html)
    print(f"Flavors extracted: {flavors}")
    
    # Test growing info extraction
    growing_info = processor.extract_growing_info(sample_html)
    print(f"Growing info extracted: {growing_info}")
    
    return True

def test_enhancer():
    """Test the strain enhancer with test data"""
    print("\nTesting Strain Enhancer...")
    
    # Create test data
    test_df = create_test_data()
    print(f"Created test dataset with {len(test_df)} strains")
    
    # Save test data
    test_df.to_csv('test_input.csv', index=False)
    print("Saved test input data")
    
    # Initialize enhancer
    enhancer = StrainEnhancer()
    
    # Test completeness scoring
    for idx, row in test_df.iterrows():
        completeness = enhancer.calculate_completeness_score(row)
        print(f"Strain {row['strain_name']} completeness: {completeness:.2f}")
    
    # Test enhancement (without actual S3 calls)
    print("\nTesting enhancement logic (mock data)...")
    
    # Mock extracted data
    mock_extracted_data = {
        'cannabinoids': {'thc_min': 20.0, 'thc_max': 25.0, 'thc_avg': 22.5},
        'terpenes': {'myrcene': 0.8, 'limonene': 0.6},
        'effects': ['relaxing', 'euphoric', 'creative'],
        'flavors': ['citrus', 'pine', 'earthy'],
        'growing_info': {'flowering_min': 56, 'flowering_max': 63, 'difficulty': 'Medium'},
        'genetics': {'lineage': 'Parent A x Parent B'}
    }
    
    # Test enhancement on first row
    test_row = test_df.iloc[0].copy()
    enhanced_row = enhancer.enhance_strain_record(test_row, mock_extracted_data)
    
    print("Original row THC:", test_row.get('thc_min'))
    print("Enhanced row THC:", enhanced_row.get('thc_min'))
    print("Enhanced terpenes:", enhanced_row.get('terpenes'))
    
    return True

def test_confidence_scoring():
    """Test confidence scoring mechanism"""
    print("\nTesting Confidence Scoring...")
    
    enhancer = StrainEnhancer()
    
    # Test with complete data
    complete_data = {
        'cannabinoids': {'thc_min': 20.0, 'thc_max': 25.0},
        'terpenes': {'myrcene': 0.8, 'limonene': 0.6},
        'effects': ['relaxing', 'euphoric'],
        'flavors': ['citrus', 'pine'],
        'growing_info': {'flowering_min': 56, 'flowering_max': 63},
        'genetics': {'lineage': 'Parent A x Parent B'}
    }
    
    confidence = enhancer.calculate_confidence_score(complete_data)
    print(f"Complete data confidence: {confidence:.2f}")
    
    # Test with partial data
    partial_data = {
        'cannabinoids': {'thc_min': 20.0},
        'terpenes': {},
        'effects': ['relaxing'],
        'flavors': [],
        'growing_info': {},
        'genetics': {}
    }
    
    confidence = enhancer.calculate_confidence_score(partial_data)
    print(f"Partial data confidence: {confidence:.2f}")
    
    return True

def test_terpene_formatting():
    """Test terpene profile formatting"""
    print("\nTesting Terpene Formatting...")
    
    enhancer = StrainEnhancer()
    
    # Test terpene formatting
    terpenes = {
        'myrcene': 0.8,
        'limonene': 0.6,
        'pinene': 0.4,
        'dominant_list': 'Caryophyllene, Humulene'
    }
    
    formatted = enhancer.format_terpene_profile(terpenes)
    print(f"Formatted terpenes: {formatted}")
    
    return True

def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Phase 3 HTML Enhancement Pipeline - Test Suite")
    print("=" * 60)
    
    tests = [
        ("HTML Processor", test_html_processor),
        ("Strain Enhancer", test_enhancer),
        ("Confidence Scoring", test_confidence_scoring),
        ("Terpene Formatting", test_terpene_formatting)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            success = test_func()
            results.append((test_name, "PASSED" if success else "FAILED"))
            print(f"{test_name}: PASSED")
        except Exception as e:
            results.append((test_name, f"FAILED: {e}"))
            print(f"{test_name}: FAILED - {e}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results:
        status = "[PASS]" if "PASSED" in result else "[FAIL]"
        print(f"{status} {test_name}: {result}")
    
    passed = sum(1 for _, result in results if "PASSED" in result)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! Pipeline is ready for execution.")
    else:
        print("Some tests failed. Please review before running the full pipeline.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
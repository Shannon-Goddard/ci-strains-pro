#!/usr/bin/env python3
"""
Dutch Passion Data Analysis & Validation Suite
Comprehensive analysis of extracted data for quality assessment and market insights
Logic designed by Amazon Q, verified by Shannon Goddard.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import json

class DutchPassionDataAnalyzer:
    def __init__(self, csv_file='dutch_passion_maximum_extraction.csv'):
        self.df = None
        self.csv_file = csv_file
        self.analysis_results = {}
        
    def load_and_validate_data(self):
        """Load CSV and perform initial validation"""
        try:
            self.df = pd.read_csv(self.csv_file, encoding='utf-8')
            print(f"✅ Loaded {len(self.df)} strains with {len(self.df.columns)} columns")
            
            # Basic validation
            print(f"📊 Data shape: {self.df.shape}")
            print(f"🎯 Unique strains: {self.df['strain_name'].nunique()}")
            print(f"💾 Memory usage: {self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def analyze_data_completeness(self):
        """Comprehensive data completeness analysis"""
        print("\n🔍 DATA COMPLETENESS ANALYSIS")
        print("=" * 50)
        
        # Overall completeness
        total_cells = self.df.shape[0] * self.df.shape[1]
        non_null_cells = self.df.count().sum()
        overall_completeness = (non_null_cells / total_cells) * 100
        
        print(f"📈 Overall Completeness: {overall_completeness:.1f}%")
        print(f"📊 Non-null cells: {non_null_cells:,} / {total_cells:,}")
        
        # Field-level completeness
        field_completeness = (self.df.count() / len(self.df) * 100).sort_values(ascending=False)
        
        print(f"\n🏆 TOP 10 MOST COMPLETE FIELDS:")
        for field, completeness in field_completeness.head(10).items():
            print(f"  {field}: {completeness:.1f}%")
        
        print(f"\n⚠️  BOTTOM 10 LEAST COMPLETE FIELDS:")
        for field, completeness in field_completeness.tail(10).items():
            print(f"  {field}: {completeness:.1f}%")
        
        # Store results
        self.analysis_results['completeness'] = {
            'overall': overall_completeness,
            'by_field': field_completeness.to_dict()
        }
        
        return field_completeness
    
    def analyze_market_tiers(self):
        """Analyze market tier distribution and characteristics"""
        print("\n💰 MARKET TIER ANALYSIS")
        print("=" * 50)
        
        if 'market_tier' in self.df.columns:
            tier_distribution = self.df['market_tier'].value_counts()
            print("📊 Market Tier Distribution:")
            for tier, count in tier_distribution.items():
                percentage = (count / len(self.df)) * 100
                print(f"  {tier}: {count} strains ({percentage:.1f}%)")
            
            # Quality score by tier
            if 'data_completeness_score' in self.df.columns:
                tier_quality = self.df.groupby('market_tier')['data_completeness_score'].agg(['mean', 'min', 'max'])
                print(f"\n📈 Quality Scores by Tier:")
                print(tier_quality.round(1))
            
            self.analysis_results['market_tiers'] = tier_distribution.to_dict()
        
    def analyze_cannabis_data_quality(self):
        """Analyze cannabis-specific data quality"""
        print("\n🌿 CANNABIS DATA QUALITY ANALYSIS")
        print("=" * 50)
        
        cannabis_fields = {
            'THC Data': ['thc_min', 'thc_max', 'thc_content', 'thc_range'],
            'CBD Data': ['cbd_min', 'cbd_max', 'cbd_content', 'cbd_range'],
            'Cultivation': ['flowering_time', 'flowering_min', 'flowering_max'],
            'Yield': ['yield_range', 'yield_amount', 'yield_min', 'yield_max'],
            'Height': ['height_range', 'height_amount', 'height_min', 'height_max'],
            'Effects': ['effects_all', 'primary_effect', 'effects_mental', 'effects_physical'],
            'Genetics': ['genetics_lineage', 'parent_1', 'parent_2', 'indica_percentage', 'sativa_percentage'],
            'Terpenes': ['terpenes', 'dominant_terpene', 'terpene_count'],
            'Flavors': ['flavors_all', 'primary_flavor', 'flavors_citrus', 'flavors_fruity']
        }
        
        for category, fields in cannabis_fields.items():
            available_fields = [f for f in fields if f in self.df.columns]
            if available_fields:
                # Count strains with any data in this category
                has_data = self.df[available_fields].notna().any(axis=1).sum()
                percentage = (has_data / len(self.df)) * 100
                print(f"🎯 {category}: {has_data}/{len(self.df)} strains ({percentage:.1f}%)")
                
                # Show field-level breakdown
                for field in available_fields:
                    field_count = self.df[field].notna().sum()
                    field_pct = (field_count / len(self.df)) * 100
                    print(f"    {field}: {field_count} ({field_pct:.1f}%)")
        
    def analyze_pricing_intelligence(self):
        """Analyze pricing data for business intelligence"""
        print("\n💵 PRICING INTELLIGENCE ANALYSIS")
        print("=" * 50)
        
        pricing_fields = [col for col in self.df.columns if 'price' in col.lower()]
        
        if pricing_fields:
            print(f"💰 Pricing Fields Available: {len(pricing_fields)}")
            
            for field in pricing_fields:
                if self.df[field].notna().sum() > 0:
                    count = self.df[field].notna().sum()
                    percentage = (count / len(self.df)) * 100
                    print(f"  {field}: {count} strains ({percentage:.1f}%)")
            
            # Analyze USD pricing if available
            if 'min_price_usd' in self.df.columns and self.df['min_price_usd'].notna().sum() > 0:
                usd_prices = self.df['min_price_usd'].dropna()
                print(f"\n💲 USD Price Analysis:")
                print(f"  Average: ${usd_prices.mean():.2f}")
                print(f"  Median: ${usd_prices.median():.2f}")
                print(f"  Range: ${usd_prices.min():.2f} - ${usd_prices.max():.2f}")
        
    def analyze_genetics_patterns(self):
        """Analyze genetics and lineage patterns"""
        print("\n🧬 GENETICS PATTERN ANALYSIS")
        print("=" * 50)
        
        if 'genetics_lineage' in self.df.columns:
            genetics_data = self.df['genetics_lineage'].dropna()
            print(f"🔬 Genetics Data: {len(genetics_data)}/{len(self.df)} strains ({len(genetics_data)/len(self.df)*100:.1f}%)")
            
            # Analyze common parent strains
            if 'parent_1' in self.df.columns and 'parent_2' in self.df.columns:
                all_parents = []
                all_parents.extend(self.df['parent_1'].dropna().tolist())
                all_parents.extend(self.df['parent_2'].dropna().tolist())
                
                if all_parents:
                    parent_counts = Counter(all_parents)
                    print(f"\n🏆 TOP 10 PARENT STRAINS:")
                    for parent, count in parent_counts.most_common(10):
                        print(f"  {parent}: {count} crosses")
        
        # Indica/Sativa analysis
        if 'indica_percentage' in self.df.columns and 'sativa_percentage' in self.df.columns:
            indica_data = self.df['indica_percentage'].dropna()
            sativa_data = self.df['sativa_percentage'].dropna()
            
            if len(indica_data) > 0:
                print(f"\n📊 Indica/Sativa Ratios: {len(indica_data)} strains")
                print(f"  Average Indica: {indica_data.mean():.1f}%")
                print(f"  Average Sativa: {sativa_data.mean():.1f}%")
    
    def analyze_extraction_method_performance(self):
        """Analyze which extraction methods performed best"""
        print("\n⚙️ EXTRACTION METHOD PERFORMANCE")
        print("=" * 50)
        
        if 'extraction_methods_used' in self.df.columns:
            # Parse extraction methods (assuming they're stored as lists or strings)
            all_methods = []
            for methods in self.df['extraction_methods_used'].dropna():
                if isinstance(methods, str):
                    # Handle string representation of lists
                    try:
                        method_list = eval(methods) if methods.startswith('[') else [methods]
                        all_methods.extend(method_list)
                    except:
                        all_methods.append(methods)
                elif isinstance(methods, list):
                    all_methods.extend(methods)
            
            if all_methods:
                method_counts = Counter(all_methods)
                print(f"🔧 Extraction Method Success Rates:")
                for method, count in method_counts.most_common():
                    percentage = (count / len(self.df)) * 100
                    print(f"  {method}: {count} strains ({percentage:.1f}%)")
        
        # Method count analysis
        if 'method_count' in self.df.columns:
            method_counts = self.df['method_count'].dropna()
            print(f"\n📈 Methods per Strain:")
            print(f"  Average: {method_counts.mean():.1f} methods")
            print(f"  Range: {method_counts.min()}-{method_counts.max()} methods")
    
    def identify_data_gaps_and_opportunities(self):
        """Identify missing data and improvement opportunities"""
        print("\n🎯 DATA GAPS & OPPORTUNITIES")
        print("=" * 50)
        
        # Critical missing data
        critical_fields = {
            'THC Content': ['thc_min', 'thc_max', 'thc_content'],
            'CBD Content': ['cbd_min', 'cbd_max', 'cbd_content'],
            'Flowering Time': ['flowering_time', 'flowering_min'],
            'Yield Data': ['yield_range', 'yield_amount'],
            'Pricing': ['jsonld_price', 'min_price_usd'],
            'Genetics': ['genetics_lineage', 'parent_1']
        }
        
        print("🚨 CRITICAL DATA GAPS:")
        for category, fields in critical_fields.items():
            available_fields = [f for f in fields if f in self.df.columns]
            if available_fields:
                has_any_data = self.df[available_fields].notna().any(axis=1).sum()
                missing = len(self.df) - has_any_data
                if missing > 0:
                    percentage = (missing / len(self.df)) * 100
                    print(f"  {category}: {missing} strains missing ({percentage:.1f}%)")
        
        # Improvement opportunities
        print(f"\n💡 IMPROVEMENT OPPORTUNITIES:")
        
        # Fields with partial data that could be enhanced
        partial_fields = []
        for col in self.df.columns:
            completeness = (self.df[col].notna().sum() / len(self.df)) * 100
            if 10 <= completeness <= 70:  # Fields with partial but improvable data
                partial_fields.append((col, completeness))
        
        partial_fields.sort(key=lambda x: x[1], reverse=True)
        
        for field, completeness in partial_fields[:10]:
            print(f"  {field}: {completeness:.1f}% complete - enhancement opportunity")
    
    def generate_market_value_assessment(self):
        """Generate market value assessment based on data quality"""
        print("\n💎 MARKET VALUE ASSESSMENT")
        print("=" * 50)
        
        # Calculate value scores
        value_metrics = {
            'cultivation_value': 0,
            'business_value': 0,
            'genetics_value': 0,
            'consumer_value': 0
        }
        
        # Cultivation value (THC, CBD, flowering, yield)
        cultivation_fields = ['thc_min', 'thc_content', 'cbd_content', 'flowering_time', 'yield_range']
        cultivation_completeness = sum((self.df[f].notna().sum() / len(self.df)) * 100 
                                     for f in cultivation_fields if f in self.df.columns)
        value_metrics['cultivation_value'] = cultivation_completeness / len([f for f in cultivation_fields if f in self.df.columns])
        
        # Business value (pricing, availability, certifications)
        business_fields = ['jsonld_price', 'min_price_usd', 'package_sizes', 'awards']
        business_completeness = sum((self.df[f].notna().sum() / len(self.df)) * 100 
                                  for f in business_fields if f in self.df.columns)
        value_metrics['business_value'] = business_completeness / len([f for f in business_fields if f in self.df.columns])
        
        # Genetics value
        genetics_fields = ['genetics_lineage', 'parent_1', 'indica_percentage']
        genetics_completeness = sum((self.df[f].notna().sum() / len(self.df)) * 100 
                                  for f in genetics_fields if f in self.df.columns)
        value_metrics['genetics_value'] = genetics_completeness / len([f for f in genetics_fields if f in self.df.columns])
        
        # Consumer value (effects, flavors, terpenes)
        consumer_fields = ['effects_all', 'flavors_all', 'terpenes']
        consumer_completeness = sum((self.df[f].notna().sum() / len(self.df)) * 100 
                                  for f in consumer_fields if f in self.df.columns)
        value_metrics['consumer_value'] = consumer_completeness / len([f for f in consumer_fields if f in self.df.columns])
        
        print("📊 Value Category Scores:")
        for category, score in value_metrics.items():
            print(f"  {category.replace('_', ' ').title()}: {score:.1f}%")
        
        # Overall market readiness
        overall_value = sum(value_metrics.values()) / len(value_metrics)
        print(f"\n🎯 Overall Market Readiness: {overall_value:.1f}%")
        
        if overall_value >= 70:
            print("✅ MARKET READY - High value dataset")
        elif overall_value >= 50:
            print("⚠️  ENHANCEMENT NEEDED - Good foundation, needs improvement")
        else:
            print("🚨 SIGNIFICANT GAPS - Major improvements required")
    
    def run_comprehensive_analysis(self):
        """Run all analysis methods"""
        print("🚀 DUTCH PASSION DATA ANALYSIS SUITE")
        print("Logic designed by Amazon Q, verified by Shannon Goddard.")
        print("=" * 60)
        
        if not self.load_and_validate_data():
            return False
        
        # Run all analyses
        self.analyze_data_completeness()
        self.analyze_market_tiers()
        self.analyze_cannabis_data_quality()
        self.analyze_pricing_intelligence()
        self.analyze_genetics_patterns()
        self.analyze_extraction_method_performance()
        self.identify_data_gaps_and_opportunities()
        self.generate_market_value_assessment()
        
        print(f"\n✅ ANALYSIS COMPLETE")
        print(f"📊 Dataset: {len(self.df)} strains × {len(self.df.columns)} columns")
        print(f"💾 Results saved to analysis_results.json")
        
        # Save analysis results
        with open('analysis_results.json', 'w') as f:
            json.dump(self.analysis_results, f, indent=2, default=str)
        
        return True

def main():
    analyzer = DutchPassionDataAnalyzer()
    analyzer.run_comprehensive_analysis()

if __name__ == "__main__":
    main()
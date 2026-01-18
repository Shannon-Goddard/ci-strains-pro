"""
Parse Vertex AI Batch Results - Extract Gemini Responses
"""

import json
from pathlib import Path
from collections import defaultdict

# Paths
RESULTS_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/vertex_batch/batch_results.jsonl")
OUTPUT_DIR = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/vertex_batch")
OUTPUT_DIR.mkdir(exist_ok=True)

def extract_json_from_response(response_text):
    """Extract JSON from Gemini response text"""
    # Remove markdown code blocks
    text = response_text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    return json.loads(text.strip())

def main():
    print("Parsing batch results...")
    
    # Read all results
    results = []
    with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))
    
    print(f"Loaded {len(results)} result batches\n")
    
    # Parse each result
    parsed_results = []
    parse_errors = []
    
    for i, result in enumerate(results):
        try:
            # Extract response text
            response_text = result['response']['candidates'][0]['content']['parts'][0]['text']
            
            # Parse JSON
            data = extract_json_from_response(response_text)
            parsed_results.append(data)
            
        except Exception as e:
            parse_errors.append(f"Batch {i}: {str(e)}")
    
    print(f"Successfully parsed: {len(parsed_results)}/{len(results)} batches")
    print(f"Parse errors: {len(parse_errors)}\n")
    
    # Save parsed results
    output_file = OUTPUT_DIR / "parsed_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_results, f, indent=2)
    
    print(f"Saved parsed results to: {output_file}")
    
    # Generate summary statistics
    total_strains = sum(r.get('strains_analyzed', 0) for r in parsed_results)
    total_anomalies = defaultdict(int)
    all_duplicates = set()
    
    for r in parsed_results:
        for key, val in r.get('anomalies', {}).items():
            total_anomalies[key] += val
        all_duplicates.update(r.get('duplicates', []))
    
    print(f"\n=== SUMMARY ===")
    print(f"Total strains analyzed: {total_strains:,}")
    print(f"\nAnomalies:")
    for key, val in total_anomalies.items():
        print(f"  {key}: {val:,}")
    print(f"\nTotal duplicate strain names: {len(all_duplicates):,}")
    
    # Save summary
    summary = {
        "total_strains": total_strains,
        "batches_parsed": len(parsed_results),
        "parse_errors": len(parse_errors),
        "anomalies": dict(total_anomalies),
        "duplicate_count": len(all_duplicates),
        "duplicates": sorted(list(all_duplicates))[:50]  # Top 50
    }
    
    summary_file = OUTPUT_DIR / "summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSaved summary to: {summary_file}")

if __name__ == "__main__":
    main()

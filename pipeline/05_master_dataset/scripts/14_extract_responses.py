"""Extract raw Gemini responses from Vertex AI batch results"""

import json
from pathlib import Path

RESULTS_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/vertex_batch/batch_results.jsonl")
OUTPUT_FILE = Path("c:/Users/uthin/OneDrive/Desktop/ci-strains-pro/pipeline/05_master_dataset/output/vertex_batch/gemini_responses.txt")

print("Extracting Gemini responses...")

with open(RESULTS_FILE, 'r', encoding='utf-8') as f:
    results = [json.loads(line) for line in f if line.strip()]

print(f"Found {len(results)} results")

# Extract all text responses
responses = []
for i, result in enumerate(results):
    try:
        text = result['response']['candidates'][0]['content']['parts'][0]['text']
        responses.append(f"=== BATCH {i+1} ===\n{text}\n\n")
    except Exception as e:
        print(f"Warning: Could not extract batch {i+1}: {e}")

# Save all responses
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.writelines(responses)

print(f"\n[OK] Saved {len(responses)} responses to: {OUTPUT_FILE}")
print(f"File size: {OUTPUT_FILE.stat().st_size / (1024*1024):.2f} MB")

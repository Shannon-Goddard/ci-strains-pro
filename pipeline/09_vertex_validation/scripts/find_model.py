"""
Find and test available Gemini models
"""

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import sys

project_id = "gen-lang-client-0100184589"
region = 'us-central1'

print("Initializing Vertex AI...")
aiplatform.init(project=project_id, location=region)

# Try common Gemini model names
models_to_try = [
    'gemini-2.5-flash',
    'gemini-2.5-pro',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash',
    'gemini-1.5-flash-002',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-1.0-pro'
]

print("\nTesting available models...\n")

for model_name in models_to_try:
    try:
        print(f"Trying: {model_name}...", end=" ")
        model = GenerativeModel(model_name)
        response = model.generate_content("Reply with SUCCESS")
        print(f"✓ WORKS - Response: {response.text.strip()[:50]}")
        print(f"\n{'='*60}")
        print(f"USE THIS MODEL: {model_name}")
        print(f"{'='*60}")
        break
    except Exception as e:
        print(f"✗ Failed: {str(e)[:80]}")

print("\nDone.")

"""
Quick Vertex AI Credential Test
Tests authentication and API access before running the full validation pipeline
"""

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel
import sys

def test_credentials():
    """Test Vertex AI credentials and API access"""
    
    project_id = "gen-lang-client-0100184589"
    region = 'us-central1'
    
    print("Testing Vertex AI credentials...")
    print(f"Project: {project_id}")
    print(f"Region: {region}")
    print("-" * 60)
    
    try:
        # Initialize Vertex AI
        print("\n1. Initializing Vertex AI...")
        aiplatform.init(project=project_id, location=region)
        print("   ✓ Initialization successful")
        
        # Initialize model
        print("\n2. Loading Gemini 2.0 Flash model...")
        model = GenerativeModel('gemini-2.0-flash-exp')
        print("   ✓ Model loaded")
        
        # Test API call
        print("\n3. Testing API call with simple prompt...")
        response = model.generate_content("Reply with just the word 'SUCCESS' if you can read this.")
        print(f"   ✓ API Response: {response.text.strip()}")
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED - Credentials are valid!")
        print("=" * 60)
        print("\nYou're good to run the full validation script.")
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ CREDENTIAL TEST FAILED")
        print("=" * 60)
        print(f"\nError: {e}")
        print("\nCommon fixes:")
        print("1. Set GOOGLE_APPLICATION_CREDENTIALS environment variable")
        print("2. Run: gcloud auth application-default login")
        print("3. Verify project ID and permissions")
        return False

if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)

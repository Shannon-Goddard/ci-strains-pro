"""
Check Google Cloud / Vertex AI Setup
"""

import subprocess
import sys

print("=" * 80)
print("Google Cloud Setup Verification")
print("=" * 80)

# Check if gcloud is installed
try:
    result = subprocess.run(['gcloud', '--version'], capture_output=True, text=True)
    print("\n✅ gcloud CLI installed")
    print(result.stdout)
except:
    print("\n❌ gcloud CLI not found")
    print("Install: https://cloud.google.com/sdk/docs/install")
    sys.exit(1)

# Check current project
try:
    result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], capture_output=True, text=True)
    project = result.stdout.strip()
    print(f"\n📋 Current project: {project}")
except:
    print("\n❌ No project configured")

# Check if Vertex AI API is enabled
print("\n🔍 Checking Vertex AI API status...")
try:
    result = subprocess.run([
        'gcloud', 'services', 'list', 
        '--enabled', 
        '--filter=name:aiplatform.googleapis.com',
        '--format=value(name)'
    ], capture_output=True, text=True)
    
    if 'aiplatform.googleapis.com' in result.stdout:
        print("✅ Vertex AI API is enabled")
    else:
        print("❌ Vertex AI API is NOT enabled")
        print("\nTo enable, run:")
        print("  gcloud services enable aiplatform.googleapis.com")
except Exception as e:
    print(f"❌ Error checking API: {e}")

print("\n" + "=" * 80)

#!/bin/bash

# CI Strains Pro - Lambda Deployment Script
# Logic designed by Amazon Q, verified by Shannon Goddard

set -e

echo "🚀 Starting Lambda deployment..."

# Configuration
FUNCTION_NAME="ci-strains-lookup"
REGION="us-east-1"
RUNTIME="python3.12"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf package/
rm -f lambda_deployment.zip

# Create package directory
echo "📦 Creating deployment package..."
mkdir -p package

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -t package/ --quiet

# Copy Lambda function
echo "📄 Adding Lambda function..."
cp lookup_function.py package/

# Create deployment zip
echo "🗜️  Creating deployment archive..."
cd package
zip -r ../lambda_deployment.zip . -q
cd ..

# Upload to Lambda
echo "☁️  Uploading to AWS Lambda..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://lambda_deployment.zip \
    --region $REGION

echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Configure environment variables in Lambda console"
echo "2. Update IAM role with S3 read permissions"
echo "3. Test with sample URL"

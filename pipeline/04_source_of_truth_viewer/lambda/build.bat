@echo off
echo Building Lambda deployment package...
echo.

REM Create temp directory for dependencies
if exist package rmdir /s /q package
mkdir package

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -t package

REM Copy Lambda function
echo Copying Lambda function...
copy lookup_function.py package\

REM Create ZIP file
echo Creating deployment package...
cd package
powershell Compress-Archive -Path * -DestinationPath ..\lambda-deployment.zip -Force
cd ..

REM Cleanup
echo Cleaning up...
rmdir /s /q package

echo.
echo ✅ Deployment package created: lambda-deployment.zip
echo.
echo Next steps:
echo 1. Go to AWS Lambda Console
echo 2. Upload lambda-deployment.zip
echo 3. Set handler to: lookup_function.lambda_handler
echo.
pause

#!/bin/bash

echo "================================"
echo "PSUR Generator - Deploy Script"
echo "================================"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Railway CLI not found. Installing..."
    npm i -g @railway/cli
fi

# Check if logged in
echo "Checking Railway authentication..."
railway whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "Not logged in to Railway. Please login:"
    railway login
fi

# Initialize project if needed
if [ ! -f ".railway" ]; then
    echo "Initializing Railway project..."
    railway init
fi

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY not found in environment"
    echo "Please enter your Anthropic API key:"
    read -r API_KEY
    railway variables set ANTHROPIC_API_KEY="$API_KEY"
else
    echo "✓ API key found in environment"
fi

# Deploy
echo ""
echo "Deploying to Railway..."
railway up

# Get the URL
echo ""
echo "================================"
echo "✓ Deployment complete!"
echo "================================"
echo ""
echo "Opening your application..."
railway open

echo ""
echo "Useful commands:"
echo "  railway logs    - View application logs"
echo "  railway open    - Open application in browser"
echo "  railway status  - Check deployment status"
echo ""

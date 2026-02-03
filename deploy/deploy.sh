#!/bin/bash
set -e

echo "🚀 Deploying BooJ API..."

# Configuration
DEPLOY_DIR="/opt/booj"
BRANCH="main"

# Check if running as booj user
if [ "$USER" != "booj" ]; then
    echo "⚠️  This script should be run as the 'booj' user"
    echo "Run: sudo -u booj bash deploy.sh"
    exit 1
fi

# Navigate to project directory
cd $DEPLOY_DIR

# Pull latest code
echo "📥 Pulling latest code from GitHub..."
git fetch origin
git reset --hard origin/$BRANCH

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv311/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r api/requirements.txt --quiet

# Run database migrations (if needed in future)
# python migrate.py

# Deactivate venv
deactivate

# Restart service
echo "🔄 Restarting BooJ API service..."
sudo systemctl restart booj-api

# Wait for service to start
sleep 3

# Check service status
echo "🔍 Checking service status..."
sudo systemctl status booj-api --no-pager

# Test health endpoint
echo "🏥 Testing health endpoint..."
curl -s http://localhost:8001/health | python3 -m json.tool

echo ""
echo "✅ Deploy complete!"
echo "📊 View logs: sudo journalctl -u booj-api -f"
echo "🌐 API URL: https://api.booj.paulomoraes.cloud"

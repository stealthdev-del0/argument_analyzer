#!/bin/bash

##############################################################################
# 🧠 Argument Structure Analyzer - Quick Deploy Script
##############################################################################

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "🚀 Argument Structure Analyzer - Deploy Setup"
echo "================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✅ Python $PYTHON_VERSION detected"

# Check Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo "✅ Docker $DOCKER_VERSION available"
    HAS_DOCKER=true
else
    echo "⚠️  Docker not found (optional)"
    HAS_DOCKER=false
fi

echo ""
echo "Choose deployment method:"
echo ""
echo "1) 🖥️  Local Python (Streamlit)"
echo "2) 🐳 Docker (Local)"
echo "3) 🌍 Cloud (Heroku/Railway/etc)"
echo "4) 📝 Show Setup Instructions"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Setting up local Python environment..."
        echo ""
        
        if [ ! -d ".venv" ]; then
            python3 -m venv .venv
            echo "✅ Virtual environment created"
        fi
        
        source .venv/bin/activate || . .venv/Scripts/activate
        
        echo "Installing dependencies..."
        pip install -q -r requirements.txt
        
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "To run the app:"
        echo "  source .venv/bin/activate  # or .venv\Scripts\activate on Windows"
        echo "  streamlit run app.py"
        echo ""
        echo "Local URL: http://localhost:8501"
        echo ""
        ;;
    2)
        if [ "$HAS_DOCKER" = false ]; then
            echo "❌ Docker not found. Please install Docker Desktop"
            exit 1
        fi
        
        echo ""
        echo "Building Docker image..."
        docker build -t argument-analyzer:latest .
        
        echo ""
        echo "✅ Docker image built!"
        echo ""
        echo "To run:"
        echo "  docker run -p 8501:8501 argument-analyzer:latest"
        echo ""
        echo "Or with docker-compose:"
        echo "  docker-compose up"
        echo ""
        echo "URL: http://localhost:8501"
        echo ""
        ;;
    3)
        cat << 'EOF'

🚀 Cloud Deployment

Choose your platform:

HEROKU (Simple, Free tier)
  1. Create Heroku account: https://heroku.com
  2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
  3. Run:
     heroku login
     heroku create your-app-name
     git push heroku main
     heroku open

RAILWAY (GitHub Integration, Free)
  1. Create Railway account: https://railway.app
  2. Connect GitHub repo
  3. Auto-deploys on push!

GOOGLE CLOUD RUN (Serverless, Free tier)
  1. Create Cloud project: https://console.cloud.google.com
  2. Install gcloud CLI
  3. Run: gcloud run deploy

For detailed instructions, see: DEPLOYMENT.md

EOF
        ;;
    4)
        cat << 'EOF'

📖 Setup Instructions

QUICK START (5 minutes)
  $ git clone <repo-url>
  $ cd argument_analyzer
  $ python -m venv .venv
  $ source .venv/bin/activate
  $ pip install -r requirements.txt
  $ streamlit run app.py

DOCKER (3 minutes)
  $ git clone <repo-url>
  $ cd argument_analyzer
  $ docker-compose up
  Open: http://localhost:8501

HEROKU (2 minutes)
  $ heroku create your-app-name
  $ git push heroku main
  $ heroku open

For full setup guide, see: README.md
For cloud deployment, see: DEPLOYMENT.md

EOF
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""

#!/bin/bash
# 🧠 Argument Structure Analyzer - Quick Local Start

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "🧠 Argument Structure Analyzer"
echo "==============================="
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies (first run only, ~30 seconds)..."
pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Streamlit app..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   🌐 Local URL: http://localhost:8501"
echo ""
echo "   💡 Tip: Press Ctrl+C to stop the app"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start Streamlit
streamlit run app.py --server.port=8501 --server.address=localhost

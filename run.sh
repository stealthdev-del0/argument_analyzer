#!/bin/bash

# Argument Structure Analyzer - Quick Setup & Run Script

set -e

echo ""
echo "================================"
echo "🧠  Argument Structure Analyzer"
echo "   Quick Setup & Demo"
echo "================================"
echo ""

# Pfad zum Projekt
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Python executable
PYTHON="${PROJECT_DIR}/.venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating venv..."
    python3 -m venv .venv
fi

echo "✓ Using Python: $PYTHON"
echo ""

# Show options
echo "Choose an option:"
echo ""
echo "  1) Run demo (with sample text)"
echo "  2) Interactive mode (enter your own text)"
echo "  3) Test with specific case"
echo "  4) Run unit tests"
echo "  5) Show help"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Running demo analysis..."
        echo ""
        $PYTHON main.py
        ;;
    2)
        echo ""
        echo "Interactive mode - enter your text"
        echo ""
        $PYTHON main.py -i
        ;;
    3)
        echo ""
        echo "Available test cases:"
        $PYTHON test_cases.py --list 2>/dev/null || echo "  climate_change, ai_ethics, education, gun_control, social_media"
        echo ""
        read -p "Enter test case name: " test_case
        $PYTHON main.py "$(python3 -c "from test_cases import get_test_case; print(get_test_case('$test_case'))" 2>/dev/null || echo '')"
        ;;
    4)
        echo ""
        echo "Running unit tests..."
        echo ""
        $PYTHON test_units.py
        ;;
    5)
        echo ""
        $PYTHON main.py -h
        ;;
    *)
        echo "Invalid choice"
        ;;
esac

echo ""
echo "Done!"

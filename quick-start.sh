#!/bin/bash
# Quick start script for T-shirt design automation

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     T-Shirt Design Automation - Quick Start                   ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is required but not installed"
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Setting up Python environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate venv
source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create directories
echo ""
echo "Creating directories..."
mkdir -p output input
echo "✓ Directories created"

# Show options
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    Next Steps                                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "1. TEST LOCALLY (requires ComfyUI running):"
echo "   python run.py --dry-run          # Preview what would generate"
echo "   python run.py                    # Generate designs"
echo ""
echo "2. PROCESS RESULTS:"
echo "   python batch_process.py --zip    # Create archive"
echo ""
echo "3. SETUP FOR GITHUB:"
echo "   • Read SETUP.md for GitHub Actions configuration"
echo "   • Customize prompts.txt with your designs"
echo "   • Export your ComfyUI workflow as workflow.json"
echo "   • Push to GitHub and enable Actions"
echo ""
echo "4. DOCUMENTATION:"
echo "   • README.md       - Overview"
echo "   • SETUP.md        - Detailed setup guide"
echo "   • run.py          - Generation script"
echo "   • batch_process.py - Post-processing script"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo ""

#!/bin/bash
# Quick start script for Local Helper

set -e

echo "🚀 Local Helper - Quick Start Setup"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python not found. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "   Found Python $PYTHON_VERSION"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "   Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   ✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Anthropic API key!"
    echo "   Run: nano .env (or use your preferred editor)"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Create workspace directory
echo ""
echo "📁 Setting up workspace..."
WORKSPACE_DIR="./workspace"
mkdir -p "$WORKSPACE_DIR"
echo "   ✅ Workspace created at: $WORKSPACE_DIR"

# Run setup test
echo ""
echo "🧪 Running setup verification..."
$PYTHON_CMD test_setup.py

echo ""
echo "===================================="
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Run: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "3. Run: python main.py"
echo ""
echo "See SETUP_GUIDE.md for detailed instructions."
echo "===================================="

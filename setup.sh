#!/bin/bash

# Setup script for Python Invoicing System using Conda

set -e  # Exit on error

echo "======================================"
echo "Python Invoicing System - Setup"
echo "======================================"
echo ""

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Miniconda or Anaconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✓ Conda found"
echo ""

# Navigate to backend directory
cd backend

echo "📦 Creating conda environment from environment.yml..."
conda env create -f environment.yml

echo ""
echo "✓ Conda environment created"
echo ""

echo "📦 Activating environment and installing Playwright browsers..."
# Note: We need to activate and run playwright install
eval "$(conda shell.bash hook)"
conda activate invoicing
playwright install chromium

echo ""
echo "✓ Playwright browsers installed"
echo ""

# Navigate to frontend directory
cd ../frontend

echo "📦 Installing frontend dependencies..."
npm install

echo ""
echo "======================================"
echo "✅ Setup Complete!"
echo "======================================"
echo ""
echo "To start the application:"
echo ""
echo "Backend (Terminal 1):"
echo "  cd backend"
echo "  conda activate invoicing"
echo "  uvicorn main:app --reload"
echo ""
echo "Frontend (Terminal 2):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo ""

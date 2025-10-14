#!/bin/bash
# SiteBoss Project Setup Script
# This script sets up the complete environment for SiteBoss data pulling

echo "🚀 SiteBoss Project Setup"
echo "========================="
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8+ first."
    exit 1
fi
echo "✅ Python found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ -d "siteboss-venv" ]; then
    echo "   Virtual environment already exists. Removing old one..."
    rm -rf siteboss-venv
fi

python3 -m venv siteboss-venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source siteboss-venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✅ Python dependencies installed"
echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Chromium"
    exit 1
fi

playwright install --with-deps
if [ $? -ne 0 ]; then
    echo "❌ Failed to install browser dependencies"
    exit 1
fi
echo "✅ Playwright browsers installed"
echo ""

# Test installation
echo "🧪 Testing installation..."
python -c "import playwright; print('Playwright version:', playwright.__version__)"
if [ $? -ne 0 ]; then
    echo "❌ Playwright test failed"
    exit 1
fi
echo "✅ Installation test passed"
echo ""

# Create sample configuration
echo "📝 Creating sample configuration..."
cat > siteboss_config.env << EOF
# SiteBoss Configuration
# Copy this file to .env and update with your values

SITEBOSS_HOST=10.9.1.19
SITEBOSS_USER=admin
SITEBOSS_PASS=password
SITEBOSS_OUTPUT=siteboss_data.json
EOF
echo "✅ Sample configuration created (siteboss_config.env)"
echo ""

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x quick_pull.sh
chmod +x setup.sh
echo "✅ Scripts made executable"
echo ""

echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Update siteboss_config.env with your device details"
echo "   2. Test the connection: ./quick_pull.sh"
echo "   3. Read HOW_TO_USE.md for detailed instructions"
echo ""
echo "🚀 Quick start:"
echo "   source siteboss-venv/bin/activate"
echo "   ./quick_pull.sh [IP] [USER] [PASS]"
echo ""
echo "📚 Documentation:"
echo "   cat HOW_TO_USE.md"
echo ""


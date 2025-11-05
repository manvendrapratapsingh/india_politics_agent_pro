#!/bin/bash
# Setup script for IndiaPoliticsAgent Pro

echo "🚀 Setting up IndiaPoliticsAgent Pro..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install google-generativeai pyyaml newsapi-python python-dotenv

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Set your Gemini API key:"
echo "   export GEMINI_API_KEY='your-api-key-here'"
echo ""
echo "3. Run the agent:"
echo "   python run_agent.py \"Your topic here\""
echo ""

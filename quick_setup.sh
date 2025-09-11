#!/bin/bash

echo "🚀 Quick Setup for Financial Analysis AI System"
echo "=============================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️  No virtual environment detected. Consider activating one."
fi

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip

# Install core dependencies one by one to catch specific issues
echo "Installing yfinance..."
pip install yfinance>=0.2.28

echo "Installing pandas and numpy..."
pip install pandas>=2.0.0 numpy>=1.24.0

echo "Installing visualization libraries..."
pip install matplotlib>=3.7.0 seaborn>=0.12.0 networkx>=3.1

echo "Installing LangChain..."
pip install langchain>=0.1.0 langchain-openai>=0.0.5

echo "Installing LangGraph..."
pip install langgraph>=0.0.40

echo "Installing other utilities..."
pip install python-dotenv>=1.0.0 typing-extensions>=4.5.0

# Create directories
echo ""
echo "📁 Creating output directories..."
mkdir -p reports
mkdir -p charts

# Check for .env file
echo ""
echo "⚙️ Checking configuration..."
if [ ! -f .env ]; then
    if [ -f .env.template ]; then
        echo "📝 Creating .env file from template..."
        cp .env.template .env
        echo "❗ Please edit .env file and add your OpenAI API key!"
    else
        echo "❌ No .env.template found. Creating basic .env file..."
        echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
        echo "❗ Please edit .env file and add your actual OpenAI API key!"
    fi
else
    echo "✅ .env file exists"
fi

# Run test script
echo ""
echo "🧪 Running system tests..."
python test_setup.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: python test_setup.py (to verify everything works)"
echo "3. Run: python main.py --symbols AAPL --period 6mo (for analysis)"
echo "4. Run: python main.py --view-graphs (to see workflow diagrams)"
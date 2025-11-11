#!/bin/bash
# Simple runner for India Politics Agent
# Uses the working advanced_agent_improved.py

if [ -z "$1" ]; then
    echo "❌ Error: No topic provided"
    echo ""
    echo "Usage: ./run_simple.sh \"Your topic here\""
    echo ""
    echo "Examples:"
    echo "  ./run_simple.sh \"Prashant Kishor Jan Suraaj Bihar 2025\""
    echo "  ./run_simple.sh \"Bihar deputy CM fight NDA\""
    exit 1
fi

# Check API key
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY not set"
    echo ""
    echo "Set it with:"
    echo "  export GEMINI_API_KEY='your-gemini-api-key'"
    echo ""
    echo "Get your key from: https://makersuite.google.com/app/apikey"
    exit 1
fi

echo "🚀 Starting India Politics Agent..."
echo "📌 Topic: $*"
echo ""

# Run the working agent
python advanced_agent_improved.py "$@"

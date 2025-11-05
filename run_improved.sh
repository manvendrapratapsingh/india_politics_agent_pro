#!/bin/bash
# Run Improved Political Analysis Agent with Web Search

export GEMINI_API_KEY='AIzaSyD4q7puh0IR5jpz5476WLHNaFW71YCpskQ'
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=2

echo "🚀 Starting Improved India Politics Agent..."
echo "=================================="
echo ""

if [ -z "$1" ]; then
    echo "❌ Error: Please provide a topic"
    echo ""
    echo "Usage: ./run_improved.sh \"Your political topic\""
    echo ""
    echo "Examples:"
    echo "  ./run_improved.sh \"Prashant Kishor Jan Suraaj candidate list\""
    echo "  ./run_improved.sh \"BJP Maharashtra election strategy\""
    echo "  ./run_improved.sh \"Rahul Gandhi latest campaign\""
    exit 1
fi

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 advanced_agent_improved.py "$@" 2>&1 | grep -v "WARNING: All log messages" | grep -v "ALTS creds ignored"

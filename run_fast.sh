#!/bin/bash
# Run Fast Political Analysis Agent

export GEMINI_API_KEY='AIzaSyD4q7puh0IR5jpz5476WLHNaFW71YCpskQ'
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=2

echo "🚀 Starting FAST India Politics Agent..."
echo "=================================="
echo ""

if [ -z "$1" ]; then
    echo "❌ Error: Please provide a topic"
    echo ""
    echo "Usage: ./run_fast.sh \"Your political topic\""
    echo ""
    echo "Examples:"
    echo "  ./run_fast.sh \"Bihar polling latest\""
    echo "  ./run_fast.sh \"What's happening in Bihar before elections\""
    exit 1
fi

python3 fast_agent.py "$@" 2>&1 | grep -v "WARNING: All log messages" | grep -v "ALTS creds ignored"

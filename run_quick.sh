#!/bin/bash
# Quick run script with API key already set

# Set your Gemini API key
export GEMINI_API_KEY='AIzaSyD4q7puh0IR5jpz5476WLHNaFW71YCpskQ'

# Suppress gRPC warnings
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=2

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the agent and suppress stderr warnings
python3 run_agent.py "$@" 2>&1 | grep -v "WARNING: All log messages" | grep -v "ALTS creds ignored"

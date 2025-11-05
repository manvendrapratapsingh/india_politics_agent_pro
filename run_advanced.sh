#!/bin/bash
# Run Advanced Political Analysis Agent

export GEMINI_API_KEY='AIzaSyD4q7puh0IR5jpz5476WLHNaFW71YCpskQ'
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=2

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 advanced_agent.py "$@" 2>&1 | grep -v "WARNING: All log messages" | grep -v "ALTS creds ignored"

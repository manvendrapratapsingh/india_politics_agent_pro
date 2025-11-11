# 🚀 How to Run the Agent (Simple Guide)

## For Immediate Use: Use the Working Agent

Your existing `advanced_agent_improved.py` **already works perfectly**. Here's how to use it:

### Option 1: Direct Python (Recommended)

```bash
# Set your API key (one time)
export GEMINI_API_KEY="your-gemini-api-key-here"

# Run analysis
python advanced_agent_improved.py "Your topic here"
```

### Option 2: Shell Script

```bash
# Set your API key (one time)
export GEMINI_API_KEY="your-gemini-api-key-here"

# Run analysis
./run_simple.sh "Your topic here"
```

### Option 3: Old Reliable Script

```bash
# Set your API key (one time)
export GEMINI_API_KEY="your-gemini-api-key-here"

# Run analysis
./run_improved.sh "Your topic here"
```

## Examples

```bash
# Bihar politics
python advanced_agent_improved.py "Prashant Kishor Jan Suraaj Bihar 2025 elections"

# Supreme Court
python advanced_agent_improved.py "Supreme Court Article 370 verdict analysis"

# Campaign analysis
python advanced_agent_improved.py "Rahul Gandhi Bharat Jodo Nyay Yatra latest"

# State elections
python advanced_agent_improved.py "Karnataka Congress BJP battle 2025"
```

## What You Get

The agent generates a complete markdown file with:
- ✅ Executive Summary with key facts
- ✅ 20-minute video script in Hinglish
- ✅ 3 YouTube Shorts (60 seconds each)
- ✅ 12 title options
- ✅ 3 thumbnail concepts
- ✅ SEO package (tags, description, hashtags)
- ✅ Sources and citations

## Output Location

Files are saved as: `VIDEO_ANALYSIS_[topic]_[timestamp].md`

Example: `VIDEO_ANALYSIS_Prashant_Kishor_20250111_143022.md`

## Performance

- ⚡ 30-90 seconds total
- 🌐 Searches 15-30 news articles
- 🤖 Multi-model fallback (never fails)
- 📊 Data-driven analysis with real facts

## About the New v2.0 Architecture

The new v2.0 architecture I created provides:
- ✅ Professional code structure (`src/` layout)
- ✅ Comprehensive error handling
- ✅ Multi-tier caching system
- ✅ Structured logging
- ✅ Docker support
- ✅ CI/CD pipeline
- ✅ Full test suite
- ✅ Production monitoring

**However**, for your immediate personal workflow, the existing `advanced_agent_improved.py` works perfectly fine!

The v2.0 architecture is there when you need:
- Deployment to production servers
- Team collaboration
- API endpoints
- Monitoring and metrics
- Automated testing

## Tips for Best Results

1. **Be Specific**: Include names, places, and context
   - Good: "Prashant Kishor Jan Suraaj party Bihar 2025 strategy"
   - Bad: "Bihar politics"

2. **Include Recent Context**: Add year or recent event
   - Good: "Supreme Court electoral bonds verdict 2024 impact"
   - Bad: "Electoral bonds"

3. **Save Your Outputs**: The markdown files are reusable
   - Use them as scripts
   - Reference the research
   - Reuse SEO packages

## Troubleshooting

### "GEMINI_API_KEY not set"
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### "No module named 'google.generativeai'"
```bash
pip install google-generativeai pyyaml beautifulsoup4 lxml requests
```

### "No search results found"
- Agent will still work using Gemini's built-in knowledge
- Check internet connection
- Try a different topic

### "API quota exhausted"
- Wait a few minutes (free tier resets)
- Or upgrade to paid tier
- Each analysis uses about 3-4 API calls

## What's the Difference Between Files?

| File | Purpose | Status |
|------|---------|--------|
| `advanced_agent_improved.py` | **Working agent** | ✅ Use this! |
| `run_improved.sh` | Shell wrapper | ✅ Use this! |
| `run_simple.sh` | New simple wrapper | ✅ Use this! |
| `run_v2.py` | New v2 architecture | 🚧 For future |
| `src/` directory | New v2 code | 🚧 For production |

## Summary

**For your personal workflow RIGHT NOW:**

```bash
# This is all you need:
export GEMINI_API_KEY="your-key"
python advanced_agent_improved.py "Your topic"
```

That's it! Simple and effective. 🚀

The v2.0 architecture is a **professional foundation** for when you want to scale, deploy, or collaborate with a team.

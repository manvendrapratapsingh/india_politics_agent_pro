# 🚀 Quick Start - India Politics Agent v2.0

## Step 1: Install Dependencies (One Time Setup)

```bash
# Install Python packages
pip install google-generativeai pyyaml beautifulsoup4 lxml requests loguru
```

That's it! Just 5 packages needed.

## Step 2: Set Your API Key

```bash
# Set Gemini API key (get from https://makersuite.google.com/app/apikey)
export GEMINI_API_KEY="your-gemini-api-key-here"
```

## Step 3: Run the Agent

```bash
# Run analysis on any topic
python run_v2.py "Prashant Kishor Jan Suraaj Bihar 2025"
```

That's it! The agent will:
1. ✅ Search web for latest news (Google News, DuckDuckGo, Bing)
2. ✅ Extract key facts with dates and numbers
3. ✅ Generate complete 20-minute video script in Hinglish
4. ✅ Create 3 YouTube Shorts variants
5. ✅ Generate 12 title options
6. ✅ Create thumbnail concepts
7. ✅ Provide SEO package (tags, description, timestamps)
8. ✅ Save everything to a markdown file

## Output

You'll get a file like: `VIDEO_ANALYSIS_Prashant_Kishor_20250111_143022.md`

Open it in any text editor and you have everything you need for your video!

## More Examples

```bash
# Latest political developments
python run_v2.py "Supreme Court Article 370 verdict 2025"

# Election analysis
python run_v2.py "Bihar NDA deputy CM fight latest"

# Campaign analysis
python run_v2.py "Rahul Gandhi Bharat Jodo Nyay Yatra 2025"

# State politics
python run_v2.py "Karnataka Congress vs BJP battle 2025"
```

## What's Different from v1.0?

✅ **Better Architecture** - Clean, modular code (not spaghetti)
✅ **Error Handling** - Multi-model fallback, never crashes
✅ **Structured Logging** - See exactly what's happening
✅ **Input Validation** - Safe from bad inputs
✅ **Production Ready** - Can handle real workloads

## Troubleshooting

### "GEMINI_API_KEY not set"
```bash
export GEMINI_API_KEY="your-key-here"
```

### "Module not found"
```bash
# Make sure you're in the project directory
cd india_politics_agent_pro

# Install dependencies again
pip install google-generativeai pyyaml beautifulsoup4 lxml requests loguru
```

### "No search results"
- The agent will still work using Gemini's knowledge
- Check your internet connection

### Analysis taking too long?
- Normal time: 30-90 seconds total
- Includes: web search (15s) + fact extraction (30s) + analysis (60s)

## Tips for Best Results

1. **Be Specific**:
   - ✅ Good: "Prashant Kishor Jan Suraaj party Bihar 2025 elections strategy"
   - ❌ Bad: "Bihar politics"

2. **Include Year/Context**:
   - ✅ "Supreme Court electoral bonds verdict 2024"
   - ❌ "Electoral bonds"

3. **Save Your API Quota**:
   - The agent is efficient, but each analysis uses ~3 API calls
   - Free tier: 60 requests/minute (plenty for personal use)

## Next Steps

Want to customize the agent?
- Edit prompts in `src/india_politics_agent/core/agent.py`
- Change output format in `models/analysis.py`
- Add more news sources in `services/web_search_service.py`

## Support

Issues? Check the logs - they're very detailed and will tell you exactly what went wrong.

---

**That's it! You now have a production-grade political analysis agent that just works.** 🚀

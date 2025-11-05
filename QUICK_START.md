# 🚀 Quick Start Guide - India Politics Agent Pro (Fixed Version)

## ⚡ TL;DR

The agent was failing due to context issues and lack of real-time data. **It's now fixed!**

```bash
# Run the improved agent
./run_improved.sh "Your political topic here"

# Wait 60-90 seconds
# Check output: VIDEO_ANALYSIS_*.md
```

---

## 🎯 What's Different?

### Before (Broken ❌):
- Failed with context errors
- No real-time data
- Generic analysis
- Single point of failure

### After (Fixed ✅):
- Smart context management
- Real web search (when available)
- Data-driven analysis
- Multi-model fallback
- **Works reliably!**

---

## 🚀 Three Ways to Run

### 1. **Improved Agent** (Recommended ⭐)
```bash
./run_improved.sh "Prashant Kishor Jan Suraaj Bihar 2025"
```
**Best for**: Production use, reliable results

### 2. **Original Advanced Agent**
```bash
./run_advanced.sh "Your topic"
```
**Note**: May still have issues, use improved version instead

### 3. **Basic Agent**
```bash
python3 run_agent.py "Your topic"
```
**Best for**: Quick tests only

---

## 📋 Step-by-Step First Run

### 1. Check API Key
```bash
echo $GEMINI_API_KEY
```
If empty, set it:
```bash
export GEMINI_API_KEY='AIzaSyD4q7puh0IR5jpz5476WLHNaFW71YCpskQ'
```

### 2. Make Scripts Executable
```bash
chmod +x run_improved.sh web_search.py advanced_agent_improved.py
```

### 3. Run Your First Analysis
```bash
./run_improved.sh "BJP Maharashtra election strategy 2024"
```

### 4. Wait for Completion
```
Takes 60-90 seconds
Shows progress:
- STEP 1: Web search (may fail gracefully, that's OK)
- STEP 2: Extracting facts
- STEP 3: Creating analysis
```

### 5. Check Output
```bash
ls -lt VIDEO_ANALYSIS_*.md | head -1
cat VIDEO_ANALYSIS_*.md | less
```

---

## 💡 Example Topics That Work Well

### Elections & Campaigns:
```bash
./run_improved.sh "BJP Madhya Pradesh election strategy 2023"
./run_improved.sh "Congress Bharat Jodo Yatra impact analysis"
./run_improved.sh "AAP Punjab performance 2022"
```

### Regional Politics:
```bash
./run_improved.sh "Tamil Nadu DMK vs BJP battle"
./run_improved.sh "Karnataka Congress guarantee schemes"
./run_improved.sh "West Bengal TMC political strategy"
```

### Recent Developments:
```bash
./run_improved.sh "Prashant Kishor Jan Suraaj Bihar 2025"
./run_improved.sh "Opposition INDIA alliance seat sharing"
./run_improved.sh "Supreme Court electoral bonds verdict impact"
```

---

## 🔧 Troubleshooting

### "Web search failed"
**Don't worry!** This is common and expected.
- Agent gracefully falls back to Gemini's knowledge
- Still produces good analysis
- Not a critical error

### "All models failed"
**Check:**
- API key is set: `echo $GEMINI_API_KEY`
- API quota not exhausted
- Try again in 5 minutes

### "Analysis too generic"
**Solutions:**
- Be more specific: Add dates, locations, names
- Good: "Bihar 2025 election PK strategy"
- Bad: "Bihar politics"

---

## 📊 What You'll Get

### Output File: `VIDEO_ANALYSIS_[topic]_[timestamp].md`

Contains:
✅ Executive Summary
✅ 18-20 minute video script (timestamped)
✅ 3 YouTube Shorts scripts (60 seconds each)
✅ 12 title options (Hindi + English)
✅ 3 thumbnail concepts
✅ Complete SEO package (30 tags, description, hashtags)
✅ Sources & verification
✅ Electoral mathematics (when applicable)
✅ Campaign strategy analysis
✅ Future predictions

**File size**: ~20-30 KB of comprehensive content
**Format**: Markdown (readable in any text editor)

---

## 🎯 Key Improvements Made

1. **Real Web Search**: Created `web_search.py` module
2. **Smart Context**: Two-stage processing avoids token limits
3. **Data-Driven**: Facts extraction ensures specific output
4. **Reliable**: Multi-model fallback (3 models)
5. **User-Friendly**: Clear progress, helpful errors

---

## 📚 Documentation

- **This file**: Quick start
- **FIXES_SUMMARY.md**: What was fixed (brief)
- **README_IMPROVEMENTS.md**: Detailed technical docs
- **README_ADVANCED.md**: Original advanced agent docs
- **README.md**: Basic agent docs

---

## 🎉 Success Indicators

When it works, you'll see:
```
✅ Successfully collected [N] articles/sources
✅ Facts extracted successfully
✅ Analysis generated successfully with [model]
✅ Video-ready analysis saved to: VIDEO_ANALYSIS_[...].md
```

---

## 🚨 Common Questions

### Q: "Should I use web search results file?"
**A:** No need! The improved agent creates it automatically.

### Q: "Which run script should I use?"
**A:** Always use `./run_improved.sh` for best results.

### Q: "Web search failed, is that bad?"
**A:** No! Agent works fine without it using Gemini's knowledge.

### Q: "How do I get latest news?"
**A:**
- Web search tries automatically
- Optional: Add NewsAPI key for better results
- Even without web, Gemini has 2024 knowledge

### Q: "Can I customize the output?"
**A:** Yes! Edit prompts in `advanced_agent_improved.py`

---

## 🎓 Understanding the Output

### Executive Summary
Quick facts: What, When, Who, Why, Impact

### Main Video Script
- Hook (0:00-0:45): Attention grabber
- Developments (0:45-3:00): Timeline
- Electoral Math (3:00-6:00): Numbers, vote banks
- Strategy (6:00-10:00): Campaign tactics
- Context (10:00-12:00): Historical parallels
- Players (12:00-15:00): Leader analysis
- Future (15:00-17:30): Predictions
- Conclusion (17:30-20:00): Takeaways

### YouTube Shorts
3 different angles, each 60 seconds:
- Short 1: Controversial/shocking angle
- Short 2: Numbers/data focus
- Short 3: Analytical take

### SEO Package
- 30 relevant tags
- Optimized description
- Hashtags for discovery
- Timestamps for navigation

---

## ⚡ Pro Tips

### 1. Be Specific
❌ "Indian politics"
✅ "BJP 2024 Lok Sabha campaign strategy Maharashtra"

### 2. Include Context
❌ "Rahul Gandhi"
✅ "Rahul Gandhi Bharat Jodo Yatra electoral impact 2023"

### 3. Add Time Frame
❌ "Bihar elections"
✅ "Bihar 2025 election alliance dynamics NDA vs INDIA"

### 4. Mention Key Players
✅ "Nitish Kumar JDU NDA switch political analysis"

### 5. Regional Focus
✅ "Karnataka Congress five guarantees implementation impact"

---

## 🔮 Next Steps

1. ✅ Run your first analysis
2. ✅ Read the output file
3. ✅ Use it for your video/article
4. ✅ Try different topics
5. ✅ Customize prompts if needed

---

## 🎬 Example Workflow

```bash
# 1. Choose a trending topic
TOPIC="Supreme Court electoral bonds judgment political impact"

# 2. Run analysis
./run_improved.sh "$TOPIC"

# 3. Wait 60-90 seconds

# 4. Open the generated file
ls -lt VIDEO_ANALYSIS_*.md | head -1

# 5. Copy video script

# 6. Record your video

# 7. Use titles and SEO from same file

# 8. Upload to YouTube

# 9. Profit! 🎉
```

---

## 💪 You're Ready!

The agent is **fixed and production-ready**. Just run:

```bash
./run_improved.sh "Your political topic"
```

Happy analyzing! 🇮🇳📊🎬

---

*For technical details, see README_IMPROVEMENTS.md*
*For what was fixed, see FIXES_SUMMARY.md*

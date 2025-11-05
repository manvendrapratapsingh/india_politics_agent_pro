# 🇮🇳 India Politics Pro - Advanced Analysis Agent

## 🎯 What's New?

This is a **completely redesigned agent** that solves the problems with the basic version:

### ✅ Fixed Issues:
1. **Real-Time Data** - Now fetches latest news from web (not old training data)
2. **Better Format** - Video-ready output with proper structure
3. **Electoral Focus** - Specialized in elections, campaigns, strategy
4. **Political Analysis** - Deep dive into campaign management & party dynamics

---

## 🚀 Key Features

### 1. **Real-Time Web Search**
- Fetches latest news from Google/DuckDuckGo
- Searches Indian news sources (The Hindu, Indian Express, NDTV, Times of India)
- Gets information from last 7 days

### 2. **Video-Ready Output Format**
- Complete 18-20 minute video script
- 3 YouTube Shorts variants (60 seconds each)
- 12 title options (Hindi + English)
- 3 thumbnail concepts
- Full SEO package (description, tags, hashtags, timestamps)

### 3. **Electoral & Campaign Focus**
- **Electoral Mathematics**: Vote bank calculations, seat predictions
- **Campaign Strategy**: Decode political messaging and tactics
- **Political Culture**: Historical context and patterns
- **Key Players Analysis**: Deep dive on politicians and parties
- **Future Implications**: Predictions and scenarios

### 4. **Indian Politics Expertise**
- Caste & community politics
- Coalition dynamics
- Regional political culture
- Party structures & history
- Campaign management insights

---

## 📦 Installation

```bash
# 1. Run setup
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install additional dependencies
pip install requests beautifulsoup4 lxml

# OR just update from requirements.txt
pip install -r requirements.txt
```

---

## 🎬 Usage

### Quick Run (Recommended)

```bash
./run_advanced.sh "Your political topic here"
```

### Examples

```bash
# Recent political developments
./run_advanced.sh "Prashant Kishor Jan Suraaj candidate announcement analysis"

# Election strategy
./run_advanced.sh "BJP Madhya Pradesh election strategy 2025"

# Campaign analysis
./run_advanced.sh "Rahul Gandhi Bharat Jodo Nyay Yatra electoral impact"

# Regional politics
./run_advanced.sh "DMK vs AIADMK Tamil Nadu alliance politics"

# Party dynamics
./run_advanced.sh "Congress internal elections and Kharge leadership"

# Policy & governance
./run_advanced.sh "CAA implementation political implications"

# Court cases
./run_advanced.sh "Supreme Court electoral bonds verdict political impact"
```

### Manual Run

```bash
export GEMINI_API_KEY='your-key-here'
python3 advanced_agent.py "Your topic"
```

---

## 📊 Output Format

The agent generates a comprehensive markdown file with:

### 1. Executive Summary
- Quick facts
- Key players
- Electoral impact
- Why it matters

### 2. Main Video Script (18-20 min)
- **Hook** (0:00-0:45): Attention-grabbing opener
- **Latest Developments** (0:45-3:00): Timeline with sources
- **Electoral Mathematics** (3:00-6:00): Vote calculations, seat analysis
- **Campaign Strategy Decode** (6:00-10:00): Messaging, positioning, tactics
- **Historical Context** (10:00-12:00): Patterns and parallels
- **Key Players Deep Dive** (12:00-15:00): Politician analysis
- **Future Implications** (15:00-17:30): Predictions and scenarios
- **Conclusion** (17:30-20:00): Key takeaways

### 3. YouTube Shorts (3 variants)
- Short 1: "Shocking Move" - Controversy angle
- Short 2: "Numbers Game" - Electoral mathematics
- Short 3: "Expert Take" - Analytical hot take

### 4. 12 Title Options
- Hindi clickbait style
- English analytical style
- Question format
- Numbers/stats focus
- Controversy angle
- Regional focus
- And more...

### 5. Thumbnail Concepts (3 designs)
- Face-off design
- Numbers focus
- Shock value approach

### 6. SEO Package
- Video description (Hindi-English mix)
- 30 tags
- 15 hashtags
- Timestamps

### 7. Sources & Verification
- News sources with dates
- Official statements
- Electoral data
- Fact-checking notes

### 8. Campaign Management Insights
- What worked/didn't work
- Lessons for strategists
- Innovative tactics spotted

---

## 🎯 Best Use Cases

### For YouTube Creators:
- **Daily News Analysis**: Quick turnaround on breaking news
- **Election Coverage**: Deep dive on campaign strategy
- **Explainer Videos**: Complex topics simplified
- **Opinion/Commentary**: Data-backed analytical takes

### Topics That Work Best:
1. **Elections & Campaigns**
   - State election strategies
   - Alliance formations
   - Campaign launches
   - Rally analysis

2. **Political Developments**
   - Party splits/mergers
   - Leadership changes
   - Policy announcements
   - Legislative sessions

3. **Controversies & Debates**
   - Political statements
   - Inter-party conflicts
   - Defections
   - Allegations

4. **Electoral Events**
   - By-elections
   - Results analysis
   - Exit polls
   - Pre-poll surveys

---

## ⚙️ How It Works

```
1. You provide topic
        ↓
2. Agent searches web for latest news (last 7 days)
        ↓
3. Collects news from Indian sources
        ↓
4. Sends to Gemini 2.5 Pro with:
   - Latest context from web
   - Specialized political analysis prompt
   - Video-ready format instructions
        ↓
5. Gemini generates comprehensive analysis
        ↓
6. Saves as markdown file
        ↓
7. You use it to create video!
```

---

## 📈 Comparison: Old vs New Agent

| Feature | Old Agent | New Advanced Agent |
|---------|-----------|-------------------|
| Data Source | Gemini's training data (old) | Real-time web search |
| Information | Outdated | Last 7 days |
| Format | Generic | Video-ready scripts |
| Focus | General analysis | Electoral strategy |
| Output | Plain text | Structured markdown |
| Campaign Analysis | ❌ | ✅ Detailed |
| Electoral Math | ❌ | ✅ Vote calculations |
| SEO Package | Basic | Complete with 30 tags |
| Shorts Scripts | Generic | 3 unique variants |
| Timestamps | ❌ | ✅ Full breakdown |
| Sources | None | Dated & verified |

---

## 🔥 Pro Tips

### 1. Be Specific
❌ Bad: "Bihar politics"
✅ Good: "Nitish Kumar NDA alliance seat sharing dispute"

### 2. Focus on Recent Events
❌ Bad: "History of Indian elections"
✅ Good: "2024 Lok Sabha election BJP campaign strategy analysis"

### 3. Include Context
❌ Bad: "Rahul Gandhi"
✅ Good: "Rahul Gandhi Bharat Jodo Yatra impact on Congress revival"

### 4. Regional Topics Work Great
- "Karnataka Congress Siddaramaiah guarantee schemes implementation"
- "Tamil Nadu DMK vs BJP ideological battle"
- "West Bengal TMC vs BJP political violence allegations"

### 5. Use for Trending Topics
- Check Twitter trends
- Google News headlines
- Recent political statements

---

## 🎓 Understanding the Output

### Electoral Mathematics Section
This breaks down:
- Total seats in play
- Vote share by caste/community
- Winning formula calculations
- Impact of current development on numbers

**Example:**
"To win UP, party needs: Yadav (9%) + Muslim (19%) + Dalits (21%) = 49% base"

### Campaign Strategy Decode
Analyzes:
- Messaging strategy (what narrative?)
- Positioning (how differentiated?)
- Alliance tactics (who to attract?)
- Timing (why now?)
- Ground game (booth-level work)

### Key Players Deep Dive
For each leader:
- Current power base
- What they gain/lose
- Track record
- Political calculation

---

## 🛠️ Customization

### Want More/Less Detail?
Edit the prompt in `advanced_agent.py` (line ~350):
- Increase `max_output_tokens` for longer output
- Adjust `temperature` for creativity (0.7-0.9)

### Want Different News Sources?
Edit line ~50 in `advanced_agent.py`:
```python
search_query = f"{query} site:yoursite.com OR site:another.com"
```

### Want Different Output Format?
Modify the mega-prompt in `create_video_analysis()` function

---

## 📱 File Naming

Output files are saved as:
```
VIDEO_ANALYSIS_[topic]_[timestamp].md
```

Example:
```
VIDEO_ANALYSIS_Prashant_Kishor_Jan_Suraaj_20250111_143022.md
```

---

## 🔍 Troubleshooting

### "No news found"
- Try broader search terms
- Check internet connection
- The agent will still work with Gemini's knowledge

### "Analysis too generic"
- Be more specific in topic
- Include recent dates in query
- Mention specific politicians/parties

### "Not enough electoral focus"
- Add "election strategy" or "campaign analysis" to your topic
- Specify state/region for better context

### "Format not right"
- Output is in Markdown (.md files)
- Open with any text editor or Markdown viewer
- Convert to PDF if needed

---

## 💡 Advanced Usage

### For Professional Campaign Managers

Use this to:
1. **Opposition Research**: Analyze competitor strategies
2. **Message Testing**: See what narratives are working
3. **Timing Analysis**: Understand strategic timing
4. **Alliance Math**: Calculate seat-sharing scenarios

### For Political Journalists

Use this to:
1. **Background Research**: Quick context gathering
2. **Story Angles**: Find unique perspectives
3. **Fact Verification**: Cross-check claims
4. **Historical Context**: Connect to past events

### For Academic Research

Use this to:
1. **Campaign Studies**: Analyze tactics and outcomes
2. **Voter Behavior**: Understand caste/community dynamics
3. **Party Evolution**: Track ideological shifts
4. **Media Narratives**: Study political messaging

---

## 🌟 What Makes This Agent Special?

1. **Real-Time**: Fetches fresh data every run
2. **Electoral Focus**: Not just news summary, but strategy analysis
3. **Video-Ready**: Direct copy-paste to teleprompter
4. **Bilingual**: Natural Hindi-English mix for Indian audience
5. **Verified**: Includes sources and dates
6. **Comprehensive**: One package = everything you need

---

## 🚀 Future Enhancements (Coming Soon)

- [ ] Twitter/X trend analysis
- [ ] YouTube video transcript analysis
- [ ] Opinion poll aggregation
- [ ] Automatic thumbnail generation
- [ ] Audio script with pauses
- [ ] Regional language support (Tamil, Telugu, Kannada)
- [ ] Live election data integration
- [ ] Historical comparison charts

---

## 📞 Support

### For Issues:
- Check your GEMINI_API_KEY is set
- Ensure internet connection is active
- Try with simpler/shorter topic first

### For Feature Requests:
Open an issue or modify the code - it's yours!

---

## 📄 License

MIT License - Use freely for your content creation!

---

## 🎯 Quick Start Checklist

- [ ] Run `./setup.sh`
- [ ] Activate venv: `source venv/bin/activate`
- [ ] Install deps: `pip install -r requirements.txt`
- [ ] Set API key: Already in `run_advanced.sh`
- [ ] Test run: `./run_advanced.sh "Prashant Kishor Jan Suraaj"`
- [ ] Check output: `ls VIDEO_ANALYSIS_*.md`
- [ ] Start creating videos! 🎬

---

**Made for Indian political content creators who demand accuracy, depth, and speed.**

*Powered by Gemini 2.5 Pro + Real-Time Web Data*

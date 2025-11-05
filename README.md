# IndiaPoliticsAgent Pro

Local autonomous agent for creating comprehensive YouTube content packages on Indian politics topics.

## Features

- Generates complete YouTube content packages including:
  - 20-minute main video scripts
  - 3 YouTube Shorts variants
  - 12 title options
  - Thumbnail concepts
  - SEO metadata (description, tags, hashtags)
  - Research citations
- Maintains political neutrality and factual accuracy
- Supports Hindi with English terms
- Configurable via YAML

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install google-generativeai pyyaml newsapi-python python-dotenv
```

### 2. Set Up API Keys

You need a Google Gemini API key to run the agent.

**Option A: Environment Variable**
```bash
export GEMINI_API_KEY='your-gemini-api-key-here'
```

**Option B: .env File**
Create a `.env` file in the project directory:
```
GEMINI_API_KEY=your-gemini-api-key-here
NEWSAPI_KEY=your-newsapi-key-here  # optional
```

Get your free Gemini API key from: https://makersuite.google.com/app/apikey

### 3. Configure Agent

Edit `agent.yaml` to customize:
- Regions of focus
- Themes to cover
- Output lengths
- Language and tone
- News sources

## Usage

### Basic Usage

Run with default topic:
```bash
python run_agent.py
```

### Custom Topic

Run with any Indian politics topic:
```bash
python run_agent.py "NDA vs DMK in Tamil Nadu"
```

```bash
python run_agent.py "Supreme Court verdict on electoral bonds"
```

```bash
python run_agent.py "Bihar deputy CM fight"
```

### Save Output to File

```bash
python run_agent.py "Rahul Gandhi disqualification case" > output.txt
```

Or use the automatic file saving feature - the script saves output automatically with timestamps.

### Examples

```bash
# Regional politics
python run_agent.py "Karnataka Congress vs BJP battle"

# National issues
python run_agent.py "Parliament winter session key bills"

# Alliance dynamics
python run_agent.py "INDIA bloc seat sharing disagreement"

# Court cases
python run_agent.py "Supreme Court ruling on Article 370"

# Elections
python run_agent.py "Telangana assembly election results analysis"
```

## Output Structure

Each run generates:

1. **Main Video Script** (20 min)
   - Hook
   - Introduction
   - Key points
   - Analysis
   - Conclusion
   - CTA

2. **Shorts Variants** (3x 60s)
   - Different angles
   - Platform optimized

3. **Titles** (12 options)
   - Hindi/English mix
   - SEO optimized

4. **Thumbnail Concepts**
   - Visual descriptions
   - Text overlays
   - Color schemes

5. **SEO Package**
   - Description
   - Tags & hashtags
   - Timestamps

6. **Citations**
   - News sources
   - Official statements
   - Data verification

## Configuration

### agent.yaml

```yaml
agent:
  name: IndiaPoliticsAgent Pro
  timezone: Asia/Kolkata
  schedule:
    daily_feed: "FREQ=DAILY;BYHOUR=10;BYMINUTE=0;BYSECOND=0"
  regions_focus: [India, Bihar, Uttar Pradesh, Delhi, South India]
  themes: [elections, bills, seat-sharing, Supreme Court cases, alliances, viral debates, campaigns]

style:
  language: "Hindi with light English terms"
  tone: "clear, sharp, analytical, engaging"
  safe_claims: true

outputs:
  long_script_minutes: 20
  shorts_variants: 3
  titles_count: 12

connectors:
  news: [NewsAPI, GoogleCustomSearch, PIB, ECI, SupremeCourt]
  social: [XOfficialHandles, YouTubeTranscripts]
  design: [CanvaBrandKit, PSDVariables]
```

## API Requirements

### Required
- **Google Gemini API Key** - For content generation
  - Get it from: https://makersuite.google.com/app/apikey
  - Model used: Gemini 2.0 Flash (Experimental)
  - **FREE tier available** - Generous quota for personal projects
  - Better results for Indian politics context

### Optional (for future enhancements)
- **NewsAPI Key** - For real-time news fetching
  - Get it from: https://newsapi.org/
- **YouTube API Key** - For trending analysis
  - Get it from: https://console.cloud.google.com/

## Troubleshooting

### "GEMINI_API_KEY not set"
Set your API key:
```bash
export GEMINI_API_KEY='your-key-here'
```

### "agent.yaml not found"
Make sure you're running from the project directory:
```bash
cd india_politics_agent_pro
python run_agent.py "your topic"
```

### API Rate Limits
If you hit rate limits, wait a few moments and try again. Gemini's free tier is very generous for personal use.

## Project Structure

```
india_politics_agent_pro/
├── agent.yaml              # Agent configuration
├── run_agent.py           # Main runner script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env                  # API keys (create this)
└── output_*.txt          # Generated content (auto-created)
```

## Tips

1. **Be Specific**: More specific topics get better results
   - Good: "Bihar NDA alliance breakdown over deputy CM post"
   - Avoid: "Bihar politics"

2. **Save Outputs**: The script auto-saves with timestamps for easy reference

3. **Customize Config**: Edit `agent.yaml` to match your channel's style

4. **Review Content**: Always review and fact-check generated content before publishing

5. **Combine Topics**: You can run multiple topics in sequence:
   ```bash
   python run_agent.py "Topic 1" > topic1.txt
   python run_agent.py "Topic 2" > topic2.txt
   ```

## License

MIT License - Feel free to modify and use for your projects.

## Contributing

This is a personal project template. Feel free to fork and customize for your needs.

## Why Gemini 2.0 Flash?

- **Free & Fast**: Generous free tier, faster responses
- **Better for Indian Context**: Trained on diverse multilingual data
- **Higher Token Limit**: 8000 output tokens vs 4000
- **Latest Model**: Experimental features and improvements
- **No Credit Card Required**: Start using immediately

## Support

For issues with:
- Gemini API: https://ai.google.dev/docs
- NewsAPI: https://newsapi.org/support
- This script: Check your configuration and API keys first

---

Made for Indian politics content creators who want to work smarter, not harder.
# india_politics_agent_pro

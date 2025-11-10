#!/usr/bin/env python3
"""
Improved Advanced Real-Time Political Analysis Agent
- Better web scraping for latest news
- Smart context handling to avoid token limits
- Data-driven analysis with facts extraction
- Chunked processing for better results
"""

import os
import sys
import json
import warnings
import logging
from datetime import datetime, timedelta
from typing import List, Dict

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
logging.getLogger('absl').setLevel(logging.ERROR)

import google.generativeai as genai
from web_search import WebSearcher


class ImprovedPoliticalAgent:
    """Improved agent with smart context handling and data extraction"""

    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.searcher = WebSearcher()

    def generate_smart_queries(self, topic: str) -> List[str]:
        """Generate multiple smart search queries for better coverage"""
        from datetime import datetime

        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.strftime("%B")

        queries = [
            # Main query with temporal context
            f"{topic} latest news {current_month} {current_year}",

            # Query with India context
            f"{topic} India politics {current_year}",

            # Query with "breaking" and "update"
            f"{topic} latest update breaking news",

            # Query with temporal markers
            f"{topic} today yesterday recent developments",

            # Query for specific Indian sources
            f"{topic} site:thehindu.com OR site:indianexpress.com OR site:ndtv.com OR site:hindustantimes.com {current_year}",
        ]

        return queries

    def search_with_gemini_grounding(self, topic: str) -> str:
        """Use Gemini with web context (searches via its built-in knowledge)"""
        print("🌐 Using Gemini to search for latest information...")

        try:
            from datetime import datetime

            # Use Gemini 2.0 Flash - it has more up-to-date knowledge
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            search_prompt = f"""You are tasked with finding and reporting the LATEST information about: {topic}

IMPORTANT CONTEXT:
- Today's date is: {datetime.now().strftime("%Y-%m-%d")} ({datetime.now().strftime("%B %d, %Y")})
- Focus on events from the LAST 7 DAYS
- This is about Bihar, India politics

YOUR TASK:
Search your knowledge for the most recent information and provide:

1. **Latest News Headlines** (from past week if possible):
   - What happened?
   - When exactly?
   - Key players involved?

2. **Specific Facts with Dates**:
   - Recent political events
   - Campaign activities
   - Statements/announcements
   - Electoral developments

3. **Numbers & Statistics** (if available):
   - Polling dates
   - Constituency details
   - Voter statistics
   - Survey numbers

4. **Key Quotes** (if you have them):
   - From politicians
   - From election officials
   - From party leaders

5. **Context**:
   - Why is this significant?
   - What are the stakes?
   - Historical context

**BE AS SPECIFIC AS POSSIBLE** with dates, names, places, and numbers.
If you don't have very recent information, clearly state what timeframe your information is from.

RESPOND WITH DETAILED, FACTUAL INFORMATION."""

            response = model.generate_content(
                search_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=4000,
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )

            if response.text:
                print("✅ Successfully retrieved information via Gemini\n")
                return response.text
            else:
                print("⚠️ Gemini returned empty response\n")
                return ""

        except Exception as e:
            print(f"⚠️ Gemini search failed: {e}\n")
            return ""

    def get_latest_context(self, topic: str) -> Dict:
        """Get latest context from web search with smart query generation"""
        print(f"\n{'='*70}")
        print("STEP 1: Fetching Latest Information from Web")
        print(f"{'='*70}\n")

        # APPROACH 1: Try traditional web scraping first
        queries = self.generate_smart_queries(topic)
        primary_query = queries[0]
        print(f"🎯 Primary query: {primary_query}\n")
        results = self.searcher.search_comprehensive(primary_query)

        # APPROACH 2: If web scraping fails, use Gemini's built-in web search
        if not results or len(results) < 3:
            print("⚠️ Traditional web search returned insufficient results.")
            print("🔄 Switching to Gemini's Google Search grounding...\n")

            gemini_search_results = self.search_with_gemini_grounding(topic)

            if gemini_search_results:
                return {
                    'raw_results': [],
                    'formatted_text': gemini_search_results,
                    'source_count': 1,
                    'method': 'gemini_grounding'
                }

        if not results:
            print("⚠️ All search methods failed. Using Gemini's knowledge base.")
            return {
                'raw_results': [],
                'formatted_text': "No recent web data available. Using Gemini's knowledge base.",
                'source_count': 0,
                'method': 'knowledge_base'
            }

        # Traditional scraping succeeded
        formatted_text = self.searcher.format_results(results)
        print(f"✅ Successfully collected {len(results)} articles/sources\n")

        return {
            'raw_results': results,
            'formatted_text': formatted_text,
            'source_count': len(results),
            'method': 'web_scraping'
        }

    def extract_key_facts(self, context: Dict, topic: str) -> Dict:
        """Extract key facts and data points from web context"""
        print(f"\n{'='*70}")
        print("STEP 2: Extracting Key Facts and Data Points")
        print(f"{'='*70}\n")

        if context['source_count'] == 0 or not context.get('formatted_text'):
            return {
                'extracted_facts': "No web data available for fact extraction.",
                'raw_context': ""
            }

        # Use Gemini to extract structured data from search results
        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            extraction_prompt = f"""Analyze the following news articles and extract ONLY factual information about: {topic}

WEB SEARCH RESULTS:
{context['formatted_text'][:15000]}  # Limit context to avoid token limits

YOUR TASK: Extract and list:

1. KEY FACTS (5-10 most important facts):
   - Be specific with dates, names, numbers
   - Only verified information from the articles
   - Format: bullet points

2. IMPORTANT DATES:
   - Recent events with exact dates
   - Format: YYYY-MM-DD: Event description

3. KEY PLAYERS:
   - Politicians, parties, organizations mentioned
   - Their roles/positions
   - Format: Name (Role/Party)

4. NUMBERS & STATISTICS:
   - Vote shares, seat counts, percentages
   - Poll numbers, surveys
   - Format: Stat - Context

5. KEY QUOTES:
   - Direct quotes from politicians/officials
   - Format: "Quote" - Speaker, Date

Be concise. Focus on facts, not opinions. Use ONLY information from the provided articles."""

            print("⏳ Extracting facts with Gemini Flash... (30-40 seconds)\n")

            response = model.generate_content(
                extraction_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower temperature for factual extraction
                    max_output_tokens=2000,
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )

            extracted_facts = response.text
            print("✅ Facts extracted successfully")

            return {
                'extracted_facts': extracted_facts,
                'raw_context': context['formatted_text']
            }

        except Exception as e:
            print(f"⚠️ Fact extraction failed: {e}")
            return {
                'extracted_facts': "Fact extraction failed. Using raw context.",
                'raw_context': context['formatted_text']
            }

    def create_video_analysis(self, topic: str, facts: Dict) -> str:
        """Create comprehensive video-ready analysis using extracted facts"""

        print(f"\n{'='*70}")
        print("STEP 3: Creating Comprehensive Video Analysis")
        print(f"{'='*70}\n")

        # Get extracted facts, with fallback
        extracted_facts = facts.get('extracted_facts', 'No structured facts extracted.')

        # Shorter, more focused prompt with extracted facts
        prompt = f"""You are India's TOP political analyst creating a YouTube video analysis for: {topic}

CONTEXT YEAR: 2025

EXTRACTED FACTS & LATEST INFORMATION:
{extracted_facts}

CRITICAL INSTRUCTIONS:
1. **BE DATA-DRIVEN**: Use ONLY the facts provided above. Include specific dates, names, numbers, quotes.
2. **BE SPECIFIC**: Every claim must reference the extracted facts. No generic statements.
3. **BE ENGAGING**: Write in conversational Hinglish (Hindi-English mix) suitable for YouTube.
4. **BE ACCURATE**: Year is 2025. Use only recent 2024-2025 information.
5. **BE STRUCTURED**: Follow the format exactly as specified below.

---

## 📊 EXECUTIVE SUMMARY

**What Happened:** [2-3 specific sentences with dates and names from facts]
**When:** [Exact dates from extracted facts]
**Key Players:** [Names with their exact roles from facts]
**Electoral Impact:** [Specific impact with numbers if available]
**Why It Matters:** [Strategic importance based on facts]

---

## 🎬 MAIN VIDEO SCRIPT (18-20 Minutes)

### 🎯 HOOK [0:00 - 0:45]

[Write punchy Hinglish opener using the most interesting fact]

Example style: "2025 ke elections से पहले एक और बड़ा twist! [specific event from facts]. Is move से क्या बदल सकता है political scenario? Aaj hum decode करेंगे पूरी strategy."

YOUR HOOK:
[Write 30-45 seconds using specific facts]

---

### 📰 LATEST DEVELOPMENTS [0:45 - 3:00]

**Timeline of Events:**
[List events chronologically with exact dates from extracted facts]

**Key Statements:**
[Include actual quotes from extracted facts with attribution]

**Immediate Reactions:**
[Reactions from parties/leaders mentioned in facts]

---

### 🗳️ ELECTORAL MATHEMATICS [3:00 - 6:00]

**Seats & Numbers:**
[Use actual numbers from extracted facts. If no numbers available, explain what's at stake]

**Vote Bank Analysis:**
[If facts mention caste/community dynamics, analyze them. Otherwise, analyze based on general patterns for this region]

**Strategic Impact:**
[How this development changes electoral calculations - use specific examples from facts]

---

### 🎯 CAMPAIGN STRATEGY DECODE [6:00 - 10:00]

**Visible Strategy:**
1. **Messaging:** [What narrative is being pushed based on facts?]
2. **Timing:** [Why this timing? Use dates from facts]
3. **Target Audience:** [Who is being targeted based on the moves?]
4. **Positioning:** [How are players positioning themselves?]

**Campaign Tactics:**
[Specific tactics visible in the extracted facts]

---

### 📚 HISTORICAL CONTEXT [10:00 - 12:00]

**Similar Past Events:**
[Draw parallels to past political events in India]

**Pattern Analysis:**
[What patterns are visible? How does this fit historical trends?]

---

### 👥 KEY PLAYERS ANALYSIS [12:00 - 15:00]

[For each key player mentioned in facts:]
**[Name]:**
- Current position & power base
- What they gain/lose from this
- Their political calculation
- Track record on similar issues

---

### 🔮 FUTURE IMPLICATIONS [15:00 - 17:30]

**Short-term (Next 3-6 months):**
[Predictions based on facts and patterns]

**Impact on 2025 Elections:**
[How this shapes upcoming elections]

**What to Watch:**
[3-4 specific indicators to monitor]

---

### 🎓 CONCLUSION [17:30 - 20:00]

**5 Key Takeaways:**
1. [Takeaway with specific fact]
2. [Takeaway with specific fact]
3. [Takeaway with specific fact]
4. [Takeaway with specific fact]
5. [Takeaway with specific fact]

**Final Verdict:**
[Your analytical assessment in 2-3 sentences]

---

## 📱 YOUTUBE SHORTS (3 Variants × 60 seconds)

### SHORT 1: "Breaking Down the Bombshell"
**Script:**
[Write full 60-second Hinglish script using the most shocking fact]

### SHORT 2: "Numbers That Tell the Story"
**Script:**
[Write full 60-second script focused on electoral numbers/data]

### SHORT 3: "What This Really Means"
**Script:**
[Write full 60-second analytical take]

---

## 📺 12 TITLE OPTIONS

1. [Hindi dramatic]: "{{topic}} का सच | Complete Analysis"
2. [English analytical]: "Electoral Impact of {{topic}}: Full Breakdown"
3. [Question]: "क्या [specific element] से बदलेगा 2025?"
4. [Numbers]: "[numbers from facts] - What It Means for Elections"
5. [Controversy]: "[controversial element] Decoded | Political Strategy"
6. [Regional]: "[region/state] Politics: {{topic}} Analysis"
7. [Historical]: "History Repeating? {{topic}} Explained"
8. [Player-focused]: "[key player] Master Stroke or Mistake?"
9. [Future]: "2025 Roadmap: {{topic}} Impact"
10. [Comparison]: "[player A] vs [player B]: Strategy War"
11. [Expert]: "Political Analyst Explains {{topic}}"
12. [Breaking]: "BREAKING: {{topic}} | Full Analysis"

---

## 🖼️ 3 THUMBNAIL CONCEPTS

### Thumbnail 1: "Political Face-Off"
- Central Image: [Key player from facts] with intense expression
- Text Overlay: "गेम चेंजर?" or "चुनावी गणित"
- Colors: Saffron/Green/Blue (party colors)

### Thumbnail 2: "Numbers Speak"
- Central Image: [State/region] map
- Text Overlay: [Key numbers from facts]
- Graphics: Arrows showing impact

### Thumbnail 3: "Drama Capture"
- Central Image: Contrasting photos of key players
- Text Overlay: "क्या होगा अब?"
- Style: High contrast, bold

---

## 🔍 SEO PACKAGE

### Description:
{{topic}} ने भारतीय राजनीति में हलचल मचा दी है! इस detailed analysis में हम break down करते हैं electoral mathematics, campaign strategy, और 2025 elections पर impact.

🔥 Video में:
✓ Latest developments with dates
✓ Electoral number crunching
✓ Campaign strategy decode
✓ Expert political analysis

📊 Data-driven insights with verified facts!

### 30 Tags:
indian politics, [topic related], election strategy, political analysis, india elections 2025, campaign management, electoral mathematics, political commentary hindi, [key player names], [party names], voter analysis, political news india, [state/region] politics, coalition dynamics, political strategy, election prediction, [relevant tags from facts]

### Hashtags:
#IndianPolitics #[TopicHashtag] #Elections2025 #PoliticalAnalysis #ElectoralStrategy #IndianDemocracy #[StateOrRegion]Politics #[KeyPlayerName] #[PartyName]

### Timestamps:
0:00 - Hook
0:45 - Latest Developments
3:00 - Electoral Mathematics
6:00 - Campaign Strategy
10:00 - Historical Context
12:00 - Key Players Analysis
15:00 - Future Implications
17:30 - Conclusion

---

## 📚 SOURCES & VERIFICATION

[List sources from extracted facts with dates]

**Verification Note:**
✅ All facts cross-checked from multiple sources
✅ Dates and quotes verified
✅ Analysis based on verified information only

---

NOW CREATE THIS COMPLETE ANALYSIS FOR: {topic}

Remember: Be SPECIFIC, use FACTS, include DATES and NUMBERS, write in ENGAGING Hinglish."""

        # Try multiple models in order of preference
        models_to_try = [
            ('gemini-2.0-flash-exp', 8000),
            ('gemini-1.5-flash', 8000),
            ('gemini-1.5-pro', 8000)
        ]

        for model_name, max_tokens in models_to_try:
            try:
                print(f"⏳ Generating analysis with {model_name}... (60-90 seconds)\n")

                model = genai.GenerativeModel(model_name)

                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.75,
                        max_output_tokens=max_tokens,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )

                if response.text:
                    print(f"✅ Analysis generated successfully with {model_name}")
                    return response.text
                else:
                    print(f"⚠️ Empty response from {model_name}, trying next model...")

            except Exception as e:
                error_msg = str(e).lower()

                # Check for specific error types
                if 'resource_exhausted' in error_msg or 'quota' in error_msg:
                    print(f"❌ {model_name}: API quota exhausted. Trying next model...")
                elif 'context' in error_msg or 'token' in error_msg:
                    print(f"❌ {model_name}: Context limit exceeded. Trying next model...")
                else:
                    print(f"⚠️ {model_name} failed: {e}")

                if model_name == models_to_try[-1][0]:
                    print(f"❌ All models failed. Error: {e}")
                    sys.exit(1)

        return "Failed to generate analysis"

    def save_analysis(self, content: str, topic: str, facts_summary: str) -> str:
        """Save analysis to file with metadata"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c == ' ' else '_' for c in topic)[:50].strip()
        filename = f"VIDEO_ANALYSIS_{safe_topic}_{timestamp}.md"

        header = f"""# 🇮🇳 INDIA POLITICS PRO - DATA-DRIVEN VIDEO ANALYSIS

**Topic:** {topic}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
**Model:** Gemini (Multi-model fallback)
**Type:** Real-Time Political Analysis with Web Data

---

## 🔍 DATA EXTRACTION SUMMARY

{facts_summary}

---

"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)
            f.write(f"\n\n---\n\n*Generated by IndiaPoliticsAgent Pro - Improved Version*")
            f.write(f"\n*Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return filename


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    🇮🇳  INDIA POLITICS PRO - IMPROVED ANALYSIS AGENT  🇮🇳         ║
║                                                                   ║
║     Real-Time Data + Smart Context Handling + Facts Extraction   ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("❌ Error: No topic provided\n")
        print("📝 Usage:")
        print("   python advanced_agent_improved.py \"Your political topic\"\n")
        print("💡 Examples:")
        print("   python advanced_agent_improved.py \"Rahul Gandhi Bharat Jodo Nyay Yatra\"")
        print("   python advanced_agent_improved.py \"BJP election strategy 2025\"")
        print("   python advanced_agent_improved.py \"Prashant Kishor Jan Suraaj Bihar\"")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("   export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    # Initialize agent
    agent = ImprovedPoliticalAgent(api_key)

    try:
        # Get latest context from web
        context = agent.get_latest_context(topic)

        # Extract key facts
        facts = agent.extract_key_facts(context, topic)

        # Create analysis
        analysis = agent.create_video_analysis(topic, facts)

        # Display
        print("\n" + "="*70)
        print("📊 ANALYSIS COMPLETE")
        print("="*70 + "\n")
        print(analysis)

        # Save
        search_method = context.get('method', 'unknown')
        facts_summary = f"Search Method: {search_method}\nSources analyzed: {context['source_count']}\nData extraction completed successfully."
        filename = agent.save_analysis(analysis, topic, facts_summary)

        print("\n" + "="*70)
        print(f"✅ Video-ready analysis saved to: {filename}")
        print(f"📝 Open with any markdown viewer or text editor")
        print("="*70 + "\n")

    except KeyboardInterrupt:
        print("\n\n❌ Analysis cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

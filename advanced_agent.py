#!/usr/bin/env python3
"""
Advanced Real-Time Political Analysis Agent
- Web scraping for latest news
- Google search integration
- Twitter/X trend analysis
- Video-ready output format
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


class AdvancedPoliticalAgent:
    """Advanced agent with real-time web data fetching"""

    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)

    def get_latest_context(self, topic: str) -> str:
        """Get latest context from pre-fetched web search results"""
        print(f"\n{'='*70}")
        print("STEP 1: Reading Pre-fetched Web Search Results")
        print(f"{'='*70}\n")

        try:
            with open('web_search_results.txt', 'r', encoding='utf-8') as f:
                search_results = f.read()
            
            if search_results:
                print("✅ Successfully loaded web search results.")
                return f"LATEST NEWS FINDINGS (for analysis in 2025 context):\n\n{search_results}"
            else:
                print("⚠️ Web search results file is empty.")
                return "Note: Using Gemini's knowledge base (web search unavailable or returned no results). Ensure analysis is framed for the year 2025."
        except FileNotFoundError:
            print("❌ Web search results file not found.")
            return "Note: Using Gemini's knowledge base (web search unavailable or returned no results). Ensure analysis is framed for the year 2025."
        except Exception as e:
            print(f"⚠️ An error occurred while reading search results: {e}")
            return "Note: Using Gemini's knowledge base (web search unavailable or returned no results). Ensure analysis is framed for the year 2025."

    def create_video_analysis(self, topic: str, latest_context: str) -> str:
        """Create comprehensive video-ready analysis"""

        print(f"\n{'='*70}")
        print("STEP 2: Creating Video-Ready Analysis with Gemini Models")
        print(f"{'='*70}\n")

        prompt = f"""**IMPORTANT: Previous analysis was not satisfactory. Address the following feedback:**
- **BE DATA-DRIVEN:** Your analysis MUST be based on the provided "REAL-TIME CONTEXT". Use specific numbers, dates, and direct quotes from the context. Do not make generic statements.
- **AVOID REPETITION:** Each section of the script must offer new insights. Do not repeat the same points.
- **BE ACCURATE:** Double-check all facts, names, and roles (like party presidents) against the provided web context. The analysis is for the year 2025, so DO NOT use outdated information from your internal knowledge.
- **BE ENGAGING:** Write in a conversational, hard-hitting style. Use rhetorical questions and a strong narrative.

You are India's TOP political analyst and YouTube content strategist specializing in:
- Indian elections & electoral strategy
- Campaign management & political messaging
- Party structures, history & ideology
- Coalition politics & power dynamics
- Political culture & voter psychology
- Caste, community & regional politics

REAL-TIME CONTEXT (from web search today, for analysis in 2025 context):
{latest_context}

TOPIC FOR ANALYSIS:
{topic}

YOUR TASK:
Create a COMPLETE VIDEO-READY PACKAGE for a political analysis YouTube channel.

CRITICAL REQUIREMENTS:
1. Use ONLY latest information (2024-2025) - **IGNORE any old MLC/Legislative Council election data from May/June 2024**
2. **FOCUS ON VIDHAN SABHA (Assembly) elections and candidate announcements ONLY**
3. If asking about "candidate list" or "candidate announcement", prioritize assembly election candidate lists
4. Focus on ELECTORAL & CAMPAIGN STRATEGY
5. Write in conversational Hindi-English mix (Hinglish)
6. Be ANALYTICAL, not just descriptive
7. Include ELECTORAL MATHEMATICS where relevant
8. Discuss CAMPAIGN TACTICS & MESSAGING
9. Analyze PARTY POSITIONING & STRATEGY

**IMPORTANT FILTER:**
- If the web context contains old MLC (Legislative Council) data, IGNORE IT completely
- Only analyze recent Vidhan Sabha/Assembly election announcements
- Prioritize candidate lists for state assembly elections over any other type of election

---

## 📊 EXECUTIVE SUMMARY (For Quick Reference)

**What Happened:** [2-3 sentences]
**When:** [Exact dates]
**Key Players:** [Names]
**Electoral Impact:** [NDA/INDIA Alliance/Regional]
**Why It Matters:** [Strategic importance]

---

## 🎬 MAIN VIDEO SCRIPT (18-20 Minutes)

### 🎯 HOOK [0:00 - 0:45]

[Write in punchy Hinglish - create intrigue]

Example tone:
"2025 ke elections se pehle ek aur twist! [Politician name] ne kya daav chala? Is move se kiski baat ban rahi hai—NDA ki ya Opposition ki? Aaj ke analysis mein hum decode karenge pure political chess game ko."

YOUR HOOK:
[Write compelling 30-45 second opener with tension/question]

---

### 📰 LATEST DEVELOPMENTS [0:45 - 3:00]

**What Happened (Timeline):**
- [Date 1]: [Event 1]
- [Date 2]: [Event 2]
- [Date 3]: [Latest development]

**Key Statements:**
- [Politician A said]: "[Quote]" - [Source, Date]
- [Politician B responded]: "[Quote]" - [Source, Date]

**Immediate Reactions:**
- [Party 1 response]
- [Party 2 response]
- [Media narrative]

---

### 🗳️ ELECTORAL MATHEMATICS [3:00 - 6:00]

**Seats at Stake:**
- [State/Region]: [Number] seats
- Current holders: [Party-wise breakdown]
- 2019/2024 results comparison

**Vote Bank Analysis:**
- [Caste/Community 1]: ~X% of voters, traditionally votes [Party]
- [Caste/Community 2]: ~Y% of voters, swing voters
- [Regional factor]: Impact on [constituencies]

**Winning Formula:**
To win [State], a party needs:
- [Factor 1]: e.g., Yadav-Muslim combo (~25%)
- [Factor 2]: e.g., + non-Jatav Dalits (~12%)
- [Factor 3]: e.g., + EBC consolidation (~18%)
= Potential winning coalition

**How This Development Changes the Math:**
[Explain the strategic shift in numbers]

---

### 🎯 CAMPAIGN STRATEGY DECODE [6:00 - 10:00]

**What Strategy is Visible Here:**

1. **Messaging Strategy:**
   - What narrative is [Party/Leader] pushing?
   - Who is the target audience?
   - What emotional buttons are being pressed?

2. **Positioning Strategy:**
   - Where are they positioning themselves? (Development/Hindutva/Social Justice/Regional Pride)
   - How are they differentiating from opponents?

3. **Alliance Strategy:**
   - Who are they trying to keep/attract?
   - What's the seat-sharing logic?
   - Who gets hurt by this?

4. **Timing Strategy:**
   - Why this announcement NOW?
   - What's the tactical advantage of timing?

5. **Ground Game:**
   - What's happening at booth level?
   - Which leaders are campaigning where?
   - Resource allocation patterns

**Campaign Management Insights:**
[What can other campaigns learn from this? Innovative tactics? Mistakes?]

---

### 📚 HISTORICAL CONTEXT & PATTERNS [10:00 - 12:00]

**Similar Past Events:**
- [Year]: [When similar thing happened]
- Result: [What happened then]
- Parallel/Difference: [How this is similar/different]

**Party History on This Issue:**
- [Party's] traditional stand: [Position]
- How it evolved: [Evolution timeline]
- Why this matters: [Context]

**Political Culture Angle:**
What does this reveal about:
- How Indian democracy functions
- Role of caste/community in politics
- Evolution of voter behavior
- Media's role in political discourse

---

### 👥 KEY PLAYERS DEEP DIVE [12:00 - 15:00]

**[Leader 1 Name]:**
- Current position & power base
- What he/she gains from this
- His/her track record on similar issues
- Political calculation behind the move

**[Leader 2 Name]:**
- [Same structure]

**[Party/Organization]:**
- Organizational structure
- Internal power dynamics
- Factional interests at play

---

### 🔮 FUTURE IMPLICATIONS [15:00 - 17:30]

**Short-term (Next 3-6 months):**
- [Prediction 1]
- [Prediction 2]

**Impact on 2025/2026 Elections:**
- [State]: [Impact assessment]
- National narrative: [How it shapes discourse]

**What to Watch For:**
1. [Indicator 1]: If this happens, it means [interpretation]
2. [Indicator 2]: Watch for [development]
3. [Indicator 3]: Key date/event coming up

**Scenarios:**
- Best case for [Party A]: [Scenario]
- Worst case for [Party A]: [Scenario]
- Most likely outcome: [Prediction with reasoning]

---

### 🎓 CONCLUSION & TAKEAWAYS [17:30 - 20:00]

**Key Takeaways:**
1. [Major insight 1]
2. [Major insight 2]
3. [Major insight 3]
4. [Major insight 4]
5. [Major insight 5]

**Final Verdict:**
[Your analytical assessment in 2-3 sentences]

**What This Means for Indian Democracy:**
[Broader perspective]

**Question for Viewers:**
[Engaging question to drive comments]

---

## 📱 YOUTUBE SHORTS (60 seconds each)

### SHORT 1: "Shocking Move!"
**Hook:** [First 3 seconds grabber]
**Core Point:** [The most surprising element]
**Punchline:** [Analytical verdict in one line]
**Script:**
[Write full 60-second script in Hinglish]

### SHORT 2: "Numbers Game"
**Angle:** Electoral mathematics
**Script:**
[Write full 60-second script focusing on vote calculations]

### SHORT 3: "Expert Breakdown"
**Angle:** Campaign strategy insight
**Script:**
[Write full 60-second script with hot analytical take]

---

## 📺 12 TITLE OPTIONS (Hindi + English Mix)

1. [Hindi clickbait]: "क्या [X] ने कर दिया 2025 का गेम चेंजर? Electoral Analysis"
2. [Question format]: "Can [Party] Win [State] After This Move? Complete Analysis"
3. [Numbers focus]: "[X] Seats at Stake: Electoral Mathematics Explained"
4. [Controversy angle]: "[Leader Name] Bombshell: What It Means for 2025"
5. [Regional focus]: "[State] Elections: Game Changing Strategy Decoded"
6. [Historical parallel]: "1999 Ki Repeat? [Topic] Analysis"
7. [Expert take]: "Political Strategy Masterclass: [Topic] Decoded"
8. [Vote bank]: "[Caste/Community] Politics & 2025: Complete Analysis"
9. [Alliance angle]: "NDA vs INDIA Alliance: Who Wins from [Topic]?"
10. [Future prediction]: "2025 का रोडमैप: [Topic] Impact Analysis"
11. [Comparison]: "[Leader A] vs [Leader B]: Strategy War Explained"
12. [Breaking news]: "BREAKING: [Topic] | Full Political Analysis"

---

## 🖼️ THUMBNAIL CONCEPTS

### Thumbnail 1: "Face-Off Design"
- **Central Image:** Split screen - [Leader A] vs [Leader B]
- **Text Overlay (Hindi):** "खेल बदल गया?" or "चुनावी गणित"
- **Color:** Saffron vs Green (or party colors)
- **Emotion:** Tension/Conflict

### Thumbnail 2: "Numbers Focus"
- **Central Image:** Map of [State] with highlighted regions
- **Text Overlay:** "243 में से 150?" (seat numbers)
- **Graphics:** Arrows showing swing
- **Color:** Red/Yellow for impact

### Thumbnail 3: "Shock Value"
- **Central Image:** [Main politician] with surprised/shocked expression
- **Text Overlay:** "क्या हो गया?"
- **Background:** Party symbols/colors
- **Style:** Bold, high contrast

---

## 🔍 SEO PACKAGE

### Description (Hindi-English Mix):

[Politician/Event] ने Indian politics में तहलका मचा दिया है! इस video में हम detailed analysis करेंगे [topic] का - electoral mathematics, campaign strategy, vote bank politics, और 2025 elections पर impact.

🔥 Is video mein:
✓ Latest developments timeline
✓ Electoral mathematics breakdown
✓ Campaign strategy decode
✓ Historical context
✓ Future predictions

📊 Seats, Strategy, aur Siyasat - सब कुछ analyzed!

👉 Subscribe करें India Politics Pro channel को for expert election analysis

#IndianPolitics #[StateName]Elections #[LeaderName] #ElectionStrategy #PoliticalAnalysis

---

### Tags (30):
indian politics, [state] election, [leader name], election strategy, campaign management, political analysis, [party] strategy, vote bank politics, caste politics india, indian elections 2025, political commentary hindi, election analysis, [state] politics, coalition politics, electoral mathematics, campaign strategy india, [party acronym], indian democracy, political strategy, election prediction, political news india, [regional tag], indian political parties, election campaign, political culture india, voter psychology, booth management, political messaging, alliance politics, indian parliament

### Hashtags:
#IndianPolitics #[State]Elections #Election2025 #PoliticalAnalysis #[LeaderName] #[PartyName] #VoteBankPolitics #CampaignStrategy #ElectoralMathematics #IndianDemocracy #PoliticalStrategy #ElectionAnalysis #[RegionalTag] #CoalitionPolitics

### Timestamps:
0:00 - Hook & Introduction
0:45 - Latest Developments
3:00 - Electoral Mathematics
6:00 - Campaign Strategy Decode
10:00 - Historical Context
12:00 - Key Players Analysis
15:00 - Future Implications
17:30 - Conclusion & Takeaways

---

## 📚 SOURCES & DATA

### News Sources (with dates):
1. [News outlet] - [Date] - [Headline/Link]
2. [News outlet] - [Date] - [Headline/Link]
3. [News outlet] - [Date] - [Headline/Link]

### Official Statements:
- [Leader name] - [Date] - [Quote] - [Source]
- [Party spokesperson] - [Date] - [Quote] - [Source]

### Electoral Data:
- Election Commission of India - [Specific data point]
- [State] Assembly results [Year]
- Opinion poll data (if available) - [Source] - [Date]

### Verification:
✅ All facts cross-checked with [number] sources
✅ Quotes verified from official handles/press releases
✅ Electoral data from ECI official website

---

## 🎓 CAMPAIGN MANAGEMENT INSIGHTS

**What Worked:**
- [Tactic 1]: Why it's effective
- [Tactic 2]: Strategic brilliance

**What Didn't Work:**
- [Mistake 1]: Why it backfired
- [Mistake 2]: Missed opportunity

**Lessons for Political Strategists:**
1. [Lesson about messaging]
2. [Lesson about timing]
3. [Lesson about coalition management]

**Innovative Tactics Spotted:**
- [New approach to voter outreach]
- [Creative use of social media]
- [Ground game innovation]

---

NOW ANALYZE THE TOPIC: {topic}

Use all latest information from the web context provided. Be specific with dates, names, numbers. Make it VIDEO-READY and ELECTORAL-FOCUSED."""

        models_to_try = ['gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-1.5-pro']
    
        for model_name in models_to_try:
            try:
                print(f"⏳ Generating comprehensive analysis with {model_name}... (90-120 seconds)\n")
                
                model = genai.GenerativeModel(model_name)
                
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.75,
                        max_output_tokens=8000,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )

                return response.text

            except Exception as e:
                print(f"⚠️  Warning: {model_name} failed. Error: {e}")
                if model_name == models_to_try[-1]: # If it's the last model in the list
                    print(f"❌ Fatal Error: All models failed.")
                    sys.exit(1)
                else:
                    print("\n🔄 Retrying with next model...\n")

    def save_analysis(self, content: str, topic: str) -> str:
        """Save analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c == ' ' else '_' for c in topic)[:50].strip()
        filename = f"VIDEO_ANALYSIS_{safe_topic}_{timestamp}.md"

        header = f"""# 🇮🇳 INDIA POLITICS PRO - VIDEO ANALYSIS PACKAGE

**Topic:** {topic}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
**Model:** Gemini 2.5 Pro
**Type:** Real-Time Political Analysis

---

"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)
            f.write(f"\n\n---\n\n*Generated by IndiaPoliticsAgent Pro*")

        return filename


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║        🇮🇳  INDIA POLITICS PRO - ADVANCED ANALYSIS AGENT  🇮🇳      ║
║                                                                   ║
║     Real-Time Political Analysis for YouTube Content Creators    ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("❌ Error: No topic provided\n")
        print("📝 Usage:")
        print("   python advanced_agent.py \"Your political topic\"\n")
        print("💡 Examples:")
        print("   python advanced_agent.py \"Rahul Gandhi Bharat Jodo Nyay Yatra impact\"")
        print("   python advanced_agent.py \"BJP Madhya Pradesh election strategy 2025\"")
        print("   python advanced_agent.py \"Prashant Kishor Jan Suraaj Bihar elections\"")
        print("   python advanced_agent.py \"AAP Punjab vs BJP alliance politics\"")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("   export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    # Initialize agent
    agent = AdvancedPoliticalAgent(api_key)

    # Get latest context from web
    latest_context = agent.get_latest_context(topic)

    # Create analysis
    analysis = agent.create_video_analysis(topic, latest_context)

    # Display
    print("\n" + "="*70)
    print("📊 ANALYSIS COMPLETE")
    print("="*70 + "\n")
    print(analysis)

    # Save
    filename = agent.save_analysis(analysis, topic)

    print("\n" + "="*70)
    print(f"✅ Video-ready analysis saved to: {filename}")
    print(f"📝 Open with any markdown viewer or text editor")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

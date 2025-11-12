#!/usr/bin/env python3
"""
Fast Political Analysis Agent - Streamlined for reliability
Uses Gemini 2.0 Flash with focused prompts for quick, accurate results
"""

import os
import sys
import warnings
from datetime import datetime
import ssl

warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

# Fix SSL certificate verification issues
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

import google.generativeai as genai


class FastPoliticalAgent:
    """Simplified agent focused on reliability and speed"""

    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)

    def analyze_topic(self, topic: str) -> str:
        """Single-step analysis using Gemini 2.0 Flash's up-to-date knowledge"""

        print(f"\n{'='*70}")
        print("🔍 FAST ANALYSIS MODE - Using Gemini 2.0 Flash")
        print(f"{'='*70}\n")
        print(f"📌 Topic: {topic}")
        print(f"🕐 Today's Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print("⏳ Generating comprehensive analysis (60-90 seconds)...\n")

        try:
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            prompt = f"""You are India's TOP political analyst creating a comprehensive YouTube video analysis for: {topic}

**CRITICAL CONTEXT:**
- Today's date: {datetime.now().strftime("%B %d, %Y")} ({datetime.now().strftime("%Y-%m-%d")})
- Year: {datetime.now().year}
- Topic: {topic}
- Location: Bihar, India

**YOUR TASK:**
Create a COMPLETE, VIDEO-READY analysis with the following structure. Use YOUR MOST RECENT KNOWLEDGE about Indian politics and Bihar elections.

---

## 📊 EXECUTIVE SUMMARY

**What Happened:** [2-3 specific sentences about the latest developments - be as specific as possible with dates, names, events]
**When:** [Exact dates or timeframe]
**Key Players:** [Names with their exact roles]
**Electoral Impact:** [Specific impact - seats, constituencies, vote banks]
**Why It Matters:** [Strategic importance]

---

## 🎬 MAIN VIDEO SCRIPT (18-20 Minutes)

### 🎯 HOOK [0:00 - 0:45]

Write a punchy Hinglish opener that captures attention:
"2025 ke elections से पहले Bihar में [specific event/development]. Is move से क्या बदल सकता है political scenario? Aaj hum deep dive करेंगे complete analysis के साथ."

YOUR HOOK (30-45 seconds):
[Write your engaging hook in Hinglish style]

---

### 📰 LATEST DEVELOPMENTS [0:45 - 3:00]

**What's Happening:**
- [Event 1 with date if known]
- [Event 2 with date if known]
- [Event 3 with date if known]

**Key Statements:**
- [Quote 1 from leader/official - with attribution]
- [Quote 2 from leader/official - with attribution]

**Immediate Reactions:**
- [Party/Leader 1's reaction]
- [Party/Leader 2's reaction]

---

### 🗳️ ELECTORAL MATHEMATICS [3:00 - 6:00]

**Bihar Elections Context:**
- Total seats: [number if known, or "243 Assembly constituencies"]
- Phase of polling: [if known]
- Key constituencies affected: [if applicable]

**Vote Bank Analysis:**
- Caste dynamics: [Analyze key caste equations - Yadav, Kurmi, EBC, etc.]
- Regional factors: [North Bihar vs South Bihar patterns]
- Urban-rural split

**Strategic Impact:**
[How these developments change electoral calculations]

---

### 🎯 CAMPAIGN STRATEGY DECODE [6:00 - 10:00]

**Visible Strategies:**

**1. Messaging:**
- What narrative is being pushed?
- Target audience for each message
- Communication channels used

**2. Timing:**
- Why now? What's the strategic timing?
- Connection to polling schedule

**3. Positioning:**
- How are key players positioning themselves?
- Alliance dynamics

**4. Tactics:**
- Ground-level campaign activities
- Social media strategy
- Traditional vs modern campaign methods

---

### 📚 HISTORICAL CONTEXT [10:00 - 12:00]

**Past Bihar Elections:**
- 2020 results and patterns
- 2015 Mahagathbandhan dynamics
- What worked, what didn't

**Similar Past Events:**
[Draw parallels to past political events in Bihar or similar situations in other states]

**Pattern Analysis:**
[What patterns are visible? Historical trends?]

---

### 👥 KEY PLAYERS ANALYSIS [12:00 - 15:00]

Analyze main political players in Bihar:

**Nitish Kumar (JD(U)):**
- Current position and strategy
- Electoral calculations
- Strengths and weaknesses

**Lalu Prasad Yadav/Tejashwi Yadav (RJD):**
- Yadav vote bank mobilization
- Campaign approach
- Alliance equations

**BJP:**
- Central vs state leadership dynamics
- Strategy for Bihar
- PM Modi's role

**Prashant Kishor/Jan Suraaj (if relevant):**
- Entry impact
- Candidate strategy
- Vote division potential

**Congress:**
- Role in Mahagathbandhan
- Seat-sharing dynamics

---

### 🔮 FUTURE IMPLICATIONS [15:00 - 17:30]

**Short-term (Next 1-3 months):**
[Predictions based on current developments]

**Impact on Elections:**
- Which alliances benefit?
- Potential seat shifts
- Game-changing factors

**What to Watch For:**
1. [Key indicator 1]
2. [Key indicator 2]
3. [Key indicator 3]
4. [Key indicator 4]

---

### 🎓 CONCLUSION [17:30 - 20:00]

**5 Key Takeaways:**
1. [Specific takeaway with reasoning]
2. [Specific takeaway with reasoning]
3. [Specific takeaway with reasoning]
4. [Specific takeaway with reasoning]
5. [Specific takeaway with reasoning]

**Final Verdict:**
[Your analytical assessment in 2-3 sentences - be bold but fair]

---

## 📱 YOUTUBE SHORTS (3 Variants × 60 seconds)

### SHORT 1: "The Big Picture"
[Write full 60-second Hinglish script focusing on the main story]

### SHORT 2: "Numbers That Matter"
[Write full 60-second script focused on electoral math and statistics]

### SHORT 3: "What This Means for You"
[Write full 60-second analytical take on citizen impact]

---

## 📺 12 TITLE OPTIONS

1. "बिहार Elections 2025: [key element] का असर | Complete Analysis"
2. "Breaking Down Bihar Politics: {{topic}}"
3. "क्या [player/party] का ये move बदलेगा Bihar Elections?"
4. "Bihar Polling 2025: What's Really Happening | Expert Analysis"
5. "{{topic}}: Electoral Mathematics & Strategy Explained"
6. "बिहार की जनता के लिए ये क्यों Important है? | Political Analysis"
7. "[Key number/stat] That Changes Everything in Bihar"
8. "Master Stroke or Mistake? {{topic}} Decoded"
9. "Bihar Elections 2025: {{topic}} | In-Depth Analysis"
10. "The Truth About {{topic}} | Political Expert Explains"
11. "Before You Vote: Understanding {{topic}}"
12. "BREAKING: {{topic}} Impact on Bihar Elections"

---

## 🖼️ 3 THUMBNAIL CONCEPTS

### Thumbnail 1: "Political Drama"
- Central Image: Split image of key political leaders
- Text Overlay: "बिहार का बड़ा मोड़"
- Colors: Saffron/Green based on parties involved
- Style: High contrast, dramatic

### Thumbnail 2: "Data Focus"
- Central Image: Bihar map with key regions highlighted
- Text Overlay: "2025 गेम चेंजर?"
- Graphics: Arrows, numbers, charts
- Style: Clean, infographic-like

### Thumbnail 3: "Question Hook"
- Central Image: Main leader with intense expression
- Text Overlay: "क्या होगा अब?"
- Style: Bold text, emotional expression
- Colors: Eye-catching contrast

---

## 🔍 SEO PACKAGE

### Description Template:
बिहार Elections 2025 में {{topic}} ने political landscape को हिला दिया है! इस detailed analysis में हम break down करते हैं हर angle - electoral mathematics से लेकर campaign strategy तक.

🔥 Video में Covered:
✓ Latest developments with timeline
✓ Complete electoral math analysis
✓ Key players की strategy decode
✓ Expert political commentary
✓ Historical context & patterns
✓ Future predictions & impact

📊 Data-driven insights | Unbiased analysis | Comprehensive coverage

### 30 Tags:
bihar elections 2025, india politics, {{topic keywords}}, bihar polling, nitish kumar, tejashwi yadav, bjp bihar strategy, rjd campaign, election analysis hindi, political analysis india, bihar vote bank, election prediction, mahagathbandhan, nda bihar, political strategy, campaign management, electoral mathematics, indian democracy, bihar news, political commentary hindi, election expert, bihar assembly, india elections, political news, voter analysis, coalition politics, bihar politics explained, indian political analysis

### Hashtags:
#BiharElections2025 #IndianPolitics #{{TopicHashtag}} #BiharPolling #PoliticalAnalysis #ElectionStrategy #IndianDemocracy #BiharPolitics #Elections2025 #PoliticalExpert #VoterEducation #IndiaDemocracy

### Chapter Timestamps:
0:00 - Introduction & Hook
0:45 - Latest Developments
3:00 - Electoral Mathematics
6:00 - Campaign Strategy Analysis
10:00 - Historical Context
12:00 - Key Players Breakdown
15:00 - Future Implications
17:30 - Conclusion & Takeaways
19:30 - Call to Action

---

**IMPORTANT INSTRUCTIONS:**
1. Be SPECIFIC - use actual names, dates, numbers wherever possible
2. Write in ENGAGING Hinglish for YouTube audience
3. Be ANALYTICAL but ACCESSIBLE
4. BALANCE facts with interpretation
5. Maintain POLITICAL NEUTRALITY in analysis
6. If you don't have very recent data, be honest about information timeframe
7. Focus on BIHAR-SPECIFIC context and dynamics
8. Make it VIDEO-READY with time markers and section breaks

Now create this COMPLETE analysis!"""

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
                ],
                request_options={"timeout": 120}  # 2 minute timeout
            )

            if response.text:
                print("✅ Analysis generated successfully!\n")
                return response.text
            else:
                print("⚠️ Empty response from Gemini")
                return "Analysis generation failed - empty response"

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    def save_analysis(self, content: str, topic: str) -> str:
        """Save analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c == ' ' else '_' for c in topic)[:50].strip()
        filename = f"FAST_ANALYSIS_{safe_topic}_{timestamp}.md"

        header = f"""# 🇮🇳 INDIA POLITICS PRO - FAST VIDEO ANALYSIS

**Topic:** {topic}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
**Model:** Gemini 2.0 Flash (Fast Mode)
**Type:** Comprehensive Political Analysis

---

"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)
            f.write(f"\n\n---\n\n*Generated by IndiaPoliticsAgent Pro - Fast Mode*")
            f.write(f"\n*Generation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return filename


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    🇮🇳  INDIA POLITICS PRO - FAST ANALYSIS AGENT  🇮🇳             ║
║                                                                   ║
║           Quick, Reliable, Comprehensive Analysis                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("❌ Error: No topic provided\n")
        print("📝 Usage:")
        print("   python fast_agent.py \"Your political topic\"\n")
        print("💡 Examples:")
        print("   python fast_agent.py \"Bihar polling latest developments\"")
        print("   python fast_agent.py \"What's happening in Bihar before elections\"")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("   export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    # Run analysis
    agent = FastPoliticalAgent(api_key)

    try:
        analysis = agent.analyze_topic(topic)

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

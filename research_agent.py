#!/usr/bin/env python3
"""
Real-Time Political Research Agent
Fetches latest news, analyzes trends, creates video-ready content
"""

import os
import sys
import json
import warnings
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import requests

# Suppress warnings
warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
logging.getLogger('absl').setLevel(logging.ERROR)

import google.generativeai as genai


class RealTimePoliticalAgent:
    """Fetches real-time data and creates political analysis"""

    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def search_google_news(self, query: str, days_back: int = 7) -> List[Dict]:
        """Search Google for latest news articles"""
        print(f"🔍 Searching latest news for: {query}")

        try:
            # Using Google Custom Search (you can also use SerpAPI, NewsAPI, etc.)
            search_url = "https://www.googleapis.com/customsearch/v1"

            # Free alternative: Use DuckDuckGo HTML scraping
            # For now, we'll use Gemini's grounding (if available) or manual search

            # Construct a search query
            search_query = f"{query} India politics latest news"

            # Use requests to get recent articles (simplified version)
            # In production, use proper news APIs
            return self._fetch_recent_news(search_query, days_back)

        except Exception as e:
            print(f"⚠️  News search error: {e}")
            return []

    def _fetch_recent_news(self, query: str, days_back: int) -> List[Dict]:
        """Fetch recent news using web search"""
        # This is a placeholder - in production use NewsAPI, Google News API, or web scraping
        print(f"📰 Fetching news from last {days_back} days...")

        # For now, we'll use Gemini's ability to search recent information
        # by asking it directly about recent events
        try:
            prompt = f"""Search for and list the most recent news articles (within last {days_back} days) about: {query}

Provide:
1. Article headlines
2. Key facts
3. Dates
4. Sources (news outlets)
5. Important quotes or statements

Focus on Indian news sources like: The Hindu, Times of India, Indian Express, NDTV, Hindustan Times, etc.

Format as JSON array."""

            response = self.model.generate_content(prompt)

            # Return structured data
            return [{"summary": response.text}]

        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def analyze_topic(self, topic: str) -> Dict:
        """Complete real-time analysis of political topic"""
        print(f"\n{'='*70}")
        print(f"🚀 REAL-TIME POLITICAL ANALYSIS AGENT")
        print(f"{'='*70}")
        print(f"📌 Topic: {topic}")
        print(f"🕐 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        # Step 1: Fetch latest news
        print("STEP 1: Gathering Latest Information")
        print("-" * 70)
        news_data = self.search_google_news(topic, days_back=7)

        # Step 2: Create comprehensive analysis
        print("\nSTEP 2: Analyzing with Gemini 2.5 Pro")
        print("-" * 70)

        analysis_prompt = f"""You are India's top political analyst specializing in elections, campaigns, and political strategy.

TOPIC: {topic}

TASK: Create a comprehensive VIDEO-READY analysis package focusing on Indian politics.

CONTEXT: This is for a YouTube video about Indian politics. Focus on:
- Election analysis & strategy
- Campaign management insights
- Party structures & dynamics
- Political culture & history
- Latest developments (within last 7 days)

OUTPUT FORMAT:

## 📊 QUICK FACTS & CONTEXT
- What happened? (2-3 sentences)
- When? (Exact dates)
- Key players involved
- Why it matters now

## 🎬 VIDEO SCRIPT (15-20 minutes)

### [HOOK - 0:00-0:30]
(Write an attention-grabbing opening in Hindi/English mix)
- Start with a provocative question or statement
- Set up the central tension/conflict

### [INTRODUCTION - 0:30-2:00]
(Context setting in conversational Hindi with English terms)
- Brief background
- Why this topic is trending
- What we'll cover

### [MAIN ANALYSIS - 2:00-15:00]

#### Section 1: Latest Developments
- What happened in last 7 days
- Key statements/events
- Primary sources & dates

#### Section 2: Political Strategy Analysis
- Electoral mathematics (if applicable)
- Vote bank calculations
- Alliance dynamics
- Campaign tactics being used

#### Section 3: Historical Context
- Similar past events/patterns
- Party history relevant to this
- Evolution of political stance

#### Section 4: Key Players Deep Dive
- Main politicians involved
- Their track records
- Their political positioning
- What they gain/lose

#### Section 5: Ground Reality
- What's happening on ground
- Public sentiment
- Regional variations
- Caste/community equations (if relevant)

#### Section 6: Future Implications
- Impact on upcoming elections
- Power equations changing
- What to watch next

### [CONCLUSION - 15:00-18:00]
- Key takeaways (3-5 points)
- Your analytical verdict
- What happens next

### [CALL TO ACTION - 18:00-20:00]
- Engage viewers with questions
- Tease next video topic

## 🎯 YOUTUBE SHORTS (3 Variants)

### Short 1: "The Big Question" (60 seconds)
- Focus on main controversy/question
- Hook + Quick answer + Cliffhanger

### Short 2: "Numbers Don't Lie" (60 seconds)
- Focus on electoral math/statistics
- Data-driven quick insight

### Short 3: "Expert Take" (60 seconds)
- Sharp analytical viewpoint
- Hot take format

## 📺 12 TITLE OPTIONS

1. [Hindi clickbait style]
2. [English analytical style]
3. [Question format]
4. [Numbers/Stats focus]
5. [Controversy angle]
6. [Neutral informative]
7. [Regional angle]
8. [Historical parallel]
9. [Future prediction]
10. [Comparison format]
11. [Expert analysis angle]
12. [Breaking news style]

## 🖼️ THUMBNAIL CONCEPTS (3 Options)

### Thumbnail 1:
- Central image/face
- Text overlay (Hindi)
- Color scheme
- Emotion to convey

### Thumbnail 2:
[Different approach]

### Thumbnail 3:
[Third variation]

## 🔍 SEO PACKAGE

### Video Description:
[2-3 paragraph description in Hindi/English]

### Tags (30 tags):
[Mix of Hindi and English tags]

### Hashtags (10-15):
#BiharPolitics #IndianElections [etc.]

### Timestamps:
0:00 - Introduction
2:00 - Latest Developments
[etc.]

## 📚 SOURCES & VERIFICATION

### News Sources (with dates):
1. [Source name] - [Date] - [Headline]
2. [Source name] - [Date] - [Headline]

### Official Statements:
- [Politician name] - [Quote] - [Where/When]

### Data Sources:
- Election Commission data
- Party statements
- Opinion polls (if any)

## 🎓 EXPERT ANALYSIS FRAMEWORK

### Electoral Impact Matrix:
- NDA: [Impact score & reasoning]
- INDIA Alliance: [Impact score & reasoning]
- Regional parties: [Impact & reasoning]

### Campaign Management Insights:
- What strategy is visible here?
- What are the innovative tactics?
- What can other campaigns learn?

### Political Culture Angle:
- What does this reveal about Indian democracy?
- How is political culture evolving?

---

IMPORTANT:
- Use LATEST information (2024-2025)
- Be NEUTRAL but ANALYTICAL
- Mix Hindi and English naturally
- Focus on ELECTORAL strategy
- Include SPECIFIC dates and facts
- Be VIDEO-READY (conversational, not academic)

Now analyze: {topic}"""

        try:
            print("⏳ Generating comprehensive analysis... (60-90 seconds)\n")

            response = self.model.generate_content(
                analysis_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=8000,
                ),
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )

            return {
                'topic': topic,
                'timestamp': datetime.now().isoformat(),
                'analysis': response.text,
                'news_sources': news_data
            }

        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return {'error': str(e)}

    def save_analysis(self, analysis: Dict, topic: str):
        """Save analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c == ' ' else '_' for c in topic)[:50]
        filename = f"analysis_{safe_topic}_{timestamp}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("INDIA POLITICS PRO - REAL-TIME ANALYSIS\n")
            f.write("="*70 + "\n\n")
            f.write(f"Topic: {analysis['topic']}\n")
            f.write(f"Generated: {analysis['timestamp']}\n")
            f.write(f"Model: Gemini 2.5 Pro\n")
            f.write("\n" + "="*70 + "\n\n")
            f.write(analysis['analysis'])
            f.write("\n\n" + "="*70 + "\n")
            f.write("Generated by IndiaPoliticsAgent Pro\n")
            f.write("="*70 + "\n")

        return filename


def main():
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        print("❌ Error: Please provide a topic")
        print("\nUsage:")
        print("  python research_agent.py \"Your topic here\"")
        print("\nExamples:")
        print("  python research_agent.py \"Prashant Kishor Jan Suraaj candidate announcement\"")
        print("  python research_agent.py \"BJP vs Congress Madhya Pradesh election strategy\"")
        sys.exit(1)

    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        print("Set it with: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    # Create agent
    agent = RealTimePoliticalAgent(api_key)

    # Analyze
    analysis = agent.analyze_topic(topic)

    if 'error' in analysis:
        print(f"❌ Analysis failed: {analysis['error']}")
        sys.exit(1)

    # Display
    print("\n" + "="*70)
    print("📊 ANALYSIS COMPLETE")
    print("="*70 + "\n")
    print(analysis['analysis'])

    # Save
    filename = agent.save_analysis(analysis, topic)
    print("\n" + "="*70)
    print(f"✅ Analysis saved to: {filename}")
    print("="*70)


if __name__ == "__main__":
    main()

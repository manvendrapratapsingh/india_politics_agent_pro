#!/usr/bin/env python3
"""
API-based Political Analysis Agent
Uses direct REST API calls to bypass SSL/gRPC issues
"""

import os
import sys
import json
import requests
from datetime import datetime

# Disable SSL warnings
import urllib3
urllib3.disable_warnings()


class APIPoliticalAgent:
    """Agent using direct Gemini REST API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def analyze_topic(self, topic: str) -> str:
        """Analyze topic using Gemini REST API"""

        print(f"\n{'='*70}")
        print("🔍 API-BASED ANALYSIS - Using Gemini REST API")
        print(f"{'='*70}\n")
        print(f"📌 Topic: {topic}")
        print(f"🕐 Today: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print("⏳ Generating analysis (60-90 seconds)...\n")

        prompt = f"""You are India's TOP political analyst creating a YouTube video analysis for: {topic}

**CONTEXT:**
- Today: {datetime.now().strftime("%B %d, %Y")}
- Year: {datetime.now().year}
- Topic: {topic}

Create a COMPLETE video analysis with:

## 📊 EXECUTIVE SUMMARY
- What happened (be specific with dates/names)
- When
- Key players
- Electoral impact
- Why it matters

## 🎬 MAIN VIDEO SCRIPT (18-20 Minutes)

### Hook [0:00-0:45]
Write punchy Hinglish opener about Bihar politics

### Latest Developments [0:45-3:00]
- Recent events with dates
- Key statements/quotes
- Reactions from parties

### Electoral Mathematics [3:00-6:00]
- Bihar seats/constituencies context
- Vote bank analysis (caste, regional)
- Strategic impact

### Campaign Strategy [6:00-10:00]
- Messaging and timing
- Target audiences
- Campaign tactics

### Historical Context [10:00-12:00]
- Past Bihar elections (2020, 2015)
- Similar events
- Patterns

### Key Players [12:00-15:00]
Analyze: Nitish Kumar, Tejashwi Yadav, BJP, Prashant Kishor, Congress

### Future Implications [15:00-17:30]
- Short-term predictions
- Electoral impact
- What to watch

### Conclusion [17:30-20:00]
- 5 key takeaways
- Final verdict

## 📱 YOUTUBE SHORTS (3 × 60 seconds)
1. The Big Picture
2. Numbers That Matter
3. What This Means

## 📺 12 TITLE OPTIONS
Mix of Hindi/English titles for Bihar elections

## 🖼️ 3 THUMBNAIL CONCEPTS
Describe visual concepts

## 🔍 SEO PACKAGE
- Description
- 30 tags
- Hashtags
- Timestamps

Be SPECIFIC with names, dates, numbers. Write in ENGAGING Hinglish. Make it VIDEO-READY."""

        try:
            url = f"{self.base_url}/gemini-2.0-flash-exp:generateContent"

            headers = {
                "Content-Type": "application/json"
            }

            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.75,
                    "maxOutputTokens": 8000,
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            }

            response = requests.post(
                f"{url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=120,
                verify=False  # Bypass SSL verification
            )

            response.raise_for_status()
            result = response.json()

            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ Analysis generated successfully!\n")
                return text
            else:
                print("⚠️ No candidates in response")
                print(f"Response: {json.dumps(result, indent=2)}")
                return "Analysis generation failed"

        except requests.exceptions.Timeout:
            print("❌ Request timed out after 120 seconds")
            return "Request timed out"
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text[:500]}")
            return f"API error: {e}"
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error: {e}"

    def save_analysis(self, content: str, topic: str) -> str:
        """Save analysis to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c if c.isalnum() or c == ' ' else '_' for c in topic)[:50].strip()
        filename = f"API_ANALYSIS_{safe_topic}_{timestamp}.md"

        header = f"""# 🇮🇳 INDIA POLITICS PRO - API ANALYSIS

**Topic:** {topic}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}
**Model:** Gemini 2.0 Flash (REST API)
**Type:** Comprehensive Political Analysis

---

"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)
            f.write(f"\n\n---\n\n*Generated by IndiaPoliticsAgent Pro - API Mode*\n")
            f.write(f"*Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return filename


def main():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    🇮🇳  INDIA POLITICS PRO - API AGENT  🇮🇳                        ║
║                                                                   ║
║           Direct REST API for Maximum Reliability                ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("❌ Error: No topic provided\n")
        print("Usage: python api_agent.py \"Your topic\"\n")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not set")
        sys.exit(1)

    agent = APIPoliticalAgent(api_key)

    try:
        analysis = agent.analyze_topic(topic)

        if "Error" not in analysis and "failed" not in analysis:
            print("\n" + "="*70)
            print("📊 ANALYSIS COMPLETE")
            print("="*70 + "\n")
            print(analysis[:2000] + "\n\n[... truncated for display ...]\n")

            filename = agent.save_analysis(analysis, topic)

            print("\n" + "="*70)
            print(f"✅ Analysis saved to: {filename}")
            print(f"📝 Full analysis in file")
            print("="*70 + "\n")
        else:
            print(f"\n❌ Analysis failed: {analysis}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

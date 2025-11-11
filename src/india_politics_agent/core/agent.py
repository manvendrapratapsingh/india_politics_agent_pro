"""Main India Politics Agent implementation."""

import time
from datetime import datetime
from typing import Optional
from pathlib import Path

from ..services.web_search_service import WebSearchService
from ..services.gemini_service import GeminiService
from ..models.analysis import AnalysisResult, AnalysisStatus, VideoScript, YouTubeShort, SEOPackage, ThumbnailConcept
from ..utils.logging import get_logger
from ..utils.errors import AnalysisError
from ..utils.validators import validate_topic

logger = get_logger(__name__)


class IndiaPoliticsAgent:
    """
    Main agent for Indian political analysis and content generation.

    This agent:
    1. Searches web for latest information
    2. Extracts key facts from search results
    3. Generates comprehensive video analysis
    """

    def __init__(self, gemini_api_key: str):
        """
        Initialize the agent.

        Args:
            gemini_api_key: Google Gemini API key
        """
        logger.info("Initializing IndiaPoliticsAgent")

        self.web_search = WebSearchService()
        self.gemini = GeminiService(gemini_api_key)

        logger.info("IndiaPoliticsAgent initialized successfully")

    def analyze(self, topic: str) -> AnalysisResult:
        """
        Analyze a political topic and generate complete content package.

        Args:
            topic: The political topic to analyze

        Returns:
            Complete analysis result

        Raises:
            AnalysisError: If analysis fails
        """
        start_time = time.time()

        # Validate input
        topic = validate_topic(topic)

        logger.info("="*70)
        logger.info(f"STARTING ANALYSIS: {topic}")
        logger.info("="*70)

        try:
            # Step 1: Web search
            print(f"\n{'='*70}")
            print("STEP 1: Fetching Latest Information from Web")
            print(f"{'='*70}\n")

            search_results = self.web_search.search(topic)

            # Step 2: Extract facts
            print(f"\n{'='*70}")
            print("STEP 2: Extracting Key Facts and Data Points")
            print(f"{'='*70}\n")

            facts = self._extract_facts(topic, search_results)

            # Step 3: Generate analysis
            print(f"\n{'='*70}")
            print("STEP 3: Creating Comprehensive Video Analysis")
            print(f"{'='*70}\n")

            analysis_text = self._generate_analysis(topic, facts)

            # Parse the analysis into structured format
            result = self._parse_analysis(
                topic=topic,
                analysis_text=analysis_text,
                facts=facts,
                sources=search_results['raw_results'],
                generation_time=time.time() - start_time
            )

            logger.info(
                "Analysis completed successfully",
                topic=topic,
                generation_time=result.generation_time_seconds,
                word_count=result.word_count,
                sources_count=result.sources_count
            )

            return result

        except Exception as e:
            logger.error(f"Analysis failed: {e}", topic=topic)
            raise AnalysisError(
                f"Failed to analyze topic: {e}",
                topic=topic
            )

    def _extract_facts(self, topic: str, search_results: dict) -> dict:
        """Extract key facts from search results."""

        if search_results['source_count'] == 0:
            logger.warning("No search results available for fact extraction")
            return {
                'extracted_facts': "No web data available for fact extraction.",
                'raw_context': ""
            }

        extraction_prompt = f"""Analyze the following news articles and extract ONLY factual information about: {topic}

WEB SEARCH RESULTS:
{search_results['formatted_text'][:15000]}

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

        try:
            print("⏳ Extracting facts... (30-40 seconds)\n")
            extracted_text = self.gemini.generate(
                prompt=extraction_prompt,
                temperature=0.3,
                max_output_tokens=2000
            )

            print("✅ Facts extracted successfully\n")

            return {
                'extracted_facts': extracted_text,
                'raw_context': search_results['formatted_text']
            }

        except Exception as e:
            logger.error(f"Fact extraction failed: {e}")
            return {
                'extracted_facts': "Fact extraction failed. Using raw context.",
                'raw_context': search_results['formatted_text']
            }

    def _generate_analysis(self, topic: str, facts: dict) -> str:
        """Generate comprehensive analysis using extracted facts."""

        extracted_facts = facts.get('extracted_facts', 'No structured facts extracted.')

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

---

### 📰 LATEST DEVELOPMENTS [0:45 - 3:00]

**Timeline of Events:**
[List events chronologically with exact dates from extracted facts]

**Key Statements:**
[Include actual quotes from extracted facts with attribution]

---

### 🗳️ ELECTORAL MATHEMATICS [3:00 - 6:00]

**Seats & Numbers:**
[Use actual numbers from extracted facts]

**Vote Bank Analysis:**
[Analyze based on facts about caste/community dynamics]

---

### 🎯 CAMPAIGN STRATEGY DECODE [6:00 - 10:00]

**Visible Strategy:**
1. **Messaging:** [What narrative is being pushed based on facts?]
2. **Timing:** [Why this timing? Use dates from facts]
3. **Target Audience:** [Who is being targeted?]

---

### 📚 HISTORICAL CONTEXT [10:00 - 12:00]

**Similar Past Events:**
[Draw parallels to past political events]

---

### 👥 KEY PLAYERS ANALYSIS [12:00 - 15:00]

[For each key player from facts]

---

### 🔮 FUTURE IMPLICATIONS [15:00 - 17:30]

**Short-term (Next 3-6 months):**
[Predictions based on facts]

**Impact on 2025 Elections:**
[How this shapes upcoming elections]

---

### 🎓 CONCLUSION [17:30 - 20:00]

**5 Key Takeaways:**
1. [Specific takeaway with fact]
2. [Specific takeaway with fact]
3. [Specific takeaway with fact]
4. [Specific takeaway with fact]
5. [Specific takeaway with fact]

---

## 📱 YOUTUBE SHORTS (3 Variants × 60 seconds)

### SHORT 1: "Breaking Down the Bombshell"
[60-second Hinglish script using most shocking fact]

### SHORT 2: "Numbers That Tell the Story"
[60-second script focused on data]

### SHORT 3: "What This Really Means"
[60-second analytical take]

---

## 📺 12 TITLE OPTIONS

1. "{topic} का सच | Complete Analysis"
2. "Electoral Impact of {topic}: Full Breakdown"
3. "क्या बदलेगा 2025? {topic} Explained"
4. "{topic} Master Stroke or Mistake?"
5. "BREAKING: {topic} | Full Analysis"
6. "{topic} Strategy Decoded"
7. "2025 Roadmap: {topic} Impact"
8. "{topic} | Political Chess Move"
9. "The Truth About {topic}"
10. "{topic} | Game Changer?"
11. "{topic} से क्या होगा?"
12. "{topic} Deep Dive Analysis"

---

## 🖼️ 3 THUMBNAIL CONCEPTS

### Thumbnail 1: "Political Face-Off"
- Central Image: Key player with intense expression
- Text Overlay: "गेम चेंजर?"
- Colors: Party colors

### Thumbnail 2: "Numbers Speak"
- Central Image: State/region map
- Text Overlay: Key numbers
- Graphics: Impact arrows

### Thumbnail 3: "Drama Capture"
- Central Image: Contrasting photos
- Text Overlay: "क्या होगा अब?"

---

## 🔍 SEO PACKAGE

### Description:
{topic} analysis with latest facts, electoral mathematics, and 2025 predictions.

### Tags:
indian politics, {topic}, elections 2025, political analysis, campaign strategy

### Hashtags:
#IndianPolitics #Elections2025 #PoliticalAnalysis

NOW CREATE THIS COMPLETE ANALYSIS FOR: {topic}"""

        try:
            print("⏳ Generating analysis... (60-90 seconds)\n")
            analysis = self.gemini.generate(
                prompt=prompt,
                temperature=0.75,
                max_output_tokens=8000
            )

            print("✅ Analysis generated successfully\n")
            return analysis

        except Exception as e:
            logger.error(f"Analysis generation failed: {e}")
            raise AnalysisError(
                f"Failed to generate analysis: {e}",
                topic=topic,
                stage="analysis_generation"
            )

    def _parse_analysis(
        self,
        topic: str,
        analysis_text: str,
        facts: dict,
        sources: list,
        generation_time: float
    ) -> AnalysisResult:
        """Parse the generated analysis into structured format."""

        # For now, create a simple structured result
        # In a full implementation, we'd parse the markdown sections

        # Extract executive summary (first section)
        exec_summary = "Analysis completed successfully. See full markdown output for details."

        # Create dummy structures (would be parsed from analysis_text in production)
        video_script = VideoScript(
            hook="See full analysis",
            latest_developments="See full analysis",
            electoral_mathematics="See full analysis",
            campaign_strategy="See full analysis",
            historical_context="See full analysis",
            key_players="See full analysis",
            future_implications="See full analysis",
            conclusion="See full analysis"
        )

        shorts = [
            YouTubeShort(
                title="Short 1",
                script="See full analysis",
                focus="controversial"
            ),
            YouTubeShort(
                title="Short 2",
                script="See full analysis",
                focus="data"
            ),
            YouTubeShort(
                title="Short 3",
                script="See full analysis",
                focus="analytical"
            )
        ]

        seo = SEOPackage(
            description=f"Complete analysis of {topic}",
            tags=["indian politics", topic, "elections 2025"],
            hashtags=["#IndianPolitics", "#Elections2025"],
            timestamps={"0:00": "Introduction"},
            titles=[f"{topic} Analysis"]
        )

        thumbnails = [
            ThumbnailConcept(
                title="Concept 1",
                central_image_description="Political scene",
                text_overlay=topic,
                color_scheme=["red", "blue"],
                style_notes="Bold and impactful"
            )
        ]

        # Extract facts list
        facts_list = facts.get('extracted_facts', '').split('\n')[:10]

        result = AnalysisResult(
            topic=topic,
            executive_summary=exec_summary + "\n\n" + analysis_text,  # Full text for now
            video_script=video_script,
            shorts=shorts,
            status=AnalysisStatus.COMPLETED,
            generated_at=datetime.now(),
            generation_time_seconds=generation_time,
            seo_package=seo,
            thumbnail_concepts=thumbnails,
            sources=[{'title': 'Source', 'source': 'Web', 'date': ''} for _ in sources[:10]],
            facts_extracted=facts_list,
            verification_notes="Facts extracted from multiple news sources",
            word_count=len(analysis_text.split()),
            sources_count=len(sources),
            model_used="gemini",
            cache_hit=False
        )

        return result

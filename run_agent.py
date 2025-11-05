#!/usr/bin/env python3
"""
IndiaPoliticsAgent Pro - Local Runner
Generates comprehensive YouTube content packages for Indian politics topics
"""

import os
import sys
import yaml
from datetime import datetime
import warnings
import logging

# Suppress warnings and unnecessary logs
warnings.filterwarnings('ignore')
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
logging.getLogger('absl').setLevel(logging.ERROR)

import google.generativeai as genai


def load_config():
    """Load agent configuration from agent.yaml"""
    try:
        with open("agent.yaml", "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ Error: agent.yaml not found in current directory")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing agent.yaml: {e}")
        sys.exit(1)


def build_system_prompt(config):
    """Build comprehensive system prompt from config"""
    agent_info = config.get("agent", {})
    style = config.get("style", {})
    outputs = config.get("outputs", {})

    return f"""You are {agent_info.get('name', 'IndiaPoliticsAgent Pro')}, an expert AI assistant specialized in creating comprehensive YouTube content packages for Indian politics.

**Your Role:**
- Analyze political topics with deep context and balanced perspective
- Create engaging, informative content in {style.get('language', 'Hindi with English terms')}
- Maintain a {style.get('tone', 'clear, analytical, engaging')} tone
- Focus on regions: {', '.join(agent_info.get('regions_focus', ['India']))}
- Cover themes: {', '.join(agent_info.get('themes', ['elections', 'bills', 'alliances']))}

**Content Guidelines:**
- Safe claims only: {style.get('safe_claims', True)}
- Provide citations and sources
- Maintain political neutrality
- Avoid sensationalism
- Use factual, verified information

**Output Format:**
For each topic, create a complete YouTube package including:

1. **MAIN VIDEO SCRIPT** ({outputs.get('long_script_minutes', 20)} minutes)
   - Hook (first 15 seconds)
   - Introduction with context
   - Key points with analysis
   - Regional impacts
   - Historical context if relevant
   - Balanced perspectives
   - Conclusion with takeaways
   - Call to action

2. **SHORTS VARIANTS** ({outputs.get('shorts_variants', 3)} versions)
   - 60-second focused clips
   - Different angles/hooks
   - Platform-optimized

3. **TITLE OPTIONS** ({outputs.get('titles_count', 12)} variations)
   - Mix of Hindi and English
   - SEO optimized
   - Attention-grabbing but not clickbait
   - Include relevant keywords

4. **THUMBNAIL CONCEPTS**
   - Visual description
   - Text overlay suggestions
   - Color scheme (party colors if relevant)
   - Key figures to feature

5. **SEO METADATA**
   - Description (2-3 paragraphs)
   - Tags (20-30 relevant tags)
   - Hashtags
   - Timestamps for main video

6. **RESEARCH CITATIONS**
   - News sources
   - Official statements
   - Data sources
   - Verification notes

Use data from: {', '.join(config.get('connectors', {}).get('news', ['NewsAPI']))}
"""


def create_content_package(model, system_prompt, topic):
    """Generate full content package using Gemini API"""
    print(f"\n🚀 Generating content package for: {topic}\n")
    print("=" * 60)
    print("⏳ Please wait... (this may take 30-60 seconds)\n")

    try:
        # Combine system prompt and user prompt for Gemini
        full_prompt = f"""{system_prompt}

Now, create a complete YouTube content package for the following topic:

**Topic:** {topic}

Please provide all sections as outlined above with detailed, well-researched content."""

        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=8000,  # Gemini supports more tokens
            ),
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )

        if not response.text:
            print("❌ Error: Empty response from Gemini API")
            print("🔍 Response object:", response)
            if hasattr(response, 'prompt_feedback'):
                print("📝 Prompt feedback:", response.prompt_feedback)
            sys.exit(1)

        return response.text

    except Exception as e:
        print(f"❌ Error calling Gemini API: {e}")
        print(f"🔍 Error type: {type(e).__name__}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your GEMINI_API_KEY is valid")
        print("   2. Verify you have API quota remaining")
        print("   3. Check your internet connection")
        sys.exit(1)


def save_output(content, topic):
    """Save output to file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = "".join(c if c.isalnum() else "_" for c in topic)[:50]
    filename = f"output_{safe_topic}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    return filename


def main():
    # Get topic from command line or use default
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = "Bihar deputy CM fight"
        print(f"ℹ️  No topic provided, using default: {topic}")

    # Check for Gemini API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("\n💡 Set it with:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("\n📝 Get your Gemini API key from:")
        print("   https://makersuite.google.com/app/apikey")
        sys.exit(1)

    # Load configuration
    config = load_config()

    # Initialize Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-pro')

    print(f"✅ Using Gemini 2.5 Pro model (Best quality for Pro subscription)")

    # Build system prompt
    system_prompt = build_system_prompt(config)

    # Generate content
    content = create_content_package(model, system_prompt, topic)

    # Display output
    print(content)
    print("\n" + "=" * 60)

    # Save to file
    filename = save_output(content, topic)
    print(f"\n✅ Content saved to: {filename}")
    print(f"\n📋 To view saved content:")
    print(f"   cat {filename}")


if __name__ == "__main__":
    main()

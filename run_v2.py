#!/usr/bin/env python3
"""
Simple runner for India Politics Agent v2.0

Usage:
    python run_v2.py "Your topic here"
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from india_politics_agent.core.agent import IndiaPoliticsAgent
from india_politics_agent.utils.logging import configure_logging, get_logger
from india_politics_agent.utils.validators import sanitize_filename

# Configure logging
configure_logging(level="INFO", structured=False)
logger = get_logger(__name__)


def main():
    """Main entry point."""

    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║    🇮🇳  INDIA POLITICS PRO v2.0 - PRODUCTION GRADE  🇮🇳          ║
║                                                                   ║
║     Real-Time Data + Smart Context + Multi-Model Fallback        ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")

    # Get topic
    if len(sys.argv) < 2:
        print("❌ Error: No topic provided\n")
        print("📝 Usage:")
        print("   python run_v2.py \"Your political topic\"\n")
        print("💡 Examples:")
        print("   python run_v2.py \"Prashant Kishor Jan Suraaj Bihar 2025\"")
        print("   python run_v2.py \"Bihar deputy CM fight NDA\"")
        print("   python run_v2.py \"Supreme Court Article 370 verdict\"")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    # Check API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("\n💡 Set it with:")
        print("   export GEMINI_API_KEY='your-gemini-api-key'")
        print("\n📝 Get your key from:")
        print("   https://makersuite.google.com/app/apikey")
        sys.exit(1)

    try:
        # Initialize agent
        print(f"📌 Topic: {topic}")
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        agent = IndiaPoliticsAgent(gemini_api_key=api_key)

        # Run analysis
        result = agent.analyze(topic)

        # Display result
        print("\n" + "="*70)
        print("📊 ANALYSIS COMPLETE")
        print("="*70 + "\n")
        print(result.executive_summary)

        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = sanitize_filename(topic)
        filename = f"VIDEO_ANALYSIS_{safe_topic}_{timestamp}.md"

        result.save(filename)

        print("\n" + "="*70)
        print(f"✅ Analysis saved to: {filename}")
        print(f"📝 Generation time: {result.generation_time_seconds:.1f} seconds")
        print(f"📚 Sources analyzed: {result.sources_count}")
        print(f"📊 Word count: {result.word_count:,}")
        print("="*70 + "\n")

        print("💡 Next steps:")
        print("   1. Open the markdown file in any text editor")
        print("   2. Review the complete video script and SEO package")
        print("   3. Use the content for your YouTube video")

    except KeyboardInterrupt:
        print("\n\n❌ Analysis cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

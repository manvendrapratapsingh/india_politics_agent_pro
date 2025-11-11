"""Web search service - uses the existing working web_search.py"""

import sys
import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Add project root to path to import the existing working module
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from web_search import WebSearcher
except ImportError:
    # Fallback if web_search not available
    WebSearcher = None

from ..utils.logging import get_logger

logger = get_logger(__name__)


class WebSearchService:
    """Web search service that wraps the existing working implementation."""

    def __init__(self):
        if WebSearcher is None:
            logger.warning("WebSearcher not available, using fallback mode")
            self.searcher = None
        else:
            self.searcher = WebSearcher()
            logger.info("WebSearchService initialized with WebSearcher")

    def search(self, query: str) -> Dict:
        """
        Search for information about the query.

        Args:
            query: Search query string

        Returns:
            Dictionary with search results
        """
        logger.info(f"Starting web search for: {query}")

        if self.searcher is None:
            logger.warning("WebSearcher not available, returning empty results")
            return {
                'raw_results': [],
                'formatted_text': "",
                'source_count': 0,
                'method': 'unavailable'
            }

        try:
            # Use the existing working search
            results = self.searcher.search_comprehensive(query)

            formatted_text = self.searcher.format_results(results)

            logger.info(
                f"Web search completed: {len(results)} results found"
            )

            return {
                'raw_results': results,
                'formatted_text': formatted_text,
                'source_count': len(results),
                'method': 'web_scraping'
            }

        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return {
                'raw_results': [],
                'formatted_text': "",
                'source_count': 0,
                'method': 'failed'
            }

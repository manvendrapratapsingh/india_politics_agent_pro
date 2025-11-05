#!/usr/bin/env python3
"""
Web Search Module for Real-Time Political Data
Fetches latest news and information from multiple sources
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict
import warnings

warnings.filterwarnings('ignore')


class WebSearcher:
    """Fetch real-time news and information"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def search_duckduckgo(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search DuckDuckGo for latest results"""
        print(f"🔍 Searching DuckDuckGo for: {query}")

        try:
            # DuckDuckGo Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': 1,
                'skip_disambig': 1
            }

            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            results = []

            # Extract abstract
            if data.get('AbstractText'):
                results.append({
                    'title': data.get('Heading', query),
                    'snippet': data.get('AbstractText'),
                    'source': data.get('AbstractSource', 'DuckDuckGo'),
                    'url': data.get('AbstractURL', '')
                })

            # Extract related topics
            for topic in data.get('RelatedTopics', [])[:max_results]:
                if isinstance(topic, dict) and 'Text' in topic:
                    results.append({
                        'title': topic.get('FirstURL', '').split('/')[-1].replace('_', ' '),
                        'snippet': topic.get('Text', ''),
                        'source': 'DuckDuckGo',
                        'url': topic.get('FirstURL', '')
                    })

            print(f"✅ Found {len(results)} results from DuckDuckGo")
            return results

        except Exception as e:
            print(f"⚠️ DuckDuckGo search failed: {e}")
            return []

    def search_google_news_rss(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Google News RSS feed"""
        print(f"📰 Searching Google News for: {query}")

        try:
            # Google News RSS feed
            url = "https://news.google.com/rss/search"
            params = {
                'q': query,
                'hl': 'en-IN',
                'gl': 'IN',
                'ceid': 'IN:en'
            }

            response = self.session.get(url, params=params, timeout=10)

            # Parse RSS feed
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)

            results = []
            for item in root.findall('.//item')[:max_results]:
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                description = item.find('description')

                if title is not None:
                    results.append({
                        'title': title.text,
                        'snippet': description.text if description is not None else '',
                        'source': 'Google News',
                        'url': link.text if link is not None else '',
                        'date': pub_date.text if pub_date is not None else ''
                    })

            print(f"✅ Found {len(results)} results from Google News")
            return results

        except Exception as e:
            print(f"⚠️ Google News search failed: {e}")
            return []

    def search_newsapi(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search using NewsAPI if available"""
        api_key = os.getenv('NEWSAPI_KEY')
        if not api_key:
            print("⚠️ NewsAPI key not found, skipping NewsAPI search")
            return []

        print(f"📡 Searching NewsAPI for: {query}")

        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'apiKey': api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': max_results,
                'domains': 'thehindu.com,indianexpress.com,ndtv.com,timesofindia.indiatimes.com,hindustantimes.com'
            }

            response = self.session.get(url, params=params, timeout=10)
            data = response.json()

            results = []
            for article in data.get('articles', []):
                results.append({
                    'title': article.get('title', ''),
                    'snippet': article.get('description', ''),
                    'source': article.get('source', {}).get('name', 'NewsAPI'),
                    'url': article.get('url', ''),
                    'date': article.get('publishedAt', '')
                })

            print(f"✅ Found {len(results)} results from NewsAPI")
            return results

        except Exception as e:
            print(f"⚠️ NewsAPI search failed: {e}")
            return []

    def search_comprehensive(self, query: str) -> List[Dict]:
        """Perform comprehensive search across multiple sources"""
        print(f"\n{'='*70}")
        print("🌐 COMPREHENSIVE WEB SEARCH")
        print(f"{'='*70}\n")
        print(f"📌 Query: {query}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        all_results = []

        # Search Google News RSS (most reliable)
        news_results = self.search_google_news_rss(query, max_results=15)
        all_results.extend(news_results)

        # Search DuckDuckGo
        ddg_results = self.search_duckduckgo(query, max_results=10)
        all_results.extend(ddg_results)

        # Search NewsAPI if available
        newsapi_results = self.search_newsapi(query, max_results=10)
        all_results.extend(newsapi_results)

        # Add specific Indian politics sources
        indian_queries = [
            f"{query} site:thehindu.com OR site:indianexpress.com",
            f"{query} India politics latest",
            f"{query} election analysis"
        ]

        for iq in indian_queries[:1]:  # Just one additional query to avoid rate limits
            more_results = self.search_duckduckgo(iq, max_results=5)
            all_results.extend(more_results)

        print(f"\n{'='*70}")
        print(f"✅ Total results collected: {len(all_results)}")
        print(f"{'='*70}\n")

        return all_results

    def format_results(self, results: List[Dict]) -> str:
        """Format search results for LLM consumption"""
        if not results:
            return "No recent news found. Analysis will use Gemini's knowledge base."

        formatted = []
        formatted.append(f"LATEST NEWS & INFORMATION (as of {datetime.now().strftime('%Y-%m-%d')})\n")
        formatted.append("="*70 + "\n")

        for i, result in enumerate(results[:20], 1):  # Limit to top 20 results
            formatted.append(f"\n[ARTICLE {i}]")
            formatted.append(f"Title: {result.get('title', 'N/A')}")
            formatted.append(f"Source: {result.get('source', 'N/A')}")
            if result.get('date'):
                formatted.append(f"Date: {result.get('date', 'N/A')}")
            if result.get('snippet'):
                formatted.append(f"Summary: {result.get('snippet', 'N/A')}")
            if result.get('url'):
                formatted.append(f"URL: {result.get('url', 'N/A')}")
            formatted.append("")

        return "\n".join(formatted)

    def save_results(self, results: List[Dict], filename: str = "web_search_results.txt"):
        """Save search results to file"""
        formatted_results = self.format_results(results)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(formatted_results)

        print(f"💾 Search results saved to: {filename}")
        return filename


def main():
    """Test the web search module"""
    if len(sys.argv) < 2:
        print("Usage: python web_search.py \"your search query\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])

    searcher = WebSearcher()
    results = searcher.search_comprehensive(query)

    if results:
        filename = searcher.save_results(results)
        print(f"\n✅ Search complete! Results saved to {filename}")
    else:
        print("\n❌ No results found")


if __name__ == "__main__":
    main()

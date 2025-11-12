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
import re
from urllib.parse import quote_plus, urljoin
import time

warnings.filterwarnings('ignore')

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False
    print("⚠️ Warning: BeautifulSoup not installed. Install with: pip install beautifulsoup4")


class WebSearcher:
    """Fetch real-time news and information with actual web scraping"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.timeout = 15

    def search_duckduckgo_html(self, query: str, max_results: int = 15) -> List[Dict]:
        """Search DuckDuckGo by scraping HTML results (actual search, not API)"""
        print(f"🔍 Searching DuckDuckGo HTML for: {query}")

        if not HAS_BS4:
            print("⚠️ BeautifulSoup not available, skipping DuckDuckGo search")
            return []

        try:
            # DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/"
            data = {
                'q': query,
                'kl': 'in-en'  # India region, English
            }

            response = self.session.post(url, data=data, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # Find all result divs
            for result_div in soup.find_all('div', class_='result')[:max_results]:
                try:
                    # Extract title and URL
                    title_elem = result_div.find('a', class_='result__a')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')

                    # Extract snippet
                    snippet_elem = result_div.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                    # Extract source domain
                    source_elem = result_div.find('a', class_='result__url')
                    source = source_elem.get_text(strip=True) if source_elem else 'Unknown'

                    if title and snippet:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'source': source,
                            'url': url,
                            'date': ''  # DuckDuckGo HTML doesn't provide dates
                        })

                except Exception as e:
                    continue

            print(f"✅ Found {len(results)} results from DuckDuckGo")
            return results

        except Exception as e:
            print(f"⚠️ DuckDuckGo HTML search failed: {e}")
            return []

    def search_google_news_rss(self, query: str, max_results: int = 20) -> List[Dict]:
        """Search Google News RSS feed - FIXED with proper parsing"""
        print(f"📰 Searching Google News RSS for: {query}")

        try:
            # Google News RSS feed URL
            encoded_query = quote_plus(query)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            if not HAS_BS4:
                print("⚠️ BeautifulSoup not available for RSS parsing")
                return []

            # Parse RSS with BeautifulSoup (more lenient than ElementTree)
            soup = BeautifulSoup(response.content, 'xml')
            results = []

            for item in soup.find_all('item')[:max_results]:
                try:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    pub_date_elem = item.find('pubDate')
                    description_elem = item.find('description')

                    if title_elem and title_elem.text:
                        # Clean up the snippet (remove HTML tags if any)
                        snippet = ''
                        if description_elem and description_elem.text:
                            snippet_soup = BeautifulSoup(description_elem.text, 'html.parser')
                            snippet = snippet_soup.get_text(strip=True)[:500]

                        # Extract source from title (Google News format: "Title - Source")
                        title_text = title_elem.text
                        source = 'Google News'
                        if ' - ' in title_text:
                            parts = title_text.rsplit(' - ', 1)
                            if len(parts) == 2:
                                title_text = parts[0]
                                source = parts[1]

                        results.append({
                            'title': title_text,
                            'snippet': snippet,
                            'source': source,
                            'url': link_elem.text if link_elem and link_elem.text else '',
                            'date': pub_date_elem.text if pub_date_elem and pub_date_elem.text else ''
                        })

                except Exception as e:
                    continue

            print(f"✅ Found {len(results)} results from Google News")
            return results

        except Exception as e:
            print(f"⚠️ Google News RSS search failed: {e}")
            return []

    def search_bing_news(self, query: str, max_results: int = 15) -> List[Dict]:
        """Search Bing News by scraping"""
        print(f"📰 Searching Bing News for: {query}")

        if not HAS_BS4:
            print("⚠️ BeautifulSoup not available, skipping Bing News")
            return []

        try:
            encoded_query = quote_plus(query)
            url = f"https://www.bing.com/news/search?q={encoded_query}&qft=interval%3d%227%22"  # Last 7 days

            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            results = []

            # Find news cards
            for card in soup.find_all('div', class_='news-card')[:max_results]:
                try:
                    title_elem = card.find('a', class_='title')
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')

                    snippet_elem = card.find('div', class_='snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''

                    source_elem = card.find('span', class_='source')
                    source = source_elem.get_text(strip=True) if source_elem else 'Bing News'

                    date_elem = card.find('span', attrs={'aria-label': True})
                    date = date_elem.get('aria-label', '') if date_elem else ''

                    if title:
                        results.append({
                            'title': title,
                            'snippet': snippet,
                            'source': source,
                            'url': url,
                            'date': date
                        })

                except Exception as e:
                    continue

            print(f"✅ Found {len(results)} results from Bing News")
            return results

        except Exception as e:
            print(f"⚠️ Bing News search failed: {e}")
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

    def fetch_article_content(self, url: str) -> str:
        """Fetch and extract main content from article URL"""
        try:
            if not HAS_BS4:
                return ""

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()

            # Try to find main content
            content = []

            # Look for article content in common locations
            article = soup.find('article')
            if article:
                paragraphs = article.find_all('p')
            else:
                paragraphs = soup.find_all('p')

            for p in paragraphs[:10]:  # First 10 paragraphs
                text = p.get_text(strip=True)
                if len(text) > 50:  # Ignore short paragraphs
                    content.append(text)

            return ' '.join(content)[:2000]  # Limit to 2000 chars

        except (requests.RequestException, requests.Timeout, ValueError) as e:
            # Log specific network and parsing errors but return empty string
            print(f"Warning: Failed to fetch article content from {url}: {e}")
            return ""

    def search_comprehensive(self, query: str) -> List[Dict]:
        """Perform comprehensive search across multiple sources with ACTUAL scraping"""
        print(f"\n{'='*70}")
        print("🌐 COMPREHENSIVE WEB SEARCH - IMPROVED")
        print(f"{'='*70}\n")
        print(f"📌 Query: {query}")
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        all_results = []
        seen_urls = set()  # Deduplicate

        # 1. Google News RSS (most reliable for news)
        print("\n📊 Phase 1: Google News RSS")
        news_results = self.search_google_news_rss(query, max_results=20)
        for result in news_results:
            if result['url'] and result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                all_results.append(result)
        print(f"   Added {len(news_results)} unique results")

        # Small delay to avoid rate limiting
        time.sleep(0.5)

        # 2. DuckDuckGo HTML scraping (actual search results)
        print("\n📊 Phase 2: DuckDuckGo HTML Search")
        ddg_results = self.search_duckduckgo_html(query, max_results=15)
        new_count = 0
        for result in ddg_results:
            if result['url'] and result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                all_results.append(result)
                new_count += 1
        print(f"   Added {new_count} unique results")

        time.sleep(0.5)

        # 3. Bing News
        print("\n📊 Phase 3: Bing News Search")
        bing_results = self.search_bing_news(query, max_results=15)
        new_count = 0
        for result in bing_results:
            if result['url'] and result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                all_results.append(result)
                new_count += 1
        print(f"   Added {new_count} unique results")

        time.sleep(0.5)

        # 4. NewsAPI if available
        print("\n📊 Phase 4: NewsAPI (if configured)")
        newsapi_results = self.search_newsapi(query, max_results=10)
        new_count = 0
        for result in newsapi_results:
            if result['url'] and result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                all_results.append(result)
                new_count += 1
        print(f"   Added {new_count} unique results")

        time.sleep(0.5)

        # 5. Targeted Indian news sources
        print("\n📊 Phase 5: Targeted Indian News Sources")
        indian_queries = [
            f"{query} site:thehindu.com OR site:indianexpress.com OR site:ndtv.com",
            f"{query} Bihar election latest",
            f"{query} polling booth"
        ]

        for iq in indian_queries[:2]:  # Do 2 targeted queries
            more_results = self.search_duckduckgo_html(iq, max_results=10)
            new_count = 0
            for result in more_results:
                if result['url'] and result['url'] not in seen_urls:
                    seen_urls.add(result['url'])
                    all_results.append(result)
                    new_count += 1
            if new_count > 0:
                print(f"   Query '{iq[:50]}...' added {new_count} results")
            time.sleep(0.5)

        # 6. Enhance results by fetching article content for top results
        if HAS_BS4 and len(all_results) > 0:
            print(f"\n📊 Phase 6: Fetching full article content for top 5 results")
            for i, result in enumerate(all_results[:5]):
                if result.get('url') and not result.get('full_content'):
                    print(f"   Fetching content from: {result['source']}")
                    content = self.fetch_article_content(result['url'])
                    if content:
                        result['full_content'] = content
                    time.sleep(0.3)

        print(f"\n{'='*70}")
        print(f"✅ TOTAL UNIQUE RESULTS: {len(all_results)}")
        print(f"   - With dates: {sum(1 for r in all_results if r.get('date'))}")
        print(f"   - With full content: {sum(1 for r in all_results if r.get('full_content'))}")
        print(f"{'='*70}\n")

        return all_results

    def format_results(self, results: List[Dict]) -> str:
        """Format search results for LLM consumption with full content"""
        if not results:
            return "No recent news found. Analysis will use Gemini's knowledge base."

        formatted = []
        formatted.append(f"LATEST NEWS & INFORMATION (as of {datetime.now().strftime('%Y-%m-%d')})\n")
        formatted.append("="*70 + "\n")
        formatted.append(f"Total Articles Found: {len(results)}\n")
        formatted.append("="*70 + "\n")

        # Prioritize results with dates (more recent)
        sorted_results = sorted(results, key=lambda x: (bool(x.get('date')), bool(x.get('full_content'))), reverse=True)

        for i, result in enumerate(sorted_results[:30], 1):  # Top 30 results
            formatted.append(f"\n[ARTICLE {i}]")
            formatted.append(f"Title: {result.get('title', 'N/A')}")
            formatted.append(f"Source: {result.get('source', 'N/A')}")

            if result.get('date'):
                formatted.append(f"Date: {result.get('date', 'N/A')}")

            if result.get('snippet'):
                formatted.append(f"Summary: {result.get('snippet', 'N/A')}")

            # Include full content if available (more detailed)
            if result.get('full_content'):
                formatted.append(f"Full Content Preview: {result.get('full_content', 'N/A')[:1000]}")

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

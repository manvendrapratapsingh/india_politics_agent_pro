"""Search result models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class SourceType(Enum):
    """Type of web source."""
    NEWS_ARTICLE = "news_article"
    OFFICIAL_STATEMENT = "official_statement"
    SOCIAL_MEDIA = "social_media"
    BLOG = "blog"
    VIDEO = "video"
    UNKNOWN = "unknown"


@dataclass
class WebSource:
    """A web source with metadata."""
    title: str
    url: str
    snippet: str
    source_name: str
    source_type: SourceType = SourceType.UNKNOWN
    published_date: Optional[datetime] = None
    full_content: Optional[str] = None
    credibility_score: float = 0.5  # 0.0 to 1.0

    def __hash__(self):
        """Make hashable for deduplication."""
        return hash(self.url)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'title': self.title,
            'url': self.url,
            'snippet': self.snippet,
            'source': self.source_name,
            'type': self.source_type.value,
            'date': self.published_date.isoformat() if self.published_date else None,
            'credibility': self.credibility_score,
        }


@dataclass
class SearchResult:
    """Result of a web search operation."""
    query: str
    sources: List[WebSource]
    total_found: int
    search_time_seconds: float
    method: str  # "web_scraping", "gemini_grounding", "cached"
    timestamp: datetime
    cache_hit: bool = False

    def get_unique_sources(self) -> List[WebSource]:
        """Get deduplicated sources."""
        seen_urls = set()
        unique = []
        for source in self.sources:
            if source.url not in seen_urls:
                seen_urls.add(source.url)
                unique.append(source)
        return unique

    def get_high_credibility_sources(self, threshold: float = 0.7) -> List[WebSource]:
        """Get only high credibility sources."""
        return [s for s in self.sources if s.credibility_score >= threshold]

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'query': self.query,
            'total_found': self.total_found,
            'search_time': self.search_time_seconds,
            'method': self.method,
            'timestamp': self.timestamp.isoformat(),
            'cache_hit': self.cache_hit,
            'sources': [s.to_dict() for s in self.sources],
        }

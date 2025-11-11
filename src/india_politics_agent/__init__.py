"""
India Politics Agent Pro - Production-Grade Political Analysis Agent

A world-class, production-ready agent for analyzing Indian politics and
generating comprehensive YouTube content packages.

Features:
- Async web scraping with connection pooling
- Redis caching with in-memory fallback
- Structured logging and metrics
- Rate limiting and circuit breakers
- Comprehensive error handling
- Rich CLI with progress bars
- 80%+ test coverage
"""

__version__ = "2.0.0"
__author__ = "India Politics Agent Team"

from .core.agent import IndiaPoliticsAgent
from .core.config import AgentConfig
from .models.analysis import AnalysisResult

__all__ = ["IndiaPoliticsAgent", "AgentConfig", "AnalysisResult"]

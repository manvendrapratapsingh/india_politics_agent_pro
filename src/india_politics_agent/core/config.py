"""Configuration management for the agent."""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
import yaml
from enum import Enum


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Environment(Enum):
    """Runtime environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class GeminiConfig:
    """Gemini API configuration."""
    api_key: str
    models: List[str] = field(default_factory=lambda: [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro-latest"
    ])
    temperature: float = 0.75
    max_output_tokens: int = 8000
    timeout_seconds: int = 120
    max_retries: int = 3
    retry_delay_seconds: float = 2.0


@dataclass
class CacheConfig:
    """Cache configuration."""
    enabled: bool = True
    backend: str = "memory"  # "memory", "redis", "hybrid"
    redis_url: Optional[str] = None
    ttl_seconds: int = 3600  # 1 hour
    max_size_mb: int = 100


@dataclass
class WebScrapingConfig:
    """Web scraping configuration."""
    timeout_seconds: int = 15
    max_results_per_source: int = 20
    concurrent_requests: int = 5
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    sources: List[str] = field(default_factory=lambda: [
        "google_news",
        "duckduckgo",
        "bing_news"
    ])
    trusted_domains: List[str] = field(default_factory=lambda: [
        "thehindu.com",
        "indianexpress.com",
        "ndtv.com",
        "hindustantimes.com",
        "timesofindia.indiatimes.com"
    ])


@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    enabled: bool = True
    requests_per_minute: int = 60
    burst_size: int = 10


@dataclass
class MonitoringConfig:
    """Monitoring and metrics configuration."""
    enabled: bool = True
    prometheus_port: int = 9090
    health_check_interval_seconds: int = 60
    metrics_path: str = "/metrics"


@dataclass
class AgentConfig:
    """Complete agent configuration."""

    # Core settings
    name: str = "IndiaPoliticsAgent Pro"
    version: str = "2.0.0"
    environment: Environment = Environment.DEVELOPMENT

    # API configurations
    gemini: GeminiConfig = field(default_factory=lambda: GeminiConfig(
        api_key=os.getenv("GEMINI_API_KEY", "")
    ))

    # Feature configurations
    cache: CacheConfig = field(default_factory=CacheConfig)
    web_scraping: WebScrapingConfig = field(default_factory=WebScrapingConfig)
    rate_limit: RateLimitConfig = field(default_factory=RateLimitConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)

    # Content settings
    regions_focus: List[str] = field(default_factory=lambda: [
        "India", "Bihar", "Uttar Pradesh", "Delhi", "South India"
    ])
    themes: List[str] = field(default_factory=lambda: [
        "elections", "bills", "seat-sharing", "Supreme Court cases",
        "alliances", "campaigns"
    ])
    language: str = "Hindi with English terms (Hinglish)"
    tone: str = "clear, sharp, analytical, engaging"

    # Output settings
    long_script_minutes: int = 20
    shorts_variants: int = 3
    titles_count: int = 12

    # Logging
    log_level: LogLevel = LogLevel.INFO
    log_file: Optional[str] = None
    structured_logging: bool = True

    # Paths
    output_dir: Path = field(default_factory=lambda: Path("outputs"))
    cache_dir: Path = field(default_factory=lambda: Path(".cache"))

    @classmethod
    def from_yaml(cls, filepath: str) -> "AgentConfig":
        """Load configuration from YAML file."""
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        # Map YAML structure to config
        config = cls()

        # Agent settings
        if 'agent' in data:
            agent_data = data['agent']
            config.name = agent_data.get('name', config.name)
            config.regions_focus = agent_data.get('regions_focus', config.regions_focus)
            config.themes = agent_data.get('themes', config.themes)

        # Style settings
        if 'style' in data:
            style_data = data['style']
            config.language = style_data.get('language', config.language)
            config.tone = style_data.get('tone', config.tone)

        # Output settings
        if 'outputs' in data:
            output_data = data['outputs']
            config.long_script_minutes = output_data.get('long_script_minutes', config.long_script_minutes)
            config.shorts_variants = output_data.get('shorts_variants', config.shorts_variants)
            config.titles_count = output_data.get('titles_count', config.titles_count)

        return config

    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Load configuration from environment variables."""
        config = cls()

        # Override from environment
        config.gemini.api_key = os.getenv("GEMINI_API_KEY", "")

        if cache_backend := os.getenv("CACHE_BACKEND"):
            config.cache.backend = cache_backend

        if redis_url := os.getenv("REDIS_URL"):
            config.cache.redis_url = redis_url

        if env := os.getenv("ENVIRONMENT"):
            config.environment = Environment(env.lower())

        if log_level := os.getenv("LOG_LEVEL"):
            config.log_level = LogLevel(log_level.upper())

        return config

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.gemini.api_key:
            errors.append("GEMINI_API_KEY is required")

        if self.cache.backend == "redis" and not self.cache.redis_url:
            errors.append("REDIS_URL is required when using Redis cache")

        if self.gemini.temperature < 0 or self.gemini.temperature > 1:
            errors.append("Temperature must be between 0 and 1")

        if self.web_scraping.timeout_seconds < 1:
            errors.append("Web scraping timeout must be at least 1 second")

        return errors

    def __post_init__(self):
        """Post-initialization setup."""
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

"""Input validation and sanitization utilities."""

import re
from typing import Optional
from .errors import ValidationError


def validate_topic(topic: str) -> str:
    """Validate and sanitize topic input using whitelist approach."""
    if not topic or not isinstance(topic, str):
        raise ValidationError("Topic must be a non-empty string", field="topic", value=topic)

    topic = topic.strip()

    if len(topic) < 3:
        raise ValidationError(
            "Topic must be at least 3 characters",
            field="topic",
            value=topic
        )

    if len(topic) > 500:
        raise ValidationError(
            "Topic must be less than 500 characters",
            field="topic",
            value=topic
        )

    # Whitelist approach: only allow safe characters
    # Allowed: letters (a-z, A-Z), numbers (0-9), spaces, hyphens, underscores, parentheses, commas, periods, apostrophes
    if not re.match(r"^[a-zA-Z0-9\s\-_(),.\']+$", topic):
        raise ValidationError(
            "Topic contains invalid characters. "
            "Allowed: a-z, A-Z, 0-9, spaces, hyphens, underscores, parentheses, commas, periods, apostrophes",
            field="topic",
            value=topic
        )

    return topic


def validate_api_key(api_key: Optional[str], key_name: str = "API_KEY") -> str:
    """Validate API key format."""
    if not api_key:
        raise ValidationError(
            f"{key_name} is required",
            field=key_name.lower(),
            value=api_key
        )

    api_key = api_key.strip()

    if len(api_key) < 10:
        raise ValidationError(
            f"{key_name} appears to be invalid (too short)",
            field=key_name.lower(),
            value="***"
        )

    # Basic format check (alphanumeric, dashes, underscores)
    if not re.match(r'^[A-Za-z0-9_-]+$', api_key):
        raise ValidationError(
            f"{key_name} contains invalid characters",
            field=key_name.lower(),
            value="***"
        )

    return api_key


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """Sanitize filename to be filesystem-safe."""
    # Remove path separators
    filename = filename.replace('/', '_').replace('\\', '_')

    # Replace problematic characters
    filename = re.sub(r'[<>:"|?*]', '', filename)

    # Replace multiple spaces/underscores with single underscore
    filename = re.sub(r'[\s_]+', '_', filename)

    # Remove leading/trailing dots and underscores
    filename = filename.strip('._')

    # Truncate if too long
    if len(filename) > max_length:
        filename = filename[:max_length]

    # Ensure we have something left
    if not filename:
        filename = "unnamed"

    return filename


def validate_url(url: str) -> bool:
    """Validate URL format."""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

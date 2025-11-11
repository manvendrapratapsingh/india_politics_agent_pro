"""Multi-tier caching system with Redis and in-memory fallback."""

import json
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime, timedelta
import pickle
from pathlib import Path

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from .logging import get_logger
from .errors import CacheError

logger = get_logger(__name__)


class CacheBackend(ABC):
    """Abstract cache backend."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL in seconds."""
        pass

    @abstractmethod
    def delete(self, key: str):
        """Delete key from cache."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all cache."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass


class MemoryCache(CacheBackend):
    """Simple in-memory cache with TTL support."""

    def __init__(self, max_size_mb: int = 100):
        self.cache: dict = {}
        self.expiry: dict = {}
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.current_size = 0

    def _is_expired(self, key: str) -> bool:
        """Check if key is expired."""
        if key not in self.expiry:
            return True
        return datetime.now() > self.expiry[key]

    def _evict_if_needed(self, new_size: int):
        """Evict oldest entries if needed."""
        while self.current_size + new_size > self.max_size_bytes and self.cache:
            # Remove first item (oldest)
            oldest_key = next(iter(self.cache))
            self.delete(oldest_key)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self.cache or self._is_expired(key):
            if key in self.cache:
                self.delete(key)
            return None
        return self.cache[key]

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache."""
        try:
            # Estimate size
            size = len(pickle.dumps(value))
            self._evict_if_needed(size)

            self.cache[key] = value
            self.expiry[key] = datetime.now() + timedelta(seconds=ttl)
            self.current_size += size

            logger.debug(f"Cached key={key}, size={size}, ttl={ttl}s")
        except Exception as e:
            logger.warning(f"Failed to cache key={key}: {e}")

    def delete(self, key: str):
        """Delete key from cache."""
        if key in self.cache:
            try:
                size = len(pickle.dumps(self.cache[key]))
                self.current_size -= size
            except:
                pass
            del self.cache[key]
        if key in self.expiry:
            del self.expiry[key]

    def clear(self):
        """Clear all cache."""
        self.cache.clear()
        self.expiry.clear()
        self.current_size = 0
        logger.info("Memory cache cleared")

    def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        return key in self.cache and not self._is_expired(key)


class RedisCache(CacheBackend):
    """Redis cache backend."""

    def __init__(self, redis_url: str, prefix: str = "india_politics:"):
        if not REDIS_AVAILABLE:
            raise CacheError("Redis library not installed. Install with: pip install redis")

        try:
            self.client = redis.from_url(redis_url, decode_responses=False)
            self.client.ping()
            self.prefix = prefix
            logger.info(f"Redis cache connected: {redis_url}")
        except Exception as e:
            raise CacheError(f"Failed to connect to Redis: {e}", details={'url': redis_url})

    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            data = self.client.get(self._make_key(key))
            if data is None:
                return None
            return pickle.loads(data)
        except Exception as e:
            logger.warning(f"Redis get failed for key={key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache."""
        try:
            data = pickle.dumps(value)
            self.client.setex(self._make_key(key), ttl, data)
            logger.debug(f"Redis cached key={key}, ttl={ttl}s")
        except Exception as e:
            logger.warning(f"Redis set failed for key={key}: {e}")

    def delete(self, key: str):
        """Delete key from cache."""
        try:
            self.client.delete(self._make_key(key))
        except Exception as e:
            logger.warning(f"Redis delete failed for key={key}: {e}")

    def clear(self):
        """Clear all cache with prefix."""
        try:
            keys = self.client.keys(f"{self.prefix}*")
            if keys:
                self.client.delete(*keys)
            logger.info(f"Redis cache cleared ({len(keys)} keys)")
        except Exception as e:
            logger.warning(f"Redis clear failed: {e}")

    def exists(self, key: str) -> bool:
        """Check if key exists."""
        try:
            return self.client.exists(self._make_key(key)) > 0
        except Exception as e:
            logger.warning(f"Redis exists check failed for key={key}: {e}")
            return False


class HybridCache(CacheBackend):
    """Hybrid cache with L1 (memory) and L2 (Redis) layers."""

    def __init__(self, redis_url: str, max_memory_mb: int = 50):
        self.l1 = MemoryCache(max_size_mb=max_memory_mb)
        try:
            self.l2 = RedisCache(redis_url)
            logger.info("Hybrid cache initialized (Memory + Redis)")
        except Exception as e:
            logger.warning(f"Redis unavailable, using memory-only cache: {e}")
            self.l2 = None

    def get(self, key: str) -> Optional[Any]:
        """Get from L1, then L2."""
        # Try L1 first
        value = self.l1.get(key)
        if value is not None:
            return value

        # Try L2 if available
        if self.l2:
            value = self.l2.get(key)
            if value is not None:
                # Populate L1
                self.l1.set(key, value)
                return value

        return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set in both L1 and L2."""
        self.l1.set(key, value, ttl)
        if self.l2:
            self.l2.set(key, value, ttl)

    def delete(self, key: str):
        """Delete from both layers."""
        self.l1.delete(key)
        if self.l2:
            self.l2.delete(key)

    def clear(self):
        """Clear both layers."""
        self.l1.clear()
        if self.l2:
            self.l2.clear()

    def exists(self, key: str) -> bool:
        """Check both layers."""
        return self.l1.exists(key) or (self.l2 and self.l2.exists(key))


class CacheManager:
    """High-level cache manager."""

    def __init__(self, backend: CacheBackend):
        self.backend = backend
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'errors': 0,
        }

    @staticmethod
    def create_key(*args, **kwargs) -> str:
        """Create cache key from arguments."""
        # Create deterministic hash from arguments
        key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get from cache with stats."""
        try:
            value = self.backend.get(key)
            if value is not None:
                self.stats['hits'] += 1
                logger.debug(f"Cache HIT: {key}")
            else:
                self.stats['misses'] += 1
                logger.debug(f"Cache MISS: {key}")
            return value
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set in cache with stats."""
        try:
            self.backend.set(key, value, ttl)
            self.stats['sets'] += 1
        except Exception as e:
            self.stats['errors'] += 1
            logger.error(f"Cache set error: {e}")

    def delete(self, key: str):
        """Delete from cache."""
        self.backend.delete(key)

    def clear(self):
        """Clear cache."""
        self.backend.clear()

    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0
        return {
            **self.stats,
            'hit_rate': f"{hit_rate:.1f}%"
        }

import os
import logging
from redis import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

# config from .env with sensible localhost defaults
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
TREKS_TTL = int(os.getenv('TREKS_CACHE_TTL', '60'))  # seconds

# one shared client (created the first time it is used)
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    return _client


def cache_get(key):
    """Return the cached string for key, or None when missing / redis down."""
    try:
        return _get_client().get(key)
    except RedisError:
        return None


def cache_set(key, value, ttl=TREKS_TTL):
    """Store a string value under key with a TTL; silently ignored if redis is down."""
    try:
        _get_client().set(key, value, ex=ttl)
    except RedisError:
        pass


def invalidate_treks():
    """Delete every cached trek payload (all listings + details) after any mutation."""
    try:
        keys = _get_client().keys('treks:*') + _get_client().keys('trek:*') + _get_client().keys('stafftrek:*') + _get_client().keys('stafftreks:*')
        if keys:
            _get_client().delete(*keys)
    except RedisError:
        pass
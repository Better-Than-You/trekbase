import os
import logging
from redis import Redis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

# reads from .env else fallback
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
TREKS_TTL = int(os.getenv('TREKS_CACHE_TTL', '60'))  # seconds

# single instance used by all
_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
    return _client

# --------------------------------------------------------------------------
def cache_get(key):
    try:
        return _get_client().get(key)
    except RedisError:
        return None


def cache_set(key, value, ttl=TREKS_TTL):
    try:
        # setting the key value with the expiry time
        _get_client().set(key, value, ex=ttl)
    except RedisError:
        pass

# -----------------------------------------------
# expire the data
def invalidate_treks():
    try:
        keys = _get_client().keys('treks:*') + _get_client().keys('trek:*') + _get_client().keys('stafftrek:*') + _get_client().keys('stafftreks:*')
        if keys:
            _get_client().delete(*keys)
    except RedisError:
        pass
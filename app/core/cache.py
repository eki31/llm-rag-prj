import os
import time

import redis
from redis.backoff import NoBackoff
from redis.retry import Retry

from app.core.logger import logger

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# After a failure, skip Redis for this long so every request doesn't pay for a failed connect
RETRY_AFTER_SECONDS = 30

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
    # No retries: redis-py retries 10 times by default, blocking the event loop for seconds when Redis is down
    retry=Retry(NoBackoff(), 0)
)

_unavailable_until = 0.0


def _mark_unavailable(error):
    global _unavailable_until
    _unavailable_until = time.monotonic() + RETRY_AFTER_SECONDS
    logger.warning(f"Redis unavailable at {REDIS_HOST}:{REDIS_PORT}, skipping cache for {RETRY_AFTER_SECONDS}s: {error}")


def cache_get(key):
    """Return the cached value, or None on a miss or if Redis is unavailable."""
    if time.monotonic() < _unavailable_until:
        return None
    try:
        return redis_client.get(key)
    except redis.RedisError as e:
        _mark_unavailable(e)
        return None


def cache_set(key, ttl, value):
    """Store a value; a Redis failure is logged and otherwise ignored."""
    if time.monotonic() < _unavailable_until:
        return
    try:
        redis_client.setex(key, ttl, value)
    except redis.RedisError as e:
        _mark_unavailable(e)

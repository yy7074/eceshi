"""
Redis 客户端
"""
import redis
from typing import Optional
from app.core.config import settings

_client: Optional[redis.Redis] = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD or None,
            decode_responses=True,
            socket_connect_timeout=3,
            socket_timeout=3,
        )
    return _client

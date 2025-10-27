import time

import rq
from redis import Redis

from .config import settings

redis = Redis.from_url(settings.REDIS_URL)
queue = rq.Queue("warming", connection=redis)


def warming_job(email: str) -> bool:
    """Mock warming job that simulates sending an email."""
    time.sleep(1)
    return True

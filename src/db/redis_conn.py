import subprocess
import logging
from typing import Tuple, TypedDict
import redis.asyncio as redis


async def create_redis_connection(host='localhost', port=6379, db=0, clear_on_startup=False) -> redis.Redis:
    """Create a Redis connection."""
    try:
        # start_redis()
        client = redis.Redis(host=host, port=port, db=db)
        await client.ping()
        logging.info("Successfully connected to Redis.")
        if clear_on_startup:
            logging.info("Flushing DB")
            await client.flushdb()
        return client
    except Exception as e:
        logging.error(f"Redis connection failed: {e}")
        raise


def start_redis():
    try:
        subprocess.run('redis-server -p 6379', shell=True)
    except Exception as e:
        logging.error(f"Failed to start Redis process: {e}")
        raise


async def fifo_push(redis_client: redis.Redis, name: str, message: str) -> None:
    await redis_client.lpush(name, message)


async def fifo_pop(redis_client: redis.Redis, name: str, timeout: int) -> str | None:
    return (await redis_client.brpop(name, timeout)).decode("utf-8")

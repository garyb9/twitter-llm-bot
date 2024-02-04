import logging
from typing import Tuple, TypedDict
import redis.asyncio as redis


async def create_redis_connection(host='localhost', port=6379, db=0, clear_on_startup=False) -> redis.Redis:
    """Create a Redis connection."""
    try:
        client = redis.Redis(host=host, port=port, db=db)
        await client.ping()
        logging.info("Successfully connected to Redis.")
        if clear_on_startup:
            logging.info("Flushing DB")
            await client.flushdb()
        return client
    except Exception as e:
        logging.error(f"Failed to connect to Redis: {e}")

    return None


async def add_link_to_set(redis_client: redis.Redis, set_name: str, link: str) -> None:
    """Add a link to a Redis set."""
    await redis_client.sadd(set_name, link)


async def add_links_to_set(redis_client: redis.Redis, set_name: str, links: set) -> None:
    """Add a list of links to a Redis set."""
    for link in links:
        await redis_client.sadd(set_name, link)


async def is_link_in_set(redis_client: redis.Redis, set_name: str, link: str) -> bool:
    """Check if a link is in a Redis set."""
    return await redis_client.sismember(set_name, link)


async def get_count(redis_client: redis.Redis, key: str) -> int:
    """Get the current count value from Redis."""
    value = await redis_client.get(key)
    return int(value) if value is not None else 0


async def get_set_len(redis_client: redis.Redis, set_key: str) -> int:
    """Get the current length of a set from Redis."""
    value = await redis_client.scard(set_key)
    return int(value) if value is not None else 0


async def get_list_len(redis_client: redis.Redis, list_key: str) -> int:
    """Get the current count value from Redis."""
    value = await redis_client.llen(list_key)
    return int(value) if value is not None else 0

async def increment_count(redis_client: redis.Redis, key: str, amount: int) -> int:
    """Increment a count value in Redis."""
    new_value = await redis_client.incrby(key, amount)
    return new_value


async def fifo_pop(redis_client: redis.Redis, redis_list_key: str) -> any:
    """Pop the first item in a list by a key"""
    return (await redis_client.lpop(redis_list_key)).decode("utf-8")


async def fifo_push(redis_client: redis.Redis, redis_list_key: str, data: list) -> any:
    """Push to the end of the list by a key"""
    return await redis_client.rpush(redis_list_key, *data)


class IncrementAddResult(TypedDict):
    new_word_count: int
    link_added: int


async def atomic_increment_and_add_link(
    redis_client: redis.Redis,
    count_key: str,
    amount: int,
    set_name: str,
    link: str
) -> IncrementAddResult:
    """Atomically increment a count and add a link to a set in Redis."""
    async with redis_client.pipeline(transaction=True) as pipe:
        await pipe.incrby(count_key, amount)
        await pipe.sadd(set_name, link)
        results = await pipe.execute()
    return {"new_word_count": results[0], "link_added": results[1]}

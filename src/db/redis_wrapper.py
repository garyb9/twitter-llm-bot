import logging
import subprocess
from typing import Optional
import redis.asyncio as redis


class RedisClientWrapper:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self, host='localhost', port=6379, db=0, clear_on_startup=False) -> None:
        """Asynchronously initialize the Redis connection."""
        try:
            self.client = redis.Redis(host=host, port=port, db=db)
            await self.client.ping()
            logging.info("Successfully connected to Redis.")
            if clear_on_startup:
                logging.info("Flushing DB")
                await self.client.flushdb()
        except Exception as e:
            logging.error(f"Redis connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        """Close the Redis connection."""
        if self.client:
            await self.client.close()
            await self.client.connection_pool.disconnect()
            logging.info("Redis connection closed.")

    def ensure_client_initialized(self):
        """Ensure that the Redis client is initialized."""
        if not self.client:
            raise Exception(
                "Redis client not initialized. Call 'connect' first.")

    async def fifo_push(self, name: str, message: str) -> None:
        """Push a message onto a FIFO queue."""
        self.ensure_client_initialized()
        await self.client.lpush(name, message)

    async def fifo_push_list(self, name: str, messages: list) -> None:
        """Atomically push a list of messages onto a FIFO queue."""
        self.ensure_client_initialized()
        if messages:
            await self.client.lpush(name, *messages)

    async def fifo_pop(self, name: str, timeout: int = 0) -> Optional[str]:
        """Pop a message from a FIFO queue."""
        self.ensure_client_initialized()
        result = await self.client.brpop(name, timeout)
        return result[1].decode("utf-8") if result else None

    async def fifo_peek(self, name: str = "default_queue", start: int = 0, end: int = -1) -> list:
        """
        Peek at messages in a FIFO queue without removing them.
        """
        self.ensure_client_initialized()
        messages = await self.client.lrange(name, start, end)
        return [message.decode("utf-8") for message in messages]

    async def fifo_clear(self, name: str) -> None:
        """
        Clear all messages from a specified FIFO queue.
        """
        self.ensure_client_initialized()
        await self.client.delete(name)
        logging.info(f"Queue '{name}' has been cleared.")


def start_redis():
    """Attempt to start a Redis server process."""
    try:
        subprocess.run(['redis-server', '-p', '6379'], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start Redis process: {e}")
        raise

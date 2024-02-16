import os
import sys
import asyncio
import logging
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import setup_env
from scheduler.scheduler_jobs import TWEET_QUEUE
from db.redis_wrapper import RedisClientWrapper
from twitter.twitter_wrapper import TwitterAsyncWrapper


async def main() -> None:
    redis_wrapper = RedisClientWrapper()
    await redis_wrapper.connect(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        clear_on_startup=bool(os.getenv("REDIS_CLEAR_ON_STARTUP", False)),
    )

    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    logging.info(tweet_text)
    tw = TwitterAsyncWrapper()
    response = await tw.post_text_tweet(tweet_text)
    logging.info(response)


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

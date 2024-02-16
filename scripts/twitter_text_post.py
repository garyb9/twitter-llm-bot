import os
import random
import sys
import asyncio
import logging
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import setup_env
from twitter.twitter_wrapper import TwitterAsyncWrapper
from tweet_generation import tweet_generation_philosophical


async def main() -> None:
    tw = TwitterAsyncWrapper()
    generated_tweets = await tweet_generation_philosophical()
    tweet_text = random.choice(generated_tweets)
    logging.info(tweet_text)
    response = await tw.post_text_tweet(tweet_text)
    logging.info(response)


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

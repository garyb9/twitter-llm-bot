import os
import sys
import asyncio
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from setup_env import setup

setup()
from twitter.twitter_wrapper import TwitterAsyncWrapper


async def main() -> None:
    tw = TwitterAsyncWrapper()
    tweets = tw.client.home_timeline(count=20)
    logging.info(tweets)


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

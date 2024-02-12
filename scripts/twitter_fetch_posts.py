import os
import sys
import asyncio
import logging
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
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

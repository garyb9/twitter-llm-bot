import os
import sys
import asyncio
import logging
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
from twitter.twitter_wrapper import TwitterWrapper


async def main() -> None:
    tw = TwitterWrapper()
    # await tw.post_text_tweet(
    #     f"Hello! I'm <NAME> and I'm here to help you with your {os.getenv('PHILOSOPHER_NAME')}.")

# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

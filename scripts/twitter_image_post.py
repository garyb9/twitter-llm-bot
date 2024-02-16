import os
import sys
import random
import asyncio
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from setup_env import setup

setup()
from twitter.twitter_wrapper import TwitterAsyncWrapper


async def main() -> None:
    tw = TwitterAsyncWrapper()
    tweet_text = """
Obstacles show us the gap between where we are and where we want to be.
    """
    # tweet_text = (await tweet_generation())[0]
    full_directory_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data")
    )
    files = [
        os.path.join(full_directory_path, f) for f in os.listdir(full_directory_path)
    ]

    sample_pics = [f for f in files if "sample_pic" in f and f.endswith("png")]
    random_pic = random.choice(sample_pics)
    response = await tw.post_image_tweet(image_path=random_pic, text=tweet_text)
    logging.info(response)


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

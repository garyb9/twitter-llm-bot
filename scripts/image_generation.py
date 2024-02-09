
import os
import sys
import asyncio
import logging
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
from typing import List
import llm.openai as openai
from llm.prompts import quote_formatter
from tweet_generation import tweet_generation


async def main() -> None:
    generated_response = await tweet_generation()

    prompt = f"""
Visualize the following quote: ```{generated_response[0]}```. 
Omit any text from the image. Use oil painting style.
    """
    generated_images = await openai.generate_image_async(prompt=prompt)

    generated_images[0].show()

# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

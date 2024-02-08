
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
from llm.prompts import str_to_list_formatter


async def tweet_generation(philosopher: str = 'Max Stirner') -> List[str]:

    messages = [
        {
            "role": "system",
            "content": "I am a tweet and quote generating machine. Generate 10 tweets of quotes by {name}, no hashtags, format each tweet as 2-3 lines, end with name."
        },
        {
            "role": "user",
            "content": f"Generate tweets inspired by the philosopher {philosopher}."
        }
    ]

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=1500,
        formatter=str_to_list_formatter
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(generated_response, indent=4)}"
    )
    return generated_response


async def main() -> None:
    generated_response = await tweet_generation()

    generated_images = await openai.generate_image_async(
        prompt=f"Visualize the following quote: ```{generated_response[0]}```. Omit any text from the image. Use oil painting style."
    )

    generated_images[0].show()

# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

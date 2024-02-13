
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
import llm.formatters as formatters


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
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(
        generated_response
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(formatted_response, indent=4)}"
    )
    return formatted_response

# Run
if __name__ == "__main__":
    try:
        asyncio.run(tweet_generation())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

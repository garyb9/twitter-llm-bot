import os
import random
import sys
import asyncio
import logging
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import setup_env
from typing import List
from llm import prompts
import llm.openai as openai
import llm.formatters as formatters


async def tweet_generation_quotes() -> List[str]:
    messages, author = prompts.prepare_prompt_for_text_model("quote_tweets")

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(generated_response)

    # Pipe an additional formatter to add author
    formatted_response_with_author = formatters.add_author(formatted_response, author)

    # Randomly merge both lists
    formatted_merged = [
        random.choice([a, b])
        for a, b in zip(formatted_response, formatted_response_with_author)
    ]

    logging.info(f"Tweets generated:\n{json.dumps(formatted_merged, indent=4)}")

    return formatted_merged


async def tweet_generation_philosophical() -> List[str]:
    messages, var = prompts.prepare_prompt_for_text_model("philosophical_tweets")

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(generated_response)

    formatted_response_with_depth = formatters.add_newlines(formatted_response)

    logging.info(
        f"Tweets generated:\n{json.dumps(formatted_response_with_depth, indent=4)}"
    )

    return formatted_response_with_depth


# Run
if __name__ == "__main__":
    try:
        # asyncio.run(tweet_generation_quotes())
        asyncio.run(tweet_generation_philosophical())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

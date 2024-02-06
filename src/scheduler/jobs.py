
import json
import logging
from llm import openai
from utils import str_to_list_formatter


async def generate_tweets():
    # TODO: temporary until we have a better way to do this.
    philosopher = "Max Stirner"

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


async def post_text_tweet_job():
    pass  # TODO:


async def post_image_tweet_job():
    pass  # TODO:

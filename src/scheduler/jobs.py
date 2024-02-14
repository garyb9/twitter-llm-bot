
import json
import logging
import random
from typing import Callable
from consts import IMAGE_QUEUE, TWEET_QUEUE
from llm import openai
from twitter.twitter_wrapper import TwitterAsyncWrapper
import llm.prompts as prompts
import llm.formatters as formatters
from db.redis_wrapper import RedisClientWrapper

twitter_wrapper = TwitterAsyncWrapper()


def job_decorator(job_id: str):
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            try:
                logging.info(f"Running: {job_id}")
                return await func(*args, **kwargs)
            except Exception as e:
                logging.error(f"An unexpected error occurred on {job_id}: {e}")
        # Set wrapper function name to the original function's name for clarity
        wrapper.__name__ = job_id
        wrapper.__qualname__ = job_id
        return wrapper
    return decorator


@job_decorator("generate_tweets_job")
async def generate_tweets_job(redis_wrapper: RedisClientWrapper):
    messages, author = prompts.prepare_prompt_for_text_model("quote_tweets")

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(
        generated_response
    )

    # Pipe an additional formatter to add author
    formatted_response_with_author = formatters.add_author(
        formatted_response, author)

    # Randomly merge both lists
    formatted_merged = [random.choice([a, b]) for a, b in zip(
        formatted_response, formatted_response_with_author)]

    logging.info(
        f"Tweets generated:\n{json.dumps(formatted_merged, indent=4)}"
    )

    # Push formatted tweets to Redis
    await redis_wrapper.fifo_push_list(TWEET_QUEUE, formatted_merged)


@job_decorator("post_text_tweet_job")
async def post_text_tweet_job(redis_wrapper: RedisClientWrapper):
    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    if tweet_text:
        response = await twitter_wrapper.post_text_tweet(
            text=tweet_text)
        logging.info(f"Posted tweet response: {response}")
    else:
        logging.warning(f"Tweet queue is empty.")


@job_decorator("post_image_tweet_job")
async def post_image_tweet_job(redis_wrapper: RedisClientWrapper):
    image_path = await redis_wrapper.fifo_pop(IMAGE_QUEUE)
    if image_path:
        response = twitter_wrapper.post_image_tweet(image_path)
        logging.info(f"Posted tweet with image response: {response}")
    else:
        logging.warning(f"Image queue is empty.")

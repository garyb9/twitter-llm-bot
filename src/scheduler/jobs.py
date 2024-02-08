
import json
import logging
from typing import Callable
from llm import openai
from twitter.twitter_wrapper import TwitterAsyncWrapper
from llm.prompts import prepare_prompt, str_to_list_formatter
from db.redis_wrapper import RedisClientWrapper

TWEET_QUEUE = "tweets"
IMAGE_QUEUE = "images"
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
    messages = prepare_prompt("quote_tweets")

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
        formatter=str_to_list_formatter
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(generated_response, indent=4)}"
    )

    await redis_wrapper.fifo_push_list(TWEET_QUEUE, generated_response)


@job_decorator("post_text_tweet_job")
async def post_text_tweet_job(redis_wrapper: RedisClientWrapper):
    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    if tweet_text:
        response = await twitter_wrapper.post_text_tweet(
            text=tweet_text)
        logging.info(f"Posted tweet response: {response}")


@job_decorator("post_image_tweet_job")
async def post_image_tweet_job(redis_wrapper: RedisClientWrapper):
    image_path = await redis_wrapper.fifo_pop(IMAGE_QUEUE)
    if image_path:
        response = twitter_wrapper.post_image_tweet(image_path)
        logging.info(f"Posted tweet with image response: {response}")

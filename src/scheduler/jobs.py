
import json
import logging
from typing import Callable
from llm import openai
from twitter import twitter_client
from utils import prepare_random_prompt, str_to_list_formatter
from db.redis_wrapper import RedisClientWrapper

TWEET_QUEUE = "tweets"
IMAGE_QUEUE = "images"


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
    category = "quote_tweets"
    messages = prepare_random_prompt(category)

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
        formatter=str_to_list_formatter
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(generated_response, indent=4)}"
    )

    await redis_wrapper.fifo_push_list(TWEET_QUEUE, messages)


@job_decorator("post_text_tweet_job")
async def post_text_tweet_job(redis_wrapper: RedisClientWrapper):
    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    if tweet_text:
        status = twitter_client.create_tweet(
            text=tweet_text)
        logging.info(f"Posted tweet: {status.id}")


@job_decorator("post_image_tweet_job")
async def post_image_tweet_job(redis_wrapper: RedisClientWrapper):
    image_path = await redis_wrapper.fifo_pop(IMAGE_QUEUE)
    if image_path:
        media = twitter_client.media_upload(image_path)
        status = twitter_client.update_status(
            status="", media_ids=[media.media_id])
        logging.info(f"Posted tweet with image: {status.id}")

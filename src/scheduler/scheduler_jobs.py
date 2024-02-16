
from asyncio import sleep
import json
import logging
import random
from typing import Callable
from consts import IMAGE_QUEUE, MAX_TEXT_GENERETIONS_PER_REQUEST, TWEET_QUEUE
from llm import openai
from twitter.twitter_wrapper import TwitterAsyncWrapper
import llm.prompts as prompts
import llm.formatters as formatters
from db.redis_wrapper import RedisClientWrapper

twitter_wrapper = TwitterAsyncWrapper()


def job_decorator(job_id: str, retries: int = 1, delay: int = 1):
    def decorator(func: Callable):
        async def wrapper(*args, **kwargs):
            attempts = 0
            while attempts <= retries:
                try:
                    logging.info(f"Running: {job_id}")
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.error(
                        f"An unexpected error occurred on {job_id}: {e}. Attempt {attempts + 1} of {retries + 1}")
                    attempts += 1
                    if attempts <= retries:
                        logging.info(
                            f"Retrying {job_id} after {delay} seconds...")
                        await sleep(delay)  # Wait before retrying
        # Set wrapper function name to the original function's name for clarity
        wrapper.__name__ = job_id
        wrapper.__qualname__ = job_id
        return wrapper
    return decorator


@job_decorator("generate_random_tweets_job")
async def generate_random_tweets_job(redis_wrapper: RedisClientWrapper, check_fifo: bool = False):
    if check_fifo:
        fifo_items = await redis_wrapper.fifo_item_count(TWEET_QUEUE)
        if fifo_items:
            logging.info(
                f"There are {fifo_items} items in queue. Skipping generation.")
            # return

    # Define the tweet generation functions and their respective weights/chacnes
    tweet_generation_options = [
        (generate_quote_tweets_job, 40),
        (generate_philosophical_tweets_job, 60),
    ]

    # Unpack the options and weights
    functions, weights = zip(*tweet_generation_options)

    # Select a tweet generation function based on the specified weights
    tweet_generation_function = random.choices(
        functions, weights=weights, k=1)[0]

    logging.info(
        f"Running randomized function: {tweet_generation_function.__name__}")

    # Call the selected function
    await tweet_generation_function(redis_wrapper)


@job_decorator("generate_quote_tweets_job")
async def generate_quote_tweets_job(redis_wrapper: RedisClientWrapper):
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
    assert len(
        formatted_response) == MAX_TEXT_GENERETIONS_PER_REQUEST, "Error with formatted response length"

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


@job_decorator("generate_philosophical_tweets_job")
async def generate_philosophical_tweets_job(redis_wrapper: RedisClientWrapper):
    messages, var = prompts.prepare_prompt_for_text_model(
        "philosophical_tweets")

    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(
        generated_response
    )
    assert len(
        formatted_response) == MAX_TEXT_GENERETIONS_PER_REQUEST, "Error with formatted response length"

    # Pipe an additional formatter to add line breaks
    formatted_response_with_depth = formatters.add_newlines(
        formatted_response
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(formatted_response_with_depth, indent=4)}"
    )

    # Push formatted tweets to Redis
    await redis_wrapper.fifo_push_list(TWEET_QUEUE, formatted_response_with_depth)


@job_decorator("post_text_tweet_job")
async def post_text_tweet_job(redis_wrapper: RedisClientWrapper):
    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    if tweet_text:
        response = await twitter_wrapper.post_text_tweet(
            text=tweet_text)
        if isinstance(response, tuple):
            logging.info(
                f"Posted tweet response: {json.dumps(response._asdict(), indent=4)}")
        else:
            logging.info(
                f"Posted tweet response: {response}")
    else:
        logging.warning(f"Tweet queue is empty.")


@job_decorator("post_image_tweet_job")
async def post_image_tweet_job(redis_wrapper: RedisClientWrapper):
    image_path = await redis_wrapper.fifo_pop(IMAGE_QUEUE)
    if image_path:
        response = twitter_wrapper.post_image_tweet(image_path)
        if isinstance(response, tuple):
            logging.info(
                f"Posted tweet response: {json.dumps(response._asdict(), indent=4)}")
        else:
            logging.info(
                f"Posted tweet response: {response}")
    else:
        logging.warning(f"Image queue is empty.")

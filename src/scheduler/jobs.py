
import json
import logging
from llm import openai
from twitter import twitter_client
from utils import str_to_list_formatter
from db.redis_wrapper import RedisClientWrapper

TWEET_QUEUE = "tweets"
IMAGE_QUEUE = "images"


async def generate_tweets_job(redis_wrapper: RedisClientWrapper):
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
        max_tokens=2000,
        formatter=str_to_list_formatter
    )

    logging.info(
        f"Tweets generated:\n{json.dumps(generated_response, indent=4)}"
    )

    await redis_wrapper.fifo_push_list(TWEET_QUEUE, messages)


async def post_text_tweet_job(redis_wrapper: RedisClientWrapper):
    tweet_text = await redis_wrapper.fifo_pop(TWEET_QUEUE)
    if tweet_text:
        status = twitter_client.create_tweet(
            text=tweet_text)
        logging.info(f"Posted tweet: {status.id}")


async def post_image_tweet_job(redis_wrapper: RedisClientWrapper):
    image_path = await redis_wrapper.fifo_pop(IMAGE_QUEUE)
    if image_path:
        media = twitter_client.media_upload(image_path)
        status = twitter_client.update_status(
            status="", media_ids=[media.media_id])
        logging.info(f"Posted tweet with image: {status.id}")

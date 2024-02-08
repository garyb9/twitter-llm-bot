import os
import tweepy
from tweepy import asynchronous

twitter_client = tweepy.Client(
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
    access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)


class TwitterAsyncWrapper:
    def __init__(self):
        self.client = asynchronous.AsyncClient(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    async def post_text_tweet(self, text: str):
        """
        Posts a text tweet.

        Parameters:
        - text (str): The text of the tweet.

        Returns:
        - The response from Twitter API after posting the tweet.
        """
        response = await self.client.create_tweet(text=text)
        return response

    async def post_image_tweet(self, image_path: str, status_text: str = ""):
        """
        Posts a tweet with an image.

        Parameters:
        - image_path (str): The file path of the image to upload.
        - status_text (str, optional): The text of the tweet, if any.

        Returns:
        - The response from Twitter API after posting the tweet.
        """
        media = self.client.media_upload(filename=image_path)
        response = self.client.create_tweet(
            status=status_text, media_ids=[media.media_id])
        return response

import os
from tweepy import asynchronous, API, OAuthHandler


class TwitterAsyncWrapper:
    def __init__(self):
        """
        Initialize the Twitter wrapper with both synchronous and asynchronous clients.

        The synchronous client (self.client) is used for operations not supported in Twitter API v2, 
        like media uploads. The asynchronous client (self.async_client) is used for operations 
        available in Twitter API v2, like posting tweets.
        """

        # Twitter API v1.1 (synchronous) for media upload
        self.client = API(
            auth=OAuthHandler(
                consumer_key=os.getenv('TWITTER_API_KEY'),
                consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
                access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
                access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
        )

        # Twitter API v2 (asynchronous) for tweeting
        self.async_client = asynchronous.AsyncClient(
            consumer_key=os.getenv('TWITTER_API_KEY'),
            consumer_secret=os.getenv('TWITTER_API_KEY_SECRET'),
            access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    async def post_text_tweet(self, text: str) -> any:
        """
        Asynchronously posts a text tweet.

        Parameters:
        - text (str): The text of the tweet to post.

        Returns:
        - response: The response from the Twitter API after posting the tweet.
        """
        response = await self.async_client.create_tweet(text=text)
        return response

    async def post_image_tweet(self, image_path: str, text: str = "") -> any:
        """
        Posts a tweet with an image. This method combines synchronous media upload
        with asynchronous tweet posting due to current API limitations.

        Parameters:
        - image_path (str): The file path of the image to upload.
        - text (str, optional): The text of the tweet, if any.

        Returns:
        - response: The response from the Twitter API after posting the tweet.
        """
        media = self.client.media_upload(filename=image_path)
        response = await self.async_client.create_tweet(
            text=text, media_ids=[media.media_id])
        return response

import pytest
from unittest.mock import AsyncMock, patch

# Assuming you have a module named `scheduler` where your job function is defined
from scheduler.jobs import generate_tweets_job, TWEET_QUEUE
from db.redis_wrapper import RedisClientWrapper
from utils import str_to_list_formatter


@pytest.mark.asyncio
async def test_generate_tweets_job():
    # Mock the RedisClientWrapper
    mock_redis = AsyncMock(spec=RedisClientWrapper)

    # Patch the dependencies
    with patch("scheduler.prepare_prompt", return_value=["Test tweet"]) as mock_prepare:
        with patch("scheduler.openai.generate_text_async", new_callable=AsyncMock) as mock_generate:
            # Mock the generate_text_async to return a specific response
            mock_generate.return_value = {"tweets": ["Tweet 1", "Tweet 2"]}

            with patch("scheduler.logging.info") as mock_logging:
                # Call the function
                await generate_tweets_job(mock_redis)

                # Assert prepare_prompt was called correctly
                mock_prepare.assert_called_once_with("quote_tweets")

                # Assert generate_text_async was called with correct parameters
                mock_generate.assert_called_once_with(
                    ["Test tweet"],
                    temperature=0.9,
                    max_tokens=2000,
                    formatter=str_to_list_formatter
                )

                # Assert logging was called with the expected message
                # You can refine this to check for the specific log message
                mock_logging.assert_called()

                # Assert that fifo_push_list was called with the correct arguments
                mock_redis.fifo_push_list.assert_called_once_with(
                    TWEET_QUEUE, ["Test tweet"])

import pytest
from scheduler.jobs import generate_tweets_job, TWEET_QUEUE
from db.redis_wrapper import RedisClientWrapper
from llm.prompts import str_to_list_formatter


@pytest.mark.asyncio
async def test_generate_tweets_job(mocker):
    # Mock the RedisClientWrapper
    mock_redis = RedisClientWrapper()
    mocker.patch.object(mock_redis, 'fifo_push_list',
                        new_callable=mocker.AsyncMock)

    # Patch the dependencies using mocker
    prepare_prompt_ret_val = ["Test prompt"]
    mock_prepare = mocker.patch(
        "scheduler.jobs.prepare_prompt",
        return_value=prepare_prompt_ret_val,
        autospec=True
    )
    generate_text_ret_val = ["Tweet 1", "Tweet 2"]
    mock_generate = mocker.patch(
        "llm.openai.generate_text_async",
        return_value=generate_text_ret_val
    )

    # Call the function
    await generate_tweets_job(mock_redis)

    # Assert prepare_prompt was called correctly
    mock_prepare.assert_called_once_with("quote_tweets")

    # Assert generate_text_async was called with correct parameters
    mock_generate.assert_called_once_with(
        prepare_prompt_ret_val,
        temperature=0.9,
        max_tokens=2000,
        formatter=str_to_list_formatter
    )

    # Assert that fifo_push_list was called with the correct arguments
    mock_redis.fifo_push_list.assert_called_once_with(
        TWEET_QUEUE, generate_text_ret_val)

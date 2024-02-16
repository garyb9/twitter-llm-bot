import pytest
from setup_env import setup

setup()
import scheduler.scheduler_jobs as scheduler_jobs
from db.redis_wrapper import RedisClientWrapper
import llm.formatters as formatters
from unittest.mock import ANY
import consts


@pytest.mark.asyncio
@pytest.mark.skip("Fix propagation of `random.choice`")
async def test_generate_random_tweets_job(mocker):
    mock_redis = RedisClientWrapper()
    # Mock random.choice to control which job function is called
    mocker.patch(
        "random.choice", side_effect=[scheduler_jobs.generate_quote_tweets_job]
    )

    # Assume generate_quote_tweets_job is being tested; prepare mocks as needed
    mocker.patch.object(mock_redis, "fifo_push_list", new_callable=mocker.AsyncMock)
    mock_prepare = mocker.patch(
        "scheduler.scheduler_jobs.prompts.prepare_prompt_for_text_model",
        return_value=(["Test prompt"], "name"),
        autospec=True,
    )
    generate_text_ret_val = '"Random Tweet 1"\n"Random Tweet 2"\n"Random Tweet 3"\n"Random Tweet 4"\n"Random Tweet 5"'
    mocker.patch("llm.openai.generate_text_async", return_value=generate_text_ret_val)

    await scheduler_jobs.generate_random_tweets_job(mock_redis)

    # Assertions specific to the job function that was mocked to be chosen
    mock_prepare.assert_called_once()


@pytest.mark.asyncio
async def test_generate_quote_tweets_job(mocker):
    # Mock the RedisClientWrapper
    mock_redis = RedisClientWrapper()
    mocker.patch.object(mock_redis, "fifo_push_list", new_callable=mocker.AsyncMock)

    # Patch the dependencies using mocker
    prepare_prompt_ret_val = ["Test prompt"]
    prepare_prompt_ret_var = "name"
    mock_prepare = mocker.patch(
        "scheduler.scheduler_jobs.prompts.prepare_prompt_for_text_model",
        return_value=(prepare_prompt_ret_val, prepare_prompt_ret_var),
        autospec=True,
    )
    generate_text_ret_val = '"Tweet 1"\n"Tweet 2"\n"Tweet 3"\n"Tweet 4"\n"Tweet 5"'
    mock_generate = mocker.patch(
        "llm.openai.generate_text_async", return_value=generate_text_ret_val
    )

    # Call the function
    await scheduler_jobs.generate_quote_tweets_job(mock_redis)

    # Assert prepare_prompt_for_text_model was called correctly
    mock_prepare.assert_called_once_with("quote_tweets")

    # Assert generate_text_async was called with correct parameters
    mock_generate.assert_called_once_with(
        prepare_prompt_ret_val,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(generate_text_ret_val)

    assert formatted_response == ["Tweet 1", "Tweet 2", "Tweet 3", "Tweet 4", "Tweet 5"]

    # Pipe an additional formatter to add author
    formatted_response_with_author = formatters.add_author(
        formatted_response, prepare_prompt_ret_var
    )

    assert formatted_response_with_author == [
        '"Tweet 1"\n\n- name -',
        '"Tweet 2"\n\n- name -',
        '"Tweet 3"\n\n- name -',
        '"Tweet 4"\n\n- name -',
        '"Tweet 5"\n\n- name -',
    ]

    # Assert that fifo_push_list was called with the correct arguments
    mock_redis.fifo_push_list.assert_called_once_with(consts.TWEET_QUEUE, ANY)


@pytest.mark.asyncio
async def test_generate_philosophical_tweets_job(mocker):
    mock_redis = RedisClientWrapper()
    mocker.patch.object(mock_redis, "fifo_push_list", new_callable=mocker.AsyncMock)

    prepare_prompt_ret_val = ["Philosophical prompt"]
    mock_prepare = mocker.patch(
        "scheduler.scheduler_jobs.prompts.prepare_prompt_for_text_model",
        return_value=(prepare_prompt_ret_val, "philosophy"),
        autospec=True,
    )
    generate_text_ret_val = '"Philosophy Tweet 1"\n"Philosophy Tweet 2"\n"Philosophy Tweet 3"\n"Philosophy Tweet 4"\n"Philosophy Tweet 5"'
    mock_generate = mocker.patch(
        "llm.openai.generate_text_async", return_value=generate_text_ret_val
    )

    await scheduler_jobs.generate_philosophical_tweets_job(mock_redis)

    mock_prepare.assert_called_once_with("philosophical_tweets")
    mock_generate.assert_called_once_with(
        prepare_prompt_ret_val,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(generate_text_ret_val)

    assert formatted_response == [
        "Philosophy Tweet 1",
        "Philosophy Tweet 2",
        "Philosophy Tweet 3",
        "Philosophy Tweet 4",
        "Philosophy Tweet 5",
    ]

    # Assert that fifo_push_list was called with the correct arguments
    mock_redis.fifo_push_list.assert_called_once_with(consts.TWEET_QUEUE, ANY)


@pytest.mark.asyncio
@pytest.mark.skip()
async def test_post_text_tweet_job(mocker):
    # Mock RedisClientWrapper
    mock_redis = RedisClientWrapper()
    tweet_text = "Sample tweet text"
    mocker.patch.object(mock_redis, "fifo_pop", return_value=tweet_text)

    # Mock tweepy.Client
    mock_twitter_client = mocker.patch("twitter.twitter_client", autospec=True)
    mock_create_tweet = mocker.AsyncMock(
        return_value=type("obj", (object,), {"id": "123456789"})
    )
    mock_twitter_client.create_tweet = mock_create_tweet

    # Call the function
    await scheduler_jobs.post_text_tweet_job(mock_redis)

    # Assertions
    mock_redis.fifo_pop.assert_called_once_with(consts.TWEET_QUEUE)
    mock_create_tweet.assert_called_once_with(text=tweet_text)


@pytest.mark.asyncio
@pytest.mark.skip()
async def test_post_image_tweet_job(mocker):
    # Mock RedisClientWrapper
    mock_redis = RedisClientWrapper()
    image_path = "/path/to/image.jpg"
    mocker.patch.object(mock_redis, "fifo_pop", return_value=image_path)

    # Mock tweepy.Client and its methods
    mock_twitter_client = mocker.patch("twitter.twitter_client", autospec=True)
    mock_media_upload = mocker.AsyncMock(
        return_value=type("obj", (object,), {"media_id": "123"})
    )
    mock_twitter_client.media_upload = mock_media_upload

    mock_update_status = mocker.AsyncMock(
        return_value=type("obj", (object,), {"id": "123456789"})
    )
    mock_twitter_client.update_status = mock_update_status

    # Call the function
    await scheduler_jobs.post_image_tweet_job(mock_redis)

    # Assertions
    mock_redis.fifo_pop.assert_called_once_with(consts.IMAGE_QUEUE)
    mock_media_upload.assert_called_once_with(image_path)
    mock_update_status.assert_called_once_with(status="", media_ids=["123"])

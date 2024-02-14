import pytest
import setup_env
import scheduler.jobs as jobs
from db.redis_wrapper import RedisClientWrapper
import llm.formatters as formatters
import consts


@pytest.mark.asyncio
async def test_generate_tweets_job(mocker):
    # Mock the RedisClientWrapper
    mock_redis = RedisClientWrapper()
    mocker.patch.object(mock_redis, 'fifo_push_list',
                        new_callable=mocker.AsyncMock)

    # Patch the dependencies using mocker
    prepare_prompt_ret_val = ["Test prompt"]
    prepare_prompt_ret_var = "name"
    mock_prepare = mocker.patch(
        "scheduler.jobs.prompts.prepare_prompt_for_text_model",
        return_value=(prepare_prompt_ret_val, prepare_prompt_ret_var),
        autospec=True
    )
    generate_text_ret_val = "\"Tweet 1\"\n\"Tweet 2\""
    mock_generate = mocker.patch(
        "llm.openai.generate_text_async",
        return_value=generate_text_ret_val
    )

    # Call the function
    await jobs.generate_tweets_job(mock_redis)

    # Assert prepare_prompt_for_text_model was called correctly
    mock_prepare.assert_called_once_with("quote_tweets")

    # Assert generate_text_async was called with correct parameters
    mock_generate.assert_called_once_with(
        prepare_prompt_ret_val,
        temperature=0.9,
        max_tokens=2000,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(
        generate_text_ret_val
    )

    assert formatted_response == ["Tweet 1", "Tweet 2"]

    # Pipe an additional formatter to add author
    formatted_response_with_author = formatters.add_author(
        formatted_response, prepare_prompt_ret_var)

    assert formatted_response_with_author == [
        '\"Tweet 1\"\n\n- name -', '\"Tweet 2\"\n\n- name -']

    # Assert that fifo_push_list was called with the correct arguments
    mock_redis.fifo_push_list.assert_called_once_with(
        consts.TWEET_QUEUE, formatted_response_with_author)


@pytest.mark.asyncio
@pytest.mark.skip()
async def test_post_text_tweet_job(mocker):
    # Mock RedisClientWrapper
    mock_redis = RedisClientWrapper()
    tweet_text = "Sample tweet text"
    mocker.patch.object(mock_redis, 'fifo_pop', return_value=tweet_text)

    # Mock tweepy.Client
    mock_twitter_client = mocker.patch('twitter.twitter_client', autospec=True)
    mock_create_tweet = mocker.AsyncMock(
        return_value=type('obj', (object,), {'id': '123456789'}))
    mock_twitter_client.create_tweet = mock_create_tweet

    # Call the function
    await jobs.post_text_tweet_job(mock_redis)

    # Assertions
    mock_redis.fifo_pop.assert_called_once_with(consts.TWEET_QUEUE)
    mock_create_tweet.assert_called_once_with(text=tweet_text)


@pytest.mark.asyncio
@pytest.mark.skip()
async def test_post_image_tweet_job(mocker):
    # Mock RedisClientWrapper
    mock_redis = RedisClientWrapper()
    image_path = "/path/to/image.jpg"
    mocker.patch.object(mock_redis, 'fifo_pop', return_value=image_path)

    # Mock tweepy.Client and its methods
    mock_twitter_client = mocker.patch('twitter.twitter_client', autospec=True)
    mock_media_upload = mocker.AsyncMock(
        return_value=type('obj', (object,), {'media_id': '123'}))
    mock_twitter_client.media_upload = mock_media_upload

    mock_update_status = mocker.AsyncMock(
        return_value=type('obj', (object,), {'id': '123456789'}))
    mock_twitter_client.update_status = mock_update_status

    # Call the function
    await jobs.post_image_tweet_job(mock_redis)

    # Assertions
    mock_redis.fifo_pop.assert_called_once_with(consts.IMAGE_QUEUE)
    mock_media_upload.assert_called_once_with(image_path)
    mock_update_status.assert_called_once_with(status="", media_ids=['123'])

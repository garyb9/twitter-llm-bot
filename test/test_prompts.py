import json
import pytest
from src.llm.openai import generate_text_async
from utils import str_to_list_formatter, prepare_random_prompt


@pytest.mark.asyncio
async def test_generate_text():
    philosopher = "Max Stirner"

    messages = [
        {
            "role": "system",
            "content": "I am a tweet and quote generating machine. Generate 10 tweets of quotes by {name}, no hashtags, format each tweet as 2-3 lines, end with name."
        },
        {
            "role": "user",
            "content": f"Please generate tweets inspired by the philosopher {philosopher}."
        }
    ]
    generated_response = await generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=1500,
        formatter=str_to_list_formatter
    )
    assert isinstance(generated_response, list)
    assert len(generated_response) == 10
    assert all(isinstance(tweet, str)
               and "Max Stirner" in tweet for tweet in generated_response), "All elements must be strings containing 'Max Stirner'"


@pytest.fixture
def mock_prompts_config(mocker):
    mock_data = {
        "quote_tweets": [
            {
                "messages": [
                    {
                        "role": "system",
                        "content": "Generate 10 tweets of quotes by {name}, no hashtags."
                    },
                    {
                        "role": "user",
                        "content": "Generate tweets inspired by the philosopher {name}."
                    }
                ],
                "input_variables": {
                    "name": ["Philosopher A", "Philosopher B"]
                }
            }
        ],
        "philosophical_tweets": [
            {
                "messages": [
                    {
                        "role": "system",
                        "content": "Generate 10 tweets about {topic} with a philosophical sense, without hashtags and emojis."
                    },
                    {
                        "role": "user",
                        "content": "Let's explore the depth of {topic} through philosophical tweets."
                    }
                ],
                "input_variables": {
                    "topic": ["Topic A", "Topic B"]
                }
            }
        ]
    }
    mocker.patch('json.load', return_value=mock_data)


def test_prepare_random_prompt_structure(mock_prompts_config):
    messages = prepare_random_prompt()
    assert isinstance(
        messages, list), "The result should be a list of messages."
    assert len(messages) > 0, "The result list should not be empty."
    for message in messages:
        assert 'role' in message and 'content' in message, "Each message should have 'role' and 'content' keys."
        assert isinstance(message['role'], str), "'role' should be a string."
        assert isinstance(message['content'],
                          str), "'content' should be a string."
        assert "{name}" not in message['content'] and "{topic}" not in message['content'], "Placeholders should be replaced."

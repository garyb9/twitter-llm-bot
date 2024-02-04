import json
import pytest
from src.llm.openai import generate_text_async
from utils import str_to_list_formatter


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

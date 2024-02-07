import pytest
from src.llm.openai import generate_text_async
from utils import str_to_list_formatter, prepare_prompt


def test_prepare_prompt_structure():
    messages = prepare_prompt()
    assert isinstance(
        messages, list), "The result should be a list of messages."
    assert len(messages) > 0, "The result list should not be empty."
    for message in messages:
        assert 'role' in message and 'content' in message, "Each message should have 'role' and 'content' keys."
        assert isinstance(message['role'], str), "'role' should be a string."
        assert isinstance(message['content'],
                          str), "'content' should be a string."
        assert "{name}" not in message['content'] and "{topic}" not in message['content'], "Placeholders should be replaced."


@pytest.mark.asyncio
@pytest.mark.skip(reason="Enable when direct prompting is required for testing")
async def test_generate_text():
    category = 'quote_tweets'
    chosen_var = "Max Stirner"
    messages = prepare_prompt(category=category, chosen_var=chosen_var)

    generated_response = await generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=1500,
        formatter=str_to_list_formatter
    )

    assert isinstance(generated_response, list)
    assert len(generated_response) == 10

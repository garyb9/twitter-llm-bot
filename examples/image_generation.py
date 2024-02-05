import os
import sys
import json
import logging
import asyncio
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
import llm.openai as openai
from utils import str_to_list_formatter
from io import BytesIO
from PIL import Image

async def main() -> None:
    philosopher = 'Max Stirner'
    
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
    
    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=1500,
        formatter=str_to_list_formatter
    )
    
    logging.info(json.dumps(generated_response, indent=4))
    
    messages = [
        {
            "role": "system",
            "content": "I am a tweet and quote image visualizer. Visualize with high definition the given quote. Do not visualize the person mentioned, if mentioned."
        },
        {
            "role": "user",
            "content": f"Please visualize the following quote: ```{generated_response[0]}```."
        }
    ]
    
    generated_image = await openai.generate_image_async(prompt=messages)
    img = Image.open(BytesIO(generated_image))
    img.show()

# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

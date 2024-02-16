import os
import random
import sys
import json
import asyncio
import logging


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from setup_env import setup

setup()
from images import image_utils
import llm.prompts as prompts
import llm.formatters as formatters
from PIL import Image
from llm import openai


async def main() -> None:

    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    image_path = os.path.join(data_path, "sample_pic_11.png")
    save_path = image_path

    messages, author = prompts.prepare_prompt_for_text_model("quote_tweets")
    generated_response = await openai.generate_text_async(
        messages,
        temperature=0.9,
        max_tokens=1500,
    )

    # Clean generated content
    formatted_response = formatters.line_split_formatter(generated_response)

    # Pipe an additional formatter to add author
    formatted_response_with_author = formatters.add_author(formatted_response, author)

    logging.info(
        f"Tweets generated:\n{json.dumps(formatted_response_with_author, indent=4)}"
    )

    # # prompt = prepare_prompt_for_image_model()
    prompt = prompts.prompts_config_image[1]["message"]
    generated_images = await openai.generate_image_async(prompt=prompt)
    generated_images[0].show()
    generated_images[0].save(image_path)

    font_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "data", "gautamib.ttf")
    )

    # centaur.ttf, avenir.ttf, gothma.ttf, lato.ttf

    image_utils.add_text_to_image(
        image_path=image_path,
        save_path=save_path,
        text=random.choice(formatted_response_with_author),
        font_path=font_path,
    )
    modified_image = Image.open(save_path)
    modified_image.show()


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

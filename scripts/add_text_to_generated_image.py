import os
import sys
import json
import asyncio
import logging


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
from images.image_utils import add_text_to_image, extend_image_upwards
from llm.prompts import prompts_config_image
from PIL import Image
from llm import openai


async def main() -> None:

    data_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data'))
    image_path = os.path.join(data_path, 'sample_pic_4.png')
    save_path = os.path.join(data_path, 'sample_pic_8.png')

    # prompt = prepare_prompt_for_image_model()
    # prompt = prompts_config_image[0]['message']
    # generated_images = await openai.generate_image_async(prompt=prompt)
    # generated_images[0].show()
    # generated_images[0].save(image_path)

    text = """
"Obstacles show us the gap between where we are and where we want to be"

- Anonymous -
    """
    font_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'gautamib.ttf'))
    # extend_image_upwards(
    #     image_path=image_path,
    #     save_path=save_path,
    # )
    add_text_to_image(
        image_path=image_path,
        save_path=save_path,
        text=text,
        font_path=font_path
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

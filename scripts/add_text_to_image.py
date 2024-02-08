import os
import cv2
import sys
import asyncio
import logging
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)
import setup_env
from images.image_utils import add_text_to_image
from PIL import Image


async def main() -> None:

    image_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_pic_4.png'))
    text = """
"Obstacles show us the gap between where we are and where we want to be" - Anonymous.
    """
    save_path = image_path.replace('pic_4', 'pic_5')
    font_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'data', 'gautamib.ttf'))
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

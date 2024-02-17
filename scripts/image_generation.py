import os
import sys
import asyncio
import logging

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from llm import prompts
import llm.openai as openai


async def main() -> None:
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    image_path = os.path.join(data_path, "sample_pic_19.png")

    prompt = prompts.prepare_prompt_for_image_model(0)
    print(f"prompt: {prompt}")
    generated_images = await openai.generate_image_async(prompt=prompt)
    for image in generated_images:
        image.save(image_path)
        image.show()


# Run
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

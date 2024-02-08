import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Image.MAX_IMAGE_PIXELS = None


def add_text_to_image(
    image_path,
    save_path,
    text,
    font_path='arial.ttf',
    color="white",
    relative_font_size=0.05,
    vertical_position=0.15,
    outline_color="black",
    outline_width=1
):
    """
    Add text to an image with specified font and color.

    Args:
    - image_path: Path to the input image.
    - save_path: Path where the modified image will be saved.
    - text: Text to add to the image.
    - font_path: Path to the .ttf font file to use.
    - color: Color of the text.
    - relative_font_size: Font size relative to the image width.
    - vertical_position: Vertical position of the text as a fraction of image height (0.5 for middle).
    """
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Calculate font size relative to the image width
    font_size = int(image_width * relative_font_size)

    # Load or set the default font
    font = ImageFont.truetype(font_path, font_size)

    # Define the maximum width for the text
    padding = 20  # Padding inside the rectangle for text
    max_width = image_width - 2 * padding

    # Estimate the average character width at this font size and calculate wrap width
    avg_char_width = sum(font.getsize(char)[
                         0] for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') / 52
    # Ensure wrap_width is at least 1
    wrap_width = max(1, int(max_width / avg_char_width))

    # Wrap the text to fit into the rectangle
    wrapped_text = textwrap.fill(text, width=wrap_width)

    # Split the wrapped text into lines to calculate the total text height
    lines = wrapped_text.split('\n')
    text_height = sum([font.getsize(line)[1]
                      for line in lines]) + padding * (len(lines) - 1)

    # Calculate the starting y position based on the vertical_position parameter
    y_position = image_height * vertical_position - text_height / 2

    # Draw the wrapped text
    for line in lines:
        # Calculate horizontal position to center the text
        text_width, line_height = draw.textsize(line, font=font)
        x_position = (image_width - text_width) / 2
        # draw.text((x_position, y_position), line, font=font, fill=color)
        draw_text_with_outline(
            draw, line, (x_position, y_position), font, color, outline_color, outline_width)

        # Move to the next line, adding padding between lines
        y_position += line_height + padding

    # Save the modified image
    image.save(save_path)


def draw_text_with_outline(draw, text, position, font, text_color, outline_color, outline_width):
    x, y = position
    # Draw outline in all directions
    for i in range(-outline_width, outline_width + 1):
        for j in range(-outline_width, outline_width + 1):
            if i != 0 or j != 0:  # to avoid drawing the text color in the outline loop
                draw.text((x + i, y + j), text, font=font, fill=outline_color)
    # Draw the main text
    draw.text(position, text, font=font, fill=text_color)


def add_text_to_image_cv2(image_path, save_path, text):
    # Load the image
    image = cv2.imread(image_path)

    # Define the size of the image
    height, width = image.shape[:2]

    # Define the font, size, and thickness
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1  # Adjust as needed
    thickness = 2   # Adjust as needed
    color = (255, 255, 255)  # White color

    # Get the text size
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]

    # Calculate the position for the text to be centered horizontally and 5% from the top
    text_x = (width - text_size[0]) // 2
    text_y = int(height * 0.05) + text_size[1]

    # Add text to image
    cv2.putText(image, text, (text_x, text_y), font,
                font_scale, color, thickness, cv2.LINE_AA)

    # Save the edited image
    cv2.imwrite(save_path, image)

    return save_path

import os
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

import numpy as np

# Image.MAX_IMAGE_PIXELS = None


def add_text_to_image(
    image_path,
    save_path,
    text,
    font_path='arial.ttf',
    relative_font_size=0.04,
    vertical_position=0.10,
    line_spacing=1.0
):
    """
    Adds wrapped text to an image with optional outline for improved legibility, 
    supports custom font and adjusts font size relative to image width.

    Parameters:
    - image_path (str): Path to the source image to which text will be added.
    - save_path (str): Path where the modified image will be saved.
    - text (str): The text content to add to the image. Supports newline characters as breaks.
    - font_path (str, optional): Path to the .ttf font file. Defaults to 'arial.ttf'.
    - relative_font_size (float, optional): Font size as a fraction of image width. Defaults to 0.04.
    - vertical_position (float, optional): Vertical start position of the text block as a fraction of image height. Defaults to 0.10.
    - line_spacing (float, optional): Space between lines of text, as a multiplier of the font size. Defaults to 1.0.
    """
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Calculate font size relative to the image width
    font_size = int(image_width * relative_font_size)
    font = ImageFont.truetype(font_path, font_size)

    # Define the maximum width for the text
    padding = 30
    max_width = image_width - 2 * padding

    # Estimate the average character width at this font size and calculate wrap width
    avg_char_width = sum(font.getsize(char)[
                         0] for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') / 52

    # Ensure wrap_width is at least 1
    wrap_width = max(1, int(max_width / avg_char_width))

    # Split the original text into paragraphs
    paragraphs = text.split('\n')

    # Wrap each paragraph and get lines
    lines = []
    for paragraph in paragraphs:
        # Adjust width based on the font size and image width
        wrapped_paragraph = textwrap.fill(paragraph, width=wrap_width)
        lines.extend(wrapped_paragraph.split('\n'))

    # Calculate the starting y position based on the vertical_position parameter
    total_text_height = (font.getsize(lines[0])[1] + line_spacing) * len(lines)
    y_position = image_height * vertical_position - total_text_height / 2

    # Calculate the color of the font based on the image and the outline color
    contrast_color = get_binary_contrast_color(image_path)
    opposite_color = get_opposite_color(contrast_color)
    outline_width = 1

    # Draw the wrapped text, line by line
    for line in lines:
        # Calculate horizontal position to center the text
        text_width, line_height = draw.textsize(line, font=font)
        x_position = (image_width - text_width) / 2
        # draw.text((x_position, y_position), line,
        #           font=font, fill=contrast_color)
        draw_text_with_outline(
            draw, line, (x_position, y_position), font, contrast_color, opposite_color, outline_width)
        y_position += line_height + line_spacing  # Adjust line spacing if necessary

    # Save the modified image
    image.save(save_path)


def add_text_to_image_with_outline(
    image_path,
    save_path,
    text,
    font_path='arial.ttf',
    color="white",
    relative_font_size=0.04,
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
    padding = 50  # Padding inside the rectangle for text
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
        # draw.text((x_position, y_position), line,
        #           font=font, fill=color)
        draw_text_with_outline(
            draw, line, (x_position, y_position), font, color, outline_color, outline_width)

        # Move to the next line, adding padding between lines
        y_position += line_height + padding

    # Save the modified image
    image.save(save_path)


def get_binary_contrast_color(image_path):
    # Load the image
    image = Image.open(image_path)

    # Calculate the dimensions of the top 50%
    width, height = image.size
    top_half = image.crop((0, 0, width, height // 2))

    # Convert the top half to a numpy array to calculate the average color
    np_top_half = np.array(top_half)
    average_color = np_top_half.mean(axis=(0, 1))

    # Calculate the grayscale equivalent of the average color
    grayscale = int(
        0.299 * average_color[0] + 0.587 * average_color[1] + 0.114 * average_color[2])

    # Determine if the grayscale equivalent is closer to black or white
    # and then choose the opposite color. A common threshold is 128 (the middle of 0-255).
    if grayscale > 128:
        return (0, 0, 0)  # black
    else:
        return (255, 255, 255)  # white


def get_opposite_color(color_tuple):
    # Invert each color component (255 - component value) to get the opposite color
    opposite_color = tuple(255 - value for value in color_tuple)
    return opposite_color


def draw_text_with_outline(draw, text, position, font, text_color, outline_color, outline_width):
    x, y = position
    # Draw outline in all directions
    for i in range(-outline_width, outline_width + 1):
        for j in range(-outline_width, outline_width + 1):
            if i != 0 or j != 0:  # to avoid drawing the text color in the outline loop
                draw.text((x + i, y + j), text, font=font, fill=outline_color)
    # Draw the main text
    draw.text(position, text, font=font, fill=text_color)


def draw_text_with_thin_outline(draw, text, position, font, text_color, outline_color, outline_width):
    x, y = position

    # Create a temporary image for drawing the outline
    temp_image = Image.new('RGBA', draw.im.size, (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)

    # Draw text outline by drawing the text in the outline color, slightly larger than the text itself
    temp_draw.text((x - outline_width, y - outline_width),
                   text, font=font, fill=outline_color)
    temp_draw.text((x + outline_width, y - outline_width),
                   text, font=font, fill=outline_color)
    temp_draw.text((x - outline_width, y + outline_width),
                   text, font=font, fill=outline_color)
    temp_draw.text((x + outline_width, y + outline_width),
                   text, font=font, fill=outline_color)

    # Blur the temporary image to create a thin outline effect
    temp_image = temp_image.filter(
        ImageFilter.GaussianBlur(radius=outline_width))

    # Paste the blurred outline onto the original image
    draw.im.paste(temp_image, (0, 0), temp_image)

    # Draw the main text over the outline
    draw.text(position, text, font=font, fill=text_color)


def extend_image_upwards(
    image_path,
    save_path,
    extension_height=100  # The number of pixels to extend upwards
):
    # Load the image
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Define the rectangle's height at the top of the image to be replicated
    rect_height = extension_height  # The height of the rectangle to replicate

    # Crop the rectangle from the top of the image
    top_rectangle = image.crop((0, 0, image_width, rect_height))

    # Create a new blank image with the same width and increased height
    new_height = image_height + extension_height
    new_image = Image.new('RGB', (image_width, new_height))

    # Paste the top rectangle repeatedly to fill the extended area
    for i in range(0, extension_height, rect_height):
        new_image.paste(top_rectangle, (0, i))

    # Paste the original image below the extended area
    new_image.paste(image, (0, extension_height))

    # Save the modified image
    new_image.save(save_path)


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

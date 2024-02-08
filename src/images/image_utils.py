import os
import cv2
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Image.MAX_IMAGE_PIXELS = None


def add_text_to_image(image_path, save_path, text, font_path='arial.ttf', color="white", relative_font_size=0.05):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size

    # Calculate font size relative to the image width
    font_size = int(image_width * relative_font_size)

    # Define the rectangle area for text: top 30% of the image
    rect_height = int(image_height * 0.3)
    padding = 20  # Padding inside the rectangle for text

    # Load or set the default font
    font = ImageFont.truetype(font_path, font_size)

    # Define the maximum width for the text
    max_width = image_width - 2 * padding

    # Estimate the average character width at this font size and calculate wrap width
    avg_char_width = sum(font.getsize(char)[
                         0] for char in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') / 52
    # Ensure wrap_width is at least 1
    wrap_width = max(1, int(max_width / avg_char_width))

    # Wrap the text to fit into the rectangle
    wrapped_text = textwrap.fill(text, width=wrap_width)

    # Calculate the starting y position to ensure text is within the top 30%
    lines = wrapped_text.split('\n')
    text_height = sum([font.getsize(line)[1]
                      for line in lines]) + padding * (len(lines) - 1)
    y_position = padding if rect_height > text_height else (
        rect_height - text_height) / 2

    # Draw the wrapped text
    for line in lines:
        # Calculate horizontal position to center the text
        text_width, line_height = draw.textsize(line, font=font)
        x_position = (image_width - text_width) / 2
        draw.text((x_position, y_position), line, font=font, fill=color)
        # Move to the next line, adding padding between lines
        y_position += line_height + padding

    # Save the modified image
    image.save(save_path)


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

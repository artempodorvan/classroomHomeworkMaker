from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random
import os

def generate_handwritten_image(text, output_path="handwritten_output.png"):
    # Load a handwritten font
    try:
        font = ImageFont.truetype("Corinthia.ttf", 48)
    except IOError:
        font = ImageFont.load_default()

    # Set image size (notebook size in grid paper style)
    img_width = 600
    img_height = 800
    img = Image.new('RGB', (img_width, img_height), color=(247, 247, 247 ))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Create grid lines like notebook paper (в клітинку)
    cell_size = 25
    for y in range(0, img.height, cell_size):
        draw.line((0, y, img.width, y), fill=(137, 207, 240), width=1)
    for x in range(0, img.width, cell_size):
        draw.line((x, 0, x, img.height), fill=(137, 207, 240), width=1)

    # Draw the red margin line on the left side
    margin_x = 60
    draw.line((img_width - 75, 0, img_width - 75, img_height), fill=(255, 0, 0), width=3)

    # Split text to fit within the width of the notebook paper
    max_width = img_width - 80  # Adjust for margin (60px) and right-side padding
    lines = []
    words = text.split(' ')
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_bbox = draw.textbbox((0, 0), test_line, font=font)
        test_width = test_bbox[2] - test_bbox[0]
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))  # Add the last line

    # Draw text on the image
    y_text = 20
    for line in lines:
        draw.text((10, y_text), line, font=font, fill=(10, 30, 191))
        # Calculate line height using textbbox to determine the correct spacing
        line_height = draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1]
        y_text += line_height + 10  # Line spacing

    # Apply filters to mimic handwriting effects
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

    # Save the notebook paper image
    img.save(output_path)
    print(f"Handwritten paper saved as {output_path}")
    return img

def place_paper_on_table(paper_image, table_image_path, folder_name, file_name="final_img.png"):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    output_path = os.path.join(folder_name, file_name)
    # Load the table image
    table_image = Image.open(table_image_path)

    # Resize the table image to be larger than the paper image
    table_image = table_image.resize((max(paper_image.width + random.randint(250, 350), table_image.width),
                                      max(paper_image.height + random.randint(250, 350), table_image.height)))

    # Calculate position to center the paper on the table
    table_width, table_height = table_image.size
    paper_width, paper_height = paper_image.size
    x_offset = (table_width - paper_width) // 2
    y_offset = (table_height - paper_height) // 2

    # Paste the paper image onto the table image using transparency to preserve the text
    table_image.paste(paper_image, (x_offset, y_offset))

    # Save the final composite image
    table_image.save(output_path)
    print(f"Final image saved as {output_path}")

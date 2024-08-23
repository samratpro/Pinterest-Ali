import os
from constants import *
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import csv
from random import randint
import glob
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Font and color constants
title_font_size = 60
title_top_margin = 130
title_font_cut = 30
post_font_size = 40
rectangle_color_1 = '#f6dcd3'
rectangle_color_2 = '#d8e8ce'
rectangle_radius = 30
ellipse_color_1 = '#d8e8ce'
ellipse_color_2 = '#f6dcd3'
bottom_section = True
bottom_text = '🔥 All-in-one Solution In The Link ➡️ 🔥'

def check_csv_delimiter(file_path):
    with open(file_path, 'r') as file:
        first_line = file.readline().strip()
        if ',' in first_line:
            return ','
        elif ';' in first_line:
            return ';'
        else:
            return ','

def open_data(folder_name):
    file_path = READY / folder_name / 'data.csv'
    delimiter = check_csv_delimiter(file_path)

    with open(file_path, "r", newline="") as data:
        heading = next(data)
        reader = csv.reader(data, delimiter=delimiter)

        for row in reader:
            create_image(row, folder_name)

def get_font(font_path, font_size):
    return ImageFont.truetype(font_path, font_size)

def get_multiline_text_size(draw, text, font):
    lines = text.split('\n')
    width = max(draw.textbbox((0, 0), line, font=font)[2] for line in lines)
    height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines)
    return width, height

def create_image(row, folder_name):
    # Font paths
    font_title_path = READY / folder_name / 'assets' / 'fonts' / 'title_font.ttf'
    font_post_path = READY / folder_name / 'assets' / 'fonts' / 'post_font.otf'

    # Font initialization
    font_title = get_font(str(font_title_path), title_font_size)
    font_post = get_font(str(font_post_path), post_font_size)

    # Image setup
    im = Image.new('RGBA', (1000, 1500))
    width, height = im.size

    # Background image
    images_path = READY / folder_name / 'assets' / 'bg' / '*.png'
    images = glob.glob(str(images_path))
    img = images[randint(0, len(images) - 1)]
    img_open = Image.open(img)
    im.paste(img_open, (0, 0))

    # Board name and title processing
    board_name = row[0]
    row.remove(row[0])

    title_color = 'black' if 'black' in img else 'white'
    draw = ImageDraw.Draw(im)

    # Title handling
    if ':' in row[0]:
        parts = row[0].split(':')
        draw.text((width / 2, title_top_margin - 15), f'{parts[0].upper()}:',
                  anchor="mb", align='center', font=font_title, fill=title_color)
        new_title = '\n'.join(parts[1].split())
    else:
        new_title = '\n'.join(row[0].split())

    draw.text((width / 2, title_top_margin), new_title.strip().upper(),
              anchor="mm", align='center', font=font_title, fill=title_color)

    # Tips section handling
    tips_number = 0
    from_top_counter = 370

    for i in row[1:]:
        tips = '\n'.join(i.split())

        # Calculate multiline text size
        size_multiline = get_multiline_text_size(draw, tips, font_post)
        offset_w = (width - size_multiline[0]) // 2
        padding_lr = 30
        padding_tb = 30

        # Draw rectangle
        shape = (offset_w - padding_lr, (from_top_counter - 35) - padding_tb,
                 offset_w + size_multiline[0] + padding_lr, (from_top_counter - 35) + size_multiline[1] + padding_tb)

        rectangle_color = rectangle_color_1 if tips_number % 2 == 0 else rectangle_color_2
        draw.rounded_rectangle(shape, fill=rectangle_color, radius=rectangle_radius)

        # Draw ellipse for numbering
        ellipse_x = offset_w - 100
        ellipse_x_right = shape[2] - 30
        ellipse_y = (from_top_counter - 35) - 70

        if tips_number % 2 == 0:
            draw.ellipse((ellipse_x, ellipse_y, ellipse_x + 100, ellipse_y + 100), fill=ellipse_color_1)
            draw.text((ellipse_x + 50, ellipse_y + 35), str(tips_number + 1),
                      font=font_post, align='center', anchor="mt", fill='black')
        else:
            draw.ellipse((ellipse_x_right, ellipse_y, ellipse_x_right + 100, ellipse_y + 100), fill=ellipse_color_2)
            draw.text((ellipse_x_right + 50, ellipse_y + 35), str(tips_number + 1),
                      font=font_post, align='center', anchor="mt", fill='black')

        # Draw tips text
        draw.multiline_text((width / 2, from_top_counter), tips,
                            font=font_post, align='center', anchor="ms", fill='black')

        # Update position for next tip
        from_top_counter += size_multiline[1] + 100
        tips_number += 1

    # Bottom section handling
    if bottom_section:
        plane_bottom = Image.new('RGB', (1000, 120), 'black')
        plane_bottom.putalpha(140)
        im.alpha_composite(plane_bottom, (0, height - 120))

        with Pilmoji(im) as pilmoji:
            pilmoji.text((100, height - 100), bottom_text.upper(),
                         font=font_title, fill='white')

    # Save the image
    images_dir = READY / folder_name / 'images'
    images_dir.mkdir(exist_ok=True)
    filename = f'{row[0]}[[{board_name}]].png'
    full_path = os.path.join(images_dir, filename)
    im.save(full_path)
    print('Image saved')

# Checking if the current module is being executed as the main script
if __name__ == '__main__':
    project_folder = 'Keto'
    open_data(project_folder)

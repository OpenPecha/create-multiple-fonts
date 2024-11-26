import os
import random
from PIL import Image, ImageDraw, ImageFont


def load_fonts(fonts_dir):
    return [os.path.join(fonts_dir, f) for f in os.listdir(fonts_dir) if f.endswith(".ttf")]


def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def create_image(width, height, background_color):
    return Image.new("RGB", (width, height), background_color)


def justify_line(draw, line, fonts, font_size, image_width, start_x, y, padding_left, padding_right):
    words = line.split()
    total_width = 0
    word_widths = []

    for word in words:
        word_width = sum(draw.textbbox((0, 0), char, font=ImageFont.truetype(random.choice(fonts), font_size))[
                         2] - draw.textbbox((0, 0), char, font=ImageFont.truetype(random.choice(fonts), font_size))[0] for char in word)
        word_widths.append(word_width)
        total_width += word_width

    spaces_to_add = len(words) - 1
    space_width = (image_width - total_width - padding_left -
                   padding_right) // spaces_to_add if spaces_to_add > 0 else 0

    x = start_x + padding_left
    for i, word in enumerate(words):
        for char in word:
            font = ImageFont.truetype(random.choice(fonts), font_size)
            bbox = draw.textbbox((0, 0), char, font=font)
            char_width = bbox[2] - bbox[0]
            draw.text((x, y), char, font=font, fill="black")
            x += char_width
        if i < spaces_to_add:
            x += space_width
    return x


def render_text(draw, text, fonts, font_size, image_width, start_x, start_y, line_spacing, padding_left, padding_right, padding_top, padding_bottom):
    lines = text.splitlines()
    y = start_y + padding_top
    for line in lines:
        x = justify_line(draw, line, fonts, font_size, image_width, start_x, y, padding_left, padding_right)
        y += line_spacing
    return y + padding_bottom


def main(fonts_dir, text_file_path, output_image_path, image_width=2400, image_height=350, font_size=50, background_color="white",  padding_left=20, padding_right=20, padding_top=20, padding_bottom=20):
    fonts = load_fonts(fonts_dir)
    text = read_text(text_file_path)
    image = create_image(image_width, image_height, background_color)
    draw = ImageDraw.Draw(image)
    line_spacing = font_size + 2
    final_y_position = render_text(draw, text, fonts, font_size, image_width, 0, 20,
                                   line_spacing, padding_left, padding_right, padding_top, padding_bottom)

    if final_y_position > image_height:
        print(f"text exceeds the image height")
        image_height = final_y_position

    image = image.resize((image_width, image_height), Image.LANCZOS)
    image.save(output_image_path)
    print(f"image saved at {output_image_path}")


if __name__ == "__main__":
    fonts_dir = "fonts"
    text_file_path = "data/txt/test.txt"
    output_image_path = "data/synt_img/derge_kangyur_1.png"
    main(fonts_dir, text_file_path, output_image_path)

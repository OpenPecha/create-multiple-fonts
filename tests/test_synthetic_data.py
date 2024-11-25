import pytest
from PIL import ImageDraw
from src.create_variant_font.synthetic_data import load_fonts, read_text, create_image, justify_line, render_text
import shutil


@pytest.fixture
def fonts_dir(tmp_path):
    font_dir = tmp_path / "fonts"
    font_dir.mkdir()

    shutil.copy("../fonts/derge_var_1.ttf", font_dir)
    shutil.copy("../fonts/derge_var_2.ttf", font_dir)

    return font_dir


@pytest.fixture
def text_file(tmp_path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("This is a test text.\nWith multiple lines.")
    return text_file


def test_load_fonts(fonts_dir):
    fonts = load_fonts(fonts_dir)
    assert len(fonts) == 2

    assert str(fonts_dir / "derge_var_1.ttf") in fonts
    assert str(fonts_dir / "derge_var_2.ttf") in fonts


def test_read_text(text_file):
    text = read_text(text_file)
    assert text == "This is a test text.\nWith multiple lines."


def test_create_image():
    image = create_image(100, 200, "white")
    assert image.size == (100, 200)
    assert image.mode == "RGB"


def test_justify_line(fonts_dir):
    fonts = load_fonts(fonts_dir)
    image = create_image(500, 100, "white")
    draw = ImageDraw.Draw(image)
    x = justify_line(draw, "This is a test", fonts, 20, 500, 0, 0, 10, 10)
    assert x > 0


def test_render_text(fonts_dir, text_file):
    fonts = load_fonts(fonts_dir)
    text = read_text(text_file)
    image = create_image(500, 200, "white")
    draw = ImageDraw.Draw(image)
    final_y = render_text(draw, text, fonts, 20, 500, 0, 0, 22, 10, 10, 10, 10)
    assert final_y > 0

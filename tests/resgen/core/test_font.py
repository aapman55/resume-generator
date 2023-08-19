import unittest

from pydantic import ValidationError

from resgen.core.font import FontStyle, Font


class TestFont(unittest.TestCase):
    def test_font_class_creation(self) -> None:
        Font(family="DummyFamily", font_style="", font_file_path="path/to/font.ttf")

    def test_font_class_creation_wrong_style(self) -> None:
        with self.assertRaises(ValidationError):
            Font(
                family="DummyFamily",
                font_style="BIG",
                font_file_path="path/to/font.ttf",
            )

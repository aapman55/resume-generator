import unittest

from resgen.core.colours import Colour
from resgen.core.document import Document
from resgen.core.style import Style, StyleRegistry, StyleNotFoundError


class TestStyle(unittest.TestCase):
    def test_style(self) -> None:
        Style(
            id="default",
            family="Helvetica",
            font_style="B",
            font_size=13,
            font_colour={"r": 0, "g": 0, "b": 0},
        )

    def test_style_activate(self) -> None:
        colour = Colour(**{"r": 0, "g": 0, "b": 0})
        style = Style(
            id="default",
            family="Helvetica",
            font_style="B",
            font_size=13,
            font_colour=colour,
        )

        doc = Document()

        style.activate(doc)

        self.assertEqual(doc.font_style, "B")
        self.assertEqual(doc.font_size_pt, 13)
        self.assertEqual(doc.font_family.lower(), "helvetica")
        self.assertEqual(doc.text_color, colour.to_device_rgb())


class TestStyleRegistry(unittest.TestCase):
    def setUp(self) -> None:
        colour = Colour(**{"r": 0, "g": 0, "b": 0})
        self.default_style = Style(
            id="default",
            family="Helvetica",
            font_style="",
            font_size=13,
            font_colour=colour,
        )

        self.special_style = Style(
            id="special",
            family="Helvetica",
            font_style="B",
            font_size=18,
            font_colour=colour,
        )

    def test_style_registry_get(self):
        reg = StyleRegistry(styles=[self.default_style, self.special_style])

        self.assertEqual(reg.get("special"), self.special_style)
        self.assertEqual(reg.get("default"), self.default_style)

        with self.assertRaises(StyleNotFoundError):
            reg.get("header")

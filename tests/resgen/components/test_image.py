import unittest
from unittest.mock import MagicMock

from resgen.components.image import RoundedProfilePicture
from resgen.core.document import Document
from tests.test_utils.dir import get_root


class TestRoundedProfilePicture(unittest.TestCase):
    def setUp(self) -> None:
        self.image_path = get_root() / "tests" / "assets" / "pig.png"

    def test_add_pdf_content(self) -> None:
        doc = Document()
        pic = RoundedProfilePicture(
            image_path=str(self.image_path),
        )

        mock_style_registry = MagicMock()

        doc.add_page()
        self.assertAlmostEqual(doc.y, 10)

        # Set the left and right margins, so we know the width
        # Since it is a circle, the width is also the height
        width = 50
        doc.set_left_margin(10)
        doc.set_right_margin(doc.w - 10 - width)

        pic.add_pdf_content(doc=doc, style_registry=mock_style_registry)

        self.assertEqual(doc.y, 10 + width)

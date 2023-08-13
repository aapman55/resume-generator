import unittest

from resgen.components.rating import draw_circle
from resgen.core.document import Document


class TestRating(unittest.TestCase):
    def test_draw_circle(self) -> None:
        doc = Document()
        doc.add_page()
        # Standaard margin van 10 mm
        self.assertAlmostEqual(doc.x, 10)

        draw_circle(doc=doc, spacing=10, filled=True)

        # 10 + spacing van 10
        self.assertAlmostEqual(doc.x, 20)
        draw_circle(doc=doc, spacing=10, filled=False)
        self.assertAlmostEqual(doc.x, 30)

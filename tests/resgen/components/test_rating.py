import unittest

from pydantic import ValidationError

from resgen.components.rating import (
    draw_circle,
    CircleRating,
    CIRCLE_TO_FONT_SIZE_RATIO,
    TitledCircleRatingList,
)
from resgen.core.document import Document
from resgen.core.page_settings import SideBar
from resgen.core.style import StyleRegistry


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


class TestCircleRating(unittest.TestCase):
    def setUp(self) -> None:
        self.style_registry = StyleRegistry(
            styles=[
                {
                    "id": "default",
                    "family": "helvetica",
                },
            ]
        )

    def test_init(self):
        CircleRating(rating=3, rating_text="dummy_rating", rating_text_style="default")

    def test_init_invalid_rating(self):
        with self.assertRaises(ValueError):
            """
            rating total smaller than rating
            """
            CircleRating(
                rating_total=2,
                rating=3,
                rating_text="dummy_rating",
                rating_text_style="default",
            )

        with self.assertRaises(ValidationError):
            """
            Rating smaller than 0
            """
            CircleRating(
                rating=-1, rating_text="dummy_rating", rating_text_style="default"
            )

        with self.assertRaises(ValidationError):
            """
            rating_total equal to 0
            """
            CircleRating(
                rating_total=0,
                rating=0,
                rating_text="dummy_rating",
                rating_text_style="default",
            )

    def test_add_pdf_content(self) -> None:
        doc = Document()
        doc.add_page()
        rating = CircleRating(
            rating=3, rating_text="dummy_rating", rating_text_style="default"
        )

        self.assertAlmostEqual(doc.y, 10)

        rating.add_pdf_content(doc=doc, style_registry=self.style_registry)

        adjust_y_for_circle_size = (1 - CIRCLE_TO_FONT_SIZE_RATIO) / 2 * doc.font_size
        self.assertAlmostEqual(
            doc.y,
            # Starting point
            10
            # dummy_rating does not fit on 1 line, so extra line
            + doc.font_size
            # Reposition due to circle size
            + adjust_y_for_circle_size
            # This one is after the circles
            + doc.font_size,
        )

    def test_add_pdf_content_multi_line_circles(self) -> None:
        width = 50
        sidebar = SideBar(
            width=width,
            align_left=True,
        )
        doc = Document(sidebar=sidebar)
        doc.add_page()
        rating = CircleRating(
            rating_total=15,
            rating=7,
            rating_text="dummy_rating",
            rating_text_style="default",
        )
        doc.switch_to_sidebar()
        self.assertAlmostEqual(doc.y, 10)

        rating.add_pdf_content(doc=doc, style_registry=self.style_registry)

        adjust_y_for_circle_size = (1 - CIRCLE_TO_FONT_SIZE_RATIO) / 2 * doc.font_size
        self.assertAlmostEqual(
            doc.y,
            # Starting point
            10
            # dummy_rating does not fit on 1 line, so extra line
            + doc.font_size
            # Reposition due to circle size
            + adjust_y_for_circle_size
            # circles fit on 3 lines so 2 extra font_size
            + doc.font_size * 2
            # This one is after the circles
            + doc.font_size,
        )


class TestTitledCircleRatingList(unittest.TestCase):
    def setUp(self) -> None:
        self.style_registry = StyleRegistry(
            styles=[
                {
                    "id": "default",
                    "family": "helvetica",
                },
            ]
        )

    def test_add_pdf_content(self) -> None:
        doc = Document()
        rating = TitledCircleRatingList(
            title="dummy title",
            title_style="default",
            rating_total=5,
            rating_text_style="default",
            rating_text_width=25,
            ratings=[
                {
                    "rating_text": "rating1",
                    "rating": 3,
                },
                {
                    "rating_text": "rating2",
                    "rating": 3,
                },
            ],
        )

        doc.add_page()

        self.assertAlmostEqual(doc.y, 10)
        rating.add_pdf_content(doc=doc, style_registry=self.style_registry)

        adjust_y_for_circle_size = (1 - CIRCLE_TO_FONT_SIZE_RATIO) / 2 * doc.font_size

        self.assertAlmostEqual(
            doc.y,
            # Starting point
            10
            # title
            + doc.font_size
            # Reposition due to circle size
            + adjust_y_for_circle_size * len(rating.ratings)
            # This one is after the circles
            + doc.font_size * len(rating.ratings),
        )

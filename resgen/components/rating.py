from pydantic import Field

from resgen.core.colours import Colour
from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry

CIRCLE_TO_FONT_SIZE_RATIO = 0.7


class CircleRating(Component):
    rating_total: int = Field(5, description="The total amount of points to be given")
    rating: int = Field(..., description="The amount of points given")
    rating_color: Colour = Field(
        Colour.white(), description="Color of the rating symbols"
    )
    rating_text: str = Field(..., description="What is the rating about")
    rating_text_style: str = Field(..., description="Style of the rating text")
    line_width: int = Field(
        2, description="Line width. X times the default width of 0.2 mm"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        style_registry.get(self.rating_text_style).activate(doc)

        doc.cell(
            w=20,
            txt=self.rating_text,
        )

        doc.set_line_width(0.2 * self.line_width)
        doc.set_draw_color(self.rating_color.to_device_rgb())
        doc.set_fill_color(self.rating_color.to_device_rgb())

        # Center the circles
        doc.set_xy(
            x=doc.x,
            y=doc.y + (1 - CIRCLE_TO_FONT_SIZE_RATIO) / 2 * doc.font_size,
        )

        for _ in range(self.rating):
            draw_filled_circle(doc)

        for _ in range(self.rating_total - self.rating):
            draw_empty_circle(doc)


def draw_filled_circle(doc: Document) -> None:
    doc.circle(
        x=doc.x,
        y=doc.y,
        r=doc.font_size * CIRCLE_TO_FONT_SIZE_RATIO,
        style="FD",
    )
    doc.set_x(doc.x + doc.font_size)


def draw_empty_circle(doc: Document) -> None:
    doc.circle(
        x=doc.x,
        y=doc.y,
        r=doc.font_size * CIRCLE_TO_FONT_SIZE_RATIO,
        style="D",
    )
    doc.set_x(doc.x + doc.font_size)

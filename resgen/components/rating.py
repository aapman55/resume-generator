import math

from fpdf import YPos
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
    rating_text_width: float = Field(
        25, description="Width of box for description. Default is 25 mm."
    )
    line_width: int = Field(
        2, description="Line width. X times the default width of 0.2 mm"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        style_registry.get(self.rating_text_style).activate(doc)

        doc.multi_cell(
            w=self.rating_text_width,
            txt=self.rating_text,
            new_y=YPos.LAST,
        )

        doc.set_line_width(0.2 * self.line_width)
        doc.set_draw_color(self.rating_color.to_device_rgb())
        doc.set_fill_color(self.rating_color.to_device_rgb())

        # Center the circles
        doc.set_xy(
            x=doc.x,
            y=doc.y + (1 - CIRCLE_TO_FONT_SIZE_RATIO) / 2 * doc.font_size,
        )

        r_margin_x = doc.w - doc.r_margin
        available_drawing_space = r_margin_x - doc.x
        circles_per_row = math.floor(available_drawing_space / doc.font_size)

        # move x such that most right circle is at the margin
        left_x_circles = (
            r_margin_x
            - circles_per_row * doc.font_size
            + (1 - CIRCLE_TO_FONT_SIZE_RATIO) * doc.font_size
        )
        doc.x = left_x_circles
        row_counter = 1

        for _ in range(self.rating):
            if row_counter > circles_per_row:
                row_counter = 1
                doc.x = left_x_circles
                doc.y += doc.font_size

            draw_filled_circle(doc, doc.font_size)
            row_counter += 1

        for _ in range(self.rating_total - self.rating):
            if row_counter > circles_per_row:
                row_counter = 1
                doc.x = left_x_circles
                doc.y += doc.font_size

            draw_empty_circle(doc, doc.font_size)
            row_counter += 1


def draw_filled_circle(doc: Document, spacing: float) -> None:
    doc.circle(
        x=doc.x,
        y=doc.y,
        r=doc.font_size * CIRCLE_TO_FONT_SIZE_RATIO,
        style="FD",
    )
    doc.set_x(doc.x + spacing)


def draw_empty_circle(doc: Document, spacing: float) -> None:
    doc.circle(
        x=doc.x,
        y=doc.y,
        r=doc.font_size * CIRCLE_TO_FONT_SIZE_RATIO,
        style="D",
    )
    doc.set_x(doc.x + spacing)

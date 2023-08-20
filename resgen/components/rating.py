"""
Module for rating components.
"""
import copy
import math
from typing import List

from fpdf import YPos, XPos
from pydantic import Field, BaseModel, root_validator

from resgen.core.colours import Colour
from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry

CIRCLE_TO_FONT_SIZE_RATIO = 0.7


class RatingListContents(BaseModel):
    """
    Used for pydantic input validation
    """

    rating: int = Field(..., description="The amount of points given", ge=0)
    rating_text: str = Field(..., description="What is the rating about")


class TitledCircleRatingList(Component):
    """
    Component that contains a list of ratings. The rating is
    shown as filled circles. If it is not a full rating the rest of
    the circles are just an outline.
    """

    title: str = Field(..., description="Title for the rating list")
    title_style: str = Field(..., description="Style for the title")
    rating_total: int = Field(
        5, description="The total amount of points to be given", gt=0
    )
    rating_color: Colour = Field(
        Colour.white(), description="Color of the rating symbols"
    )
    rating_text_style: str = Field(..., description="Style of the rating text")
    rating_text_width: float = Field(
        25, description="Width of box for description. Default is 25 mm."
    )
    line_width: int = Field(
        2, description="Line width. X times the default width of 0.2 mm"
    )
    ratings: List[RatingListContents] = Field(
        ..., description="List of ratings with description"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        style_registry.get(self.title_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.title,
            new_x=XPos.LMARGIN,
        )

        common_config = copy.deepcopy(self.dict())
        #  Remove the ratings
        common_config.pop("ratings")

        remove_margins_config = {
            "left_padding": 0,
            "right_padding": 0,
            "bottom_padding": 0,
            "top_padding": 0,
        }
        common_config.update(remove_margins_config)

        for rating in self.ratings:
            CircleRating(
                **common_config,
                rating=rating.rating,
                rating_text=rating.rating_text,
            ).build(doc=doc, style_registry=style_registry)


class CircleRating(Component):
    """
    Component that contains a single rating. The rating is
    shown as filled circles. If it is not a full rating the rest of
    the circles are just an outline.
    """

    rating_total: int = Field(
        5, description="The total amount of points to be given", gt=0
    )
    rating: int = Field(..., description="The amount of points given", ge=0)
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

    @root_validator
    def validate_rating_not_larger_than_total(cls, values):
        """
        This validator makes sure that the total ratings is a higher number
        than the rating.
        :param values:
        :return:
        """
        rating = values.get("rating")
        rating_total = values.get("rating_total")
        if rating > rating_total:
            raise ValueError(
                f"The value of the rating is larger than the total. ('{rating}' > '{rating_total}')"
            )

        return values

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
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

            draw_circle(doc=doc, spacing=doc.font_size, filled=True)
            row_counter += 1

        for _ in range(self.rating_total - self.rating):
            if row_counter > circles_per_row:
                row_counter = 1
                doc.x = left_x_circles
                doc.y += doc.font_size

            draw_circle(doc=doc, spacing=doc.font_size, filled=False)
            row_counter += 1

        # Reset x and y ready for the next component
        doc.ln(doc.font_size)


def draw_circle(doc: Document, spacing: float, filled: bool = True) -> None:
    """
    Draw circle at current position and move to the next x position
    :param doc:
    :param spacing:
    :param filled:
    :return:
    """
    doc.circle(
        x=doc.x,
        y=doc.y,
        r=doc.font_size * CIRCLE_TO_FONT_SIZE_RATIO,
        style="FD" if filled else "D",
    )
    doc.set_x(doc.x + spacing)

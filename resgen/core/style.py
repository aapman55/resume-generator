"""
This module contains all classes that are related to Styles
"""

from typing import List

from pydantic import BaseModel, Field

from resgen.core.colours import Colour
from resgen.core.document import Document
from resgen.core.font import FontStyle


class StyleNotFoundError(Exception):
    """Custom exception when a style was not found"""


class Style(BaseModel):
    """
    A style is the combination of font family, style (Italic, Bold ,regular),
    size and colour. This pre-defined combination is given an id that can
    be referenced in the components.

    By pre-defining styles it is easier to keep a more uniform configuration and
    also easier to change multiple components at once.
    """

    id: str = Field(
        ...,
        description="Identifier that will be used in components to locate the style",
    )
    family: str = Field(
        ..., description="Name of the font, needs to correspond to a registered font"
    )
    font_style: FontStyle = Field(
        FontStyle.REGULAR, description="Regular, Bold or Italic"
    )
    font_size: int = Field(12, description="Size of the font")
    font_colour: Colour = Field(Colour.black(), description="Colour of the text")

    def activate(self, document: Document) -> None:
        """
        Set this style
        :param document: A resgen Document class
        :return:
        """
        document.set_text_color(self.font_colour.to_device_rgb())
        document.set_font(
            family=self.family,
            style=self.font_style.value,
            size=self.font_size,
        )


class StyleRegistry(BaseModel):
    """
    This class is for storing all the Styles
    It also contains a method for retrieval
    """

    styles: List[Style] = Field(..., description="List of styles")

    def get(self, style_id: str) -> Style:
        """
        Retrieve a Style based on the id
        :param style_id:
        :return: Style
        """
        for style in self.styles:
            if style.id == style_id:
                return style

        raise StyleNotFoundError(f"The style {style_id} could not be found!")

from typing import List

from pydantic import BaseModel, Field

from resgen.core.colours import Colour
from resgen.core.document import Document
from resgen.core.font import FontStyle


class StyleNotFoundError(Exception):
    """Custom exception when a style was not found"""


class Style(BaseModel):
    id: str = Field(..., description="Identifier that will be used in components to locate the style")
    family: str = Field(..., description="Name of the font, needs to correspond to a registered font")
    font_style: FontStyle = Field(FontStyle.REGULAR, description="Regular, Bold or Italic")
    font_size: int = Field(12, description="Size of the font")
    font_colour: Colour = Field(Colour.black(), description="Colour of the text")

    def activate(self, document: Document) -> None:
        document.set_text_color(self.font_colour.to_device_rgb())
        document.set_font(
            family=self.family,
            style=self.font_style.value,
            size=self.font_size,
        )


class StyleRegistry(BaseModel):
    styles: List[Style] = Field(..., description="List of styles")

    def get(self, style_id: str) -> Style:
        for style in self.styles:
            if style.id == style_id:
                return style

        raise StyleNotFoundError(f"The style {style_id} could not be found!")

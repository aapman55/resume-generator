from enum import Enum
from pydantic import BaseModel, Field


class FontStyle(Enum):
    BOLD = "B"
    ITALIC = "I"
    REGULAR = ""


class Font(BaseModel):
    family: str = Field(..., description="Name of the font, can be chosen freely.")
    font_style: FontStyle = Field(
        FontStyle.REGULAR, description="Regular, Bold or Italic"
    )
    font_file_path: str = Field(..., description="Path to the font file")

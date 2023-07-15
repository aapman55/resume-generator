from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from resgen.core.colours import Colour


class PaperSize(Enum):
    A4 = "A4"


class Orientation(Enum):
    LANDSCAPE: str = "LANDSCAPE"
    PORTRAIT: str = "PORTRAIT"


class SideBar(BaseModel):
    width: int = Field(40, description="Width of the sidebar in mm")
    fill_colour: Colour = Field(
        Colour.white(), description="Background color of the sidebar"
    )
    align_left: bool = Field(
        default=True, description="If Ture aligns left, otherwise right."
    )


class PageSettings(BaseModel):
    papersize: PaperSize = Field(default=PaperSize.A4)
    orientation: Orientation = Field(default=Orientation.PORTRAIT)
    sidebar: Optional[SideBar] = Field(default=None, description="Define sidebar")

    class Config:
        arbitrary_types_allowed = True

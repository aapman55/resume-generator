"""
Module for page related configurations
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from resgen.core.colours import Colour


class PaperSize(Enum):
    """
    Used to restrict the input and validation for Pydantic
    """

    A4 = "A4"


class Orientation(Enum):
    """
    Used to restrict the input and validation for Pydantic
    """

    LANDSCAPE: str = "LANDSCAPE"
    PORTRAIT: str = "PORTRAIT"


class SideBar(BaseModel):
    """
    Definition for the sidebar
    """

    width: int = Field(40, description="Width of the sidebar in mm")
    fill_colour: Colour = Field(
        Colour.white(), description="Background color of the sidebar"
    )
    align_left: bool = Field(
        default=True, description="If Ture aligns left, otherwise right."
    )


class PageSettings(BaseModel):
    """
    Defines the configuration of the pages
    """

    papersize: PaperSize = Field(default=PaperSize.A4)
    orientation: Orientation = Field(default=Orientation.PORTRAIT)
    sidebar: Optional[SideBar] = Field(default=None, description="Define sidebar")

    class Config:
        """
        Needed to supress warning
        """

        arbitrary_types_allowed = True

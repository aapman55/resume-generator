"""
Module for colours
"""
from __future__ import annotations
from typing import Optional

from fpdf.drawing import DeviceRGB
from pydantic import BaseModel, Field


class Colour(BaseModel):
    """
    Used as helper and validator for input with pydantic
    """

    r: int = Field(..., description="RED", ge=0, le=255)
    g: int = Field(..., description="GREEN", ge=0, le=255)
    b: int = Field(..., description="BLUE", ge=0, le=255)
    a: Optional[float] = Field(None, description="ALFA", ge=0, le=1)

    def to_device_rgb(self) -> DeviceRGB:
        """
        Creates a FPDF colour class.
        :return:
        """
        return DeviceRGB(
            r=self.r / 255.0,
            g=self.g / 255.0,
            b=self.b / 255.0,
            a=self.a / 255.0 if self.a else self.a,
        )

    @classmethod
    def white(cls) -> Colour:
        """
        Convenience method for the color white.
        Used in defaults of components.
        :return:
        """
        return cls(r=255, g=255, b=255)

    @classmethod
    def black(cls) -> Colour:
        """
        Convenience method for the color white.
        Used in defaults of components.
        :return:
        """
        return cls(r=0, g=0, b=0)

from __future__ import annotations

from fpdf.drawing import DeviceRGB
from pydantic import BaseModel, Field


class Colour(BaseModel):
    r: int = Field(..., description="RED", ge=0, le=255)
    g: int = Field(..., description="GREEN", ge=0, le=255)
    b: int = Field(..., description="BLUE", ge=0, le=255)
    a: float = Field(None, description="ALFA", ge=0, le=1)

    def to_device_rgb(self) -> DeviceRGB:
        return DeviceRGB(
                r=self.r/255.0,
                g=self.g/255.0,
                b=self.b/255.0,
                a=self.a/255.0 if self.a else self.a,
        )

    @classmethod
    def white(cls) -> Colour:
        return cls(r=255, g=255, b=255)

    @classmethod
    def black(cls) -> Colour:
        return cls(r=0, g=0, b=0)

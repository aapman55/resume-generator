from __future__ import annotations
from pydantic import BaseModel, Field


class FillColour(BaseModel):
    r: int = Field(..., description="RED", ge=0, le=255)
    g: int = Field(..., description="GREEN", ge=0, le=255)
    b: int = Field(..., description="BLUE", ge=0, le=255)

    @classmethod
    def white(cls) -> FillColour:
        return cls(r=255, g=255, b=255)

from __future__ import annotations
from pydantic import BaseModel, Field

from resgen.core.document import Document


class FillColour(BaseModel):
    r: int = Field(..., description="RED", ge=0, le=255)
    g: int = Field(..., description="GREEN", ge=0, le=255)
    b: int = Field(..., description="BLUE", ge=0, le=255)

    def set_fill_colour(self, document: Document):
        document.set_fill_color(
            self.r, self.g, self.b
        )

    @classmethod
    def white(cls) -> FillColour:
        return cls(r=255, g=255, b=255)

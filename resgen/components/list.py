from typing import List

from fpdf import XPos
from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class TitledList(Component):
    title: str = Field(..., description="Title of the list")
    title_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )
    list_values: List[str] = Field(..., description="Contents of the list")
    list_values_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        # Title
        style_registry.get(self.title_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.title,
            new_x=XPos.LEFT,
        )

        # List values
        style_registry.get(self.list_values_style).activate(doc)
        for val in self.list_values:
            doc.multi_cell (
                w=0,
                txt=val,
                new_x=XPos.LEFT,
            )


from typing import List, Dict

from fpdf import XPos, Align, YPos
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
            doc.multi_cell(
                w=0,
                txt=val,
                new_x=XPos.LEFT,
            )


class TitledKeyValueList(Component):
    title: str = Field(..., description="Title of the list")
    title_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )
    key_values: Dict[str, str] = Field(
        ..., description="Contents of the key value pairs"
    )
    key_values_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        style_registry.get(self.title_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.title,
            new_x=XPos.LEFT,
        )

        # List values
        style_registry.get(self.key_values_style).activate(doc)
        available_width = doc.w - doc.l_margin - doc.r_margin
        for k, v in self.key_values.items():
            # cell size wraps around content
            doc.cell(
                txt=k,
                align=Align.L,
            )
            # cell size extends to end
            # next cell will start at the left margin
            # next cell will start on a new line
            doc.multi_cell(
                w=0,
                txt=v,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
                align=Align.R,
            )

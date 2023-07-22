from fpdf import XPos
from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class Experience(Component):
    title: str = Field(..., description="Job description")
    experience_start: str = Field(..., description="Begin date")
    experience_end: str = Field("Present", description="End date")
    description: str = Field(..., description="What did you do")

    text_style: str = Field(..., description="Reference to the registered style_id")

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        style_registry.get(self.text_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.title,
            new_x=XPos.LEFT,
            fill=True if self.fill_colour else False,
        )
        doc.multi_cell(w=0, txt=self.experience_start, new_x=XPos.LEFT)
        doc.multi_cell(w=0, txt=self.experience_end, new_x=XPos.LEFT)
        doc.multi_cell(w=0, txt=self.description, new_x=XPos.LEFT)

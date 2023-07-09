from fpdf import XPos
from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document


class Experience(Component):
    title: str = Field(..., description="Job description")
    experience_start: str = Field(... , description="Begin date")
    experience_end: str = Field("Present", description="End date")
    description: str = Field(..., description="What did you do")

    def add_pdf_content(self, pdf: Document):
        pdf.multi_cell(w=0, txt=self.title, new_x=XPos.LEFT)
        pdf.multi_cell(w=0, txt=self.experience_start, new_x=XPos.LEFT)
        pdf.multi_cell(w=0, txt=self.experience_end, new_x=XPos.LEFT)
        pdf.multi_cell(w=0, txt=self.description, new_x=XPos.LEFT)




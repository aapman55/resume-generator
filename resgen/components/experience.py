from fpdf import FPDF
from pydantic import Field

from resgen.components.component import Component


class Experience(Component):
    start_year: int = Field(..., description="Year of the start")
    start_month: int = Field(..., description="Month of the start")
    end_year: int = Field(..., description="Year of the end")
    end_month: int = Field(..., description="Month of the end")
    description: str = Field(..., description="What did you do")

    def add_pdf_content(self, pdf: FPDF):
        pass

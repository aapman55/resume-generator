from abc import ABC, abstractmethod
from enum import Enum

from fpdf import FPDF
from fpdf.enums import XPos
from pydantic import BaseModel, Field


class PaperSize(Enum):
    A4 = "a4"


class Orientation(Enum):
    LANDSCAPE: str = "LANDSCAPE"
    PORTRAIT: str = "PORTRAIT"


class PageSettings(BaseModel):
    papersize: PaperSize = Field(default=PaperSize.A4)
    orientation: Orientation = Field(default=Orientation.PORTRAIT)

    class Config:
        arbitrary_types_allowed = True

    def create_new(self) -> FPDF:
        return FPDF(
            orientation=self.orientation.value,
            format=self.papersize.value,
            unit="mm"
        )


class Document(BaseModel, ABC):
    page_settings: PageSettings = Field(..., description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def build(self):
        raise NotImplementedError()


class Resume(Document):

    def build(self) -> None:
        pdf = self.page_settings.create_new()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 16)
        pdf.set_margins(0, 0)
        for i in range(10):
            pdf.set_font("Helvetica", "", (i+1)*16)
            pdf.set_margins(left= i*2, top=0, right=0)
            pdf.multi_cell(w= 0, txt="Hello world ", border= 1, new_x= XPos.LEFT)
            print(f"{pdf.page=} {pdf.get_x()=} {pdf.get_y()=}")
        pdf.page = 1
        pdf.set_y(0)
        pdf.set_font("Helvetica", "", 16)
        pdf.set_margins(0, 0)
        for i in range(10):
            pdf.set_font("Helvetica", "", (i+1)*16)
            pdf.set_margins(left= i*2, top=0, right=0)
            pdf.multi_cell(w= 0, txt="Hallo wereld ", border= 1, new_x= XPos.LEFT)
            print(f"{pdf.page=} {pdf.get_x()=} {pdf.get_y()=}")

        pdf.output(self.output_name)


if __name__ == "__main__":
    doc = Resume(
        page_settings = PageSettings(
            orientation=Orientation.PORTRAIT,
            papersize=PaperSize.A4,
        ),
        output_name="hello_world.pdf",
    )
    doc.build()

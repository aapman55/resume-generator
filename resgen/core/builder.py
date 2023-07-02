from enum import Enum

from fpdf import XPos
from pydantic import BaseModel, Field

from resgen.core.component import init_class


class PaperSize(Enum):
    A4 = "A4"


class Orientation(Enum):
    LANDSCAPE: str = "LANDSCAPE"
    PORTRAIT: str = "PORTRAIT"


class PageSettings(BaseModel):
    papersize: PaperSize = Field(default=PaperSize.A4)
    orientation: Orientation = Field(default=Orientation.PORTRAIT)

    class Config:
        arbitrary_types_allowed = True


class DocumentBuilder(BaseModel):
    document_class_name: str = Field(default="resgen.components.document.Resume")
    page_settings: PageSettings = Field(..., description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")

    def build(self) -> None:
        document_class = init_class(self.document_class_name)
        document = document_class(
            orientation=self.page_settings.orientation.value,
            unit="mm",
            format=self.page_settings.papersize.value,
        )

        document.set_font("Helvetica", "", 16)
        document.set_margins(0, 0)
        document.add_page()
        for i in range(10):
            document.set_font("Helvetica", "", (i + 1) * 16)
            document.set_margins(left=i * 2, top=0, right=0)
            document.multi_cell(w=0, txt="Hello world ", border=1, new_x=XPos.LEFT)
            print(f"{document.page=} {document.get_x()=} {document.get_y()=}")
        # document.page = 1
        # document.set_y(0)
        document.set_font("Helvetica", "", 16)
        document.set_margins(0, 0)
        for i in range(10):
            document.set_font("Helvetica", "", (i + 1) * 16)
            document.set_margins(left=i * 2, top=0, right=0)
            document.multi_cell(w=0, txt="Hallo wereld ", border=1, new_x=XPos.LEFT)
            print(f"{document.page=} {document.get_x()=} {document.get_y()=}")

        document.output(self.output_name)


if __name__ == "__main__":
    pdf = DocumentBuilder(
        page_settings={
            "orientation": "LANDSCAPE",
            "papersize": "A4",
        },
        output_name="hello_world.pdf",
    )

    pdf.build()
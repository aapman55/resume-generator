from enum import Enum
from typing import List, Dict

from fpdf import XPos
from pydantic import BaseModel, Field

from resgen.core.component import init_class, Component, init_component
from resgen.core.document import Document


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
    document_class_name: str = Field(default="resgen.core.document.Resume")
    page_settings: PageSettings = Field(PageSettings(), description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")
    components: List[Dict] = Field(..., description="List of components of type Component")

    def build(self) -> Document:
        document_class = init_class(self.document_class_name)
        document = document_class(
            orientation=self.page_settings.orientation.value,
            unit="mm",
            format=self.page_settings.papersize.value,
        )

        document.set_font("Helvetica", "", 16)
        document.set_margins(20, 0)
        document.add_page()

        for component in self.components:
            init_component(component).build(document)

        document.output(self.output_name)

        return document


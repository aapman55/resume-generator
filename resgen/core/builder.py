from typing import List, Dict

from pydantic import BaseModel, Field

from resgen.core.component import init_class, init_component
from resgen.core.document import Document
from resgen.core.page_settings import PageSettings


class DocumentBuilder(BaseModel):
    document_class_name: str = Field(default="resgen.core.document.Resume")
    page_settings: PageSettings = Field(PageSettings(), description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")
    components: List[Dict] = Field(
        ..., description="List of components of type Component"
    )

    def build(self) -> Document:
        document_class = init_class(self.document_class_name)
        document = document_class(
            orientation=self.page_settings.orientation.value,
            unit="mm",
            format=self.page_settings.papersize.value,
            sidebar=self.page_settings.sidebar,
        )

        document.set_font("Helvetica", "", 16)
        document.add_page()
        header_height = document.get_y()

        document.switch_to_main_content()

        for component in self.components:
            init_component(component).build(document)

        if self.page_settings.sidebar:
            document.switch_to_sidebar()
            document.set_y(header_height)

            for component in self.components:
                init_component(component).build(document)

        document.output(self.output_name)

        return document

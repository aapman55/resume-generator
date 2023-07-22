from typing import List, Dict

from pydantic import BaseModel, Field

from resgen.core.component import init_class, init_component
from resgen.core.document import Document
from resgen.core.font import Font
from resgen.core.page_settings import PageSettings
from resgen.core.style import StyleRegistry


class DocumentBuilder(BaseModel):
    document_class_name: str = Field(default="resgen.core.document.Resume")
    page_settings: PageSettings = Field(PageSettings(), description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")
    components: List[Dict] = Field(
        ..., description="List of components of type Component"
    )
    style_registry: StyleRegistry = Field(..., description="Style Registry")
    custom_fonts: List[Font] = Field(
        default_factory=list, description="Custom fonts you want to register"
    )

    def register_fonts(self, doc: Document) -> None:
        for font in self.custom_fonts:
            doc.register_font(font)

    def build(self) -> Document:
        document_class = init_class(self.document_class_name)
        document = document_class(
            orientation=self.page_settings.orientation.value,
            unit="mm",
            format=self.page_settings.papersize.value,
            sidebar=self.page_settings.sidebar,
        )
        # Add custom fonts
        self.register_fonts(document)

        # document.set_font("Helvetica", "", 16)
        document.add_page()
        header_height = document.get_y()

        document.switch_to_main_content()

        for component in self.components:
            init_component(component).build(document, self.style_registry)

        if self.page_settings.sidebar:
            document.page = list(document.pages)[0]
            document.switch_to_sidebar()
            document.set_y(header_height)

            for component in self.components:
                init_component(component).build(document, self.style_registry)

        document.output(self.output_name)

        return document

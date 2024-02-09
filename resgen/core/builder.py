"""
This module contains the builder that loops
through all the components.
"""

from typing import List, Dict

from pydantic import BaseModel, Field

from resgen.core.component import init_class, init_component
from resgen.core.document import Document
from resgen.core.font import Font
from resgen.core.page_settings import PageSettings
from resgen.core.style import StyleRegistry


class DocumentBuilder(BaseModel):
    """
    This is the builder that assembles the whole pdf
    """

    document_class_name: str = Field(default="resgen.core.document.Resume")
    page_settings: PageSettings = Field(PageSettings(), description="Page settings")
    output_name: str = Field(..., description="The filename of the exported PDF.")
    components: List[Dict] = Field(
        ..., description="List of components of type Component"
    )
    sidebar_components: List[Dict] = Field(
        default_factory=list,
        description="List of components of type Component for the sidebar",
    )
    style_registry: StyleRegistry = Field(..., description="Style Registry")
    custom_fonts: List[Font] = Field(
        default_factory=list, description="Custom fonts you want to register"
    )

    def register_fonts(self, doc: Document) -> None:
        """
        Method to register custom-fonts with the FPDF class
        :param doc:
        :return:
        """
        for font in self.custom_fonts:
            doc.register_font(font)

    def build(self) -> Document:
        """
        Main assembly method
        :return:
        """
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

            for component in self.sidebar_components:
                init_component(component).build(document, self.style_registry)

        # Give a warning when sidebar_components are defined but the sidebar is not
        if self.sidebar_components and not self.page_settings.sidebar:
            print("WARNING: You have defined sidebar components but not a sidebar!")

        document.output(self.output_name)

        return document

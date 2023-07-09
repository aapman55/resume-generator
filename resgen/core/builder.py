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

    def switch_to_sidebar(self, document: Document) -> None:
        if self.page_settings.sidebar:
            if self.page_settings.sidebar.align_left:
                document.set_left_margin(0)
                document.set_right_margin(document.w - self.page_settings.sidebar.width)
            else:
                document.set_left_margin(document.w - self.page_settings.sidebar.width)
                document.set_right_margin(0)

    def draw_sidebar_background(self, document) -> None:
        top_left_x = 0
        top_left_y = 0
        if not self.page_settings.sidebar.align_left:
            top_left_x = document.w - self.page_settings.sidebar.width

        original_fill_colour = document.fill_color
        self.page_settings.sidebar.fill_colour.set_fill_colour(document)

        for page_number in document.pages.keys():
            document.page = page_number
            document.rect(
                x=top_left_x,
                y=top_left_y,
                w=self.page_settings.sidebar.width,
                h=document.h,
                style="F",  # Fill rectangle
            )

        document.set_fill_color(original_fill_colour)

    def switch_to_main_content(self, document: Document) -> None:
        if self.page_settings.sidebar:
            if self.page_settings.sidebar.align_left:
                document.set_right_margin(0)
                document.set_left_margin(self.page_settings.sidebar.width)
            else:
                document.set_right_margin(self.page_settings.sidebar.width)
                document.set_left_margin(0)

    def build(self) -> Document:
        document_class = init_class(self.document_class_name)
        document = document_class(
            orientation=self.page_settings.orientation.value,
            unit="mm",
            format=self.page_settings.papersize.value,
        )

        document.set_font("Helvetica", "", 16)
        document.add_page()
        header_height = document.get_y()

        self.switch_to_main_content(document)

        for component in self.components:
            init_component(component).build(document)

        # The assumption is that the there is fewer contents in the sidebar
        # So if we built-up the main content first. We know how much we need
        # to colour in the sidebar.
        self.draw_sidebar_background(document)

        self.switch_to_sidebar(document)
        document.set_y(header_height)

        for component in self.components:
            init_component(component).build(document)

        document.output(self.output_name)

        return document

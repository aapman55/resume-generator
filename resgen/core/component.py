import importlib
from abc import ABC, abstractmethod
from copy import deepcopy
from importlib import import_module
from typing import Dict, Any

from pydantic import BaseModel, Field

from resgen.core.colours import Colour
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class Component(BaseModel, ABC):
    top_padding: int = Field(5, description="How much space before the component in mm")
    bottom_padding: int = Field(
        5, description="How much space after the component in mm"
    )
    left_padding: int = Field(5, description="How much space after the component in mm")
    right_padding: int = Field(
        5, description="How much space after the component in mm"
    )
    fill_colour: Colour = Field(None, description="Background colour in RGB")

    def build(self, doc: Document, style_registry: StyleRegistry):
        # Save previous settings
        original_lmargin = doc.l_margin
        original_rmargin = doc.r_margin
        original_fill_colour = doc.fill_color

        # set fill colour
        if self.fill_colour:
            doc.set_fill_color(self.fill_colour.to_device_rgb())

        # Set padding
        doc.set_left_margin(original_lmargin + self.left_padding)
        doc.set_right_margin(original_rmargin + self.right_padding)
        doc.ln(self.top_padding)

        # contents
        self.add_pdf_content(doc, style_registry)

        # bottom padding
        doc.ln(self.bottom_padding)

        # restore previous settings
        doc.set_left_margin(original_lmargin)
        doc.set_right_margin(original_rmargin)
        doc.set_fill_color(original_fill_colour)

    @abstractmethod
    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        """
        To be implemented by child class
        """


def init_class(full_class_path: str) -> Any:
    import sys

    module = ".".join(full_class_path.split(".")[:-1])
    clazz = full_class_path.split(".")[-1]

    return getattr(import_module(module), clazz)


def init_component(yamlconfig: Dict) -> Component:
    yamlconfig_copy = deepcopy(yamlconfig)
    component = yamlconfig_copy.pop("component")

    return init_class(component)(**yamlconfig_copy)

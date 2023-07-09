from abc import ABC, abstractmethod
from copy import deepcopy
from importlib import import_module
from typing import Dict, Any

from fpdf import FPDF
from pydantic import BaseModel, Field

from resgen.core.document import Document


class Component(BaseModel, ABC):
    bottom_padding: int = Field(20, description="How much space after the component in mm")

    def build(self, pdf: Document):
        self.add_pdf_content(pdf)
        # margin to next component
        pdf.ln(self.bottom_padding)

    @abstractmethod
    def add_pdf_content(self, pdf: FPDF):
        ...


def init_class(full_class_path: str) -> Any:
    module = ".".join(full_class_path.split(".")[:-1])
    clazz = full_class_path.split(".")[-1]

    return getattr(import_module(module), clazz)


def init_component(yamlconfig: Dict) -> Component:
    yamlconfig_copy = deepcopy(yamlconfig)
    component = yamlconfig_copy.pop("component")

    return init_class(component)(**yamlconfig_copy)

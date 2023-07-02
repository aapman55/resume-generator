from abc import ABC, abstractmethod
from copy import deepcopy
from importlib import import_module
from typing import Dict, Any

from fpdf import FPDF
from pydantic import BaseModel


class Component(BaseModel, ABC):
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

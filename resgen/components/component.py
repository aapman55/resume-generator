from abc import ABC, abstractmethod

from fpdf import FPDF
from pydantic import BaseModel


class Component(BaseModel, ABC):
    @abstractmethod
    def add_pdf_content(self, pdf: FPDF):
        ...

"""
Module for profile related components
"""
from fpdf import XPos
from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class ProfileHeadline(Component):
    """
    This components shows your name and your job role
    """

    name: str = Field(..., description="Name of the person the resume is for")
    name_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )
    job_title: str = Field(..., description="Job title")
    job_title_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        style_registry.get(self.name_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.name,
            new_x=XPos.LEFT,
        )
        style_registry.get(self.job_title_style).activate(doc)
        doc.multi_cell(
            w=0,
            txt=self.job_title,
            new_x=XPos.LEFT,
        )


class ProfileDescription(Component):
    """
    This component contains the profile description.
    You can let it stand out by giving it a background fill and increasing the
    cell_padding.
    """

    text: str = Field(..., description="The text of your profile description.")
    cell_padding: int = Field(
        5,
        description=(
            "Padding of the entire cell. This option allows for a background colour"
            "that strectches out more."
        ),
    )
    text_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        original_c_margin = doc.c_margin

        doc.c_margin = self.cell_padding
        style_registry.get(self.text_style).activate(doc)

        self._add_vertical_margin(doc)
        doc.multi_cell(
            w=0,
            txt=self.text.strip(),
            fill=True if self.fill_colour else False,
            new_x=XPos.LEFT,
        )
        self._add_vertical_margin(doc)

        # Return settings to normal
        doc.c_margin = original_c_margin

    def _add_vertical_margin(self, doc: Document):
        """
        The cell padding does not add vertical space before and after the cell.
        To have an uniform padding, we need to add it ourselves. This is a helper
        function for that.
        :param doc:
        :return:
        """
        doc.rect(
            x=doc.x,
            y=doc.y,
            w=doc.w - doc.r_margin - doc.l_margin,
            h=self.cell_padding,
            style="F",
        )
        doc.y += self.cell_padding

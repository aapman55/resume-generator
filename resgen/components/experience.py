"""
Module for experiences
"""

from typing import List, Optional

from fpdf import XPos, Align
from pydantic import Field, BaseModel

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class Experience(BaseModel):
    """
    Common inputs for Experiences
    """

    title: str = Field(..., description="Job description")
    experience_start: str = Field(..., description="Begin date")
    experience_end: str = Field("Present", description="End date")
    description: str = Field(..., description="What did you do")
    skills_used: Optional[List[str]] = Field(
        default_factory=list, description="List of skills used during this experience."
    )

    @property
    def experience_range(self) -> str:
        """
        Convenience method to concatenate begin and end. Or to omit end if it is te same
        as the begin.
        :return:
        """
        if self.experience_start.strip() == self.experience_end.strip():
            return self.experience_start.strip()

        return f"{self.experience_start.strip()} - {self.experience_end.strip()}"


class ExperiencesDetailed(Component):
    """
    This component is meant for longer descriptions
    """

    experiences_title: str = Field(
        "Employment History", description="Title for this set of experiences"
    )
    experiences: List[Experience] = Field(..., description="List of experiences")
    experiences_title_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    begin_end_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    title_style: str = Field(..., description="Reference to the registered style_id")
    description_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    spacing_between_experiences: float = Field(
        2.0, description="Space between experiences"
    )
    spacing_between_experience_elements: float = Field(
        1.0, description="Space between elements of an experience"
    )
    skills_used_title_style: Optional[str] = Field(
        None, description="Reference to the registered style_id"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        style_registry.get(self.experiences_title_style).activate(doc)

        doc.multi_cell(
            w=0,
            txt=self.experiences_title,
            new_x=XPos.LMARGIN,
        )

        doc.ln(self.spacing_between_experience_elements)

        for experience in self.experiences:
            # Time Period
            style_registry.get(self.begin_end_style).activate(doc)
            doc.cell(
                txt=experience.experience_range,
                new_x=XPos.RIGHT,
            )

            # Title
            style_registry.get(self.title_style).activate(doc)
            doc.multi_cell(
                w=0,
                txt=experience.title,
                new_x=XPos.LMARGIN,
                align=Align.R,
            )

            doc.ln(self.spacing_between_experience_elements)

            # Description
            style_registry.get(self.description_style).activate(doc)
            doc.multi_cell(w=0, txt=experience.description, new_x=XPos.LEFT)

            # Skills
            if experience.skills_used:
                doc.ln(self.spacing_between_experience_elements)
                style_registry.get(
                    self.skills_used_title_style or self.title_style
                ).activate(doc)

                doc.cell(
                    txt="Skills used: ",
                )
                previous_font_size = doc.font_size
                style_registry.get(self.description_style).activate(doc)

                # Calculate new Y such that the bottoms coincide
                doc.set_xy(doc.x, doc.y + (previous_font_size - doc.font_size) * 0.8)
                doc.multi_cell(w=0, txt=", ".join(experience.skills_used))

            # Some padding at the end
            doc.ln(self.spacing_between_experiences)


class ExperiencesCompact(Component):
    """
    This component is meant for oneliners
    """

    experiences_title: str = Field(
        "Employment History", description="Title for this set of experiences"
    )
    experiences: List[Experience] = Field(..., description="List of experiences")
    experiences_title_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    begin_end_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    title_style: str = Field(..., description="Reference to the registered style_id")
    description_style: str = Field(
        ..., description="Reference to the registered style_id"
    )
    experience_timespan_width: float = Field(
        35.0, description="Width of the box for 'year start - year end'"
    )
    spacing_between_experiences: float = Field(
        2.0, description="Space between experiences"
    )
    spacing_between_experience_elements: float = Field(
        1.0, description="Space between elements of an experience"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        style_registry.get(self.experiences_title_style).activate(doc)

        doc.multi_cell(
            w=0,
            txt=self.experiences_title,
            new_x=XPos.LMARGIN,
        )

        doc.ln(self.spacing_between_experience_elements)

        for experience in self.experiences:
            # Time Period
            style_registry.get(self.begin_end_style).activate(doc)
            doc.cell(
                w=self.experience_timespan_width,
                txt=experience.experience_range,
                new_x=XPos.RIGHT,
            )

            # Title
            style_registry.get(self.title_style).activate(doc)
            doc.multi_cell(
                w=0,
                txt=experience.title,
                new_x=XPos.LEFT,
                align=Align.L,
            )
            retain_x = doc.x

            doc.ln(self.spacing_between_experience_elements)

            # Description
            doc.set_x(retain_x)
            style_registry.get(self.description_style).activate(doc)
            doc.multi_cell(w=0, txt=experience.description, new_x=XPos.LEFT)

            # Some padding at the end
            doc.ln(self.spacing_between_experiences)

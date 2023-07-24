from typing import List

from fpdf import XPos, YPos, Align
from pydantic import Field, BaseModel

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class Experience(BaseModel):
    title: str = Field(..., description="Job description")
    experience_start: str = Field(..., description="Begin date")
    experience_end: str = Field("Present", description="End date")
    description: str = Field(..., description="What did you do")


class ExperienceDetailed(Component):
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

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry) -> None:
        style_registry.get(self.experiences_title_style).activate(doc)
        print(f"{doc.x=}, {doc.y=}")
        doc.multi_cell(
            w=0,
            txt=self.experiences_title,
            new_x=XPos.LMARGIN,
        )

        for experience in self.experiences:
            # Time Period
            style_registry.get(self.begin_end_style).activate(doc)
            doc.cell(
                txt=f"{experience.experience_start.strip()} - {experience.experience_end.strip()}",
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

            # Description
            style_registry.get(self.description_style).activate(doc)
            doc.multi_cell(w=0, txt=experience.description, new_x=XPos.LEFT)

            # Some padding at the end
            doc.multi_cell(w=0, txt="", new_x=XPos.LEFT)

from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class RoundedProfilePicture(Component):
    image_path: str = Field(..., description="Path to the image")

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        width = doc.w - doc.l_margin - doc.r_margin
        with doc.round_clip(
            x=doc.x,
            y=doc.y,
            r=width,
        ):
            doc.image(
                name=self.image_path,
                w=width,
                keep_aspect_ratio=True,
            )

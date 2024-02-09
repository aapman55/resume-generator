"""
Module for images
"""
from pydantic import Field

from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class RoundedProfilePicture(Component):
    """
    Component for a rounded image.
    Input image does not have to be rounded.
    """

    image_path: str = Field(..., description="Path to the image")
    compress: bool = Field(
        True, description="Whether to compress the image to save space"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        """
        Draw the component specific content
        :param doc: resgen Document class
        :param style_registry: resgen StyleRegistry class
        :return:
        """
        width = doc.w - doc.l_margin - doc.r_margin
        original_image_filter = doc.image_cache.image_filter
        if self.compress:
            doc.set_image_filter("DCTDecode")

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
        doc.set_image_filter(original_image_filter)

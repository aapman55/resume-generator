from typing import List

from pydantic import Field

from resgen.core.colours import Colour
from resgen.core.component import Component
from resgen.core.document import Document
from resgen.core.style import StyleRegistry

FILL_FACTOR = 0.9


class CircleSeparatedHorizontalList(Component):
    """
    Constructs a horizontal list separated by filled circles
    """

    list_values: List[str] = Field(..., description="Contents of the list")
    list_values_style: str = Field(
        ..., description="ID of registered style in the style registry."
    )
    circle_to_font_ratio: float = Field(
        0.8, description="How large should the circle be as a ratio of the font size"
    )
    circle_fill_colour: Colour = Field(
        ..., description="Colour of the separator circles"
    )

    def add_pdf_content(self, doc: Document, style_registry: StyleRegistry):
        style_registry.get(self.list_values_style).activate(doc)
        lines = fit_list_on_lines(self.list_values, doc)

        # Backup active fill colour
        original_fill_colour = doc.fill_color

        # set circle fill colour
        doc.set_fill_color(self.circle_fill_colour.to_device_rgb())

        # Put the text and separators
        for line in lines:
            for i, value in enumerate(line):
                doc.cell(txt=value)

                #  Do not draw the circle when it is the last element on the line
                if i >= len(line) - 1:
                    continue

                # Draw circle separator
                doc.circle(
                    x=doc.x,
                    y=doc.y,
                    r=doc.font_size * self.circle_to_font_ratio,
                    style="F",
                )

                # The circle does not progress the cursors, so we do it manually
                doc.set_x(doc.x + doc.font_size * self.circle_to_font_ratio)
            # Move to the next line
            doc.ln()

        #  Recover original fill colour
        doc.set_fill_color(original_fill_colour)


def fit_list_on_lines(list_values: List[str], doc: Document) -> List[List[str]]:
    """
    Utility to fill a line with text until the line is full.
    Then move on to the next line
    """
    # Initialize line variables
    output = []
    current_line = []
    current_x = 0

    # Go through the values
    for value in list_values:
        string_width = doc.get_string_width(value)

        # If the new string does not fit on the line, start a new one
        if (current_x + string_width) > doc.content_width * FILL_FACTOR:
            output.append(current_line)
            current_line = [value]
            current_x = string_width
            continue

        # Add current string to the current line
        current_line.append(value)
        current_x += string_width

    # Add the last line to the output
    output.append(current_line)
    return output

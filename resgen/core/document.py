from abc import ABC

from fpdf import FPDF

from resgen.core.font import Font


class Document(FPDF, ABC):
    def header(self):
        pass

    def footer(self):
        pass

    def register_font(self, font: Font) -> None:
        self.add_font(
            family=font.family,
            style=font.style.value,
            fname=font.font_file_path,
        )


class Resume(Document):
    def header(self):
        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Title", border=1, align="C")
        # Performing a line break:
        self.ln(20)

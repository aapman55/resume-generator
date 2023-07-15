from abc import ABC

from fpdf import FPDF

from resgen.core.font import Font
from resgen.core.page_settings import SideBar


class Document(FPDF, ABC):
    def __init__(
        self,
        orientation: str = "portrait",
        unit: str = "mm",
        format: str = "A4",
        sidebar: SideBar = None,
    ):
        super().__init__(
            orientation=orientation,
            unit=unit,
            format=format,
        )

        self.sidebar = sidebar

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

    def switch_to_sidebar(self) -> None:
        if self.sidebar:
            if self.sidebar.align_left:
                self.set_left_margin(0)
                self.set_right_margin(self.w - self.sidebar.width)
            else:
                self.set_left_margin(self.w - self.sidebar.width)
                self.set_right_margin(0)

    def _draw_sidebar_background(self) -> None:
        top_left_x = 0
        top_left_y = 0
        if not self.sidebar.align_left:
            top_left_x = self.w - self.sidebar.width

        original_fill_colour = self.fill_color
        self.set_fill_color(
            r=self.sidebar.fill_colour.r,
            g=self.sidebar.fill_colour.g,
            b=self.sidebar.fill_colour.b,
        )

        self.rect(
            x=top_left_x,
            y=top_left_y,
            w=self.sidebar.width,
            h=self.h,
            style="F",  # Fill rectangle
        )

        self.set_fill_color(original_fill_colour)

    def switch_to_main_content(self) -> None:
        if self.sidebar:
            if self.sidebar.align_left:
                self.set_right_margin(0)
                self.set_left_margin(self.sidebar.width)
            else:
                self.set_right_margin(self.sidebar.width)
                self.set_left_margin(0)

    def add_page(
        self, orientation="", format="", same=False, duration=0, transition=None
    ):
        super().add_page(
            orientation=orientation,
            format=format,
            same=same,
            duration=duration,
            transition=transition,
        )

        if self.sidebar:
            self._draw_sidebar_background()


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

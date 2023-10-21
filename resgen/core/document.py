"""
Module for documents
"""

from abc import ABC

from fpdf import FPDF

from resgen.core.font import Font
from resgen.core.page_settings import SideBar


class Document(FPDF, ABC):
    """
    Default Document. Inherits from the class FPDF, so that we can
    make it clearer that you can add header and footer. Also, the methods
    to switch from and to a sidebar are added.
    """

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
        self.in_main_content = True

    def header(self):
        """
        If required you can create a child class and override this method
        """

    def footer(self):
        """
        If required you can create a child class and override this method
        """

    def register_font(self, font: Font) -> None:
        """
        Add custom font. ttf or otf
        :param font:
        :return:
        """
        self.add_font(
            family=font.family,
            style=font.font_style.value,
            fname=font.font_file_path,
        )

    def switch_to_sidebar(self) -> None:
        """
        Change the margins such that we draw in the sidebar area.
        Takes into account whether the sidebar is on the left or right.
        :return:
        """
        if self.sidebar:
            if self.sidebar.align_left:
                self.set_left_margin(0)
                self.set_right_margin(self.w - self.sidebar.width)
            else:
                self.set_left_margin(self.w - self.sidebar.width)
                self.set_right_margin(0)

            self.in_main_content = False

    def _draw_sidebar_background(self) -> None:
        """
        Draws a rectangle where the sidebar is.
        :return:
        """
        top_left_x = 0
        top_left_y = 0
        if not self.sidebar.align_left:
            top_left_x = self.w - self.sidebar.width

        original_fill_colour = self.fill_color

        self.set_fill_color(self.sidebar.fill_colour.to_device_rgb())

        with self.local_context(fill_opacity=self.sidebar.fill_colour.a):
            self.rect(
                x=top_left_x,
                y=top_left_y,
                w=self.sidebar.width,
                h=self.h,
                style="F",  # Fill rectangle
            )

        self.set_fill_color(original_fill_colour)

    def switch_to_main_content(self) -> None:
        """
        Change the margins such that we draw in the main area.
        Takes into account whether the sidebar is on the left or right.
        :return:
        """
        if self.sidebar:
            if self.sidebar.align_left:
                self.set_right_margin(0)
                self.set_left_margin(self.sidebar.width)
            else:
                self.set_right_margin(self.sidebar.width)
                self.set_left_margin(0)

            self.in_main_content = True

    def add_page(
        self, orientation="", format="", same=False, duration=0, transition=None
    ):
        """
        Override of the FPDF add_page method. This is so that we can draw the sidebar
        each time a page is added.
        :param orientation:
        :param format:
        :param same:
        :param duration:
        :param transition:
        :return:
        """
        # Save current settings

        super().add_page(
            orientation=orientation,
            format=format,
            same=same,
            duration=duration,
            transition=transition,
        )

        if self.sidebar:
            self._draw_sidebar_background()

    @property
    def content_width(self) -> float:
        return self.w - self.l_margin - self.r_margin


class Resume(Document):
    """
    Example implementation of a custom Document
    """

    def header(self):
        """
        Custom header
        :return:
        """
        orig_l_margin = self.l_margin
        orig_r_margin = self.r_margin

        self.set_left_margin(0)
        self.set_right_margin(0)

        # Setting font: helvetica bold 15
        self.set_font("helvetica", "B", 15)
        # Moving cursor to the right:
        self.cell(80)
        # Printing title:
        self.cell(30, 10, "Title", border=1, align="C")
        # Performing a line break:
        self.ln(20)

        #  Switch back to original settings
        self.set_left_margin(orig_l_margin)
        self.set_right_margin(orig_r_margin)

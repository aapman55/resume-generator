import unittest

from resgen.core.document import Document, Resume
from resgen.core.font import Font
from resgen.core.page_settings import SideBar

from tests.test_utils.dir import get_root


class TestDocument(unittest.TestCase):
    def setUp(self) -> None:
        self.font1 = Font(
            family="Roboto",
            font_style="",
            font_file_path=str(get_root() / "tests" / "assets" / "Roboto-Regular.ttf"),
        )

    def test_init(self) -> None:
        doc = Document()

        self.assertIsNone(doc.sidebar)
        self.assertTrue(doc.in_main_content)
        self.assertEqual(doc.cur_orientation, "P")

    def test_register_font(self) -> None:
        doc = Document()
        doc.register_font(font=self.font1)

    def test_switch_to_sidebar_left(self) -> None:
        width = 20
        sidebar = SideBar(
            width=width,
        )
        doc = Document(sidebar=sidebar)

        self.assertTrue(doc.in_main_content)
        doc.switch_to_sidebar()
        self.assertFalse(doc.in_main_content)
        self.assertEqual(doc.l_margin, 0)
        # Right margin is measured from the right edge
        self.assertEqual(doc.r_margin, doc.w - width)

    def test_switch_to_sidebar_right(self) -> None:
        width = 20
        sidebar = SideBar(
            width=width,
            align_left=False,
        )
        doc = Document(sidebar=sidebar)

        self.assertTrue(doc.in_main_content)
        doc.switch_to_sidebar()
        self.assertFalse(doc.in_main_content)
        self.assertEqual(doc.l_margin, doc.w - width)
        # Right margin is measured from the right edge
        self.assertEqual(doc.r_margin, 0)

    def test_switch_to_main_left_sidebar(self):
        width = 20
        sidebar = SideBar(
            width=width,
            align_left=True,
        )
        doc = Document(sidebar=sidebar)

        self.assertTrue(doc.in_main_content)
        doc.switch_to_sidebar()
        self.assertFalse(doc.in_main_content)
        doc.switch_to_main_content()
        self.assertTrue(doc.in_main_content)
        self.assertEqual(doc.l_margin, width)
        self.assertEqual(doc.r_margin, 0)

    def test_switch_to_main_right_sidebar(self):
        width = 20
        sidebar = SideBar(
            width=width,
            align_left=False,
        )
        doc = Document(sidebar=sidebar)

        self.assertTrue(doc.in_main_content)
        doc.switch_to_sidebar()
        self.assertFalse(doc.in_main_content)
        doc.switch_to_main_content()
        self.assertTrue(doc.in_main_content)
        self.assertEqual(doc.l_margin, 0)
        self.assertEqual(doc.r_margin, width)

    def test_add_page_left_sidebar(self):
        width = 20
        sidebar = SideBar(
            width=width,
            align_left=True,
        )
        doc = Document(sidebar=sidebar)
        doc.add_page()
        doc.add_page()
        self.assertEqual(len(doc.pages), 2)

    def test_add_page_right_sidebar(self):
        width = 20
        sidebar = SideBar(
            width=width,
            align_left=False,
        )
        doc = Document(sidebar=sidebar)
        doc.add_page()
        doc.add_page()
        self.assertEqual(len(doc.pages), 2)

    def test_content_width(self):
        doc = Document()
        doc.set_left_margin(10)
        doc.set_right_margin(20)

        self.assertEqual(doc.w - 30, doc.content_width)


class TestResume(unittest.TestCase):
    def test_header(self) -> None:
        # The header creates a cell with text of 10mm then adds a newline of 20mm
        doc = Resume()
        doc.add_page()
        self.assertEqual(doc.y, 30)

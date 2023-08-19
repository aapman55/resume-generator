import unittest
from unittest.mock import MagicMock, call

from resgen.core.builder import DocumentBuilder
from resgen.core.document import Document


class TestDocumentBuilder(unittest.TestCase):
    def setUp(self) -> None:
        self.minimal_inputs = {
            "output_name": "path/to/output.pdf",
            "components": [
                {"component": "tests.resgen.core.mock_component.EmptyComponent"}
            ],
            "style_registry": {
                "styles": [
                    {
                        "id": "standard",
                        "family": "dummy_family",
                    }
                ]
            },
        }

    def test_init(self):
        # Using minimal input
        inputs = self.minimal_inputs

        DocumentBuilder(**inputs)

    def test_register_fonts(self):
        inputs = self.minimal_inputs
        custom_fonts = [
            {
                "family": "family1",
                "font_style": "",
                "font_file_path": "path/to/font1.ttf",
            },
            {
                "family": "family2",
                "font_style": "B",
                "font_file_path": "path/to/font2.ttf",
            },
        ]

        inputs["custom_fonts"] = custom_fonts

        mock_document = MagicMock()

        builder = DocumentBuilder(**inputs)
        builder.register_fonts(mock_document)

        self.assertEqual(mock_document.register_font.call_count, 2)

    @unittest.mock.patch.object(Document, "output", new=MagicMock())
    def test_build(self):
        """
        This test runs through all actual functions of fpdf but just
        patches the output method
        """
        inputs = self.minimal_inputs
        builder = DocumentBuilder(**inputs)
        builder.build()

        self.assertEqual(Document.output.call_args_list, [call("path/to/output.pdf")])

    @unittest.mock.patch.object(Document, "output", new=MagicMock())
    @unittest.mock.patch("builtins.print")
    def test_build_with_sidebar_components_not_in_page_settings(self, mock_print):
        """
        This test runs through all actual functions of fpdf but just
        patches the output method

        Tests that adding sidebar_components does nothing without defining
        the sidebar in the page_settings.
        """
        inputs = self.minimal_inputs
        sidebar_config = [
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
        ]

        inputs["sidebar_components"] = sidebar_config
        builder = DocumentBuilder(**inputs)
        doc = builder.build()

        self.assertEqual(Document.output.call_args_list, [call("path/to/output.pdf")])
        self.assertTrue(doc.in_main_content)
        mock_print.assert_called_once_with(
            "WARNING: You have defined sidebar components but not a sidebar!"
        )

    @unittest.mock.patch.object(Document, "output", new=MagicMock())
    def test_build_with_sidebar_components_in_page_settings(self):
        """
        This test runs through all actual functions of fpdf but just
        patches the output method

        Tests that adding sidebar_components with defining
        the sidebar in the page_settings will render the sidebar.
        """
        inputs = self.minimal_inputs
        sidebar_config = [
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
            {"component": "tests.resgen.core.mock_component.EmptyComponent"},
        ]

        # page settings include sidebar
        page_settings = {"sidebar": {}}

        inputs["sidebar_components"] = sidebar_config
        inputs["page_settings"] = page_settings
        builder = DocumentBuilder(**inputs)
        doc = builder.build()

        self.assertEqual(Document.output.call_args_list, [call("path/to/output.pdf")])
        self.assertFalse(doc.in_main_content)

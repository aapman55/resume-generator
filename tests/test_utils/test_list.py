import unittest

from resgen.components.list import TitledList, TitledKeyValueList
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class TestTitledList(unittest.TestCase):
    def setUp(self) -> None:
        self.style_registry = StyleRegistry(
            styles=[
                {
                    "id": "default",
                    "family": "helvetica",
                },
            ]
        )

    def test_init(self) -> None:
        TitledList(
            title="Some Title",
            title_style="some_style",
            list_values=["value1", "value2"],
            list_values_style="some_list_style",
        )

    def test_add_pdf_contents(self) -> None:
        doc = Document()
        doc.add_page()
        titled_list = TitledList(
            title="Some Title",
            title_style="default",
            list_values=["value1", "value2"],
            list_values_style="default",
        )

        # Default top margin is 10 mm
        self.assertAlmostEqual(doc.y, 10)
        titled_list.add_pdf_content(doc=doc, style_registry=self.style_registry)

        # Adding title + 2 list items (no top and bottom margin because those are added in build())
        # doc.font_size is the physical height in mm
        self.assertAlmostEqual(doc.y, 10 + doc.font_size * 3)


class TestTitledKeyValueList(unittest.TestCase):
    def setUp(self) -> None:
        self.style_registry = StyleRegistry(
            styles=[
                {
                    "id": "default",
                    "family": "helvetica",
                },
            ]
        )

    def test_add_pdf_contents(self) -> None:
        doc = Document()
        doc.add_page()
        titled_list = TitledKeyValueList(
            title="Some Title",
            title_style="default",
            key_values={
                "key1": "value1",
                "key2": "value2",
            },
            key_values_style="default",
        )

        # Default top margin is 10 mm
        self.assertAlmostEqual(doc.y, 10)
        titled_list.add_pdf_content(doc=doc, style_registry=self.style_registry)

        # Adding title + 2 list items (no top and bottom margin because those are added in build())
        # doc.font_size is the physical height in mm
        self.assertAlmostEqual(doc.y, 10 + doc.font_size * 3)

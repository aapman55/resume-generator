import unittest

from resgen.components.profile import ProfileDescription, ProfileHeadline
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class TestProfileHeadline(unittest.TestCase):
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
        headline = ProfileHeadline(
            name="dummy_name",
            name_style="default",
            job_title="dummy_job_title",
            job_title_style="default",
        )

        # Standard top margin
        self.assertAlmostEqual(doc.y, 10)

        # add contents
        headline.add_pdf_content(doc=doc, style_registry=self.style_registry)

        # Check y location again
        self.assertAlmostEqual(doc.y, 10 + 2 * doc.font_size)


class TestProfileDescription(unittest.TestCase):
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
        headline = ProfileDescription(
            text="dummy_name\n\ndummy_profile\n\n",
            text_style="default",
        )

        # Standard top margin
        self.assertAlmostEqual(doc.y, 10)

        # add contents
        headline.add_pdf_content(doc=doc, style_registry=self.style_registry)

        # Check y location again
        # Has standard cell padding of 5 mm. This adds 5mm around the text.
        # So here on top and bottom
        # We also put 2 newlines in between, so 3 lines in total.
        # Trailing newlines are stripped.
        self.assertAlmostEqual(doc.y, 10 + 2 * 5 + 3 * doc.font_size)

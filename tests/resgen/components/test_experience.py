import unittest

from resgen.components.experience import (
    Experience,
    ExperiencesDetailed,
    ExperiencesCompact,
)
from resgen.core.document import Document
from resgen.core.style import StyleRegistry


class TestExperience(unittest.TestCase):
    def setUp(self) -> None:
        self.exp1 = Experience(
            title="dummy_title",
            experience_start="  2023 Jan ",
            experience_end=" 2023 Aug ",
            description="dummy experience",
            skills_used=[
                "dummy skill 1",
                "dummy skill 2",
            ],
        )

        self.exp2 = Experience(
            title="dummy_title",
            experience_start="  2023 Jan ",
            experience_end=" 2023 Jan ",
            description="dummy experience",
            skills_used=[
                "dummy skill 1",
                "dummy skill 2",
            ],
        )

    def test_experience_range(self) -> None:
        exp = self.exp1

        self.assertEqual(exp.experience_range, "2023 Jan - 2023 Aug")

    def test_experience_range_nor_range(self) -> None:
        exp = self.exp2
        self.assertEqual(exp.experience_range, "2023 Jan")


class TestExperienceDetailed(unittest.TestCase):
    def setUp(self) -> None:
        self.exp1 = Experience(
            title="dummy_title",
            experience_start="  2023 Jan ",
            experience_end=" 2023 Aug ",
            description="dummy experience",
            skills_used=[
                "dummy skill 1",
                "dummy skill 2",
            ],
        )

        self.exp2 = Experience(
            title="dummy_title",
            experience_start="  2023 Jan ",
            experience_end=" 2023 Jan ",
            description="dummy experience",
            skills_used=[
                "dummy skill 1",
                "dummy skill 2",
            ],
        )

        self.style_registry = StyleRegistry(
            styles=[
                {
                    "id": "default",
                    "family": "helvetica",
                },
            ]
        )

    def test_add_pdf_content(self) -> None:
        doc = Document()
        doc.add_page()

        experience_detailed = ExperiencesDetailed(
            experiences_title="dummy title",
            experiences=[self.exp1, self.exp2],
            experiences_title_style="default",
            begin_end_style="default",
            title_style="default",
            description_style="default",
            skills_used_title_style="default",
        )

        self.assertAlmostEqual(doc.y, 10)

        experience_detailed.add_pdf_content(doc=doc, style_registry=self.style_registry)

        self.assertAlmostEqual(
            doc.y,
            10 +
            # Overall Title
            doc.font_size +
            # Spacing between elements
            experience_detailed.spacing_between_experience_elements +
            # We have 2 identical experiences
            (
                # Experience Title and time range (should fit on 1 line)
                doc.font_size
                +
                # Spacing between title and description
                experience_detailed.spacing_between_experience_elements
                +
                # Description, int this test it fits on 1 row
                doc.font_size
                +
                # We have defined skills (x2) but should fit on 1 line
                # Also includes spacing
                experience_detailed.spacing_between_experience_elements
                + doc.font_size
                +
                # End of experience has a line spacing
                experience_detailed.spacing_between_experiences
            )
            * 2,
        )

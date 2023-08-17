import unittest

from resgen.components.experience import (
    Experience,
    ExperiencesDetailed,
    ExperiencesCompact,
)


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

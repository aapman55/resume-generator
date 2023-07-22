import unittest

from resgen.core.document import Resume
from resgen.core.component import init_class, init_component
from resgen.components.experience import Experience


class TestComponent(unittest.TestCase):
    def test_init_class(self):
        actual_class = init_class(full_class_path="resgen.core.document.Resume")
        self.assertEqual(actual_class, Resume)

    def test_init_class_fail(self):
        actual_class = init_class(full_class_path="resgen.core.document.Document")
        self.assertNotEqual(actual_class, Resume)

    def test_init_component(self):
        input_dict = {
            "component": "resgen.components.experience.Experience",
            "title": "First job",
            "experience_start": "June 2021",
            "description": "I did absolutely nothing",
            "general_style": "standard_style",
        }
        actual_component = init_component(input_dict)
        expected_component = Experience(
            title="First job",
            experience_start="June 2021",
            description="I did absolutely nothing",
            general_style="standard_style",
        )

        self.assertEqual(actual_component, expected_component)

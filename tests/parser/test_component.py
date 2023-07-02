import unittest

from resgen.components.document import Resume
from resgen.core.component import init_class, init_component
from resgen.components.experience import Experience

class TestComponent(unittest.TestCase):

    def test_init_class(self):
        actual_class = init_class(full_class_path="resgen.components.document.Resume")
        self.assertEqual(actual_class, Resume)

    def test_init_class_fail(self):
        actual_class = init_class(full_class_path="resgen.components.document.Orientation")
        self.assertNotEqual(actual_class, Resume)

    def test_init_component(self):
        input_dict = {
            "component": "resgen.components.experience.Experience",
            "start_year": 2010,
            "start_month":  6,
            "end_year": 2011,
            "end_month": 4,
            "description": "I did absolutely nothing",
        }
        actual_component = init_component(input_dict)
        expected_component = Experience(
            start_year=2010,
            start_month=6,
            end_year=2011,
            end_month=4,
            description="I did absolutely nothing",
        )

        self.assertEqual(actual_component, expected_component)

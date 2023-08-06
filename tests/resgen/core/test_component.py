import unittest
from unittest.mock import MagicMock

from resgen.core.document import Resume
from resgen.core.component import init_class, init_component
from tests.resgen.core.mock_component import EmptyComponent


class TestComponent(unittest.TestCase):
    def test_init_class(self):
        actual_class = init_class(
            full_class_path="tests.resgen.core.mock_component.EmptyComponent"
        )
        self.assertEqual(actual_class, EmptyComponent)

    def test_init_class_fail(self):
        actual_class = init_class(
            full_class_path="tests.resgen.core.mock_component.EmptyComponent"
        )
        self.assertNotEqual(actual_class, Resume)

    def test_init_component(self):
        input_dict = {
            "component": "tests.resgen.core.mock_component.EmptyComponent",
        }
        actual_component = init_component(input_dict)
        expected_component = EmptyComponent()

        self.assertEqual(actual_component, expected_component)

    def test_component_build(self):
        mock_document = MagicMock()
        mock_style_registry = MagicMock()

        comp = EmptyComponent()
        comp.build(mock_document, mock_style_registry)

        self.assertEqual(mock_document.set_fill_color.call_count, 1)
        self.assertEqual(mock_document.set_left_margin.call_count, 2)
        self.assertEqual(mock_document.set_right_margin.call_count, 2)
        self.assertEqual(mock_document.ln.call_count, 2)

    def test_component_build_with_fill_color(self):
        mock_document = MagicMock()
        mock_style_registry = MagicMock()

        comp = EmptyComponent(fill_colour={"r": 255, "g": 255, "b": 255})
        comp.build(mock_document, mock_style_registry)

        self.assertEqual(mock_document.set_fill_color.call_count, 2)
        self.assertEqual(mock_document.set_left_margin.call_count, 2)
        self.assertEqual(mock_document.set_right_margin.call_count, 2)
        self.assertEqual(mock_document.ln.call_count, 2)

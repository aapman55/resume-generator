import unittest

from resgen.components.list import TitledList


class TestTitledList(unittest.TestCase):
    def test_init(self) -> None:
        TitledList(
            title="Some Title",
            title_style="some_style",
            list_values=["value1", "value2"],
            list_values_style="some_list_style",
        )

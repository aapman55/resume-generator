import sys
import unittest
from unittest.mock import MagicMock

from resgen.console.cli import run
from resgen.core.document import Document


class TestCLI(unittest.TestCase):
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

    @unittest.mock.patch.object(Document, "output", new=MagicMock())
    @unittest.mock.patch("resgen.console.cli.load_yaml")
    def test_cli(self, mock_load_yaml) -> None:
        test_args = ["resgen", "/path/to/config.yaml"]
        mock_load_yaml.return_value = self.minimal_inputs

        with unittest.mock.patch.object(sys, "argv", test_args):
            #  Run the cli
            run()
            # Asserts
            mock_load_yaml.assert_called_once_with("/path/to/config.yaml")

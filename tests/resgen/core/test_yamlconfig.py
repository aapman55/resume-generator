from pathlib import Path
from unittest import TestCase

from resgen.core.yamlconfig import load_yaml


class TestYamlConfig(TestCase):
    def test_load_yaml(self):
        actual = load_yaml(str(Path(__file__).parent / "mock_yaml.yaml"))
        expected = {
            "name": "test_yaml",
            "page_settings": {
                "orientation": "LANDSCAPE",
                "paper_size": "a4",
            },
            "side_bar": None,
            "content": {
                "components": [
                    {
                        "component": "resgen.components.document.Resume",
                        "content": "Hello world",
                    }
                ]
            },
        }

        self.assertDictEqual(actual, expected)

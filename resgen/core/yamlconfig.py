"""
Module for parsing yaml config

At this moment nothing custom is done. If in the future custom steps
are needed, it is easier to change it centrally.
"""


from pathlib import Path
from typing import Dict

import yaml


def load_yaml(path: str) -> Dict:
    """
    Load a yaml file
    :param path: Path to the yaml file
    :return: A dictionary of the yaml contents
    """
    return yaml.safe_load(Path(path).read_text())

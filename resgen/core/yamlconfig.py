from pathlib import Path
from typing import Dict

import yaml


def load_yaml(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text())

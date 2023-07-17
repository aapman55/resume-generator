import argparse

from resgen.core.yamlconfig import load_yaml
from resgen.core.builder import DocumentBuilder


def run() -> None:
    parser = argparse.ArgumentParser(prog="resgen")
    parser.add_argument("filepath")
    args = parser.parse_args()
    yaml_content = load_yaml(args.filepath)

    builder = DocumentBuilder(**yaml_content)

    builder.build()

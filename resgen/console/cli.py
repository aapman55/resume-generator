"""
Module for cli interaction
"""
import argparse
import sys
from pathlib import Path

from resgen.core.yamlconfig import load_yaml
from resgen.core.builder import DocumentBuilder


def run() -> None:
    """
    This is the main function called via the cli.
    This function is installed as script and also in the __main__.py
    :return:
    """
    # Add local folder to path so that plugins work
    sys.path.append(str(Path(".").resolve()))

    # parse command
    parser = argparse.ArgumentParser(prog="resgen")
    parser.add_argument("filepath")
    args = parser.parse_args()
    yaml_content = load_yaml(args.filepath)

    builder = DocumentBuilder(**yaml_content)

    builder.build()

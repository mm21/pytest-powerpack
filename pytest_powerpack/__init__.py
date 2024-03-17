from pathlib import Path
import os

from pytest import Config


def pytest_configure(config: Config):

    config.addinivalue_line(
        "markers", "output_filename: name of file to be generated and compared"
    )


ROOT_PATH = Path(os.getcwd())
"""
Root path from which pytest is invoked. Should generally be the project root.
"""

BUILD_ROOT_PATH = ROOT_PATH / "build"
"""
Directory containing build artifacts. May be configurable in the future.
"""

from .comparison import *

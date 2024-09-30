"""
A plugin containing extra batteries for pytest.
"""

from pyrollup import rollup
from pytest import Config
from _pytest.config.argparsing import Parser

from .comparison import *
from .utils import *

from . import comparison, utils

__all__ = rollup(comparison, utils)


def pytest_configure(config: Config):

    config.addinivalue_line(
        "markers", "output_filename: name of file to be generated and compared"
    )


def pytest_addoption(parser: Parser):
    parser.addini(
        "powerpack_auto_newline",
        help="Enable newline and underline test name for readability",
        default=False,
    )

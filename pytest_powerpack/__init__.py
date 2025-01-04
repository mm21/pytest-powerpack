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
        "markers",
        "powerpack_compare_file: name of file to be generated and compared",
    )


def pytest_addoption(parser: Parser):
    parser.addini(
        "powerpack_underline",
        help="Enable underline under test name for readability",
        default=False,
    )

    parser.addini(
        "powerpack_expect_folder",
        help="Name of folder in which to place expected files for comparisons",
        default="_expect",
    )

    parser.addini(
        "powerpack_out_folder",
        help="Name of folder in which to place generated files for comparisons; should be ignored by source control",
        default="__out__",
    )

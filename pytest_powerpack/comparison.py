"""
Provides helpers to compare generated artifacts with expected output.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import logging

from pytest import FixtureRequest, Mark, fixture

from ._const import ROOT_PATH

__all__ = [
    "ComparisonFiles",
    "build_dir",
    "expect_dir",
    "output_file",
    "expect_file",
    "comparison_files",
    "compare_files",
]

BUILD_ROOT_PATH = ROOT_PATH / "build"
"""
Directory containing build artifacts.

TODO: get from .env
"""

EXPECT_DIRNAME: str = "_expect"
"""
Name of directory in which to look for expected files.

TODO: get from .env
"""


@dataclass
class ComparisonFiles:
    """
    Wraps a pair of output and expected files to be compared.
    """

    output_file: Path
    expect_file: Path


@fixture
def build_dir(request: FixtureRequest) -> Path:
    """
    Create and return a build directory for this test. Especially useful
    for artifacts needing to be manually inspected upon running the
    test.
    """

    rel_path: Path = _get_relative_path(request)
    build_path: Path = BUILD_ROOT_PATH / rel_path

    # ensure path exists
    build_path.mkdir(parents=True, exist_ok=True)

    return build_path


@fixture
def expect_dir(request: FixtureRequest) -> Path:
    """
    Return the directory containing the expected output for this test,
    located at: [test parent folder]/_expected/[test file basename]/[test name]

    The directory must already exist.
    """

    file_path = Path(request.node.fspath)
    parent_dir: Path = file_path.parent
    test_name: str = request.node.name

    expect_dir: Path = parent_dir / EXPECT_DIRNAME / file_path.stem / test_name

    assert expect_dir.exists()
    assert expect_dir.is_dir()

    return expect_dir


@fixture
def output_file(request: FixtureRequest, build_dir: Path) -> Path:
    """
    Return the path to a file, with filename based on the
    output_filename marker.
    """
    filename: str = _get_filename(request)
    path: Path = build_dir / filename
    return path


@fixture
def expect_file(request: FixtureRequest, expect_dir: Path) -> Path:
    """
    Return a path to the file containing expected output, with filename
    based on the output_filename marker.
    """
    filename: str = _get_filename(request)
    path: Path = expect_dir / filename
    return path


@fixture
def comparison_files(output_file: Path, expect_file: Path) -> ComparisonFiles:
    """
    Wrapper for getting output and expected files.
    """
    return ComparisonFiles(output_file, expect_file)


def compare_files(comparison_files: ComparisonFiles):
    """
    Convenience function to compare the generated vs expected data.
    """
    logging.debug(
        f"Comparing: {comparison_files.output_file} <-> {comparison_files.expect_file}"
    )

    with comparison_files.output_file.open() as output_fh, comparison_files.expect_file.open() as expect_fh:
        output_str: str = output_fh.read()
        expect_str: str = expect_fh.read()

        assert output_str == expect_str


def _get_relative_path(request: FixtureRequest) -> Path:
    """
    Return the path of this test relative to the project root.
    """

    file_path = Path(request.node.fspath)
    test_name: str = request.node.name

    # get parent folder of this file, relative to root
    parent_path: Path = file_path.relative_to(ROOT_PATH).parent

    # get module name as basename of test file
    mod_name: str = os.path.splitext(file_path.name)[0]

    # get relative path using the above info
    rel_path: Path = parent_path / mod_name / test_name

    return rel_path


def _get_filename(request: FixtureRequest) -> str:
    """
    Get filename from output_filename marker.
    """

    err: str = (
        "Exactly one output_filename marker argument must be provided to use output_path fixture"
    )

    marker: Mark | None = request.node.get_closest_marker("output_filename")

    # validate
    assert marker is not None, err
    assert len(marker.args) == 1, err
    filename: str = marker.args[0]
    assert isinstance(filename, str), err

    return filename

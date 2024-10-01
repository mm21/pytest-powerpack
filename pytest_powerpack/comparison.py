"""
Provides helpers to compare generated artifacts with expected output.
"""

from dataclasses import dataclass
from pathlib import Path
import os
import logging

from pytest import FixtureRequest, Mark, fixture

__all__ = [
    "ComparisonFiles",
    "powerpack_build_path",
    "powerpack_expect_path",
    "powerpack_build_file",
    "powerpack_expect_file",
    "powerpack_comparison_files",
    "compare_files",
]


@dataclass
class ComparisonFiles:
    """
    Wraps a pair of expected and generated files to be compared.
    """

    expect_file: Path
    build_file: Path


@fixture
def powerpack_expect_path(request: FixtureRequest) -> Path:
    """
    Return the folder from which to get expected files for comparison.
    Must already exist.
    """

    expect_folder = request.config.getini("powerpack_expect_folder")
    assert isinstance(expect_folder, str)

    testcase_folder, mod_name = _get_testcase_info(request)
    expect_path = testcase_folder / expect_folder / mod_name

    # ensure path exists
    assert (
        expect_path.is_dir()
    ), f"Folder containing expected files for comparison does not exist: {expect_path}"

    return expect_path


@fixture
def powerpack_build_path(request: FixtureRequest) -> Path:
    """
    Return the folder in which to place generated files for comparison.
    Will be created if it does not exist.
    """
    build_folder = request.config.getini("powerpack_build_folder")
    assert isinstance(build_folder, str)

    testcase_folder, mod_name = _get_testcase_info(request)
    build_path = testcase_folder / build_folder / mod_name

    # ensure path exists
    build_path.mkdir(parents=True, exist_ok=True)

    return build_path


@fixture
def powerpack_expect_file(
    request: FixtureRequest, powerpack_expect_path: Path
) -> Path:
    """
    Return path to the file containing expected output, with filename
    based on the powerpack_compare_file marker.
    """
    filename: str = _get_compare_file(request)
    path: Path = powerpack_expect_path / filename
    return path


@fixture
def powerpack_build_file(
    request: FixtureRequest, powerpack_build_path: Path
) -> Path:
    """
    Return path to the file to be generated by testcase, with filename
    based on the powerpack_compare_file marker.
    """
    filename: str = _get_compare_file(request)
    path: Path = powerpack_build_path / filename
    return path


@fixture
def powerpack_comparison_files(
    powerpack_expect_file: Path, powerpack_build_file: Path
) -> ComparisonFiles:
    """
    Wrapper for getting output and expected files.
    """
    return ComparisonFiles(powerpack_expect_file, powerpack_build_file)


def compare_files(comparison_files: ComparisonFiles):
    """
    Convenience function to compare the generated vs expected data.
    """
    logging.debug(
        f"Comparing: {comparison_files.expect_file} <-> {comparison_files.build_file}"
    )

    with comparison_files.expect_file.open() as expect_fh, comparison_files.build_file.open() as build_fh:
        expect_str: str = expect_fh.read()
        build_str: str = build_fh.read()

        assert expect_str == build_str


def _get_testcase_info(request: FixtureRequest) -> tuple[Path, str]:
    """
    Return the folder containing this testcase along with the module name
    (i.e. test_*).
    """
    file_path = Path(request.node.fspath)
    assert file_path.is_file()

    folder = file_path.parent
    mod_name: str = os.path.splitext(file_path.name)[0]

    return folder, mod_name


def _get_compare_file(request: FixtureRequest) -> str:
    """
    Get filename from powerpack_compare_file marker.
    """

    err: str = (
        "Exactly one powerpack_compare_file marker argument must be provided to use output_path fixture"
    )

    marker: Mark | None = request.node.get_closest_marker(
        "powerpack_compare_file"
    )

    # validate
    assert marker is not None, err
    assert len(marker.args) == 1, err
    filename: str = marker.args[0]
    assert isinstance(filename, str), err

    return filename

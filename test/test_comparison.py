from pytest import mark

from pytest_powerpack.comparison import ComparisonFiles, compare_files


@mark.output_filename("test.txt")
def test_hello(comparison_files: ComparisonFiles):
    """
    Generate a simple test file and compare against expected content.
    """

    with open(comparison_files.output_file, "w") as fh:
        fh.write("Hello, world!")

    compare_files(comparison_files)

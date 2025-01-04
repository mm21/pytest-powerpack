from pytest import mark

from pytest_powerpack.comparison import ComparisonFiles, compare_files


@mark.powerpack_compare_file("test.txt")
def test_hello(powerpack_comparison_files: ComparisonFiles):
    """
    Generate a simple test file and compare against expected content.
    """

    with open(powerpack_comparison_files.out_file, "w") as fh:
        fh.write("Hello, world!")

    compare_files(powerpack_comparison_files)

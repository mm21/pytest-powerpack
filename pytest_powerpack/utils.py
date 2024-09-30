"""
General utilities.
"""

from pytest import FixtureRequest, fixture

__all__ = [
    "auto_newline",
]


@fixture(autouse=True)
def auto_newline(request: FixtureRequest):
    """
    Print a newline and underlines test name.
    """
    if request.config.getini("powerpack_auto_newline") == "True":
        print("\n" + "-" * len(request.node.nodeid))

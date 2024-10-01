"""
General utilities.
"""

from pytest import FixtureRequest, fixture

__all__ = [
    "powerpack_underline",
]


@fixture(autouse=True)
def powerpack_underline(request: FixtureRequest):
    """
    Print a newline and underlines test name.
    """
    if request.config.getini("powerpack_underline") == "True":
        print("\n" + "-" * len(request.node.nodeid))

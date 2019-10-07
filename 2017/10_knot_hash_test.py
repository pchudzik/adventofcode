import importlib
import pytest

module = importlib.import_module("10_knot_hash")
rotate = module.rotate


@pytest.mark.parametrize(
    "puzzle, positions, result",
    [
        ([0, 1, 2, 3, 4], [3], [2, 1, 0, 3, 4]),
        ([0, 1, 2, 3, 4], [3, 4], [4, 3, 0, 1, 2]),
        ([0, 1, 2, 3, 4], [3, 4, 1], [4, 3, 0, 1, 2]),
        ([0, 1, 2, 3, 4], [3, 4, 1, 5], [3, 4, 2, 1, 0]),
    ]
)
def test_rotate(puzzle, positions, result):
    assert rotate(puzzle, positions) == result

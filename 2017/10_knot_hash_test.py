import importlib
import pytest

module = importlib.import_module("10_knot_hash")
single_round = module.single_round
knot_hash = module.knot_hash


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
    assert single_round(puzzle, positions)[0] == result

@pytest.mark.parametrize(
    "puzzle, result",[
        ("", "a2582a3a0e66e6e86e3812dcb672a272"),
        ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
        ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
        ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e")])
def test_knot_hash(puzzle, result):
    assert knot_hash(puzzle) == result


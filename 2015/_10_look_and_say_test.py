import pytest

from _10_look_and_say import look_and_say


@pytest.mark.parametrize(
    "puzzle, result", [
        ("1", "11"),
        ("211", "1221"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211")])
def test_look_and_say(puzzle, result):
    assert look_and_say(puzzle) == result

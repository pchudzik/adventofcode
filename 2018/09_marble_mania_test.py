import pytest
import importlib

module = importlib.import_module("09_marble_mania")
Board = module.Board
play = module.play


@pytest.mark.parametrize("players, last_marble, highest_score", [
    [10, 25, 32],
    [10, 1618, 8317],
    [13, 7999, 146373],
    [17, 1104, 2764],
    [21, 6111, 54718],
    [30, 5807, 37305],
])
def test_scores(players, last_marble, highest_score):
    max_score = play(players, last_marble)

    assert max_score == highest_score

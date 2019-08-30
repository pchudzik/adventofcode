import importlib
import pytest

module = importlib.import_module("03_spiral_memory")
calculate_position = module.calculate_position
calculate_manhattan_distance = module.calculate_manhattan_distance


@pytest.mark.parametrize(
    "digit, expected_position", [
        (1, (0, 0)),
        (2, (1, 0)),
        (3, (1, 1)),
        (4, (0, 1)),
        (5, (-1, 1)),
        (6, (-1, 0)),
        (7, (-1, -1)),
        (8, (0, -1)),
        (9, (1, -1)),
        (10, (2, -1)),
        (17, (-2, 2)),
        (21, (-2, -2)),
        (13, (2, 2)),
        (25, (2, -2)),
        (49, (3, -3)),
        (50, (4, -3)),
        (81, (4, -4)),
        (82, (5, -4))
    ])
def test_count_position_of_cell(digit, expected_position):
    res = list(calculate_position(digit))
    assert res[-1] == expected_position


@pytest.mark.parametrize(
    "digit, expected_distance", [
        (1, 0),
        (12, 3),
        (23, 2),
        (1024, 31)
    ])
def test_calculate_manhattan_distance(digit, expected_distance):
    assert calculate_manhattan_distance(digit) == expected_distance
import pytest

from _03_spiral_memory import calculate_spiral, calculate_manhattan_distance, stress_test


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
    res = None
    for x in calculate_spiral():
        if x[0] == digit:
            res = x
            break

    assert res == (digit, *expected_position)


@pytest.mark.parametrize(
    "digit, expected_distance", [
        (1, 0),
        (12, 3),
        (23, 2),
        (1024, 31)
    ])
def test_calculate_manhattan_distance(digit, expected_distance):
    assert calculate_manhattan_distance(digit) == expected_distance


@pytest.mark.parametrize(
    "end_sum, result", [
        (2, (4, 0, 1)),
        (4, (5, -1, 1)),
        (5, (10, -1, 0)),
        (10, (11, -1, -1)),
        (11, (23, 0, -1)),
        (23, (25, 1, -1)),
        (25, (26, 2, -1)),
        (26, (54, 2, 0)),
        (54, (57, 2, 1)),
        (57, (59, 2, 2)),
        (59, (122, 1, 2)),
        (122, (133, 0, 2)),
        (133, (142, -1, 2)),
        (142, (147, -2, 2)),
        (147, (304, -2, 1)),
        (304, (330, -2, 0)),
        (330, (351, -2, -1)),
        (351, (362, -2, -2)),
        (362, (747, -1, -2)),
        (747, (806, 0, -2)),
    ])
def test_stress_test(end_sum, result):
    assert stress_test(end_sum) == result

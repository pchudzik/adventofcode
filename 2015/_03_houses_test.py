import pytest

from _03_houses import find_number_of_houses, find_number_of_houses_with_robots


@pytest.mark.parametrize(
    "input, result", [
        (">", 2),
        ("^>v<", 4),
        ("^v^v^v^v^v", 2)
    ])
def test_find_number_of_houses(input, result):
    assert find_number_of_houses(input) == result


@pytest.mark.parametrize(
    "input, result", [
        ("^v", 3),
        ("^>v<", 3),
        ("^v^v^v^v^v", 11)
    ])
def test_find_number_of_houses_with_robot(input, result):
    assert find_number_of_houses_with_robots(input, 2) == result

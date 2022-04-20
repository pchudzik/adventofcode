import pytest

from _01_floors import count_floors, first_basement_entry_position


@pytest.mark.parametrize(
    "floors, expected_result", [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3)])
def test_count_floors(floors, expected_result):
    assert count_floors(floors) == expected_result


@pytest.mark.parametrize(
    "floors, expected_result", [
        (')', 1),
        ('()())', 5)
    ])
def test_first_basement_entry_position(floors, expected_result):
    assert first_basement_entry_position(floors) == expected_result

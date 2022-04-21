import pytest

from _01_city_navigation import distance_calculator, distance_calculator_2


@pytest.mark.parametrize(
    "input, blocks_away", [
        ("R2, L3", 5),
        ("R2, R2, R2", 2),
        ("R5, L5, R5, R3", 12)])
def test_distance_calculator(input, blocks_away):
    assert distance_calculator(input) == blocks_away


def test_part_two():
    assert distance_calculator_2("R8, R4, R4, R8") == 4

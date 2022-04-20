import pytest

from _01_the_tyranny_of_the_rocket_equation import calculate_fuel, calculate_fuel_with_fuel, part1, part2


@pytest.mark.parametrize("mass, expected_fuel", [
    (12, 2),
    (14, 2),
    (1969, 654),
    (100756, 33583)
])
def test_calculate_fuel(mass, expected_fuel):
    assert calculate_fuel(mass) == expected_fuel


def test_part1():
    assert part1([12, 14, 1969, 100756]) == 34241


@pytest.mark.parametrize("mass, expected_fuel", [
    (12, 2),
    (1969, 966),
    (100756, 50346)
])
def test_calculate_fuel_with_fuel(mass, expected_fuel):
    assert calculate_fuel_with_fuel(mass) == expected_fuel


def test_part2():
    assert part2([12, 1969, 100756]) == 51314

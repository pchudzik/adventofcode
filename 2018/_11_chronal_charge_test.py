import pytest

from _11_chronal_charge import find_power_level, \
    find_largest_power_square, \
    find_largest_power_square_any_size, \
    calculate_grid


@pytest.mark.parametrize("cell, serial_id, fuel_level", [
    ((0, 0), 1, -5),
    ((3, 5), 8, 4),
    ((122, 79), 57, -5),
    ((217, 196), 39, 0),
    ((101, 153), 71, 4),
])
def test_find_power_level(cell, serial_id, fuel_level):
    assert find_power_level(cell, serial_id) == fuel_level


@pytest.mark.parametrize("serial, position, total_power", [
    (18, (33, 45), 29),
    (42, (21, 61), 30)
])
def test_find_largest_power_square(serial, position, total_power):
    grid = calculate_grid(serial)

    result = find_largest_power_square(grid)

    assert result.position == position
    assert result.size == 3
    assert result.total_power == total_power


@pytest.mark.skip
@pytest.mark.parametrize("serial, position, square_size, total_power", [
    (18, (90, 269), 16, 113),
    (42, (232, 251), 12, 119)
])
def test_find_largest_power_square_of_any_size(serial, position, square_size, total_power):
    grid = calculate_grid(serial)

    result = find_largest_power_square_any_size(grid)

    assert result.position == position
    assert result.size == square_size
    assert result.total_power == total_power

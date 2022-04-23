"""
--- Day 11: Chronal Charge ---

You watch the Elves and their sleigh fade into the distance as they head toward the North Pole.

Actually, you're the one fading. The falling sensation returns.

The low fuel warning light is illuminated on your wrist-mounted device. Tapping it once causes it to project a hologram
of the situation: a 300x300 grid of fuel cells and their current power levels, some negative. You're not sure what
negative power means in the context of time travel, but it can't be good.

Each fuel cell has a coordinate ranging from 1 to 300 in both the X (horizontal) and Y (vertical) direction. In X,Y
notation, the top-left cell is 1,1, and the top-right cell is 300,1.

The interface lets you select any 3x3 square of fuel cells. To increase your chances of getting to your destination, you
decide to choose the 3x3 square with the largest total power.

The power level in a given fuel cell can be found through the following process:
* Find the fuel cell's rack ID, which is its X coordinate plus 10.
* Begin with a power level of the rack ID times the Y coordinate.
* Increase the power level by the value of the grid serial number (your puzzle input).
* Set the power level to itself multiplied by the rack ID.
* Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
* Subtract 5 from the power level.

For example, to find the power level of the fuel cell at 3,5 in a grid with serial number 8:
* The rack ID is 3 + 10 = 13.
* The power level starts at 13 * 5 = 65.
* Adding the serial number produces 65 + 8 = 73.
* Multiplying by the rack ID produces 73 * 13 = 949.
* The hundreds digit of 949 is 9.
* Subtracting 5 produces 9 - 5 = 4.

So, the power level of this fuel cell is 4.

Here are some more example power levels:

Fuel cell at  122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4.

Your goal is to find the 3x3 square which has the largest total power. The square must be entirely within the 300x300
grid. Identify this square using the X,Y coordinate of its top-left fuel cell. For example:

For grid serial number 18, the largest total 3x3 square has a top-left corner of 33,45 (with a total power of 29); these
fuel cells appear in the middle of this 5x5 region:

-2  -4   4   4   4
-4   4   4   4  -5
 4   3   3   4  -4
 1   1   2   4  -3
-1   0   2  -5  -2

For grid serial number 42, the largest 3x3 square's top-left is 21,61 (with a total power of 30); they are in the middle
of this region:

-3   4   2   2   2
-4   4   3   3   4
-5   3   3   4  -4
 4   3   3   4  -3
 3   3   3  -5  -1

What is the X,Y coordinate of the top-left fuel cell of the 3x3 square with the largest total power?

Your puzzle answer was 235,38.

--- Part Two ---

You discover a dial on the side of the device; it seems to let you select a square of any size, not just 3x3. Sizes from
1x1 to 300x300 are supported.

Realizing this, you now must find the square of any size with the largest total power. Identify this square by including
its size as a third parameter after the top-left coordinate: a 9x9 square with a top-left corner of 3,5 is identified as
3,5,9.

For example:

For grid serial number 18, the largest total square (with a total power of 113) is 16x16 and has a top-left corner of
90,269, so its identifier is 90,269,16.

For grid serial number 42, the largest total square (with a total power of 119) is 12x12 and has a top-left corner of
232,251, so its identifier is 232,251,12.

What is the X,Y,size identifier of the square with the largest total power?

Your puzzle answer was 233,146,13.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from sys import maxsize
from collections import namedtuple

GRID_SIZE = 300

PowerCell = namedtuple("PowerCell", "position, size, total_power")
MINIMUM_POWER = PowerCell(None, None, -maxsize)


def find_power_level(cell, serial_id):
    x, y = cell
    rack_id = x + 10
    power_level = rack_id * y
    fuel_level = str((power_level + serial_id) * rack_id)
    if len(fuel_level) < 3:
        fuel_level = 0
    else:
        fuel_level = int(fuel_level[-3])

    return fuel_level - 5


def find_largest_power_square_any_size(grid):
    biggest_so_far = PowerCell(None, None, -maxsize)
    for square_size in range(1, GRID_SIZE + 1):
        most_power_for_square = find_largest_power_square(grid, square_size)
        if most_power_for_square.total_power > biggest_so_far.total_power:
            biggest_so_far = most_power_for_square
    return biggest_so_far


def find_largest_power_square(grid, square_size=3):
    biggest = MINIMUM_POWER
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            power = _find_square_power(grid, (x, y), square_size)
            if power > biggest.total_power:
                biggest = PowerCell((x, y), square_size, power)
    return biggest


def _find_square_power(grid, position, square_size):
    """
    https://en.wikipedia.org/wiki/Summed-area_table
    https://github.com/ckreisl/summed-area-table
    """
    x, y = position

    if x + square_size >= GRID_SIZE or y + square_size >= GRID_SIZE:
        return -maxsize

    a, b, c, d = 0, 0, 0, 0
    if x > 0 and y > 0:
        a = grid[x - 1][y - 1]
    if y > 0:
        b = grid[x + square_size - 1][y - 1]
    if x > 0:
        c = grid[x - 1][y + square_size - 1]

    d = grid[x + square_size - 1][y + square_size - 1]

    return a - b - c + d


def calculate_grid(serial_id):
    """
    https://en.wikipedia.org/wiki/Summed-area_table
    https://github.com/ckreisl/summed-area-table
    """
    summed_area_table = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = find_power_level((x, y), serial_id)

            if y > 0:
                value += summed_area_table[x][y - 1]
            if x > 0:
                value += summed_area_table[x - 1][y]
            if x > 0 and y > 0:
                value -= summed_area_table[x - 1][y - 1]

            summed_area_table[x][y] = value

    return summed_area_table


if __name__ == "__main__":
    serial_id = 9306
    grid = calculate_grid(serial_id)

    part1 = find_largest_power_square(grid)
    print(f"part 1: {part1.position[0]},{part1.position[1]}")

    part2 = find_largest_power_square_any_size(grid)
    print(f"part 2: {part2.position[0]},{part2.position[1]},{part2.size}")

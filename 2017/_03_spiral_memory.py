"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while
spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the
location of the only access port for this memory system) by programs that can only move up, down, left, or right. They
always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the access
port?

Your puzzle answer was 438.

--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, in the
same allocation order as shown above, they store the sum of the values in all adjacent squares, including diagonals.

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values:

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...
What is the first value written that is larger than your puzzle input?

Your puzzle answer was 266330.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

Your puzzle input was 265149.

"""


def calculate_spiral():
    yield 1, 0, 0
    yield 2, 1, 0

    x, y = 1, 1
    digit = 2
    direction = "right"
    while True:
        digit += 1
        yield digit, x, y

        if x == y and x > 0 < y:  # top right corner
            direction = "left"
        elif abs(x) == y and x < 0 < y:  # top left corner
            direction = "down"
        elif x == y and x < 0 > y:  # bottom left corner
            direction = "right"
        elif x == abs(y) and x > 0 > y:  # bottom right corner
            direction = "up"
            x += 1
            digit += 1
            yield digit, x, y

        if direction == "right":
            x += 1
        if direction == "left":
            x -= 1
        if direction == "up":
            y += 1
        if direction == "down":
            y -= 1


def calculate_manhattan_distance(to_digit):
    # Manhattan Distance between two points (x1, y1) and (x2, y2) is: |x1 – x2| + |y1 – y2|
    last = None
    for coordinates in calculate_spiral():
        if coordinates[0] == to_digit:
            last = coordinates
            break
    last = last[1:]
    return sum(map(abs, last))


def stress_test(end_sum):
    cache = {
        (0, 0): 1,
        (1, 0): 1
    }
    for coordinates in calculate_spiral():
        if coordinates[0] > 2:
            position = coordinates[1:]
            adjacent_squares = filter(
                lambda p: p in cache, [
                    (position[0] - 1, position[1]),
                    (position[0] + 1, position[1]),
                    (position[0], position[1] - 1),
                    (position[0], position[1] + 1),
                    (position[0] + 1, position[1] + 1),
                    (position[0] - 1, position[1] + 1),
                    (position[0] - 1, position[1] - 1),
                    (position[0] + 1, position[1] - 1),
                ])
            sum_of_values = sum(map(lambda p: cache[p], adjacent_squares))
            cache[position] = sum_of_values
            if sum_of_values > end_sum:
                return (sum_of_values, *position)


if __name__ == "__main__":
    puzzle = 265149
    print(f"part1: {calculate_manhattan_distance(puzzle)}")
    print(f"part2: {stress_test(puzzle)}")

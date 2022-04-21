"""
--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by
stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve
all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar; the second
puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get
- the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work
them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then,
follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of
blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the
destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the
destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?

Your puzzle answer was 271.


--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the
first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?

Your puzzle answer was 153.
"""

_directions = {
    "NORTH": {
        "R": "EAST",
        "L": "WEST"
    },
    "SOUTH": {
        "R": "WEST",
        "L": "EAST"
    },
    "WEST": {
        "R": "NORTH",
        "L": "SOUTH"
    },
    "EAST": {
        "R": "SOUTH",
        "L": "NORTH"
    }
}


def distance_calculator_2(input_str):
    visited = [(0, 0)]
    current_position = (0, 0, "NORTH")
    for next_step in input_str.split(", "):
        road = _move(current_position, next_step)
        current_position = road[-1]
        for x, y, _ in road:
            if (x, y) in visited:
                return _find_distance(x, y)
            else:
                visited.append((x, y))


def distance_calculator(input_str):
    destination = (0, 0, "NORTH")
    for step in input_str.split(", "):
        destination = _move(destination, step)[-1]
    return _find_distance(*destination)


def _find_distance(x, y, *_):
    return abs(x) + abs(y)


def _move(current_position, next_step):
    next_dir = _directions[current_position[2]][next_step[0]]
    blocks = int(next_step[1:])

    x, y, _ = current_position
    steps = range(1, blocks + 1)

    if next_dir == "NORTH":
        return [(x + step, y, next_dir) for step in steps]
    elif next_dir == "SOUTH":
        return [(x - step, y, next_dir) for step in steps]
    elif next_dir == "WEST":
        return [(x, y - step, next_dir) for step in steps]
    elif next_dir == "EAST":
        return [(x, y + step, next_dir) for step in steps]


if __name__ == "__main__":
    input_str = "R4, R3, R5, L3, L5, R2, L2, R5, L2, R5, R5, R5, R1, R3, L2, L2, L1, R5, L3, R1, L2, R1, L3, L5, L1, R3, L4, R2, R4, L3, L1, R4, L4, R3, L5, L3, R188, R4, L1, R48, L5, R4, R71, R3, L2, R188, L3, R2, L3, R3, L5, L1, R1, L2, L4, L2, R5, L3, R3, R3, R4, L3, L4, R5, L4, L4, R3, R4, L4, R1, L3, L1, L1, R4, R1, L4, R1, L1, L3, R2, L2, R2, L1, R5, R3, R4, L5, R2, R5, L5, R1, R2, L1, L3, R3, R1, R3, L4, R4, L4, L1, R1, L2, L2, L4, R1, L3, R4, L2, R3, L1, L5, R4, R5, R2, R5, R1, R5, R1, R3, L3, L2, L2, L5, R2, L2, R5, R5, L2, R3, L5, R5, L2, R4, R2, L1, R3, L5, R3, R2, R5, L1, R3, L2, R2, R1"
    print(f"part1 = {distance_calculator(input_str)}")
    print(f"part2 = {distance_calculator_2(input_str)}")

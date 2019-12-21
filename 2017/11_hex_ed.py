r"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in
distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps
required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).
Your puzzle answer was 707.

--- Part Two ---

How many steps away is the furthest he ever got from his starting position?

Your puzzle answer was 1490.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

# It's all based on https://www.redblobgames.com/grids/hexagons/

from functools import reduce

_moves = {
    "n": lambda x, y, z: (x, y + 1, z - 1),
    "s": lambda x, y, z: (x, y - 1, z + 1),
    "nw": lambda x, y, z: (x - 1, y + 1, z),
    "sw": lambda x, y, z: (x - 1, y, z + 1),
    "se": lambda x, y, z: (x + 1, y - 1, z),
    "ne": lambda x, y, z: (x + 1, y, z - 1)
}


def shortest_path_finder(path):
    start = 0, 0, 0
    end = reduce(
        lambda position, move: next_coordinate(position, move),
        path.split(","),
        start)
    return find_distance(start, end)


def furthest_point(path):
    start = 0, 0, 0
    current = start
    max_distance = 0
    for step in path.split(","):
        current = next_coordinate(current, step)
        current_distance = find_distance(start, current)
        max_distance = max(current_distance, max_distance)

    return max_distance


def find_distance(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def next_coordinate(current, direction):
    return _moves[direction](*current)


if __name__ == "__main__":
    with open("11_hex_ed.txt") as file:
        path = file.readline()
        print(f"part1: {shortest_path_finder(path)}")
        print(f"part1: {furthest_point(path)}")

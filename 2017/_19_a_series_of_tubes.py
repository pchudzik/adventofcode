"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input), but
it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take,
starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction, and only turn
left or right when there's no other option. In addition, someone has left letters on the line; these also don't change
its direction, but it can use them to keep track of where it's been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

* Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to the
  first +.
* Travel right, up, and right, passing through B in the process.
* Continue down (collecting C), right, and up (collecting D).
* Finally, go all the way left through E and stopping at F.

Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it would
see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line wrapping.)

Your puzzle answer was LIWQYKMRP.

--- Part Two ---

The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |
     |  +--+
     A  |  C
 F---|--|-E---+
     |  |  |  D
     +B-+  +--+

...the packet would go:

* 6 steps down (including the first line at the top of the diagram).
* 3 steps right.
* 4 steps up.
* 3 steps right.
* 4 steps down.
* 3 steps right.
* 2 steps up.
* 13 steps left (including the F it stops on).

This would result in a total of 38 steps.

How many steps does the packet need to go?

Your puzzle answer was 16764.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

import re
from collections import deque, namedtuple

Ctx = namedtuple("Ctx", "x, y, previous, steps, letters, visited")


def _vertical_moves(x, y):
    return [
        (x + 1, y),
        (x - 1, y)
    ]


def _horizontal_moves(x, y):
    return [
        (x, y + 1),
        (x, y - 1)
    ]


def _available_paths_validator(maze):
    def predicate(visited, nx, ny):
        if nx >= len(maze) or ny >= len(maze[nx]):
            return False

        move = maze[nx][ny]

        return (nx, ny) not in visited and (move.isalpha() or move in "+|-")

    return predicate


def _find_all_letters(maze: str):
    pattern = re.compile(r"\w")
    return sum(len(pattern.findall(line)) for line in maze)


def _is_going(direction, maze, current, previous):
    x, y = current
    px, py = previous if previous is not None else (x, y)

    if maze[x][y] == "+":
        return False

    if direction == "vertical":
        return py == y
    elif direction == "horizontal":
        return px == x


def _find_available_moves(maze, previous, x, y):
    if is_going_vertically(maze, (x, y), previous):
        available_moves = _vertical_moves(x, y)
    elif is_going_horizontally(maze, (x, y), previous):
        available_moves = _horizontal_moves(x, y)
    else:
        available_moves = _vertical_moves(x, y) + _horizontal_moves(x, y)
    return available_moves


def is_going_vertically(maze, current, previous):
    return _is_going("vertical", maze, current, previous)


def is_going_horizontally(maze, current, previous):
    return _is_going("horizontal", maze, current, previous)


def walker(maze, starting_point):
    expected_letters_count = _find_all_letters(maze)
    paths = deque([(Ctx(*starting_point, None, 1, list(), set()))])
    check_if_path_available = _available_paths_validator(maze)

    def is_crossroad(visited, x, y, previous):
        possible_moves = [
            (nx, ny)
            for nx, ny in _vertical_moves(x, y) + _horizontal_moves(x, y)
            if check_if_path_available(visited, nx, ny) and (nx, ny) != previous]
        return len(possible_moves) > 1

    while paths:
        x, y, previous, steps, letters, visited = paths.popleft()

        if (x, y) in visited:
            continue

        visited.add((x, y))

        if maze[x][y].isalpha():
            letters.append(maze[x][y])
            if len(letters) >= expected_letters_count:
                return "".join(letters), steps

        available_moves = [
            (nx, ny)
            for nx, ny in _find_available_moves(maze, previous, x, y)
            if check_if_path_available(visited, nx, ny) and (nx, ny) != previous]

        if is_crossroad(visited, x, y, previous):
            visited.remove((x, y))

        for nx, ny in available_moves:
            paths.append(Ctx(nx, ny, (x, y), steps + 1, list(letters), set(visited)))


if __name__ == "__main__":
    with open("_19_a_series_of_tubes.txt") as file:
        puzzle = file.readlines()
        path, steps = walker(puzzle, (0, 89))
        print(f"part 1: {path}")
        print(f"part 2: {steps}")

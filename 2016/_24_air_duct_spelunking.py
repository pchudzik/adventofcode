from collections import deque
from itertools import combinations, permutations
from sys import maxsize

"""
--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight, and all of the controls and
related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that
have been routed through the HVAC system. If you can direct it to each of those locations, you should be able to bypass
the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant locations
marked (your puzzle input). 0 is your current location, from which the cleaning robot embarks; the other numbers are (in
no particular order) the locations the robot needs to visit at least once each. Walls are marked as #, and open passages
are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########
To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

0 to 4 (2 steps)
4 to 1 (4 steps; it can't move diagonally)
1 to 2 (6 steps)
2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route. This path is the fewest steps (in the above
example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every non-0
number marked on the map at least once?

Your puzzle answer was 502.

--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and
then return to 0?

Your puzzle answer was 724.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Maze:
    def __init__(self, maze):
        self.maze = [l.strip() for l in maze]
        self.max_x = len(self.maze[0])
        self.max_y = len(self.maze)

    def find_location(self, number):
        number = str(number)
        for y in range(self.max_y):
            for x in range(self.max_x):
                if self.maze[y][x] == number:
                    return x, y

    def find_path(self, start, end):
        start = self.find_location(start)
        end = self.find_location(end)

        queue = deque()
        visited = set()
        visited.add(start)
        queue.append((*start, 0))

        while queue:
            x, y, distance = queue.popleft()
            if (x, y) == end:
                return distance

            possible_moves = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]

            possible_moves = [
                loc
                for loc in possible_moves
                if self._is_valid_coordinate(*loc) and loc not in visited and self._is_open_space(*loc)
            ]

            for move in possible_moves:
                visited.add(move)
                queue.append((*move, distance + 1))

    def _is_open_space(self, x, y):
        location = self.maze[y][x]
        return location == '.' or location.isdigit()

    def _is_valid_coordinate(self, x, y):
        return 0 <= x < self.max_x and 0 <= y < self.max_y

    def __repr__(self):
        return "\n".join(self.maze)


def find_shortest_path_to_all_points(maze):
    all_points = {int(space) for row in maze.maze for space in row if space.isdigit()}

    all_distances = dict()
    for point_xy in combinations(all_points, 2):
        distance = maze.find_path(point_xy[0], point_xy[1])
        all_distances[(point_xy[0], point_xy[1])] = distance
        all_distances[(point_xy[1], point_xy[0])] = distance

    part1 = _find_shortest_distance(all_points, all_distances)
    part2 = _find_shortest_distance(all_points, all_distances, end=0)

    return part1, part2


def _find_shortest_distance(all_points, all_distances, end=None):
    min_distance = maxsize
    all_points = list(all_points)
    all_points.remove(0)

    for path in permutations(all_points):
        path = [0, *path]
        if end is not None:
            path.append(end)
        distance = 0
        for idx in range(len(path) - 1):
            distance += all_distances[(path[idx], path[idx + 1])]

        if distance < min_distance:
            min_distance = distance

    return min_distance


if __name__ == "__main__":
    with open("_24_air_duct_spelunking.txt") as file:
        maze = Maze(file.readlines())

        solution = find_shortest_path_to_all_points(maze)

        print(f"part1: {solution[0]}")
        print(f"part2: {solution[1]}")

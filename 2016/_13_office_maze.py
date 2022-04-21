from collections import deque

""" You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny
atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either a wall
or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward positive
x and y; negative values are invalid, as they represent a location outside the building. You are in a small waiting area
at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can
determine whether a given x,y coordinate will be a wall or an open space using a simple system:

Find x*x + 3*x + 2*x*y + y + y*y.
Add the office designer's favorite number (your puzzle input).
Find the binary representation of that sum; count the number of bits that are 1.
If the number of bits that are 1 is even, it's an open space.
If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as ., the corner of
the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###
Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

Your puzzle answer was 82.

--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?

Your puzzle answer was 138.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

Your puzzle input was 1362.
"""


class Maze:
    def __init__(self, size, favorite_number):
        self.max_x = size[0]
        self.max_y = size[1]
        self.favorite_number = favorite_number

        self.maze = self.generate_maze()

    def generate_maze(self):
        maze = [[False] * self.max_x for _ in range(self.max_y)]
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                value = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + self.favorite_number
                value = bin(value).count('1') % 2
                maze[y][x] = value == 0
        return maze

    def all_reachable_locations_within_distance(self, max_steps):
        all_reachable_locations = set()

        def count_location(x, y, distance):
            if distance <= max_steps:
                all_reachable_locations.add((x, y))

        self._find_path(count_location)

        return all_reachable_locations

    def shortest_path(self, end):
        return self._find_path(lambda x, y, distance: distance if (x, y) == end else None)

    def _find_path(self, step_handler):
        queue = deque()
        visited = set()
        visited.add((1, 1))
        queue.append((1, 1, 0))

        while queue:
            x, y, distance = queue.popleft()
            stop_result = step_handler(x, y, distance)
            if stop_result:
                return stop_result

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
        return self.maze[y][x]

    def _is_valid_coordinate(self, x, y):
        return 0 <= x < self.max_x and 0 <= y < self.max_y

    def __repr__(self):
        result = ""
        for row in self.maze:
            for space in row:
                result += "." if space else "#"
            result += "\n"
        return result.strip()


if __name__ == "__main__":
    favorite_number = 1362
    maze = Maze((100, 100), favorite_number)
    print("part1", maze.shortest_path((31, 39)))
    print("part2", len(maze.all_reachable_locations_within_distance(50)))

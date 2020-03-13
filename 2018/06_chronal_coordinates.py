"""
--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify
new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It
recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from
the other points.

Using only the Manhattan distance, determine the area around łeach coordinate by counting the number of integer X,Y
locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of
coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each
location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever
outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is
closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest
area is 17.

What is the size of the largest area that isn't infinite?

Your puzzle answer was 5035.

--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many
coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each
location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that
location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as
follows, where abs() is the absolute value function:

Distance to coordinate A: abs(4-1) + abs(3-1) =  5
Distance to coordinate B: abs(4-1) + abs(3-6) =  6
Distance to coordinate C: abs(4-8) + abs(3-3) =  4
Distance to coordinate D: abs(4-3) + abs(3-4) =  2
Distance to coordinate E: abs(4-5) + abs(3-5) =  3
Distance to coordinate F: abs(4-8) + abs(3-9) = 10
Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total
distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less
than 10000?

Your puzzle answer was 35294.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

from collections import namedtuple, defaultdict

Point = namedtuple("Point", "x,y")


class AreaBounds:
    def __init__(self, all_points):
        self.minx = min(all_points, key=lambda p: p.x).x
        self.maxx = max(all_points, key=lambda p: p.x).x
        self.miny = min(all_points, key=lambda p: p.y).y
        self.maxy = max(all_points, key=lambda p: p.y).y

    def is_outside(self, point):
        return any((
            point.x <= self.minx,
            point.x >= self.maxx,
            point.y <= self.miny,
            point.y >= self.maxy
        ))


def parse_points(puzzle):
    def create_point(p):
        a, b = p.strip().split(",")
        return Point(int(a), int(b))

    return [create_point(p) for p in puzzle]


def calculate_area(all_points):
    bounds = AreaBounds(all_points)
    in_bounds_points = {p for p in all_points if not bounds.is_outside(p)}

    grid = dict()
    for x in range(bounds.minx, bounds.maxx + 1):
        for y in range(bounds.miny, bounds.maxy + 1):
            coordinate = Point(x, y)
            closes_point = find_shortest_distance(coordinate, all_points)
            if closes_point in in_bounds_points:
                grid[Point(x, y)] = closes_point

    result = dict()
    for point in all_points:
        if point not in in_bounds_points:
            result[point] = None
        else:
            result[point] = sum(1 for p in grid.values() if p == point)

    return result


def find_all_safe_regions(all_points, max_distance=10_000):
    bounds = AreaBounds(all_points)

    result = []
    for x in range(bounds.minx, bounds.maxx + 1):
        for y in range(bounds.miny, bounds.maxy + 1):
            coordinate = Point(x, y)
            all_distances = find_all_distances(coordinate, all_points)
            distance = sum(all_distances.values())
            if distance < max_distance:
                result.append(Point(x, y))
    return result


def find_max_area(all_points):
    return max(area for area in calculate_area(all_points).values() if area is not None)


def find_all_distances(point, other_points):
    return {
        point2: manhattan_distance(point, point2)
        for point2 in other_points
    }


def find_shortest_distance(coordinate, points):
    distances = defaultdict(list)
    for point, distance in find_all_distances(coordinate, points).items():
        distances[distance].append(point)

    shortest_distance = min(distances.keys())

    if len(distances[shortest_distance]) > 1:
        return None

    return distances[shortest_distance][0]


def manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


if __name__ == "__main__":
    with open("06_chronal_coordinates.txt") as file:
        points = parse_points(file.readlines())

        print(f"part 1: {find_max_area(points)}")
        print(f"part 2: {len(find_all_safe_regions(points))}")

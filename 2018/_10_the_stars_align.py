import re

"""
--- Day 10: The Stars Align ---

It's no use; your navigation system simply isn't capable of providing walking directions in the arctic circle, and
certainly not in 1018.

The Elves suggest an alternative. In times like these, North Pole rescue operations will arrange points of light in the
sky to guide missing Elves back to base. Unfortunately, the message is easy to miss: the points move slowly enough that
it takes hours to align them, but have so much momentum that they only stay aligned for a second. If you blink at the
wrong time, it might be hours before another message appears.

You can see these points of light floating in the distance, and record their position in the sky and their velocity, the
relative change in position per second (your puzzle input). The coordinates are all given from your perspective; given
enough time, those positions and velocities will move the points into a cohesive message!

Rather than wait, you decide to fast-forward the process and calculate what the points will eventually spell.

For example, suppose you note the following points:

position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>

Each line represents one point. Positions are given as <X, Y> pairs: X represents how far left (negative) or right
(positive) the point appears, while Y represents how far up (negative) or down (positive) the point appears.

At 0 seconds, each point has the position given. Each second, each point's velocity is added to its position. So, a
point with velocity <1, -2> is moving to the right, but is moving upward twice as quickly. If this point's initial
position were <3, 9>, after 3 seconds, its position would become <6, 3>.

Over time, the points listed above would move like this:

Initially:
........#.............
................#.....
.........#.#..#.......
......................
#..........#.#.......#
...............#......
....#.................
..#.#....#............
.......#..............
......#...............
...#...#.#...#........
....#..#..#.........#.
.......#..............
...........#..#.......
#...........#.........
...#.......#..........

After 1 second:
......................
......................
..........#....#......
........#.....#.......
..#.........#......#..
......................
......#...............
....##.........#......
......#.#.............
.....##.##..#.........
........#.#...........
........#...#.....#...
..#...........#.......
....#.....#.#.........
......................
......................

After 2 seconds:
......................
......................
......................
..............#.......
....#..#...####..#....
......................
........#....#........
......#.#.............
.......#...#..........
.......#..#..#.#......
....#....#.#..........
.....#...#...##.#.....
........#.............
......................
......................
......................

After 3 seconds:
......................
......................
......................
......................
......#...#..###......
......#...#...#.......
......#...#...#.......
......#####...#.......
......#...#...#.......
......#...#...#.......
......#...#...#.......
......#...#..###......
......................
......................
......................
......................

After 4 seconds:
......................
......................
......................
............#.........
........##...#.#......
......#.....#..#......
.....#..##.##.#.......
.......##.#....#......
...........#....#.....
..............#.......
....#......#...#......
.....#.....##.........
...............#......
...............#......
......................
......................

After 3 seconds, the message appeared briefly: HI. Of course, your message will be much longer and will take many more
seconds to appear.

What message will eventually appear in the sky?

Your puzzle answer was ABGXJBXF.

--- Part Two ---

Good thing you didn't have to wait, because that would have taken a long time - much longer than the 3 seconds in the
example above.

Impressed by your sub-hour communication capabilities, the Elves are curious: exactly how many seconds would they have
needed to wait for that message to appear?

Your puzzle answer was 10619.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Message:
    def __init__(self, points):
        self.points = points

    def snapshot(self, max_screen_size=None):
        result = []
        positions = {p.position for p in self.points}
        min_x = min(x for x, y in positions)
        max_x = max(x for x, y in positions)
        min_y = min(y for x, y in positions)
        max_y = max(y for x, y in positions)

        if max_screen_size is None or abs(max_y) - abs(min_y) < max_screen_size:
            for y in range(min_y, max_y + 1):
                line = ""
                for x in range(min_x, max_x + 1):
                    if (x, y) in positions:
                        line += "#"
                    else:
                        line += "."
                result.append(line)

        return result

    def tick(self):
        for point in self.points:
            point.tick()


class Point:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def tick(self):
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1])

    def transpose(self, x, y):
        return self.position[0] + x, self.position[1] + y

    def __repr__(self):
        return f"({self.position}, {self.velocity})"


def parse(lines):
    def split_numbers(numbers):
        return tuple(map(lambda n: int(n.strip()), numbers.split(",")))

    pattern = re.compile(r"position=<(.*?)> velocity=<(.*?)>")

    result = []
    for line in lines:
        line = line.strip()
        pos, velocity = pattern.match(line).groups()
        result.append(Point(split_numbers(pos), split_numbers(velocity)))

    return result


if __name__ == "__main__":

    with open("_10_the_stars_align.txt") as file:
        points = parse(file.readlines())
        msg = Message(points)

        for time in range(20_000):
            pretty_msg = "\n".join(msg.snapshot(max_screen_size=10))
            if len(pretty_msg) > 0:
                break
            msg.tick()

        print(f"part 1:\n{pretty_msg}")
        print(f"part 2: {time}")

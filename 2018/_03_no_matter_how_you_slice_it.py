import re
from collections import defaultdict

"""
--- Day 3: No Matter How You Slice It ---

The Elves managed to locate the chimney-squeeze prototype fabric for Santa's suit (thanks to someone who helpfully wrote
its box IDs on the wall of the warehouse in the middle of the night). Unfortunately, anomalies are still affecting them
- nobody can even agree on how to cut the fabric.

The whole piece of fabric they're working on is a very large square - at least 1000 inches on each side.

Each Elf has made a claim about which area of fabric would be ideal for Santa's suit. All claims have an ID and consist
of a single rectangle with edges parallel to the edges of the fabric. Each claim's rectangle is defined as follows:

* The number of inches between the left edge of the fabric and the left edge of the rectangle.
* The number of inches between the top edge of the fabric and the top edge of the rectangle.
* The width of the rectangle in inches.
* The height of the rectangle in inches.

A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge, 2 inches from
the top edge, 5 inches wide, and 4 inches tall. Visually, it claims the square inches of fabric represented by # (and
ignores the square inches of fabric represented by .) in the diagram below:

...........
...........
...#####...
...#####...
...#####...
...#####...
...........
...........
...........

The problem is that many of the claims overlap, causing two or more claims to cover part of the same areas. For example,
consider the following claims:

#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2

Visually, these claim the following areas:

........
...2222.
...2222.
.11XX22.
.11XX22.
.111133.
.111133.
........

The four square inches marked with X are claimed by both 1 and 2. (Claim 3, while adjacent to the others, does not
overlap either of them.)

If the Elves all proceed with their own plans, none of them will have enough fabric. How many square inches of fabric
are within two or more claims?

Your puzzle answer was 124850.

--- Part Two ---

Amidst the chaos, you notice that exactly one claim doesn't overlap by even a single square inch of fabric with any
other claim. If you can somehow draw attention to it, maybe the Elves will be able to make Santa's suit after all!

For example, in the claims above, only claim 3 is intact after all claims are made.

What is the ID of the only claim that doesn't overlap?

Your puzzle answer was 1097.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Claim:
    def __init__(self, **kwargs):
        width = int(kwargs["width"])
        height = int(kwargs["height"])

        self.id = int(kwargs["id"])
        self.x1, self.y1 = int(kwargs["top_x"]), int(kwargs["top_y"])
        self.x2, self.y2 = self.x1 + width, self.y1 + height

    def area(self):
        for x in range(self.x1, self.x2):
            for y in range(self.y1, self.y2):
                yield x, y


def parse(puzzle):
    pattern = re.compile(r"#(?P<id>\d+)\s@\s(?P<top_x>\d+),(?P<top_y>\d+):\s(?P<width>\d+)x(?P<height>\d+)")

    def _parse_single(puzzle):
        puzzle = pattern.match(puzzle)
        d = puzzle.groupdict()
        return Claim(**d)

    return [_parse_single(line) for line in puzzle]


def check_overlap(c1: Claim, c2: Claim):
    return not (c1.x1 >= c2.x2 or c2.x1 >= c1.x2 or c1.y1 >= c2.y2 or c2.y1 >= c1.y2)


def find_overlapping_area(claims):
    canvas = defaultdict(int)

    for c in claims:
        for xy in c.area():
            canvas[xy] += 1

    return sum(1 for val in canvas.values() if val > 1)


def find_single_not_overlapping(claims):
    overlaps = set()

    for c1 in claims:
        for c2 in (c for c in claims if c is not c1):
            if check_overlap(c1, c2):
                overlaps.update((c1, c2))

    return set(claims).difference(overlaps).pop()


if __name__ == "__main__":
    with open("_03_no_matter_how_you_slice_it.txt") as file:
        claims = parse(line.strip() for line in file.readlines())

        print(f"part 1: {find_overlapping_area(claims)}")
        print(f"part 2: {find_single_not_overlapping(claims).id}")

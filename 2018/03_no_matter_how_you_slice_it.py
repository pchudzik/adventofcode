import re
from collections import defaultdict


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
    with open("03_no_matter_how_you_slice_it.txt") as file:
        claims = parse(line.strip() for line in file.readlines())

        print(f"part 1: {find_overlapping_area(claims)}")
        print(f"part 2: {find_single_not_overlapping(claims).id}")

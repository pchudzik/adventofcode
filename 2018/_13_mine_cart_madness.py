r"""
--- Day 13: Mine Cart Madness ---

A crop of this size requires significant logistics to transport produce, soil, fertilizer, and so on. The Elves are very
busy pushing things around in carts on some kind of rudimentary system of tracks they've come up with.

Seeing as how cart-and-track systems don't appear in recorded history for another 1000 years, the Elves seem to be
making this up as they go along. They haven't even figured out how to avoid collisions yet.

You map out the tracks (your puzzle input) and see where you can help.

Tracks consist of straight paths (| and -), curves (/ and \), and intersections (+). Curves connect exactly two
perpendicular pieces of track; for example, this is a closed loop:

/----\
|    |
|    |
\----/

Intersections occur when two perpendicular paths cross. At an intersection, a cart is capable of turning left, turning
right, or continuing straight. Here are two loops connected by two intersections:

/-----\
|     |
|  /--+--\
|  |  |  |
\--+--/  |
   |     |
   \-----/

Several carts are also on the tracks. Carts always face either up (^), down (v), left (<), or right (>). (On your
initial map, the track under each cart is a straight path matching the direction the cart is facing.)

Each time a cart has the option to turn (by arriving at any intersection), it turns left the first time, goes straight
the second time, turns right the third time, and then repeats those directions starting again with left the fourth time,
straight the fifth time, and so on. This process is independent of the particular intersection at which the cart has
arrived - that is, the cart has no per-intersection memory.

Carts all move at the same speed; they take turns moving a single step at a time. They do this based on their current
location: carts on the top row move first (acting from left to right), then carts on the second row move (again from
left to right), then carts on the third row, and so on. Once each cart has moved one step, the process repeats; each of
these loops is called a tick.

For example, suppose there are two carts on a straight track:

|  |  |  |  |
v  |  |  |  |
|  v  v  |  |
|  |  |  v  X
|  |  ^  ^  |
^  ^  |  |  |
|  |  |  |  |

First, the top cart moves. It is facing down (v), so it moves down one square. Second, the bottom cart moves. It is
facing up (^), so it moves up one square. Because all carts have moved, the first tick ends. Then, the process repeats,
starting with the first cart. The first cart moves down, then the second cart moves up - right into the first cart,
colliding with it! (The location of the crash is marked with an X.) This ends the second and last tick.

Here is a longer example:

/->-\
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/-->\
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \->--/
  \------/

/---v
|   |  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+>-/
  \------/

/---\
|   v  /----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-+->/
  \------/

/---\
|   |  /----\
| /->--+-\  |
| | |  | |  |
\-+-/  \-+--^
  \------/

/---\
|   |  /----\
| /-+>-+-\  |
| | |  | |  ^
\-+-/  \-+--/
  \------/

/---\
|   |  /----\
| /-+->+-\  ^
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /----<
| /-+-->-\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /---<\
| /-+--+>\  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /--<-\
| /-+--+-v  |
| | |  | |  |
\-+-/  \-+--/
  \------/

/---\
|   |  /-<--\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/

/---\
|   |  /<---\
| /-+--+-\  |
| | |  | |  |
\-+-/  \-<--/
  \------/

/---\
|   |  v----\
| /-+--+-\  |
| | |  | |  |
\-+-/  \<+--/
  \------/

/---\
|   |  /----\
| /-+--v-\  |
| | |  | |  |
\-+-/  ^-+--/
  \------/

/---\
|   |  /----\
| /-+--+-\  |
| | |  X |  |
\-+-/  \-+--/
  \------/

After following their respective paths for a while, the carts eventually crash. To help prevent crashes, you'd like to
know the location of the first crash. Locations are given in X,Y coordinates, where the furthest left column is X=0 and
the furthest top row is Y=0:

           111
 0123456789012
0/---\
1|   |  /----\
2| /-+--+-\  |
3| | |  X |  |
4\-+-/  \-+--/
5  \------/

In this example, the location of the first crash is 7,3.

Your puzzle answer was 116,91.

--- Part Two ---

There isn't much you can do to prevent crashes in this ridiculous system. However, by predicting the crashes, the Elves
know where to be in advance and instantly remove the two crashing carts the moment any crash occurs.

They can proceed like this for a while, but eventually, they're going to run out of carts. It could be useful to figure
out where the last cart that hasn't crashed will end up.

For example:

/>-<\
|   |
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/

/---\
|   |
| v-+-\
| | | |
\-+-/ |
  |   |
  ^---^

/---\
|   |
| /-+-\
| v | |
\-+-/ |
  ^   ^
  \---/

/---\
|   |
| /-+-\
| | | |
\-+-/ ^
  |   |
  \---/

After four very expensive crashes, a tick ends with only one cart remaining; its final location is 6,4.

What is the location of the last cart at the end of the first tick where it is the only cart left?

Your puzzle answer was 8,23.

Both parts of this puzzle are complete! They provide two gold stars: **
"""
import enum


@enum.unique
class Direction(enum.Enum):
    north = "^"
    east = ">"
    south = "v"
    west = "<"


class Track:
    def __init__(self, track: str):
        self.track = track \
            .replace("^", "|") \
            .replace("v", "|") \
            .replace(">", "-") \
            .replace("<", "-") \
            .split("\n")

    def possible_moves(self, current_position):
        x, y = current_position
        node = self.track[y][x]
        if node == "|":
            return {
                Direction.north: (x, y - 1),
                Direction.south: (x, y + 1)
            }
        elif node == "-":
            return {
                Direction.east: (x + 1, y),
                Direction.west: (x - 1, y)
            }
        elif node == "/":
            if self.is_track((x + 1, y), "-+"):  # south to east
                return {
                    Direction.north: (x + 1, y),
                    Direction.west: (x, y + 1)
                }
            elif self.is_track((x - 1, y), "-+"):  # west to north
                return {
                    Direction.south: (x - 1, y),
                    Direction.east: (x, y - 1)
                }
            else:
                raise ValueError(f"Unexpected / curve at {x + 1, y + 1}")
        elif node == "\\":
            if self.is_track((x, y + 1), "|+"):  # south to west
                return {
                    Direction.north: (x - 1, y),
                    Direction.east: (x, y + 1)
                }
            elif self.is_track((x + 1, y), "-+"):  # east to north
                return {
                    Direction.south: (x + 1, y),
                    Direction.west: (x, y - 1)
                }
            else:
                raise ValueError(f"Unexpected \\ curve at {x + 1, y + 1}")
        elif node == "+":
            return {
                Direction.north: (x, y - 1),
                Direction.east: (x + 1, y),
                Direction.south: (x, y + 1),
                Direction.west: (x - 1, y),
            }
        else:
            raise ValueError(f"{x + 1, y + 1} is out of the track")

    def is_track(self, position, expected):
        if self._is_on_track(position):
            x, y = position
            return self.track[y][x] in expected
        return False

    def _is_on_track(self, point):
        x, y = point
        if 0 <= y < len(self.track):
            if 0 <= x < len(self.track[y]):
                return self.track[y][x] != " "

        return False


class Cart:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.intersection_number = 0

    def __repr__(self):
        return str(self.position) + " " + str(self.direction.value)

    def move(self, track):
        possible_moves = track.possible_moves(self.position)
        if track.is_track(self.position, "-") or track.is_track(self.position, "|"):
            self.position = possible_moves[self.direction]
        elif track.is_track(self.position, "/"):
            moves = {
                Direction.north: Direction.east,
                Direction.east: Direction.north,
                Direction.south: Direction.west,
                Direction.west: Direction.south,
            }
            self.position = possible_moves[self.direction]
            self.direction = moves[self.direction]
        elif track.is_track(self.position, "\\"):
            moves = {
                Direction.north: Direction.west,
                Direction.west: Direction.north,
                Direction.south: Direction.east,
                Direction.east: Direction.south,
            }
            self.position = possible_moves[self.direction]
            self.direction = moves[self.direction]
        elif track.is_track(self.position, "+"):
            possible_moves = track.possible_moves(self.position)
            moves = {
                Direction.north: {
                    0: Direction.west,
                    1: Direction.north,
                    2: Direction.east
                },
                Direction.south: {
                    0: Direction.east,
                    1: Direction.south,
                    2: Direction.west
                },
                Direction.east: {
                    0: Direction.north,
                    1: Direction.east,
                    2: Direction.south
                },
                Direction.west: {
                    0: Direction.south,
                    1: Direction.west,
                    2: Direction.north
                }
            }
            self.position = possible_moves[moves[self.direction][self.intersection_number % 3]]
            self.direction = moves[self.direction][self.intersection_number % 3]
            self.intersection_number += 1


def simulator(track, carts):
    while True:
        carts = carts_move_order(carts)
        for cart in carts:
            cart.move(track)
            collisions = detect_collisions(carts)
            if len(collisions) > 0:
                return collisions[0]


def simulator_last_cart_standing(track, carts: list):
    while len(carts) > 1:
        collisions = []
        carts = carts_move_order(carts)
        for cart in carts:
            if cart.position not in collisions:
                cart.move(track)
                collisions += set(detect_collisions(carts))

        carts_to_remove = [c for c in carts if c.position in collisions]
        for c in carts_to_remove:
            carts.remove(c)

    return carts[0].position


def carts_move_order(carts):
    return sorted(
        carts,
        key=lambda c: c.position[0] * 100_000 + c.position[1])


def detect_collisions(carts):
    carts_on_track = set()
    collided = []
    for cart in carts:
        if cart.position in carts_on_track:
            collided.append(cart.position)
        carts_on_track.add(cart.position)

    return collided


def parse(puzzle: str):
    puzzle = puzzle.split("\n")

    carts = []
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            try:
                carts.append(Cart(
                    (x, y),
                    Direction(puzzle[y][x])))
            except ValueError:
                continue

    return carts


if __name__ == "__main__":
    with open("_13_mine_cart_madness.txt") as file:
        puzzle = "".join(file.readlines())
        track = Track(puzzle)
        carts_p1 = parse(puzzle)
        carts_p2 = parse(puzzle)

        collision = simulator(track, carts_p1)
        last_cart_standing = simulator_last_cart_standing(track, carts_p2)
        print(f"part 1: {collision[0], collision[1]}")
        print(f"part 2: {last_cart_standing[0], last_cart_standing[1]}")

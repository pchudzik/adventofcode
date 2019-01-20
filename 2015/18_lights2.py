"""
--- Day 18: Like a GIF For Your Yard ---

After the million lights incident, the fire code has gotten stricter: now, at most ten thousand lights are allowed. You
arrange them in a 100x100 grid.

Never one to let you down, Santa again mails you instructions on the ideal lighting configuration. With so few lights,
he says, you'll have to resort to animation.

Start by setting your lights to the included initial configuration (your puzzle input). A # means "on", and a . means
"off".

Then, animate your grid in steps, where each step decides the next configuration based on the current one. Each light's
next state (either on or off) depends on its current state and the current states of the eight lights adjacent to it
(including diagonals). Lights on the edge of the grid might have fewer than eight neighbors; the missing ones always
count as "off".

For example, in a simplified 6x6 grid, the light marked A has the neighbors numbered 1 through 8, and the light marked
B, which is on an edge, only has the neighbors marked 1 through 5:

1B5...
234...
......
..123.
..8A4.
..765.

The state a light should have next is based on its current state (on or off) plus the number of neighbors that are on:

A light which is on stays on when 2 or 3 neighbors are on, and turns off otherwise.
A light which is off turns on if exactly 3 neighbors are on, and stays off otherwise.
All of the lights update simultaneously; they all consider the same current state before moving to the next.

Here's a few steps from an example configuration of another 6x6 grid:

Initial state:
.#.#.#
...##.
#....#
..#...
#.#..#
####..

After 1 step:
..##..
..##.#
...##.
......
#.....
#.##..

After 2 steps:
..###.
......
..###.
......
.#....
.#....

After 3 steps:
...#..
......
...#..
..##..
......
......

After 4 steps:
......
......
..##..
..##..
......
......
After 4 steps, this example has four lights on.

In your grid of 100x100 lights, given your initial configuration, how many lights are on after 100 steps?

Your puzzle answer was 768.

--- Part Two ---

You flip the instructions over; Santa goes on to point out that this is all just an implementation of Conway's Game of
Life. At least, it was, until you notice that something's wrong with the grid of lights you bought: four lights, one in
each corner, are stuck on and can't be turned off. The example above will actually run like this:

Initial state:
##.#.#
...##.
#....#
..#...
#.#..#
####.#

After 1 step:
#.##.#
####.#
...##.
......
#...#.
#.####

After 2 steps:
#..#.#
#....#
.#.##.
...##.
.#..##
##.###

After 3 steps:
#...##
####.#
..##.#
......
##....
####.#

After 4 steps:
#.####
#....#
...#..
.##...
#.....
#.#..#

After 5 steps:
##.###
.##..#
.##...
.##...
#.#...
##...#
After 5 steps, this example now has 17 lights on.

In your grid of 100x100 lights, given your initial configuration, but with the four corners always in the on state, how
many lights are on after 100 steps?

Your puzzle answer was 781.
"""


def parse_lights_input(lights_input, stuck=[]):
    result = []
    for x in range(len(lights_input)):
        lights_row = []
        result.append(lights_row)
        for y in range(len(lights_input[x])):
            lights_row.append(SingleLight(
                lights_input[x][y] == "#",
                coordinates=(x, y),
                is_stuck=(x, y) in stuck))
    return Lights(result)


def count_lights(lights, state):
    return len(list(
        filter(
            lambda l: l.is_lit == state,
            lights)))


class SingleLight:
    ON = True
    OFF = False

    def __init__(self, is_lit, coordinates=(0, 0), is_stuck=False):
        self.is_lit = is_stuck or is_lit
        self.next_state = None
        self.coordinates = coordinates
        self.is_stuck = is_stuck

    def __repr__(self):
        return "#" if self.is_lit else "."

    def calculate_next_state(self, neighbours):
        on_neighbours = count_lights(neighbours, SingleLight.ON)

        if self.is_stuck:
            self.next_state = SingleLight.ON
        else:
            self.next_state = on_neighbours in (2, 3) if self.is_lit else on_neighbours == 3

        return self.next_state

    def transition(self):
        self.is_lit = self.next_state
        self.next_state = None

    def neighbours(self, grid_size):
        x, y = self.coordinates
        max_x, max_y = grid_size

        def is_in_range(x, y):
            return 0 <= x < max_x and 0 <= y < max_y

        return filter(
            lambda coordinates: is_in_range(*coordinates),
            (
                # @formatter:off
                (x - 1, y + 1),
                (x,     y + 1),
                (x + 1, y + 1),
                (x + 1, y),
                (x + 1, y - 1),
                (x,     y - 1),
                (x - 1, y - 1),
                (x - 1, y)
                # @formatter:on
            ))


class Lights:

    def __init__(self, all_lights):
        self.all_lights = all_lights

    @property
    def size(self):
        return len(self.all_lights), len(self.all_lights[0])

    @property
    def number_of_on(self):
        return count_lights(self.__all_lights(), SingleLight.ON)

    @property
    def number_of_off(self):
        return count_lights(self.__all_lights(), SingleLight.OFF)

    def next_state(self):
        x_size, y_size = self.size
        for x in range(x_size):
            for y in range(y_size):
                light = self.all_lights[x][y]
                light.calculate_next_state(
                    self.all_lights[x][y]
                    for x, y
                    in self[x, y].neighbours(self.size))

        for light in self.__all_lights():
            light.transition()

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.all_lights[x][y]

    def neighbours(self, x, y):
        neighbours_coordinates = self.all_lights[x][y].neighbours(self.size)
        return [self.all_lights[x][y] for x, y in neighbours_coordinates]

    def __all_lights(self):
        return (light for lights_row in self.all_lights for light in lights_row)

    def __repr__(self):
        result = ""
        for lights_row in self.all_lights:
            for light in lights_row:
                result += str(light)
            result += "\n"

        return result.strip()


if __name__ == "__main__":
    with open("18_lights2.txt") as file:
        lines = [line.strip() for line in file.readlines()]
        lights = parse_lights_input(lines)
        stuck_lights = parse_lights_input(lines, stuck=[
            (0, 0), (0, 99),
            (99, 0), (99, 99)
        ])

        for x in range(100):
            lights.next_state()
            stuck_lights.next_state()

        print("Number of lights still lit after 100 frames", lights.number_of_on)
        print(
            "Number of lights still lit after 100 frames with corner lights stuck",
            stuck_lights.number_of_on)

"""
--- Day 22: Sporifica Virus ---

Diagnostics indicate that the local grid computing cluster has been contaminated with the Sporifica Virus. The grid
computing cluster is a seemingly-infinite two-dimensional grid of compute nodes. Each node is either clean or infected
by the virus.

To prevent overloading the nodes (which would render them useless to the virus) or detection by system administrators,
exactly one virus carrier moves through the network, infecting or cleaning nodes as it moves. The virus carrier is
always located on a single node in the network (the current node) and keeps track of the direction it is facing.

To avoid detection, the virus carrier works in bursts; in each burst, it wakes up, does some work, and goes back to
sleep. The following steps are all executed in order one time each burst:

* If the current node is infected, it turns to its right. Otherwise, it turns to its left. (Turning is done in-place;
  the current node does not change.)
* If the current node is clean, it becomes infected. Otherwise, it becomes cleaned. (This is done after the node is
  considered for the purposes of changing direction.)
* The virus carrier moves forward one node in the direction it is facing.

Diagnostics have also provided a map of the node infection status (your puzzle input). Clean nodes are shown as .;
infected nodes are shown as #. This map only shows the center of the grid; there are many more nodes beyond those shown,
but none of them are currently infected.

The virus carrier begins in the middle of the map facing up.

For example, suppose you are given a map like this:

..#
#..
...

Then, the middle of the infinite grid looks like this, with the virus carrier's position marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on a clean node, so it turns left, infects the node, and moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]# . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on an infected node, so it turns right, cleans the node, and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . . # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Four times in a row, the virus carrier finds a clean, infects it, turns left, and moves forward, ending in the same
place and still facing up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . #[#]. # . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Now on the same node as before, it sees an infection, which causes it to turn right, clean the node, and move forward:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . # .[.]# . . .
. . # # # . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

After the above actions, a total of 7 bursts of activity had taken place. Of them, 5 bursts of activity caused an
infection.

After a total of 70, the grid looks like this, with the virus carrier facing up:

. . . . . # # . .
. . . . # . . # .
. . . # . . . . #
. . # . #[.]. . #
. . # . # . . # .
. . . . . # # . .
. . . . . . . . .
. . . . . . . . .

By this time, 41 bursts of activity caused an infection (though most of those nodes have since been cleaned).

After a total of 10000 bursts of activity, 5587 bursts will have caused an infection.

Given your actual map, after 10000 bursts of activity, how many bursts cause a node to become infected? (Do not count
nodes that begin infected.)

Your puzzle answer was 5411.

--- Part Two ---

As you go to remove the virus from the infected nodes, it evolves to resist your attempt.

Now, before it infects a clean node, it will weaken it to disable your defenses. If it encounters an infected node, it
will instead flag the node to be cleaned in the future. So:

* Clean nodes become weakened.
* Weakened nodes become infected.
* Infected nodes become flagged.
* Flagged nodes become clean.

Every node is always in exactly one of the above states.

The virus carrier still functions in a similar way, but now uses the following logic during its bursts of action:

* Decide which way to turn based on the current node:
  * If it is clean, it turns left.
  * If it is weakened, it does not turn, and will continue moving in the same direction.
  * If it is infected, it turns right.
  * If it is flagged, it reverses direction, and will go back the way it came.
* Modify the state of the current node, as described above.
* The virus carrier moves forward one node in the direction it is facing.

Start with the same map (still using . for clean and # for infected) and still with the virus carrier starting in the
middle and facing up.

Using the same initial state as the previous example, and drawing weakened as W and flagged as F, the middle of the
infinite grid looks like this, with the virus carrier's position again marked with [ ]:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . . #[.]. . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

This is the same as before, since no initial nodes are weakened or flagged. The virus carrier is on a clean node, so it
still turns left, instead weakens the node, and moves left:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . # . . .
. . .[#]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The virus carrier is on an infected node, so it still turns right, instead flags the node, and moves up:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . .[.]. # . . .
. . . F W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

This process repeats three more times, ending on the previously-flagged node and facing right:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. . W[F]W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Finding a flagged node, it reverses direction and cleans the node:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
. .[W]. W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

The weakened node becomes infected, and it continues in the same direction:

. . . . . . . . .
. . . . . . . . .
. . . . . . . . .
. . W W . # . . .
.[.]# . W . . . .
. . . . . . . . .
. . . . . . . . .
. . . . . . . . .

Of the first 100 bursts, 26 will result in infection. Unfortunately, another feature of this evolved virus is speed; of
the first 10000000 bursts, 2511944 will result in infection.

Given your actual map, after 10000000 bursts of activity, how many bursts cause a node to become infected? (Do not count
nodes that begin infected.)

Your puzzle answer was 2511416.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Grid:
    def __init__(self, *, infected=None):
        self.infected = set(infected) if infected else set()
        self.started_infection = 0

    def is_infected(self, position):
        return position in self.infected

    def burst(self, position):
        if self.is_infected(position):
            self._cure(position)
        else:
            self._infect(position)

    def next_move(self, current_position, previous_position):
        if self.is_infected(current_position):
            return self._go_right(current_position, previous_position)
        else:
            return self._go_left(current_position, previous_position)

    def _infect(self, position):
        self.infected.add(position)
        self.started_infection += 1

    def _cure(self, position):
        self.infected.remove(position)

    def _go_right(self, current, previous):
        """
        0,0 | 0,1 | 0,2
        1,0 | 1,1 | 1,2
        2,0 | 2,1,| 2,2
        """

        direction = self._get_direction(current, previous)
        x, y = current
        if direction == "north":
            return x, y + 1
        elif direction == "south":
            return x, y - 1
        elif direction == "east":
            return x + 1, y
        elif direction == "west":
            return x - 1, y

    def _go_left(self, current, previous):
        """
        0,0 | 0,1 | 0,2
        1,0 | 1,1 | 1,2
        2,0 | 2,1,| 2,2
        """

        direction = self._get_direction(current, previous)
        x, y = current
        if direction == "north":
            return x, y - 1
        elif direction == "south":
            return x, y + 1
        elif direction == "west":
            return x + 1, y
        elif direction == "east":
            return x - 1, y

    def _get_direction(self, current, previous):
        x, y = current
        xp, yp = previous

        if xp == x:  # moving horizontally
            if yp < y:
                return "east"
            else:
                return "west"
        elif yp == y:  # moving vertically
            if xp < x:
                return "south"
            else:
                return "north"


class Grid2(Grid):
    def __init__(self, *, infected=None, weakened=None, flagged=None):
        Grid.__init__(self, infected=infected)
        self.weakened = set(weakened) if weakened else set()
        self.flagged = set(flagged) if flagged else set()

    def burst(self, position):
        if self.is_flagged(position):
            self._clean(position)
        elif self.is_infected(position):
            self._flag(position)
        elif self.is_weakened(position):
            self._infect(position)
        else:
            self._weaken(position)

    def is_weakened(self, position):
        return position in self.weakened

    def is_flagged(self, position):
        return position in self.flagged

    def next_move(self, current_position, previous_position):
        if self.is_weakened(current_position):
            return self._go_the_same_direction(current_position, previous_position)
        elif self.is_infected(current_position):
            return self._go_right(current_position, previous_position)
        elif self.is_flagged(current_position):
            return self._go_reverse(previous_position)
        else:
            return self._go_left(current_position, previous_position)

    def _clean(self, position):
        self.flagged.remove(position)

    def _flag(self, position):
        self.infected.remove(position)
        self.flagged.add(position)

    def _infect(self, position):
        self.weakened.remove(position)
        self.infected.add(position)
        self.started_infection += 1

    def _weaken(self, position):
        self.weakened.add(position)

    def _go_the_same_direction(self, current, previous):
        direction = self._get_direction(current, previous)
        x, y = current

        if direction == "north":
            return x - 1, y
        elif direction == "south":
            return x + 1, y
        elif direction == "west":
            return x, y - 1
        elif direction == "east":
            return x, y + 1

    def _go_reverse(self, previous):
        return previous


def parse_input(input):
    nodes = set()

    for row in range(len(input)):
        for column in range(len(input[row])):
            state = input[row][column]
            if state == "#":
                nodes.add((row, column))

    return nodes


def find_center(input):
    center = int(len(input) / 2)
    return center, center


def virus_carrier(iterations, starting_point, grid):
    current = starting_point
    previous = starting_point[0] + 1, starting_point[1]

    for i in range(iterations):
        current, previous = burst(current, previous, grid)


def burst(current, previous, grid):
    next = grid.next_move(current, previous)
    grid.burst(current)
    return next, current


if __name__ == "__main__":
    with open("22_sporifica_virus.txt") as file:
        lines = list(map(str.strip, file.readlines()))
        nodes = parse_input(lines)
        grid1 = Grid(infected=nodes)
        grid2 = Grid2(infected=nodes)
        center = find_center(lines)

        virus_carrier(10_000, center, grid1)
        print(f"part 1: {grid1.started_infection}")

        virus_carrier(10_000_000, center, grid2)
        print(f"part 2: {grid2.started_infection}")

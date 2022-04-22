"""
--- Day 24: Electromagnetic Moat ---

The CPU itself is a large, black building surrounded by a bottomless pit. Enormous metal tubes extend outward from the
side of the building at regular intervals and descend down into the void. There's no way to cross, but you need to get
inside.

No way, of course, other than building a bridge out of the magnetic components strewn about nearby.

Each component has two ports, one on each end. The ports come in all different types, and only matching types can be
connected. You take an inventory of the components by their port types (your puzzle input). Each port is identified by
the number of pins it uses; more pins mean a stronger connection for your bridge. A 3/7 component, for example, has a
type-3 port on one side, and a type-7 port on the other.

Your side of the pit is metallic; a perfect surface to connect a magnetic, zero-pin port. Because of this, the first
port you use must be of type 0. It doesn't matter what type of port you end with; your goal is just to make the bridge
as strong as possible.

The strength of a bridge is the sum of the port types in each component. For example, if your bridge is made of
components 0/3, 3/7, and 7/4, your bridge has a strength of 0+3 + 3+7 + 7+4 = 24.

For example, suppose you had the following components:

0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10

With them, you could make the following valid bridges:

0/1
0/1--10/1
0/1--10/1--9/10
0/2
0/2--2/3
0/2--2/3--3/4
0/2--2/3--3/5
0/2--2/2
0/2--2/2--2/3
0/2--2/2--2/3--3/4
0/2--2/2--2/3--3/5

(Note how, as shown by 10/1, order of ports within a component doesn't matter. However, you may only use each port on a
component once.)

Of these bridges, the strongest one is 0/1--10/1--9/10; it has a strength of 0+1 + 1+10 + 10+9 = 31.

What is the strength of the strongest bridge you can make with the components you have available?

Your puzzle answer was 2006.

--- Part Two ---

The bridge you've built isn't long enough; you can't jump the rest of the way.

In the example above, there are two longest bridges:

0/2--2/2--2/3--3/4
0/2--2/2--2/3--3/5

Of them, the one which uses the 3/5 component is stronger; its strength is 0+2 + 2+2 + 2+3 + 3+5 = 19.

What is the strength of the longest bridge you can make? If you can make multiple bridges of the longest length, pick
the strongest one.

Your puzzle answer was 1994.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


class Bridge:
    def __init__(self, left_pin, right_pin):
        self.pins = (left_pin, right_pin)

    @property
    def strength(self):
        return sum(self.pins)

    def compatible(self, other):
        return other in self.pins

    def remaining_pin(self, used):
        if self.pins[0] == used:
            return self.pins[1]
        elif self.pins[1] == used:
            return self.pins[0]

    def __eq__(self, other):
        if not isinstance(other, Bridge):
            return NotImplemented

        return self.pins == other.pins

    def __hash__(self):
        return hash(self.pins)

    def __repr__(self):
        return "/".join(map(str, self.pins))


def parse(puzzle):
    result = []
    for row in puzzle:
        left, right = row.split("/")
        result.append(Bridge(int(left), int(right)))
    return result


def find_available_bridges(bridges):
    starting_bridges = [(0, bridge) for bridge in bridges if 0 in bridge.pins]
    stack = list()

    for bridge in starting_bridges:
        stack.append(([bridge], [bridge for bridge in bridges if 0 not in bridge.pins]))

    result = set()
    while stack:
        connection, remaining_bridges = stack.pop()
        result.add(tuple([pin_bridge[1] for pin_bridge in connection]))

        used_pin, bridge = connection[-1]
        available_pin = bridge.remaining_pin(used_pin)

        for compatible in find_compatible_bridges(available_pin, remaining_bridges):
            next_connection = connection + [(available_pin, compatible)]
            remaining = [bridge for bridge in remaining_bridges if bridge != compatible]
            stack.append((next_connection, remaining))

    return result


def find_compatible_bridges(pin, bridges):
    return [bridge for bridge in bridges if bridge.compatible(pin)]


def path_strength(bridges):
    return sum(map(lambda b: b.strength, bridges))


def find_strongest_bridge(bridges):
    return max(map(path_strength, bridges))


def find_longest_and_strongest_bridge(bridges):
    longest_bridge = max(map(len, bridges))
    longest_paths = [path for path in bridges if len(path) == longest_bridge]
    return find_strongest_bridge(longest_paths)


if __name__ == "__main__":
    with open("_24_electromagnetic_moat.txt") as file:
        bridges = parse(map(str.strip, file.readlines()))
        all_bridges = find_available_bridges(bridges)
        print(f"part 1: {find_strongest_bridge(all_bridges)}")
        print(f"part 2: {find_longest_and_strongest_bridge(all_bridges)}")

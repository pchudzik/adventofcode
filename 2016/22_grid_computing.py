import re


class Node:
    def __init__(self, x, y, size, used):
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.used = int(used)

    def can_transfer_to(self, other_node):
        if self.x == other_node.x and self.y == other_node.y:
            return False

        if self.used == 0:
            return False

        return self.used <= other_node.available

    @property
    def available(self):
        return self.size - self.used

    @property
    def usage(self):
        return round(self.used / self.size, 4)

    @staticmethod
    def parse(line):
        node = re.match(
            r"\/dev\/grid\/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T.*",
            line)

        return Node(
            *node.groups())


def parse_input():
    with open("22_grid_computing.txt") as file:
        next(file)
        next(file)
        return list(map(
            lambda line: Node.parse(line.strip()),
            file))


def find_pairs_viable_to_transfer(nodes):
    return set(filter(
        lambda x: x is not None,
        (
            (n1, n2)
            for n1 in nodes
            for n2 in nodes
            if n1.can_transfer_to(n2)
        )))


def print_grid(nodes):
    max_x = max(nodes, key=lambda n: n.x)
    max_y = max(nodes, key=lambda n: n.y)

    min_used = min(nodes, key=lambda n: n.used)

    for y in range(max_y.y + 1):
        for x in range(max_x.x + 1):
            node = next(filter(
                lambda n: n.x == x and n.y == y,
                nodes))

            display = ".."
            if node.used == 0:
                display = "EE"
            if node.used > min_used.available:
                display = "##"
            print(display, " ", sep="", end="")
        print("")


def print_initial_moves():
    print("""First moves:
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 30 31
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 29 ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 28 ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 27 ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 26 ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 19 20 21 22 23 24 25 ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 18 ## ## ## ## ## ## ##
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 17 16 15 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 14 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 13 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 12 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 11 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 10 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 09 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 08 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 07 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 06 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 05 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 04 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 03 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 02 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. 01 .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. EE .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..
.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..""")


if __name__ == "__main__":
    nodes = parse_input()
    print(f"part 1: {len(find_pairs_viable_to_transfer(nodes))}")

    max_x = max(nodes, key=lambda n: n.x)
    print(f"part 2: 181 [number of moves to position ({max_x.x}, 0) + (5 * {max_x.x}-1)]")

    print("\n\nThe grid:")
    print_grid(nodes)
    print_initial_moves()

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


if __name__ == "__main__":
    nodes = parse_input()
    print(f"part 1: {len(find_pairs_viable_to_transfer(nodes))}")

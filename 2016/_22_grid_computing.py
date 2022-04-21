import re

"""
--- Day 22: Grid Computing ---

You gain access to a massive storage cluster arranged in a grid; each storage node is only connected to the four nodes
directly adjacent to it (three if the node is on an edge, two if it's in a corner).

You can directly access data only on node /dev/grid/node-x0-y0, but you can perform some limited actions on the other
nodes:

You can get the disk usage of all nodes (via df). The result of doing this is in your puzzle input.

You can instruct a node to move (not copy) all of its data to an adjacent node (if the destination node has enough space
to receive the data). The sending node is left empty after this operation.

Nodes are named by their position: the node named node-x10-y10 is adjacent to nodes node-x9-y10, node-x11-y10,
node-x10-y9, and node-x10-y11.

Before you begin, you need to understand the arrangement of data on these nodes. Even though you can only move data
between directly connected nodes, you're going to need to rearrange a lot of the data to get access to the data you
need. Therefore, you need to work out how you might be able to shift data around.

To do this, you'd like to count the number of viable pairs of nodes. A viable pair is any two nodes (A,B), regardless of
whether they are directly connected, such that:

Node A is not empty (its Used is not zero).
Nodes A and B are not the same node.
The data on node A (its Used) would fit on node B (its Avail).
How many viable pairs of nodes are there?

Your puzzle answer was 952.

--- Part Two ---

Now that you have a better understanding of the grid, it's time to get to work.

Your goal is to gain access to the data which begins in the node with y=0 and the highest x (that is, the node in the
top-right corner).

For example, suppose you have the following grid:

Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%

In this example, you have a storage grid 3 nodes wide and 3 nodes tall. The node you can access directly, node-x0-y0, is
almost full. The node containing the data you want to access, node-x2-y0 (because it has y=0 and the highest x value),
contains 6 terabytes of data - enough to fit on your node, if only you could make enough space to move it there.

Fortunately, node-x1-y1 looks like it has enough free space to enable you to move some of this data around. In fact, it
seems like all of the nodes have enough space to hold any node's data (except node-x0-y2, which is much larger, very
full, and not moving any time soon). So, initially, the grid's capacities and connections look like this:

( 8T/10T) --  7T/ 9T -- [ 6T/10T]
    |           |           |
  6T/11T  --  0T/ 8T --   8T/ 9T
    |           |           |
 28T/32T  --  7T/11T --   6T/ 9T
 
The node you can access directly is in parentheses; the data you want starts in the node marked by square brackets.

In this example, most of the nodes are interchangable: they're full enough that no other node's data would fit, but
small enough that their data could be moved around. Let's draw these nodes as .. The exceptions are the empty node,
which we'll draw as _, and the very large, very full node, which we'll draw as #. Let's also draw the goal data as G.
Then, it looks like this:

(.) .  G
 .  _  .
 #  .  .
 
The goal is to move the data in the top right, G, to the node in parentheses. To do this, we can issue some commands to
the grid and rearrange the data:

Move data from node-y0-x1 to node-y1-x1, leaving node node-y0-x1 empty:

(.) _  G
 .  .  .
 #  .  .

Move the goal data from node-y0-x2 to node-y0-x1:

(.) G  _
 .  .  .
 #  .  .

At this point, we're quite close. However, we have no deletion command, so we have to move some more data around. So,
next, we move the data from node-y1-x2 to node-y0-x2:

(.) G  .
 .  .  _
 #  .  .

Move the data from node-y1-x1 to node-y1-x2:

(.) G  .
 .  _  .
 #  .  .

Move the data from node-y1-x0 to node-y1-x1:

(.) G  .
 _  .  .
 #  .  .

Next, we can free up space on our node by moving the data from node-y0-x0 to node-y1-x0:

(_) G  .
 .  .  .
 #  .  .

Finally, we can access the goal data by moving the it from node-y0-x1 to node-y0-x0:

(G) _  .
 .  .  .
 #  .  .

So, after 7 steps, we've accessed the data we want. Unfortunately, each of these moves takes time, and we need to be
efficient:

What is the fewest number of steps required to move your goal data to node-x0-y0?

Your puzzle answer was 181.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


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
    with open("_22_grid_computing.txt") as file:
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

from functools import reduce
from collections import deque

"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and
watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources that
are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk, the state
of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128 bits
which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row. For
example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of flqrgnkx-0,
the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4
bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary value,
high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins with
a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used
squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#   
....#.#.   
#.#.##.#   
.##.#...   
##..#..#   
.#...#..   
##.#.##.-->
|      |   
V      V   

In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?

Your puzzle answer was 8190.

--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all
adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own isolated
regions, while several adjacent squares all count as a single region.

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the
squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are
present.

How many regions are present given your key string?

Your puzzle answer was 1134.

Both parts of this puzzle are complete! They provide two gold stars: **
"""

max_x = 128
max_y = 128


def _single_round(items, positions, current_position=0, skip=0):
    for position in positions:
        item_indexes_to_rotate_src = _find_range(items, current_position, position)
        item_indexes_to_rotate_dst = list(reversed(item_indexes_to_rotate_src))
        tmp = dict((index, items[index]) for index in item_indexes_to_rotate_src)
        for i in range(len(item_indexes_to_rotate_src)):
            src_index = item_indexes_to_rotate_src[i]
            dst_index = item_indexes_to_rotate_dst[i]
            items[dst_index] = tmp[src_index]

        current_position = _next_position(items, current_position, position, skip)
        skip += 1

    return items, current_position, skip


def knot_hash(puzzle):
    number_of_rounds = 64
    const_suffix = [17, 31, 73, 47, 23]

    lenghts = list(bytearray(puzzle, "utf8")) + const_suffix
    current_position = 0
    skip = 0

    items = list(range(256))
    for i in range(number_of_rounds):
        items, current_position, skip = _single_round(items, lenghts, current_position, skip)

    result_hex = "".join(_to_hex_string(_dense_hash(items)))
    return "".join(_to_bin(result_hex))


def _to_bin(items):
    return [
        "{0:04b}".format(int(item, 16))
        for item in items
    ]


def _to_hex_string(items):
    return [
        "{0:0{1}x}".format(item, 2)
        for item in items
    ]


def _dense_hash(items):
    word_size = 16
    items = [items[i:i + word_size] for i in range(0, len(items), word_size)]
    return [
        reduce(xor, characters)
        for characters in items
    ]


def xor(a, b):
    return a ^ b


def _next_position(puzzle, current_position, position, skip):
    index = current_position
    for i in range(position + skip):
        index += 1
        if index >= len(puzzle):
            index = 0

    return index


def _find_range(puzzle, current_position, position):
    item_indexes = []
    index = current_position
    for _ in range(position):
        if index >= len(puzzle):
            index = 0
        item_indexes.append(index)
        index += 1

    return item_indexes


def find_disk_layout(puzzle):
    return [knot_hash(f"{puzzle}-{i}") for i in range(max_x)]


def find_used_space(disk_layout):
    return sum(int(bit) for item in disk_layout for bit in item)


def _find_region_items(disk_layout, starting_point, already_found):
    to_check = deque()
    to_check.append(starting_point)
    region = set()

    def can_check(coordinate):
        x, y = coordinate
        return 0 <= x < max_x and 0 <= y < max_y \
               and coordinate not in already_found \
               and coordinate not in region \
               and coordinate not in to_check

    while to_check:
        x, y = to_check.popleft()
        if disk_layout[x][y] == "1":
            region.add((x, y))
            for coordinate in filter(can_check, [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]):
                to_check.append(coordinate)

    return region


def find_regions(disk_layout):
    in_any_region = set()
    found_regions = set()

    for x in range(max_x):
        for y in range(max_y):
            if (x, y) not in in_any_region and disk_layout[x][y] == "1":
                region = _find_region_items(disk_layout, (x, y), in_any_region)
                found_regions.add(frozenset(region))
                in_any_region.update(region)

    return len(found_regions)


if __name__ == "__main__":
    puzzle = "ffayrhll"
    disk_layout = find_disk_layout(puzzle)

    print(f"part 1: {find_used_space(disk_layout)}")
    print(f"part 2: {find_regions(disk_layout)}")

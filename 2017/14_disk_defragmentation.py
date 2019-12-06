from functools import reduce


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
    return [knot_hash(f"{puzzle}-{i}") for i in range(128)]


def find_used_space(disk_layout):
    return sum(int(bit) for item in disk_layout for bit in item)


def find_regions(puzzle):
    return 0


if __name__ == "__main__":
    puzzle = "ffayrhll"
    disk_layout = find_disk_layout(puzzle)

    print(f"part 1: {find_used_space(puzzle)}")

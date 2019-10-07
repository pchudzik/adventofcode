def rotate(items, positions):
    current_position = 0
    skip = 0
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

    return items


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


if __name__ == "__main__":
    positions = [63, 144, 180, 149, 1, 255, 167, 84, 125, 65, 188, 0, 2, 254, 229, 24]
    result = rotate(list(range(256)), positions)

    print(f"part1: {result[0] * result[1]}")

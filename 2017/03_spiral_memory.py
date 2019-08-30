def calculate_position(to_digit):
    if to_digit >= 1:
        yield 0, 0
    if to_digit >= 2:
        yield 1, 0

    x, y = 1, 1
    digit = 2
    direction = "right"
    while to_digit > digit:
        yield x, y
        digit += 1

        if x == y and x > 0 < y:  # top right corner
            direction = "left"
        elif abs(x) == y and x < 0 < y:  # top left corner
            direction = "down"
        elif x == y and x < 0 > y:  # bottom left corner
            direction = "right"
        elif x == abs(y) and x > 0 > y:  # bottom right corner
            if digit >= to_digit:
                break
            direction = "up"
            x += 1
            digit += 1
            yield x, y

        if direction == "right":
            x += 1
        if direction == "left":
            x -= 1
        if direction == "up":
            y += 1
        if direction == "down":
            y -= 1


def calculate_manhattan_distance(to_digit):
    # Manhattan Distance between two points (x1, y1) and (x2, y2) is: |x1 – x2| + |y1 – y2|
    last = None
    for coordinates in calculate_position(to_digit):
        last = coordinates

    return sum(map(abs, last))


if __name__ == "__main__":
    puzzle = 265149
    print(f"part1: {calculate_manhattan_distance(puzzle)}")

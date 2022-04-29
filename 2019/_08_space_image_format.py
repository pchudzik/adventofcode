from typing import Iterable, Generator

WIDTH = 25
HEIGHT = 6


def to_chunks(width: int, bytes: list) -> Generator[list, None, None]:
    for i in range(0, len(bytes), width):
        yield bytes[i:i + width]


def part1(image):
    def count_digits(digit: int, layer: Iterable[int]) -> int:
        return sum(1 if p == digit else 0 for p in layer)

    layers = to_chunks(WIDTH * HEIGHT, image)
    layer_with_fewest_zeros = min(layers, key=lambda layer: count_digits(0, layer))
    return count_digits(1, layer_with_fewest_zeros) * count_digits(2, layer_with_fewest_zeros)


def part2(image):
    black = 0
    white = 1
    transparent = 2

    layers = list(to_chunks(WIDTH * HEIGHT, image))
    image = []
    for i in range(WIDTH * HEIGHT):
        color = next(
            (
                pixel
                for layer in layers
                if (pixel := layer[i]) == black or pixel == white
            ),
            transparent
        )

        image.append(" " if color == black else "#")

    rows = ("".join(line) for line in to_chunks(WIDTH, image))
    return "\n".join(rows)


if __name__ == "__main__":
    with open("_08_space_image_format.txt") as file:
        puzzle = [int(c) for c in file.readline().strip()]
        print("part 1:", part1(puzzle))
        print("part 2:\n", part2(puzzle), sep="")

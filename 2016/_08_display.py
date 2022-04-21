import operator
from functools import reduce

"""
--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication after a
long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk). Then, it displays a code
on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how it
works. Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are your
puzzle input. The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three somewhat
peculiar operations:

* rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
* rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off
  the right end appear at the left end of the row.
* rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that would
  fall off the bottom appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

rect 3x2 creates a small rectangle in the top-left corner:
###....
###....
.......

rotate column x=1 by 1 rotates the second column down by one pixel:
#.#....
###....
.#.....

rotate row y=0 by 4 rotates the top row right by four pixels:
....#.#
###....
.#.....

rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the
top:
.#..#.#
#.#....
.#.....

As you can see, this display technology is extremely powerful, and will soon dominate the tiny-code-displaying-screen
market. That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did
work, how many pixels should be lit?

Your puzzle answer was 116.

--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is 5 pixels
wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

Your puzzle answer was UPOJFLBCEZ.
"""


class Display:
    def __init__(self, width, height, initial=None, lit_pixel="#", blank_pixel="."):
        self.width = width
        self.height = height
        self._lit_pixel = lit_pixel
        self._blank_pixel = blank_pixel
        self._display = [[False] * width for _ in range(height)] if initial is None else initial

    def execute(self, cmd):
        self._display = _cmd_parser(cmd)(self._clone())

    @property
    def display(self):
        return list(map(
            lambda row: "".join(self._lit_pixel if pixel else self._blank_pixel for pixel in row),
            (row for row in self._display)))

    @property
    def lit_pixels(self):
        return sum([reduce(operator.add, row) for row in self._display])

    def _clone(self):
        return [row[:] for row in self._display]

    def __repr__(self):
        return f"Display(width={self.width}, height={self.height}, initial={self._display})"


def _cmd_parser(cmd: str):
    if cmd.startswith("rect"):
        x, y = cmd.replace("rect ", "").split("x")
        return rect(int(x), int(y))
    elif cmd.startswith("rotate row"):
        column, pixels_count = cmd.replace("rotate row y=", "").split(" by ")
        return rotate_row(int(column), int(pixels_count))
    elif cmd.startswith("rotate column"):
        column, pixels_count = cmd.replace("rotate column x=", "").split(" by ")
        return rotate_column(int(column), int(pixels_count))
    else:
        raise NotImplemented("Invalid command")


def rect(width, height):
    def do_execute(display):
        for yc in range(height):
            for xc in range(width):
                display[yc][xc] = True
        return display

    return do_execute


def rotate_column(column, pixels_count):
    def transpose_display(display):
        return [[display[j][i] for j in range(len(display))] for i in range(len(display[0]))]

    def do_execute(display):
        transposed = transpose_display(display)
        result = rotate_row(column, pixels_count)(transposed)
        return transpose_display(result)

    return do_execute


def rotate_row(row, pixels_count):
    def do_execute(display):
        original = display[row]
        width = len(original)
        display[row] = [original[(p - pixels_count) % width] for p in range(width)]
        return display

    return do_execute


if __name__ == "__main__":
    with open("_08_display.txt") as file:
        cmds = file.readlines()
        display = Display(50, 6, lit_pixel="#", blank_pixel=" ")
        for cmd in cmds:
            display.execute(cmd.strip())

        print(f"p1 = {display.lit_pixels}")
        print("p2=\n", "\n".join(display.display), sep="")

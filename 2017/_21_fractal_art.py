"""
--- Day 21: Fractal Art ---

You find a program trying to generate some art. It uses a strange process that involves repeatedly enhancing the detail
of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on (#) or off (.). The program always
begins with this pattern:

.#.
..#
###
Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have a size of 3.

Then, the program repeats the following process:

* If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and convert each 2x2 square into a 3x3
 square by following the corresponding enhancement rule.
* Otherwise, the size is evenly divisible by 3; break the pixels up into 3x3 squares, and convert each 3x3 square into a
 4x4 square by following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however, it seems to be missing rules. The artist
explains that sometimes, one must rotate or flip the input pattern to find a match. (Never rotate or flip the output
pattern, though.) Each pattern is written concisely: rows are listed as single units, ordered top-down, and separated by
slashes. For example, the following rules correspond to the adjacent patterns:

../.#  =  ..
          .#

                .#.
.#./..#/###  =  ..#
                ###

                        #..#
#..#/..../#..#/.##.  =  ....
                        #..#
                        .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For example, all of the following patterns
match the same rule:

.#.   .#.   #..   ###
..#   #..   #.#   ..#
###   ###   ##.   .#.

Suppose the book contained the following two rules:

../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It divides evenly into a single square; the
square matches the second rule, which produces:

#..#
....
....
#..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is used. It divides evenly into four squares:

#.|.#
..|..
--+--
..|..
#.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of which require some flipping and rotation to
line up with the rule. The output for the rule is the same in all four cases:

##.|##.
#..|#..
...|...
---+---
##.|##.
#..|#..
...|...

Finally, the squares are joined into a new grid:

##.##.
#..#..
......
##.##.
#..#..
......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

Your puzzle answer was 197.

--- Part Two ---

How many pixels stay on after 18 iterations?

Your puzzle answer was 3081737.

Both parts of this puzzle are complete! They provide two gold stars: **

"""


def pattern_reader(pattern):
    return pattern.replace("/", "\n")


def rule_definition_parser(puzzle):
    result = dict()
    for line in puzzle:
        src, dst = line.split(" => ")
        result[pattern_reader(src.strip())] = pattern_reader(dst.strip())
    return result


def pattern_variants(pattern):
    def upside_down(pattern):
        return pattern[::-1]

    def mirror(pattern):
        return [line[::-1] for line in pattern]

    def flip(pattern):
        result = []
        for i in range(len(pattern)):
            column = ""
            for j in range(len(pattern[i])):
                column += pattern[j][i]
            result.append(column[::-1])
        return result

    def variants(pattern):
        pattern = pattern.split("\n")

        yield pattern

        all_fns = [flip, upside_down, mirror]
        for fn1 in all_fns:
            yield fn1(pattern)
            for fn2 in all_fns:
                yield fn1(fn2(pattern))
                for fn3 in all_fns:
                    yield fn1(fn2(fn3(pattern)))

    return map(lambda l: "\n".join(l), variants(pattern))


def divide_pattern(pattern, size):
    length = len(pattern)

    result = []
    for row in range(0, length, size):
        row_items = []
        for column in range(0, length, size):
            tmp = [pattern[x][column:column + size] for x in range(row, row + size)]
            row_items.append("\n".join(tmp))
        result.append(row_items)
    return result


def auto_divide(pattern):
    if len(pattern) % 2 == 0:
        return divide_pattern(pattern, 2)
    elif len(pattern) % 3 == 0:
        return divide_pattern(pattern, 3)


def join_pattern(patterns):
    result = ""

    for items in patterns:
        tmp = []
        for column in items:
            column_index = 0
            for line in column.split("\n"):
                if len(tmp) <= column_index:
                    tmp.append("")
                tmp[column_index] += line
                column_index += 1
        result += "\n".join(tmp) + "\n"

    return result.strip()


def transform(initial, rules, iterations):
    for iteration in range(iterations):
        initial = auto_divide(initial.split("\n"))

        for row in range(len(initial)):
            for column in range(len(initial[row])):
                item = initial[row][column]
                for variant in pattern_variants(item):
                    if variant in rules:
                        initial[row][column] = rules[variant]
                        break

        initial = join_pattern(initial)

    return initial


def lit_pixels(initial, rules, iterations):
    initial = transform(initial, rules, iterations)
    return initial.count("#")


if __name__ == "__main__":
    pattern = (".#.\n"
               "..#\n"
               "###")
    with open("_21_fractal_art.txt") as file:
        rules = rule_definition_parser(file.readlines())
        print(f"part 1: {lit_pixels(pattern, rules, 5)}")
        print(f"part 2: {lit_pixels(pattern, rules, 18)}")

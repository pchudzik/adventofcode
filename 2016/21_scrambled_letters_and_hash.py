import re
from functools import reduce

"""
--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling function to store its passwords. It shouldn't be much
trouble to create your own scrambled password so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is provided in your puzzle input). Starting with the
password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:

- swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
- swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the
  string).
- rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn
  abcd into dabc.
- rotate based on position of letter X means that the whole string should be rotated to the right based on the index of
  letter X (counting from 0) as determined before this instruction does any rotations. Once the index is determined,
  rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the
  index was at least 4.
- reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y)
  should be reversed in order.
- move position X to position Y means that the letter which is at index X should be removed from the string, then
  inserted such that it ends up at index Y.

For example, suppose you start with abcde and perform the following operations:

- swap position 4 with position 0 swaps the first and last letters, producing the input for the next step, ebcda.
- swap letter d with letter b swaps the positions of d and b: edcba.
- reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
- rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of the string:
  bcdea.
- move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4 (the end of the
  string): bdeac.
- move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0 (the front of the
  string): abdec.
- rotate based on position of letter b finds the index of letter b (1), then rotates the string right once plus a number
  of times equal to that index (2): ecabd.
- rotate based on position of letter d finds the index of letter d (4), then rotates the string right once, plus a number
  of times equal to that index, plus an additional time because the index was at least 4, for a total of 6 right
  rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system. Given the list of scrambling
operations in your puzzle input, what is the result of scrambling abcdefgh?

Your puzzle answer was ghfacdbe.

--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually modify the password file on the system.
You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

Your puzzle answer was fhgcdaeb.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def password_generator(cmds, str):
    return reduce(
        lambda result, cmd: parse_cmd(cmd)(result),
        cmds,
        str)


def unscrabble_password(cmds, str):
    return reduce(
        lambda result, cmd: parse_cmd(cmd).undo(result),
        reversed(cmds),
        str)


def parse_cmd(cmd: str):
    if cmd.lower().startswith("swap position"):
        pattern = re.compile(r".*(\d).*(\d)").match(cmd)
        return swap_position(int(pattern.group(1)), int(pattern.group(2)))
    elif cmd.lower().startswith("swap letter"):
        pattern = re.compile(r"^swap letter ([a-zA-Z]) with letter ([a-zA-Z])$").match(cmd)
        return swap_letter(pattern.group(1), pattern.group(2))
    elif re.match(r"rotate (left|right)", cmd.lower()):
        pattern = re.compile(r".*(left|right) (\d).*").match(cmd)
        return rotate(pattern.group(1), int(pattern.group(2)))
    elif cmd.lower().startswith("rotate based on position"):
        pattern = re.compile(".*([a-zA-Z])$").match(cmd)
        return rotate_based_on_position(pattern.group(1))
    elif cmd.lower().startswith("reverse positions"):
        pattern = re.compile(r".*(\d).*(\d)").match(cmd)
        return reverse_positions(int(pattern.group(1)), int(pattern.group(2)))
    elif cmd.lower().startswith("move position"):
        pattern = re.compile(r".*(\d).*(\d)").match(cmd)
        return move_position(int(pattern.group(1)), int(pattern.group(2)))
    else:
        raise ValueError(f"cmd error {cmd}")


def move_position(x, y):
    def cmd(str):
        ch = str[x]

        result = []
        for i in range(len(str)):
            if i == y:
                result.append(ch + str[i] if x > y else str[i] + ch)
            elif i == x:
                result.append("")
            else:
                result.append(str[i])

        return "".join(result)

    def undo(str):
        return move_position(y, x)(str)

    cmd.undo = undo

    return cmd


def reverse_positions(x, y):
    def cmd(str):
        chunk = str[x:y + 1]
        return str[:x] + chunk[::-1] + str[y + 1:]

    def undo(str):
        return cmd(str)

    cmd.undo = undo

    return cmd


def rotate(direction, x):
    def cmd(str):
        if x == 0:
            return str

        if direction == "left":
            first = str[:x]
            second = str[x:]
            return second + first
        elif direction == "right":
            first = str[:len(str) - x]
            second = str[-x:]
            return second + first
        else:
            raise ValueError(f"unknown direction - {direction}")

    def undo(str):
        return rotate("right" if direction == "left" else "left", x)(str)

    cmd.undo = undo

    return cmd


def swap_letter(x, y):
    def cmd(str):
        return "".join(
            x if c == y else y if c == x else c
            for c in str)

    def undo(str):
        return swap_letter(y, x)(str)

    cmd.undo = undo

    return cmd


def swap_position(x, y):
    def cmd(str):
        cx = str[x]
        cy = str[y]

        return "".join(
            cy if i == x else cx if i == y else str[i]
            for i in range(len(str)))

    def undo(str):
        return swap_position(y, x)(str)

    cmd.undo = undo

    return cmd


def rotate_based_on_position(letter, direction="right"):
    def cmd(str):
        index = str.index(letter)
        result = rotate(direction, index + 1)(str)
        return result if index < 4 else rotate(direction, 1)(result)

    def undo(str):
        reverse_lookup = {
            1: ("right", 7),
            3: ("right", 6),
            5: ("right", 5),
            7: ("right", 4),
            2: ("right", 2),
            4: ("right", 1),
            6: ("right", 8),
            0: ("left", 1)
        }
        reverse_params = reverse_lookup[str.index(letter)]
        return rotate(*reverse_params)(str)

    cmd.undo = undo

    return cmd


if __name__ == "__main__":
    with open("21_scrambled_letters_and_hash.txt") as file:
        cmds = file.readlines()
        print(f"part 1: {password_generator(cmds, 'abcdefgh')}")
        print(f"part 2: {unscrabble_password(cmds, 'fbgdceah')}")
"""
--- Day 4: Secure Container ---

You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on
a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle answer was 895.

--- Part Two ---

An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of
matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle answer was 591.

Both parts of this puzzle are complete! They provide two gold stars: **
"""


def numbers_never_decrease(pswd: str) -> bool:
    for i in range(len(pswd) - 1):
        a = int(pswd[i])
        b = int(pswd[i + 1])
        if b < a:
            return False
    return True


def has_double_digit(pswd: str) -> bool:
    for i in range(len(pswd) - 1):
        a = pswd[i]
        b = pswd[i + 1]
        if a == b:
            return True
    return False


def has_no_double_digit_in_part_of_bigger_group(pswd: str) -> bool:
    for i in range(0, 10):
        i_str = str(i)
        if i_str * 2 in pswd:
            index = pswd.index(i_str * 2)
            previous_different = True if index == 0 else pswd[index - 1] != i_str
            next_different = True if index + 2 >= len(pswd) else pswd[index + 2] != i_str
            if next_different and previous_different:
                return True
    return False


def is_valid_password(pswd: str, conditions) -> bool:
    return all(condition(pswd) for condition in conditions)


def run_puzzle(range_start: int, range_end: int, conditions) -> int:
    count = 0
    for i in range(range_start, range_end):
        is_valid = is_valid_password(str(i), conditions)
        if is_valid:
            count += 1
    return count


def part1(range_start: int, range_end: int) -> int:
    return run_puzzle(range_start, range_end, (has_double_digit, numbers_never_decrease))


def part2(range_start: int, range_end: int) -> int:
    return run_puzzle(range_start, range_end, (numbers_never_decrease, has_no_double_digit_in_part_of_bigger_group,))


if __name__ == "__main__":
    print("part 1:", part1(284639, 748759))
    print("part 2:", part2(284639, 748759))

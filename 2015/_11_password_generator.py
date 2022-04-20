"""
--- Day 11: Corporate Policy ---

Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has devised a method of coming up with a password
based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase letters (for
security reasons), so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter one step;
if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They
cannot skip letters; abd doesn't count.

Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are
therefore confusing.

Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

For example:

hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement
(because it contains i and l).

abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.

abbcegjk fails the third requirement, because it only has one double letter (bb).

The next password after abcdefgh is abcdffaa.

The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi...,
since i is not allowed.

Given Santa's current password (your puzzle input), what should his next password be?

Your puzzle answer was hxbxxyzz.

--- Part Two ---

Santa's password expired again. What's the next one?

Your puzzle answer was hxcaabcc.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, you should return to your advent calendar and try another puzzle.

Your puzzle input was hxbxwxba.
"""


def next_password(pswd, position=-1):
    if -position > len(pswd):
        return "a" * len(pswd)

    beginning = pswd[:position]
    end = pswd[position + 1:] if position < -1 else ""

    incremented_char = next_character(pswd[position])

    if incremented_char == "a":
        return next_password(
            beginning + incremented_char + end,
            position=position - 1)

    return beginning + incremented_char + end


def find_next_password_matching_rules(pswd):
    rules = [
        has_increasing_straight_of_three_letters,
        has_at_least_two_different_non_overlapping_pairs_of_letters,
        has_no_forbidden_letters
    ]

    next_pswd = next_password(pswd)
    while not matches_all_rules(next_pswd, rules):
        next_pswd = next_password(next_pswd)
    return next_pswd


def matches_all_rules(pswd, rules):
    return all(map(lambda rule: rule(pswd), rules))


def next_character(char):
    next_char = ord(char) + 1
    return chr(next_char) if next_char <= ord("z") else "a"


def __find_substring(string, substrings):
    return next((x for x in substrings if x in string), None)


def has_increasing_straight_of_three_letters(string):
    acceptable_substrings = [
        chr(x) + chr(x + 1) + chr(x + 2)
        for x in range(ord("a"), ord("y"))
    ]
    return __find_substring(string, acceptable_substrings) is not None


def has_no_forbidden_letters(string):
    forbidden_letters = ["i", "o", "l"]
    return __find_substring(string, forbidden_letters) is None


def has_at_least_two_different_non_overlapping_pairs_of_letters(string, matches=0, already_found=""):
    if matches == 2:
        return True

    possible_pairs = [chr(x) + chr(x) for x in range(ord("a"), ord("z") + 1) if chr(x) != already_found]
    found = __find_substring(string, possible_pairs)

    if found is None:
        return False

    return has_at_least_two_different_non_overlapping_pairs_of_letters(
        string,
        matches=matches + 1,
        already_found=found[0])


if __name__ == "__main__":
    puzzle = "hxbxwxba"
    pass2 = find_next_password_matching_rules(puzzle)
    pass3 = find_next_password_matching_rules(pass2)
    print("Next password is ", pass2)
    print("Yet another password is ", pass3)

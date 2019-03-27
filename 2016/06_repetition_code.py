from collections import Counter

"""
--- Day 6: Signals and Noise ---

Something is jamming your communications with Santa. Fortunately, your signal is only partially jammed, and protocol in
situations like this is to switch to a simple repetition code to get the message through.

In this model, the same message is sent repeatedly. You've recorded the repeating message signal (your puzzle input),
but the data seems quite corrupted - almost too badly to recover. Almost.

All you need to do is figure out which character is most frequent for each position. For example, suppose you had
recorded the following messages:

eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar

The most common character in the first column is e; in the second, a; in the third, s, and so on. Combining these
characters returns the error-corrected message, easter.

Given the recording in your puzzle input, what is the error-corrected version of the message being sent?

Your puzzle answer was ygjzvzib.

--- Part Two ---

Of course, that would be the message - if you hadn't agreed to use a modified repetition code instead.

In this modified code, the sender instead transmits what looks like random data, but for each character, the character
they actually want to send is slightly less likely than the others. Even after signal-jamming noise, you can look at the
letter distributions in each column and choose the least common letter to reconstruct the original message.

In the above example, the least common character in the first column is a; in the second, d, and so on. Repeating this
process for the remaining characters produces the original message, advent.

Given the recording in your puzzle input and this new decoding methodology, what is the original message that Santa is
trying to send?

Your puzzle answer was pdesmnoz.
"""


def decode_modified_repetition_code(code):
    return _decode_repetition_code(code, which_to_pick="least")


def decode_repetition_code(code):
    return _decode_repetition_code(code, which_to_pick="most")


def _decode_repetition_code(code, *, which_to_pick):
    code = [message.strip() for message in code]
    pick_strategy = 0 if which_to_pick == "most" else -1

    result = ""

    for letter_index in range(len(code[0])):
        repeated_letters = [msg[letter_index] for msg in code]
        most_common_letter = Counter(repeated_letters).most_common()[pick_strategy][0]
        result += most_common_letter

    return result


if __name__ == "__main__":
    with open("06_repetition_code.txt") as file:
        code = file.readlines()
        print(f"p1 = {decode_repetition_code(code)}")
        print(f"p2 = {decode_modified_repetition_code(code)}")

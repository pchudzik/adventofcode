import ast

"""
--- Day 8: Matchsticks ---

Space on the sleigh is limited this year, and so Santa will be bringing his list as a digital copy. He needs to know how
much space it will take up when stored.

It is common in many programming languages to provide a way to escape special characters in strings. For example, C,
JavaScript, Perl, Python, and even PHP handle special characters in very similar ways.

However, it is important to realize the difference between the number of characters in the code representation of the
string literal and the number of characters in the in-memory string itself.

For example:

"" is 2 characters of code (the two double quotes), but the string contains zero characters.

"abc" is 5 characters of code, but 3 characters in the string data.

"aaa\"aaa" is 10 characters of code, but the string itself contains six "a" characters and a single, escaped quote
character, for a total of 7 characters in the string data.

"\\x27" is 6 characters of code, but the string itself contains just one - an apostrophe ('), escaped using hexadecimal
notation.

Santa's list is a file that contains many double-quoted string literals, one on each line. The only escape sequences
used are \\ (which represents a single backslash), \" (which represents a lone double-quote character), and \\x plus two
hexadecimal characters (which represents a single character with that ASCII code).

Disregarding the whitespace in the file, what is the number of characters of code for string literals minus the number
of characters in memory for the values of the strings in total for the entire file?

For example, given the four strings above, the total number of characters of string code (2 + 5 + 10 + 6 = 23) minus the
total number of characters in memory for string values (0 + 3 + 7 + 1 = 11) is 23 - 11 = 12.

Your puzzle answer was 1371.

--- Part Two ---

Now, let's go the other way. In addition to finding the number of characters of code, you should now encode each code
representation as a new string and find the number of characters of the new encoded representation, including the
surrounding double quotes.

For example:

"" encodes to "\"\"", an increase from 2 characters to 6.

"abc" encodes to "\"abc\"", an increase from 5 characters to 9.

"aaa\"aaa" encodes to "\"aaa\\\"aaa\"", an increase from 10 characters to 16.

"\\x27" encodes to "\"\\x27\"", an increase from 6 characters to 11.

Your task is to find the total number of characters to represent the newly encoded strings minus the number of
characters of code in each original string literal. For example, for the strings above, the total encoded length (6 + 9
+ 16 + 11 = 42) minus the characters in the original code representation (23, just like in the first part of this
puzzle) is 42 - 23 = 19.

Your puzzle answer was 2117.
"""


def escaped_bytes(input_bytes):
    result = []
    for byte in input_bytes:
        if byte == b'"':
            result.append(b'\\')
            result.append(byte)
        elif byte == b'\\':
            result.append(b'\\')
            result.append(byte)
        else:
            result.append(byte)

    return [b'"'] + result + [b'"']


def length_calculator(input_bytes):
    input_string = ast.literal_eval(b''.join(input_bytes).decode("utf-8"))
    return len(input_bytes), len(input_string)


def total_length_calculator(inputs):
    return sum(map(
        lambda length: length[0] - length[1],
        [length_calculator(input_bytes) for input_bytes in inputs]))


def read_file_binary(file_name):
    with open(file_name, "rb") as file:
        byte = file.read(1)
        total = []
        row = []
        while byte != b"":
            if byte == b"\n":
                total.append(row)
                row = []
            else:
                row.append(byte)
            byte = file.read(1)

        return total


def total_length_calculator2(inputs):
    return sum(map(
        lambda input_bytes: len(escaped_bytes(input_bytes)) - len(input_bytes),
        inputs))


if __name__ == "__main__":
    content = read_file_binary("08_strings_length.lst")
    print(
        " ".join([
            "The number of characters of code for string literals",
            "minus the number of characters in memory for the values of the strings"]),
        total_length_calculator(content))

    print(
        " ".join([
            "The total number of characters to represent the newly encoded strings",
            "minus the number of characters of code in each original string literal"]),
        total_length_calculator2(content))

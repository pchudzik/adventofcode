import re
import json

"""
--- Day 12: JSAbacusFramework.io ---

Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

For example:

[1,2,3] and {"a":2,"b":4} both have a sum of 6.
[[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
{"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
[] and {} both have a sum of 0.
You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?

Your puzzle answer was 119433.

--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything red.

Ignore any object (and all of its children) which has any property with the value "red". Do this only for objects ({...}), not arrays ([...]).

[1,2,3] still has a sum of 6.
[1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
{"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire structure is ignored.
[1,"red",5] has a sum of 6, because "red" in an array has no effect.
Your puzzle answer was 68466.
"""


def sum_of_numbers_regexp(json):
    numbers = re.compile("-?\\d+")
    return sum([int(num_str) for num_str in numbers.findall(json)])


def sum_of_numbers_dict(data, values_has_no_red=lambda values: True):
    if type(data) == int:
        return data

    collection = []

    if type(data) == dict:
        collection = data.values() if values_has_no_red(data.values()) else []
    elif type(data) == list:
        collection = data

    return sum([sum_of_numbers_dict(value, values_has_no_red=values_has_no_red) for value in collection])


def has_no_red_value_red(collection):
    return "red" not in collection


def sum_of_numbers_dict_exclude_red(data):
    return sum_of_numbers_dict(
        data,
        values_has_no_red=has_no_red_value_red)


if __name__ == "__main__":
    with open("12_numbers_counter.json") as file:
        data = json.load(file)
        print("Sum of all numbers in file is:", sum_of_numbers_dict(data))
        print("Sum of all numbers excluding red in file is:", sum_of_numbers_dict_exclude_red(data))

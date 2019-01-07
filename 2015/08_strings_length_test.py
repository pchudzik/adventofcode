import pytest
import importlib

length_calculator = importlib \
    .import_module("08_strings_length") \
    .length_calculator

total_length_calculator = importlib \
    .import_module("08_strings_length") \
    .total_length_calculator

escaped_bytes = importlib \
    .import_module("08_strings_length") \
    .escaped_bytes

total_length_calculator2 = importlib \
    .import_module("08_strings_length") \
    .total_length_calculator2


@pytest.mark.parametrize(
    "input_string, result", [
        ([b'"', b'"'], (2, 0)),
        ([b'"', b'a', b'b', b'c', b'"'], (5, 3)),
        ([b'"', b'a', b'a', b'a', b'\\', b'"', b'a', b'a', b'a', b'"'], (10, 7)),
        ([b'"', b'\\', b'x', b'2', b'7', b'"'], (6, 1))
    ])
def test_length_calculator(input_string, result):
    assert length_calculator(input_string) == result


def test_total_length():
    input_strings = [
        [b'"', b'"'],
        [b'"', b'a', b'b', b'c', b'"'],
        [b'"', b'a', b'a', b'a', b'\\', b'"', b'a', b'a', b'a', b'"'],
        [b'"', b'\\', b'x', b'2', b'7', b'"']
    ]

    assert total_length_calculator(input_strings) == (2 + 5 + 10 + 6) - (0 + 3 + 7 + 1)


@pytest.mark.parametrize(
    "input_bytes, result", [
        ([b'"', b'"'], [b'"', b'\\', b'"', b'\\', b'"', b'"', ]),
        ([b'"', b'a', b'b', b'c', b'"'], [b'"', b'\\', b'"', b'a', b'b', b'c', b'\\', b'"', b'"']),
        (
                [b'"', b'a', b'a', b'a', b'\\', b'"', b'a', b'a', b'a', b'"'],
                [b'"', b'\\', b'"', b'a', b'a', b'a', b'\\', b'\\', b'\\', b'"', b'a', b'a', b'a', b'\\', b'"', b'"']),
        ([b'"', b'\\', b'x', b'2', b'7', b'"'], [b'"', b'\\', b'"', b'\\', b'\\', b'x', b'2', b'7', b'\\', b'"', b'"'])
    ])
def test_escaped_bytes(input_bytes, result):
    assert escaped_bytes(input_bytes) == result


def test_total_length_calculator2():
    input_strings = [
        [b'"', b'"'],
        [b'"', b'a', b'b', b'c', b'"'],
        [b'"', b'a', b'a', b'a', b'\\', b'"', b'a', b'a', b'a', b'"'],
        [b'"', b'\\', b'x', b'2', b'7', b'"']
    ]

    assert total_length_calculator2(input_strings) == (6 + 9 + 16 + 11) - (2 + 5 + 10 + 6)

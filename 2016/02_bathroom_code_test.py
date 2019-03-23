import importlib
import pytest

find_code_standard_keypad = importlib.import_module("02_bathroom_code").find_code_standard_keypad
find_code_star_keypad = importlib.import_module("02_bathroom_code").find_code_star_keypad


def test_find_code_on_standard_keypad():
    code = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD"
    ]

    assert find_code_standard_keypad(code) == "1985"


def test_find_code_on_star_keypad():
    code = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD"
    ]

    assert find_code_star_keypad(code) == "5DB3"

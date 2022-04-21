from _02_bathroom_code import find_code_standard_keypad, find_code_star_keypad


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

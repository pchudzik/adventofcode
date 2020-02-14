import pytest
import importlib

module = importlib.import_module("02_inventory_management_system")
count_letters = module.count_letters
checksum = module.checksum
find_box = module.find_box


@pytest.mark.parametrize("letters, twos, threes", [
    ("abcdef", 0, 0),
    ("bababc", 1, 1),
    ("abbcde", 1, 0),
    ("abcccd", 0, 1),
    ("aabcdd", 1, 0),
    ("abcdee", 1, 0),
    ("ababab", 0, 1)
])
def test_count_letters(letters, twos, threes):
    assert count_letters(letters) == (twos, threes)


def test_checksum():
    ids = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab"
    ]

    assert checksum(ids) == 12


def test_find_box():
    ids = [
        "abcde",
        "fghij",
        "klmno",
        "pqrst",
        "fguij",
        "axcye",
        "wvxyz"
    ]

    assert find_box(ids) == "fgij"

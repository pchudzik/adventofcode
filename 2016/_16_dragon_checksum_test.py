import pytest

from _16_dragon_checksum import data_filler, checksum, find_checksum


@pytest.mark.parametrize(
    "input, expected", [
        ("1", "100"),
        ("0", "001"),
        ("11111", "11111000000"),
        ("111100001010", "1111000010100101011110000")])
def test_data_filler(input, expected):
    assert data_filler(input) == expected


def test_checksum():
    assert checksum("110010110100") == "100"


def test_find_checksum():
    assert find_checksum("10000", 20) == "01100"

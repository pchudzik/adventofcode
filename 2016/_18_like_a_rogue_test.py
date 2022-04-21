import pytest

from _18_like_a_rogue import is_trap, Row, find_safe_tiles


@pytest.mark.parametrize(
    "left, center, right, expected", [
        (True, True, False, True),
        (True, False, False, True),
        (False, True, True, True),
        (False, False, True, True),
        (True, False, True, False),
        (True, True, True, False),
        (True, False, True, False)
    ])
def test_is_trap(left, center, right, expected):
    assert is_trap(left, center, right) == expected


def test_parse_row():
    assert Row.parse("..^^.").puzzle == (False, False, True, True, False)


@pytest.mark.parametrize(
    "row, next_row", [
        ("..^^.", ".^^^^"),
        (".^^^^", "^^..^"),
        (".^^.^.^^^^", "^^^...^..^"),
        ("^^^...^..^", "^.^^.^.^^."),
        ("^.^^.^.^^.", "..^^...^^^"),
        ("..^^...^^^", ".^^^^.^^.^"),
        (".^^^^.^^.^", "^^..^.^^..")])
def test_next_row(row, next_row):
    assert str(Row.parse(row).next_row()) == next_row


@pytest.mark.parametrize(
    "puzzle, safe_tiles", [
        ("..^^.", 3),
        (".^^^^", 1)])
def counts_safe_tiles(puzzle, safe_tiles):
    assert Row.parse(puzzle).safe_tiles == safe_tiles


def test_find_safe_tiles():
    assert find_safe_tiles(".^^.^.^^^^", 10) == 38
